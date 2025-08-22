#!/usr/bin/env python3
"""
Test script to verify GPTs API connection
"""

import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_gpt_api():
    """Test the GPTs API connection"""
    
    api_key = os.getenv("GPT_API_KEY")
    api_url = os.getenv("GPT_API_URL")
    
    if not api_key:
        print("❌ GPT_API_KEY not found in environment variables")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "gpt-4",
        "messages": [
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": "Hello! Can you respond with just 'API test successful'?"}
        ],
        "max_tokens": 50,
        "temperature": 0.7
    }
    
    try:
        print("🔌 Testing GPTs API connection...")
        response = requests.post(api_url, headers=headers, json=payload, timeout=30)
        
        if response.status_code == 200:
            result = response.json()
            message = result["choices"][0]["message"]["content"]
            print(f"✅ API test successful! Response: {message}")
            return True
        else:
            print(f"❌ API test failed. Status: {response.status_code}")
            print(f"Response: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Error testing API: {e}")
        return False

if __name__ == "__main__":
    test_gpt_api()
