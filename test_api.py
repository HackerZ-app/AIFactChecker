import requests
import json

# --- CONFIGURATION ---
# Paste your exact API key between the quotes
API_KEY = "AIzaSyAxcnZyorIzh45G4eVzNYmMafSgQMKDoLE" 
# ---------------------

# The URL and a simple query
FACTCHECK_URL = "https://factchecktools.googleapis.com/v1alpha1/claims:search"
params = {
    "query": "The sky is blue",
    "key": API_KEY
}

print("--- Sending request directly to Google's API... ---")

try:
    # Make the request to the Google API
    response = requests.get(FACTCHECK_URL, params=params)

    # Print the status code we received from Google
    print(f"Google's Response Status Code: {response.status_code}")
    
    # Print the raw text response from Google
    print("\n--- Raw Response from Google ---")
    print(response.text)
    print("---------------------------------")
    
    # Try to format it as clean JSON to check if it's valid
    if response.status_code == 200:
        print("\n--- Formatted JSON (Success!) ---")
        print(json.dumps(response.json(), indent=2))
        print("---------------------------------")

except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred while making the request: {e}")












    from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app)

# Set your Gemini API key as an environment variable instead of hardcoding
# Example (Linux/Mac): export GEMINI_API_KEY="YOUR_KEY"
# Example (Windows): set GEMINI_API_KEY="YOUR_KEY"
# Directly assign your Gemini API key (not recommended for production)
GEMINI_API_KEY = "AIzaSyAxcnZyorIzh45G4eVzNYmMafSgQMKDoLE"


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

# Add this new route before your /check route
@app.route('/')
def index():
    return render_template('index.html')

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
    app.run(port=5500, debug=True)






<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>AI Fact Checker</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Google Fonts: Montserrat -->
    <link href="https://fonts.googleapis.com/css2?family=Montserrat:wght@400;500;600;700&display=swap" rel="stylesheet">
    <style>
        body {
            font-family: 'Montserrat', sans-serif;
            background: linear-gradient(270deg, #e0eafc, #cfdef3, #a1c4fd, #c2e9fb);
            background-size: 800% 800%;
            animation: gradientMove 18s ease infinite;
        }
        @keyframes gradientMove {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        .spinner {
            animation: spin 1s linear infinite;
        }
        .highlight-true { background-color: rgba(16, 185, 129, 0.2); }
        .highlight-false { background-color: rgba(239, 68, 68, 0.2); }
        .highlight-misleading { background-color: rgba(245, 158, 11, 0.2); }
        .highlight-unverified { background-color: rgba(156, 163, 175, 0.2); }
    </style>
</head>
<body class="text-gray-800">

<div class="container mx-auto p-4 sm:p-6 md:p-8 max-w-3xl min-h-screen">
    <!-- Header Section -->
    <div class="text-center mb-8">
        <svg class="mx-auto h-16 w-16 text-blue-500 drop-shadow-lg" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9.5 2.1a9.5 9.5 0 0 1 10 9.5c0 2.5-.9 4.8-2.5 6.5"/><path d="M15 2.5A9.5 9.5 0 0 0 8.5 22"/><path d="M2.5 15a9.5 9.5 0 0 0 19 0"/><path d="M8.5 2a9.5 9.5 0 0 0 0 19"/></svg>
        <h1 class="text-4xl sm:text-5xl font-bold text-gray-900 mt-2">AI Fact Checker</h1>
        <p class="mt-2 text-lg text-gray-600">Instantly analyze claims, articles, or text for facts.</p>
    </div>

    <!-- Input Form Section -->
    <div class="bg-white/70 backdrop-blur-xl p-6 rounded-2xl shadow-2xl border border-gray-200">
        <form id="fact-check-form">
            <textarea id="text-input" class="w-full h-40 p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition duration-200 resize-none" placeholder="e.g., A new study shows the moon is made of cheese..."></textarea>
            <div id="error-message" class="text-red-600 text-sm mt-2 text-center h-5"></div>
            <div class="flex flex-col sm:flex-row gap-2 mt-2">
                <button id="clear-btn" type="button" class="w-full sm:w-auto bg-gray-200 text-gray-700 font-semibold py-3 px-6 rounded-lg hover:bg-gray-300 active:scale-[0.98] transition-all duration-150">Clear</button>
                <button id="submit-button" type="submit" class="w-full flex-1 flex justify-center items-center gap-3 bg-blue-600 text-white font-semibold py-3 px-4 rounded-lg hover:bg-blue-700 active:scale-[0.98] transition-transform duration-150 disabled:bg-gray-400 disabled:cursor-not-allowed">
                    <svg id="button-icon" xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="m21.73 18-8-14a2 2 0 0 0-3.46 0l-8 14A2 2 0 0 0 4 21h16a2 2 0 0 0 1.73-3Z"/><path d="M12 9v4"/><path d="M12 17h.01"/></svg>
                    <span id="button-text">Check Fact</span>
                </button>
            </div>
        </form>
    </div>

    <!-- Results Section -->
    <div id="results" class="mt-8"></div>
    
    <footer class="text-center mt-8">
        <button id="about-btn" class="text-sm text-gray-600 hover:text-blue-600 hover:underline">About this tool</button>
    </footer>
</div>
    
<!-- About Modal -->
<div id="about-modal" class="fixed inset-0 bg-black bg-opacity-40 backdrop-blur-sm flex justify-center items-center hidden">
    <div class="bg-white p-8 rounded-2xl shadow-2xl max-w-sm w-full mx-4 text-center">
        <h2 class="text-2xl font-bold mb-2">About AI Fact Checker</h2>
        <p class="text-gray-600 mb-6">This tool uses Google Fact Check API to analyze claims and provide verdicts. For demonstration purposes only.</p>
        <button id="close-modal-btn" class="bg-blue-600 text-white font-semibold py-2 px-6 rounded-lg hover:bg-blue-700 transition-colors">Close</button>
    </div>
</div>

<script>
    const verdictStyles = {
        "True": { badge: "bg-green-100 text-green-800", icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-6 h-6 text-green-500"><circle cx="12" cy="12" r="10"/><path d="M16 8l-4.5 8-3.5-4"/></svg>`, highlight: "highlight-true" },
        "False": { badge: "bg-red-100 text-red-800", icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-6 h-6 text-red-500"><circle cx="12" cy="12" r="10"/><path d="M15 9l-6 6"/><path d="M9 9l6 6"/></svg>`, highlight: "highlight-false" },
        "Misleading": { badge: "bg-yellow-100 text-yellow-800", icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-6 h-6 text-yellow-500"><circle cx="12" cy="12" r="10"/><path d="M12 8v4"/><path d="M12 16h.01"/></svg>`, highlight: "highlight-misleading" },
        "Unverified": { badge: "bg-gray-100 text-gray-800", icon: `<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-6 h-6 text-gray-500"><circle cx="12" cy="12" r="10"/><path d="M12 16v-4"/><path d="M12 8h.01"/></svg>`, highlight: "highlight-unverified" }
    };

    function displayResults(data) {
        let highlightedHtml = data.originalText;
        data.claims.forEach(claim => {
            const style = verdictStyles[claim.verdict] || verdictStyles["Unverified"];
            if (style && style.highlight && claim.claim) {
                const regex = new RegExp(claim.claim.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&'), 'gi');
                highlightedHtml = highlightedHtml.replace(regex, `<span class="p-1 rounded ${style.highlight}">${claim.claim}</span>`);
            }
        });

        const highlightedTextSection = `
            <div class="bg-white/70 backdrop-blur-xl p-6 rounded-2xl shadow-xl border border-gray-200 mb-6">
                <h2 class="text-xl font-bold mb-3">Analyzed Text</h2>
                <p class="text-gray-700 leading-relaxed whitespace-pre-wrap">${highlightedHtml}</p>
            </div>
        `;
        
        let claimsHtml = "";
        if (data.claims.length === 0) {
            claimsHtml = `<div class="bg-yellow-100 border border-yellow-300 text-yellow-800 p-4 rounded-lg text-center">No claims or sources found for your query.</div>`;
        } else {
            claimsHtml = data.claims.map(claim => {
                const style = verdictStyles[claim.verdict] || verdictStyles["Unverified"];
                const sourcesHtml = claim.sources.length > 0
                    ? `<div class="mt-4 pt-4 border-t border-gray-200">
                           <h4 class="font-semibold text-sm text-gray-600 mb-2">Sources:</h4>
                           <ul class="space-y-1">
                             ${claim.sources.map(source => `<li><a href="${source.url}" target="_blank" rel="noopener noreferrer" class="text-blue-600 hover:underline text-sm flex items-center gap-1.5"><svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" class="w-4 h-4"><path d="M10 13a5 5 0 0 0 7.54.54l3-3a5 5 0 0 0-7.07-7.07l-1.72 1.72"/><path d="M14 11a5 5 0 0 0-7.54-.54l-3 3a5 5 0 0 0 7.07 7.07l1.72-1.72"/></svg>${source.title}</a></li>`).join('')}
                           </ul>
                       </div>`
                    : '';
                
                return `
                    <div class="bg-white/70 backdrop-blur-xl p-5 rounded-2xl shadow-xl border border-gray-200 mb-4 transition-all duration-300 hover:shadow-2xl">
                        <div class="flex items-start gap-4">
                            <div>${style.icon}</div>
                            <div class="flex-1">
                                <span class="text-sm font-semibold px-3 py-1 rounded-full ${style.badge}">${claim.verdict}</span>
                                <blockquote class="mt-3 text-gray-800 italic">“${claim.claim || "No claim found"}”</blockquote>
                            </div>
                        </div>
                        <div class="mt-3 pl-10">
                            <p class="text-sm text-gray-600">${claim.explanation || ""}</p>
                            ${sourcesHtml}
                        </div>
                    </div>
                `;
            }).join('');
        }

        resultsDiv.innerHTML = highlightedTextSection + claimsHtml;
    }

    // DOM references
    const form = document.getElementById('fact-check-form');
    const textInput = document.getElementById('text-input');
    const resultsDiv = document.getElementById('results');
    const errorMessage = document.getElementById('error-message');
    const submitButton = document.getElementById('submit-button');
    const buttonText = document.getElementById('button-text');
    const buttonIcon = document.getElementById('button-icon');
    const clearBtn = document.getElementById('clear-btn');
    const aboutBtn = document.getElementById('about-btn');
    const aboutModal = document.getElementById('about-modal');
    const closeModalBtn = document.getElementById('close-modal-btn');

    // Show spinner while loading
    function showSpinner() {
        buttonIcon.classList.add('spinner');
        buttonText.textContent = 'Checking...';
        submitButton.disabled = true;
    }
    function hideSpinner() {
        buttonIcon.classList.remove('spinner');
        buttonText.textContent = 'Check Fact';
        submitButton.disabled = false;
    }

    // Form submit handler
    form.addEventListener('submit', async (e) => {
        e.preventDefault();
        errorMessage.textContent = '';
        resultsDiv.innerHTML = '';
        const text = textInput.value.trim();
        if (!text) {
            errorMessage.textContent = 'Please enter some text to check.';
            return;
        }
        showSpinner();
        try {
            const response = await fetch('http://localhost:5500/check', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ text })
            });
            const data = await response.json();
            hideSpinner();
            if (data.error) {
                errorMessage.textContent = data.error;
            } else {
                displayResults(data);
            }
        } catch (err) {
            hideSpinner();
            errorMessage.textContent = 'Could not connect to backend. Is the server running?';
        }
    });

    // Clear button handler
    clearBtn.addEventListener('click', () => {
        textInput.value = '';
        errorMessage.textContent = '';
        resultsDiv.innerHTML = '';
    });

    // About modal handlers
    aboutBtn.addEventListener('click', () => {
        aboutModal.classList.remove('hidden');
    });
    closeModalBtn.addEventListener('click', () => {
        aboutModal.classList.add('hidden');
    });

    // Allow Enter to submit, Shift+Enter for newline
    textInput.addEventListener('keydown', function(e) {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            submitButton.click();
        }
    });
</script>
</body>
</html>