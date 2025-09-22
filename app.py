from flask import Flask, request, jsonify, render_template, redirect, url_for
from flask_cors import CORS
import requests
from bs4 import BeautifulSoup
import google.generativeai as genai
from collections import Counter
from difflib import SequenceMatcher
from datetime import datetime
import os
import re
from dotenv import load_dotenv # Loads environment variables from a .env file

# Load variables from the .env file in your project folder
load_dotenv()

app = Flask(__name__)
CORS(app)

# --- CONFIGURATION (Loaded securely from your .env file) ---
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# This check is crucial: it stops the app if the keys are not configured.
if not GEMINI_API_KEY or not SEARCH_ENGINE_ID:
    raise ValueError("API keys not found! Please create a .env file in the project root and add your GEMINI_API_KEY and SEARCH_ENGINE_ID.")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash-latest')
FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
CUSTOM_SEARCH_URL = "https://www.googleapis.com/customsearch/v1"

# --- HELPER: Relevance Check Function ---
def is_similar(a, b):
    """Checks if two strings are similar enough."""
    return SequenceMatcher(None, a, b).ratio() > 0.75

# --- DATA GATHERING FUNCTIONS ---
def fact_check(query):
    params = {"query": f'"{query}"', "key": GEMINI_API_KEY}
    try:
        response = requests.get(FACTCHECK_URL, params=params)
        response.raise_for_status()
        return response.json().get("claims", [])
    except requests.RequestException: return []

def google_search_trusted_sources(query):
    try:
        params = {'key': GEMINI_API_KEY, 'cx': SEARCH_ENGINE_ID, 'q': query}
        response = requests.get(CUSTOM_SEARCH_URL, params=params)
        response.raise_for_status()
        search_results = response.json().get('items', [])
        return [{'title': item['title'], 'url': item['link'], 'snippet': item.get('snippet', '')} for item in search_results[:5]]
    except requests.RequestException: return []

# --- Date-Aware AI Analysis Function ---
def get_ai_analysis(all_sources, original_query):
    if not all_sources:
        return {"verdict": "Unverified", "summary": "No sources found to generate an analysis.", "confidence": 0}

    combined_text = ""
    for source in all_sources[:4]:
        if 'snippet' in source: combined_text += f"Source: {source['title']}\nSnippet: {source['snippet']}\n\n"
        try:
            response = requests.get(source['url'], headers={'User-Agent': 'Mozilla/5.0'}, timeout=5)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                combined_text += soup.get_text()[:2000] + "\n\n"
        except requests.RequestException: continue
    
    if not combined_text: return {"verdict": "Unverified", "summary": "Could not fetch content from sources.", "confidence": 10}
    
    current_date = datetime.now().strftime("%B %d, %Y")
    prompt = f"""
    You are a meticulous fact-checking AI. The current date is {current_date}.
    Analyze the following claim based ONLY on the provided text from trusted sources: "{original_query}"
    Your task is to determine if the claim is true or false *right now*.
    Begin your response with one of these exact phrases:
    - "Verdict: Likely True"
    - "Verdict: Likely False"
    - "Verdict: Potentially Misleading"
    - "Verdict: Context Available"
    Follow the verdict with a detailed, one-paragraph explanation summarizing the evidence from the sources. Do not use any outside knowledge.
    Provided text:
    {combined_text}
    """
    
    try:
        safety_settings = [{"category": c, "threshold": "BLOCK_NONE"} for c in ["HARM_CATEGORY_HARASSMENT", "HARM_CATEGORY_HATE_SPEECH", "HARM_CATEGORY_SEXUALLY_EXPLICIT", "HARM_CATEGORY_DANGEROUS_CONTENT"]]
        response = model.generate_content(prompt, safety_settings=safety_settings)
        ai_response_text = response.text
        verdict_match = re.match(r"Verdict: (Likely True|Likely False|Potentially Misleading|Context Available)", ai_response_text)
        if verdict_match:
            verdict = verdict_match.group(1)
            summary = ai_response_text.replace(verdict_match.group(0), "").strip()
            confidence = 85
        else:
            verdict = "Uncertain"
            summary = "The AI could not determine a definitive verdict from the sources."
            confidence = 30
        return {"verdict": verdict, "summary": summary, "confidence": confidence}
    except Exception as e:
        print(f"Gemini API error: {e}")
        return {"verdict": "Uncertain", "summary": "The AI analysis failed due to an API error.", "confidence": 0}

# --- Main Route and Verdict Logic ---
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check():
    query = request.form['text']
    return redirect(url_for('output', query=query))

@app.route('/output')
def output():
    query = request.args.get('query', '')
    if not query: return redirect(url_for('index'))
    fact_check_results = fact_check(query)
    trusted_sources_results = google_search_trusted_sources(query)
    relevant_fc_claim = next((c for c in fact_check_results if is_similar(query.lower(), c.get("text", "").lower())), None)
    if relevant_fc_claim:
        fc_reviews = relevant_fc_claim.get("claimReview", [])
        verdicts = [r.get("textualRating") for r in fc_reviews]
        if "False" in verdicts: verdict = "Likely False"
        elif "True" in verdicts: verdict = "Likely True"
        else: verdict = "Potentially Misleading"
        explanation = f"A highly relevant claim was rated '{verdict}' by a fact-checking organization."
        confidence = 95
        summary_data = get_ai_summary_context(trusted_sources_results, query)
        fc_sources = [{"title": r.get("publisher", {}).get("name", ""), "url": r.get("url", "")} for r in fc_reviews]
        final_verdict = {
            "verdict": verdict, "explanation": explanation, "confidence_score": confidence,
            "fact_check_sources": fc_sources, "trusted_sources": trusted_sources_results
        }
    else:
        all_sources_for_summary = trusted_sources_results
        analysis_result = get_ai_analysis(all_sources_for_summary, query)
        final_verdict = {
            "verdict": analysis_result["verdict"],
            "explanation": "The verdict is based on an AI analysis of trusted sources like Wikipedia and reputable news outlets.",
            "confidence_score": analysis_result["confidence"],
            "fact_check_sources": [],
            "trusted_sources": trusted_sources_results
        }
        summary_data = {"summary": analysis_result["summary"]}
    return render_template('output.html', query=query, summary_data=summary_data, verdict_data=final_verdict)

def get_ai_summary_context(trusted_sources, original_query):
    """Helper function for AI summary (used only if a direct fact-check is found)"""
    if not trusted_sources: return {"summary": "No additional sources found for context."}
    combined_text = ""
    for source in trusted_sources[:2]:
        if 'snippet' in source: combined_text += f"Snippet: {source['snippet']}\n\n"
    prompt = f"Briefly summarize the context on the topic: '{original_query}' based on these snippets:\n{combined_text}"
    try:
        response = model.generate_content(prompt)
        return {"summary": response.text}
    except: return {"summary": "Could not generate a contextual summary."}

if __name__ == '__main__':
    app.run(port=5500, debug=True)

