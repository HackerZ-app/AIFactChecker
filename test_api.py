import requests
import json
import os
from dotenv import load_dotenv

# Load variables from the .env file
load_dotenv()

# --- CONFIGURATION (Loaded securely) ---
API_KEY = os.getenv("GEMINI_API_KEY")
# ------------------------------------

# Check if the key was loaded successfully
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file. Please create one.")

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
    else:
        print("\n--- Request Failed ---")
        print("The API returned a non-success status code. Check the raw response above for error details.")


except requests.exceptions.RequestException as e:
    print(f"\nAn error occurred while making the request: {e}")
