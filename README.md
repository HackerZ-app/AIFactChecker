# AI-Powered Fact Checker

This web application provides a date-aware, AI-analyzed verdict on claims by synthesizing real-time evidence from professional fact-checking databases and a curated list of trusted sources.

## Features
- **Hybrid Evidence Model:** Combines Google's Fact Check API with a custom search of trusted sources (Wikipedia, BBC, Reuters, etc.).
- **Date-Aware AI Analysis:** Uses the Gemini AI to determine if a claim is true *right now*, providing accurate answers for time-sensitive queries.
- **Intelligent Verdict System:** Generates a single, nuanced verdict (e.g., "Likely True", "Likely False") with a calculated confidence score.
- **Dynamic Frontend:** A clean, modern UI with a separate results page, built with Flask and Tailwind CSS.

## Project Setup

Follow these steps to run the project on your local machine.

### 1. Prerequisites
- Python 3.8+
- An active Google Cloud account with billing enabled.
- Git installed on your system.

### 2. Installation

First, clone the repository to your machine:
```bash
git clone <your-repository-url>
cd AIFactChecker
