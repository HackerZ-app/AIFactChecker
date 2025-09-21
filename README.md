# AI Fact Checker

An intelligent fact-checking application that verifies claims and statements against credible sources using AI-powered analysis and real-time news data.

## Features

- **AI-Powered Analysis**: Uses OpenAI's GPT models to analyze claims against credible sources
- **Real-time News Integration**: Searches current news articles using NewsAPI
- **Entity Extraction**: Identifies key people, organizations, dates, and numbers in claims
- **Credibility Scoring**: Provides a numerical credibility score (0-100) for each claim
- **Web Interface**: Clean, responsive web interface for easy claim submission
- **Source Verification**: Cross-references claims with multiple news sources

## Technology Stack

- **Backend**: Python, Flask
- **Frontend**: HTML, CSS, JavaScript, Bootstrap
- **AI**: OpenAI GPT-3.5-turbo
- **APIs**: NewsAPI for news articles
- **NLP**: NLTK, TextBlob for text processing

## Installation

1. Clone the repository:
```bash
git clone https://github.com/HackerZ-app/AIFactChecker.git
cd AIFactChecker
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
```

Edit `.env` file and add your API keys:
- `OPENAI_API_KEY`: Your OpenAI API key
- `NEWS_API_KEY`: Your NewsAPI key (get from https://newsapi.org/)

## Usage

1. Start the application:
```bash
python app.py
```

2. Open your browser and go to `http://localhost:5000`

3. Enter a claim or statement you want to fact-check

4. Review the AI analysis, credibility score, and related articles

## API Endpoints

- `GET /`: Main web interface
- `POST /check`: Fact-check a claim
  ```json
  {
    "claim": "Your claim to check"
  }
  ```
- `GET /health`: Health check endpoint

## Configuration

### Required API Keys

1. **OpenAI API Key**: 
   - Sign up at https://platform.openai.com/
   - Generate an API key in your dashboard
   - Add to `.env` as `OPENAI_API_KEY`

2. **NewsAPI Key**:
   - Sign up at https://newsapi.org/
   - Get your free API key
   - Add to `.env` as `NEWS_API_KEY`

### Environment Variables

- `OPENAI_API_KEY`: OpenAI API key for AI analysis
- `NEWS_API_KEY`: NewsAPI key for fetching news articles
- `FLASK_ENV`: Flask environment (development/production)
- `FLASK_DEBUG`: Enable Flask debug mode (True/False)

## How It Works

1. **Claim Input**: User submits a claim through the web interface
2. **Entity Extraction**: The system identifies key entities (people, organizations, dates, numbers)
3. **Article Search**: Searches for related news articles using NewsAPI
4. **AI Analysis**: Uses OpenAI's GPT to analyze the claim against found articles
5. **Credibility Scoring**: Calculates a score based on AI analysis and supporting evidence
6. **Results Display**: Shows comprehensive results including:
   - Credibility score with visual indicator
   - Detailed AI analysis
   - Related news articles
   - Identified entities

## Example Response

```json
{
  "claim": "The claim you checked",
  "sentiment": 0.1,
  "entities": {
    "people": ["John Doe"],
    "organizations": ["NASA"],
    "dates": ["2023"],
    "numbers": ["100"]
  },
  "related_articles": [
    {
      "title": "Article Title",
      "description": "Article description",
      "url": "https://example.com",
      "source": "News Source",
      "published_at": "2023-01-01T00:00:00Z"
    }
  ],
  "ai_analysis": "Detailed AI analysis of the claim",
  "credibility_score": 75,
  "timestamp": "2023-01-01T00:00:00Z"
}
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Disclaimer

This tool is designed to assist in fact-checking but should not be considered the final authority on any claim. Always verify important information through multiple credible sources.
