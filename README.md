# AI Fact Checker

A dynamic web application that verifies news and information against credible sources using AI-powered fact-checking algorithms.

![AI Fact Checker](https://img.shields.io/badge/Status-Active-green) ![License](https://img.shields.io/badge/License-MIT-blue) ![Version](https://img.shields.io/badge/Version-1.0.0-orange)

## 🌟 Features

- **Dynamic UI**: Modern, responsive web interface for fact-checking
- **Real-time Analysis**: Instant fact verification with loading states
- **Credible Sources**: Integration with trusted news and fact-checking organizations
- **Smart Categorization**: Automatic claim type detection (health, politics, science, etc.)
- **Confidence Scoring**: AI-powered confidence levels for fact-check results
- **Source Verification**: Detailed source credibility and relevance scoring
- **Mobile Responsive**: Works seamlessly on desktop and mobile devices

## 🚀 Quick Start

### Option 1: Simple Web Application (Frontend Only)

1. **Clone the repository**:
   ```bash
   git clone https://github.com/HackerZ-app/AIFactChecker.git
   cd AIFactChecker
   ```

2. **Open in browser**:
   ```bash
   # On most systems, you can simply open index.html in your browser
   open index.html
   # Or use a simple HTTP server
   python -m http.server 8000
   # Then visit http://localhost:8000
   ```

### Option 2: Full Application with Backend API

1. **Install Python dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the Flask backend**:
   ```bash
   python app.py
   ```

3. **Open the application**:
   - Backend API: http://localhost:5000
   - Frontend: Open `index.html` in your browser

### Option 3: Docker Deployment

1. **Using Docker Compose** (Recommended):
   ```bash
   docker-compose up -d
   ```
   - Application will be available at http://localhost

2. **Using Docker only**:
   ```bash
   docker build -t ai-fact-checker .
   docker run -p 5000:5000 ai-fact-checker
   ```

## 🎯 How to Use

1. **Enter a Claim**: Type or paste any news article, statement, or claim into the text area
2. **Click "Check Facts"**: The AI will analyze your claim against credible sources
3. **Review Results**: See the verdict, confidence score, and supporting sources
4. **Explore Sources**: Click on source links to read the full articles

### Example Claims to Test

- "COVID-19 vaccines are 95% effective against severe disease"
- "The 2020 US election was the most secure in American history"
- "Climate change is causing more frequent extreme weather events"
- "SpaceX successfully landed humans on Mars in 2024"

## 🏗️ Architecture

### Frontend Components
- **HTML5**: Semantic structure with accessibility features
- **CSS3**: Modern styling with animations and responsive design
- **JavaScript (ES6+)**: Dynamic functionality and API integration

### Backend Components
- **Flask**: Python web framework for REST API
- **CORS**: Cross-origin resource sharing support
- **Gunicorn**: Production WSGI server

### Infrastructure
- **Docker**: Containerization for easy deployment
- **Nginx**: Reverse proxy and static file serving
- **Docker Compose**: Multi-container orchestration

## 📊 Credible Sources

The application uses the following trusted sources for fact-checking:

### News Organizations
- **Reuters** (95% credibility score)
- **Associated Press** (94% credibility score)
- **BBC News** (92% credibility score)
- **NPR** (91% credibility score)

### Fact-Checking Organizations
- **Snopes** (89% credibility score)
- **PolitiFact** (88% credibility score)
- **FactCheck.org** (90% credibility score)

### Specialized Sources
- **World Health Organization** (96% credibility score) - Health
- **CDC** (95% credibility score) - Health
- **NASA** (97% credibility score) - Science

## 🔧 API Documentation

### Endpoints

#### POST /api/fact-check
Check facts for a given claim.

**Request:**
```json
{
  "claim": "Your claim or statement to fact-check"
}
```

**Response:**
```json
{
  "claim": "The original claim",
  "analysis": {
    "keywords": ["extracted", "keywords"],
    "type": "health|politics|science|economics|general",
    "sentiment": "positive|negative|neutral",
    "complexity": "low|medium|high"
  },
  "sources": [
    {
      "name": "Source Name",
      "url": "https://example.com/article",
      "credibilityScore": 95,
      "relevanceScore": 87,
      "excerpt": "Article excerpt..."
    }
  ],
  "verdict": {
    "type": "true|false|mixed|unverified",
    "label": "Human-readable verdict"
  },
  "confidence": 85,
  "timestamp": "2024-01-01T12:00:00Z"
}
```

#### GET /api/sources
Get list of all credible sources.

#### GET /api/health
Health check endpoint.

## 🛠️ Development

### Project Structure
```
AIFactChecker/
├── index.html          # Main web page
├── styles.css          # Styling and responsive design
├── script.js           # Frontend JavaScript logic
├── app.py             # Flask backend API
├── requirements.txt   # Python dependencies
├── Dockerfile         # Docker container configuration
├── docker-compose.yml # Multi-container setup
├── nginx.conf         # Nginx configuration
└── README.md          # This file
```

### Adding New Features

1. **Frontend**: Modify `script.js` for new UI features
2. **Backend**: Update `app.py` for new API endpoints
3. **Styling**: Edit `styles.css` for visual changes

### Testing Locally

1. Start the backend: `python app.py`
2. Open `index.html` in your browser
3. Test with various types of claims

## 📱 Mobile Support

The application is fully responsive and supports:
- Touch-friendly interface
- Optimized layouts for mobile screens
- Fast loading on mobile networks
- Accessible navigation

## 🔒 Security Features

- Input validation and sanitization
- CORS protection
- Rate limiting (in production setup)
- No storage of user claims

## 🚀 Deployment Options

### Local Development
- Simple file serving or Python HTTP server

### Cloud Deployment
- **Heroku**: Use included `Dockerfile`
- **AWS**: Deploy with ECS or Elastic Beanstalk
- **Google Cloud**: Use Cloud Run
- **DigitalOcean**: Deploy with App Platform

### Self-Hosted
- Use Docker Compose for full stack deployment
- Nginx reverse proxy included

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Inspired by the need for accurate information in the digital age
- Built with modern web technologies for accessibility and performance
- Designed to promote media literacy and critical thinking

---

**Disclaimer**: This is a demonstration application. While it uses realistic source credibility scores and fact-checking methodology, it should not be used as the sole source for determining the truthfulness of claims. Always verify important information through multiple credible sources.
