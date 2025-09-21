import os
import requests
import openai
from flask import Flask, render_template, request, jsonify
from dotenv import load_dotenv
from textblob import TextBlob
import nltk
from urllib.parse import urlparse
import re
from datetime import datetime

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'dev-secret-key')

# Configure OpenAI
openai.api_key = os.environ.get('OPENAI_API_KEY')

class FactChecker:
    def __init__(self):
        self.news_api_key = os.environ.get('NEWS_API_KEY')
        
    def analyze_claim(self, claim):
        """Analyze a claim for fact-checking"""
        try:
            # Basic text analysis
            blob = TextBlob(claim)
            sentiment = blob.sentiment.polarity
            
            # Extract key entities/topics
            entities = self._extract_entities(claim)
            
            # Search for related articles
            related_articles = self._search_related_articles(claim, entities)
            
            # AI-powered fact check
            ai_analysis = self._ai_fact_check(claim, related_articles)
            
            # Credibility assessment
            credibility_score = self._calculate_credibility(ai_analysis, related_articles)
            
            return {
                'claim': claim,
                'sentiment': sentiment,
                'entities': entities,
                'related_articles': related_articles,
                'ai_analysis': ai_analysis,
                'credibility_score': credibility_score,
                'timestamp': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'error': f"Error analyzing claim: {str(e)}",
                'claim': claim,
                'timestamp': datetime.now().isoformat()
            }
    
    def _extract_entities(self, text):
        """Extract key entities from text"""
        # Simple entity extraction using regex patterns
        entities = {
            'people': re.findall(r'\b[A-Z][a-z]+ [A-Z][a-z]+\b', text),
            'organizations': re.findall(r'\b[A-Z][A-Z0-9&\s]{2,}\b', text),
            'dates': re.findall(r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}\b', text),
            'numbers': re.findall(r'\b\d+(?:,\d{3})*(?:\.\d+)?\b', text)
        }
        
        # Filter out empty lists
        return {k: v for k, v in entities.items() if v}
    
    def _search_related_articles(self, claim, entities, limit=5):
        """Search for articles related to the claim"""
        if not self.news_api_key:
            return []
        
        try:
            # Create search query from claim and entities
            query_terms = []
            
            # Add key words from claim
            blob = TextBlob(claim)
            for word, pos in blob.tags:
                if pos in ['NN', 'NNP', 'NNPS', 'NNS'] and len(word) > 3:
                    query_terms.append(word)
            
            # Add entities
            for entity_list in entities.values():
                query_terms.extend(entity_list)
            
            query = ' '.join(query_terms[:10])  # Limit query length
            
            # Search using NewsAPI
            url = 'https://newsapi.org/v2/everything'
            params = {
                'q': query,
                'apiKey': self.news_api_key,
                'language': 'en',
                'sortBy': 'relevancy',
                'pageSize': limit
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                articles = []
                
                for article in data.get('articles', []):
                    articles.append({
                        'title': article.get('title', ''),
                        'description': article.get('description', ''),
                        'url': article.get('url', ''),
                        'source': article.get('source', {}).get('name', ''),
                        'published_at': article.get('publishedAt', '')
                    })
                
                return articles
            
        except Exception as e:
            print(f"Error searching articles: {e}")
        
        return []
    
    def _ai_fact_check(self, claim, related_articles):
        """Use AI to analyze the claim against related articles"""
        if not openai.api_key:
            return "AI fact-checking unavailable: OpenAI API key not configured"
        
        try:
            # Prepare context from related articles
            context = "\n".join([
                f"Article: {article['title']}\nDescription: {article['description']}\nSource: {article['source']}"
                for article in related_articles[:3]  # Use top 3 articles
            ])
            
            prompt = f"""
            As a fact-checker, analyze the following claim against the provided context from credible news sources.
            
            Claim to check: "{claim}"
            
            Context from news sources:
            {context}
            
            Please provide:
            1. A factual assessment (True/False/Partly True/Unverifiable)
            2. Key evidence supporting or contradicting the claim
            3. Any important context or nuances
            4. Confidence level (High/Medium/Low)
            
            Keep your response concise and objective.
            """
            
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are a professional fact-checker. Provide objective, evidence-based analysis."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.3
            )
            
            return response.choices[0].message.content.strip()
            
        except Exception as e:
            return f"AI analysis error: {str(e)}"
    
    def _calculate_credibility(self, ai_analysis, related_articles):
        """Calculate a credibility score based on various factors"""
        score = 50  # Start with neutral score
        
        # Adjust based on AI analysis
        if "True" in ai_analysis and "False" not in ai_analysis:
            score += 20
        elif "False" in ai_analysis:
            score -= 30
        elif "Partly True" in ai_analysis:
            score += 5
        elif "Unverifiable" in ai_analysis:
            score -= 10
        
        # Adjust based on confidence level
        if "High" in ai_analysis:
            score += 10
        elif "Low" in ai_analysis:
            score -= 10
        
        # Adjust based on number of supporting articles
        score += min(len(related_articles) * 5, 20)
        
        # Ensure score is within bounds
        return max(0, min(100, score))

# Initialize fact checker
fact_checker = FactChecker()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check', methods=['POST'])
def check_fact():
    data = request.get_json()
    claim = data.get('claim', '').strip()
    
    if not claim:
        return jsonify({'error': 'Please provide a claim to check'}), 400
    
    result = fact_checker.analyze_claim(claim)
    return jsonify(result)

@app.route('/health')
def health():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    # Download required NLTK data
    try:
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
    except:
        pass
    
    app.run(debug=True, host='0.0.0.0', port=5000)