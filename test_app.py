#!/usr/bin/env python3
"""
Simple test script to verify the AI Fact Checker application
"""

import requests
import json
import time

def test_application():
    """Test the fact checker application"""
    base_url = "http://localhost:5000"
    
    print("🧪 Testing AI Fact Checker Application")
    print("=" * 50)
    
    # Test health endpoint
    print("1. Testing health endpoint...")
    try:
        response = requests.get(f"{base_url}/health", timeout=10)
        if response.status_code == 200:
            print("✅ Health check passed")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check failed: {e}")
        return False
    
    # Test main page
    print("\n2. Testing main page...")
    try:
        response = requests.get(base_url, timeout=10)
        if response.status_code == 200 and "AI Fact Checker" in response.text:
            print("✅ Main page loads correctly")
        else:
            print(f"❌ Main page failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Main page failed: {e}")
        return False
    
    # Test fact checking endpoint with a simple claim
    print("\n3. Testing fact checking functionality...")
    test_claim = "The Earth is round"
    
    try:
        response = requests.post(
            f"{base_url}/check",
            json={"claim": test_claim},
            headers={"Content-Type": "application/json"},
            timeout=30
        )
        
        if response.status_code == 200:
            data = response.json()
            print("✅ Fact check endpoint works")
            print(f"   Claim: {data.get('claim', 'N/A')}")
            print(f"   Credibility Score: {data.get('credibility_score', 'N/A')}")
            
            if 'error' in data:
                print(f"   Note: {data['error']}")
            else:
                print("   AI Analysis available: ✅" if data.get('ai_analysis') else "   AI Analysis: ❌")
                print(f"   Related Articles: {len(data.get('related_articles', []))}")
                print(f"   Entities Found: {len(data.get('entities', {}))}")
        else:
            print(f"❌ Fact check failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Fact check failed: {e}")
        return False
    
    print("\n🎉 All tests passed! Application is working correctly.")
    print("\n📝 Note: For full functionality, make sure to:")
    print("   - Set up your OpenAI API key in .env file")
    print("   - Set up your NewsAPI key in .env file")
    
    return True

if __name__ == "__main__":
    test_application()