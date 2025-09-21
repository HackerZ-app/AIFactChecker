from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import re
from datetime import datetime
import random
import time

app = Flask(__name__)
CORS(app)

# Credible sources database
CREDIBLE_SOURCES = [
    {
        "name": "Reuters",
        "baseUrl": "reuters.com",
        "credibilityScore": 95,
        "type": "news"
    },
    {
        "name": "Associated Press",
        "baseUrl": "apnews.com",
        "credibilityScore": 94,
        "type": "news"
    },
    {
        "name": "BBC News",
        "baseUrl": "bbc.com",
        "credibilityScore": 92,
        "type": "news"
    },
    {
        "name": "NPR",
        "baseUrl": "npr.org",
        "credibilityScore": 91,
        "type": "news"
    },
    {
        "name": "Snopes",
        "baseUrl": "snopes.com",
        "credibilityScore": 89,
        "type": "fact-check"
    },
    {
        "name": "PolitiFact",
        "baseUrl": "politifact.com",
        "credibilityScore": 88,
        "type": "fact-check"
    },
    {
        "name": "FactCheck.org",
        "baseUrl": "factcheck.org",
        "credibilityScore": 90,
        "type": "fact-check"
    },
    {
        "name": "World Health Organization",
        "baseUrl": "who.int",
        "credibilityScore": 96,
        "type": "health"
    },
    {
        "name": "CDC",
        "baseUrl": "cdc.gov",
        "credibilityScore": 95,
        "type": "health"
    },
    {
        "name": "NASA",
        "baseUrl": "nasa.gov",
        "credibilityScore": 97,
        "type": "science"
    }
]

class FactChecker:
    def __init__(self):
        self.sources = CREDIBLE_SOURCES
        
    def extract_keywords(self, text):
        """Extract keywords from text"""
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by'}
        words = re.findall(r'\b\w+\b', text.lower())
        keywords = [word for word in words if len(word) > 3 and word not in common_words]
        return keywords[:10]
    
    def identify_claim_type(self, claim):
        """Identify the type of claim"""
        health_keywords = ['health', 'medical', 'disease', 'vaccine', 'treatment', 'doctor', 'hospital', 'medicine', 'covid', 'virus', 'bacteria']
        politics_keywords = ['government', 'president', 'election', 'policy', 'congress', 'senate', 'vote', 'political', 'democrat', 'republican']
        science_keywords = ['research', 'study', 'scientist', 'experiment', 'data', 'climate', 'space', 'technology', 'scientific']
        economics_keywords = ['economy', 'market', 'stock', 'price', 'inflation', 'economic', 'financial', 'money', 'business']
        
        lower_claim = claim.lower()
        
        if any(keyword in lower_claim for keyword in health_keywords):
            return 'health'
        elif any(keyword in lower_claim for keyword in politics_keywords):
            return 'politics'
        elif any(keyword in lower_claim for keyword in science_keywords):
            return 'science'
        elif any(keyword in lower_claim for keyword in economics_keywords):
            return 'economics'
        
        return 'general'
    
    def analyze_sentiment(self, text):
        """Analyze sentiment of the text"""
        positive_words = ['good', 'great', 'excellent', 'amazing', 'wonderful', 'fantastic', 'awesome', 'brilliant', 'outstanding', 'perfect']
        negative_words = ['bad', 'terrible', 'awful', 'horrible', 'disgusting', 'worst', 'hate', 'fail', 'wrong', 'false']
        
        words = text.lower().split()
        positive_count = sum(1 for word in words if word in positive_words)
        negative_count = sum(1 for word in words if word in negative_words)
        
        if positive_count > negative_count:
            return 'positive'
        elif negative_count > positive_count:
            return 'negative'
        return 'neutral'
    
    def assess_complexity(self, text):
        """Assess the complexity of the claim"""
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 'low'
            
        avg_words_per_sentence = len(text.split()) / len(sentences)
        
        if avg_words_per_sentence > 20:
            return 'high'
        elif avg_words_per_sentence > 12:
            return 'medium'
        return 'low'
    
    def find_matching_sources(self, claim):
        """Find credible sources related to the claim"""
        claim_type = self.identify_claim_type(claim)
        
        # Filter sources based on claim type
        relevant_sources = []
        for source in self.sources:
            if claim_type == 'health' and source['type'] in ['health', 'fact-check']:
                relevant_sources.append(source)
            elif claim_type == 'science' and source['type'] in ['science', 'fact-check']:
                relevant_sources.append(source)
            elif source['type'] in ['fact-check', 'news']:
                relevant_sources.append(source)
        
        # Randomly select 3-6 sources
        num_sources = min(len(relevant_sources), random.randint(3, 6))
        selected_sources = random.sample(relevant_sources, num_sources)
        
        # Generate mock data for each source
        sources_with_data = []
        for source in selected_sources:
            source_data = source.copy()
            source_data.update({
                'title': self.generate_source_title(claim, source),
                'url': f"https://{source['baseUrl']}/{self.generate_slug(claim)}",
                'excerpt': self.generate_source_excerpt(claim, source),
                'publishDate': self.generate_recent_date(),
                'relevanceScore': random.randint(70, 95)
            })
            sources_with_data.append(source_data)
        
        return sources_with_data
    
    def generate_source_title(self, claim, source):
        """Generate a realistic title for the source"""
        titles = {
            'fact-check': [
                f"Fact Check: {claim[:50]}...",
                f"Is it true that {claim[:40]}?",
                f"Verifying claims about {self.extract_keywords(claim)[0] if self.extract_keywords(claim) else 'recent news'}"
            ],
            'news': [
                f"Breaking: {claim[:45]}...",
                f"Report: {claim[:50]}...",
                f"Analysis: {claim[:45]}..."
            ],
            'health': [
                f"Health Alert: {claim[:40]}...",
                f"Medical Update: {claim[:35]}...",
                f"Health Officials: {claim[:35]}..."
            ],
            'science': [
                f"Study: {claim[:45]}...",
                f"Research: {claim[:40]}...",
                f"Scientists: {claim[:35]}..."
            ]
        }
        
        source_type = source['type']
        type_titles = titles.get(source_type, titles['news'])
        return random.choice(type_titles)
    
    def generate_source_excerpt(self, claim, source):
        """Generate a realistic excerpt"""
        excerpts = [
            "Our investigation into this claim reveals important details that provide context and clarity...",
            "According to verified sources and expert analysis, the facts surrounding this matter are...",
            "Recent evidence and expert testimony suggest that the situation is more nuanced than initially reported...",
            "Multiple credible sources have confirmed key aspects of this story while highlighting areas that require further clarification...",
            "Our fact-checking team has reviewed available evidence and consulted with experts in the field..."
        ]
        return random.choice(excerpts)
    
    def generate_recent_date(self):
        """Generate a recent date"""
        days_ago = random.randint(0, 30)
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        date = date.replace(day=date.day - days_ago) if date.day > days_ago else date.replace(month=date.month-1, day=30-days_ago+date.day)
        return date.strftime('%Y-%m-%d')
    
    def generate_slug(self, text):
        """Generate URL slug from text"""
        slug = re.sub(r'[^\w\s]', '', text.lower())
        slug = re.sub(r'\s+', '-', slug)
        return slug[:50]
    
    def calculate_verdict(self, analysis, sources):
        """Calculate the overall verdict"""
        if not sources:
            return {'type': 'unverified', 'label': 'Unverified'}
        
        source_count = len(sources)
        avg_credibility = sum(source['credibilityScore'] for source in sources) / source_count
        avg_relevance = sum(source['relevanceScore'] for source in sources) / source_count
        
        # Simple verdict logic
        verdict_score = (avg_credibility * 0.4) + (avg_relevance * 0.3) + (source_count * 5) + random.randint(0, 20)
        
        if verdict_score > 85:
            return {'type': 'true', 'label': 'Likely True'}
        elif verdict_score > 70:
            return {'type': 'mixed', 'label': 'Mixed/Partial'}
        elif verdict_score > 50:
            return {'type': 'unverified', 'label': 'Unverified'}
        else:
            return {'type': 'false', 'label': 'Likely False'}
    
    def calculate_confidence(self, analysis, sources):
        """Calculate confidence level"""
        if not sources:
            return 30
        
        source_count = len(sources)
        avg_credibility = sum(source['credibilityScore'] for source in sources) / source_count
        complexity_factor = {'low': 1.1, 'medium': 1.0, 'high': 0.9}[analysis['complexity']]
        
        confidence = (avg_credibility / 100) * complexity_factor * (min(source_count, 5) / 5)
        confidence = max(0.3, min(0.95, confidence + random.uniform(-0.05, 0.05)))
        
        return round(confidence * 100)
    
    def check_facts(self, claim):
        """Main fact checking function"""
        # Analyze claim
        keywords = self.extract_keywords(claim)
        claim_type = self.identify_claim_type(claim)
        sentiment = self.analyze_sentiment(claim)
        complexity = self.assess_complexity(claim)
        
        analysis = {
            'keywords': keywords,
            'type': claim_type,
            'sentiment': sentiment,
            'complexity': complexity,
            'length': len(claim)
        }
        
        # Find matching sources
        sources = self.find_matching_sources(claim)
        
        # Calculate verdict and confidence
        verdict = self.calculate_verdict(analysis, sources)
        confidence = self.calculate_confidence(analysis, sources)
        
        return {
            'claim': claim,
            'analysis': analysis,
            'sources': sources,
            'verdict': verdict,
            'confidence': confidence,
            'timestamp': datetime.now().isoformat()
        }

# Initialize fact checker
fact_checker = FactChecker()

@app.route('/')
def home():
    return jsonify({
        'message': 'AI Fact Checker API',
        'version': '1.0.0',
        'endpoints': {
            'POST /api/fact-check': 'Check facts for a claim',
            'GET /api/sources': 'Get list of credible sources'
        }
    })

@app.route('/api/fact-check', methods=['POST'])
def check_facts():
    try:
        data = request.get_json()
        
        if not data or 'claim' not in data:
            return jsonify({'error': 'Missing claim in request body'}), 400
        
        claim = data['claim'].strip()
        
        if len(claim) < 10:
            return jsonify({'error': 'Claim must be at least 10 characters long'}), 400
        
        # Simulate processing time
        time.sleep(random.uniform(1, 3))
        
        # Perform fact check
        result = fact_checker.check_facts(claim)
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sources', methods=['GET'])
def get_sources():
    return jsonify({
        'sources': CREDIBLE_SOURCES,
        'total': len(CREDIBLE_SOURCES)
    })

@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)