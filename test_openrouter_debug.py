import os
import requests
import json

# Load API Key
try:
    with open("fastapi openrouter .txt", "r") as f:
        api_key = f.read().strip()
except:
    api_key = os.environ.get("OPENROUTER_API_KEY")

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json",
    "HTTP-Referer": "https://isabella.ai",
}

print("Testing GET /models...")
try:
    url = "https://openrouter.io/api/v1/models"
    response = requests.get(url, headers=headers)
    print(f"Status: {response.status_code}")
    if response.status_code != 200:
        print(f"Response: {response.text}")
    else:
        print("GET /models success")
except Exception as e:
    print(f"Error: {e}")

print("\nTesting POST /chat/completions with minimal payload...")
url = "https://openrouter.io/api/v1/chat/completions"
payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "hi"}]
}
try:
    response = requests.post(url, headers=headers, json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {response.text}")
except Exception as e:
    print(f"Error: {e}")
