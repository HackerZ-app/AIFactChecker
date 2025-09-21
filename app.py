from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Set your Gemini API key as an environment variable instead of hardcoding
# Example (Linux/Mac): export GEMINI_API_KEY="YOUR_KEY"
# Example (Windows): set GEMINI_API_KEY="YOUR_KEY"
# Directly assign your Gemini API key (not recommended for production)
GEMINI_API_KEY = "AIzaSyAEVTCVR2KHS0cr5bNv7Kc5VjJcM9ajRqg"


FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"

def fact_check(query):
    params = {
        "query": query,
        "key": GEMINI_API_KEY
    }
    response = requests.get(FACTCHECK_URL, params=params)
    
    if response.status_code != 200:
        return {"error": "Fact Check API request failed", "status_code": response.status_code}

    data = response.json()
    claims = []

    for claim in data.get("claims", []):
        claims.append({
            "claim": claim.get("text"),
            "verdict": claim.get("claimReview")[0].get("textualRating") if claim.get("claimReview") else "Unverified",
            "confidence": 1,  # Hardcoded since Fact Check API does not provide numeric confidence
            "explanation": claim.get("claimReview")[0].get("title") if claim.get("claimReview") else "",
            "sources": [
                {
                    "title": review.get("publisher", {}).get("name", ""),
                    "url": review.get("url", "")
                } for review in claim.get("claimReview", [])
            ]
        })
    
    if not claims:
        claims.append({
            "claim": query,
            "verdict": "Unverified",
            "confidence": 0,
            "explanation": "No matching claim found in Google Fact Check database.",
            "sources": []
        })

    return claims

@app.route('/check', methods=['POST'])
def check_facts():
    if not request.is_json or 'text' not in request.json:
        return jsonify({"error": "Invalid request: missing 'text' field"}), 400

    input_text = request.json['text']
    claims = fact_check(input_text)

    return jsonify({
        "originalText": input_text,
        "claims": claims
    })

if __name__ == '__main__':
    app.run(port=5001, debug=True)
