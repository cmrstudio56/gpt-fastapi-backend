import requests
import json

# Read API key
with open("fastapi openrouter .txt", "r") as f:
    api_key = f.read().strip()

# Test 1: Check if API key is valid by getting models list
print("=== TEST 1: Validating API Key ===")
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
}

try:
    r = requests.get("https://openrouter.io/api/v1/models", headers=headers, timeout=5)
    print(f"Status: {r.status_code}")
    if r.status_code == 200:
        models = r.json()
        print(f" API Key is VALID - Found {len(models.get('data', []))} models")
        # Show first few model IDs
        first_models = [m['id'] for m in models.get('data', [])[:5]]
        print(f"Sample models: {first_models}")
    else:
        print(f" API Key validation failed: {r.text}")
except Exception as e:
    print(f"Error: {e}")

# Test 2: Try a simple POST with correct headers
print("\n=== TEST 2: Testing POST Endpoint ===")
payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "hello"}],
    "max_tokens": 10
}

try:
    r = requests.post("https://openrouter.io/api/v1/chat/completions", 
                      headers=headers, 
                      json=payload, 
                      timeout=10)
    print(f"Status: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
