import requests
import json

api_key = "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"

# Try WITHOUT extra headers
headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [
        {"role": "user", "content": "hello"}
    ],
    "temperature": 1,
    "max_tokens": 50
}

print("Test 1: Minimal headers, POST /chat/completions")
r = requests.post(
    "https://openrouter.io/api/v1/chat/completions",
    headers=headers,
    json=payload,
    timeout=10
)
print(f"Status: {r.status_code}")
print(f"Headers returned: {dict(r.headers)}")
print(f"Body: {r.text if r.text else '(empty)'}")

if r.status_code == 405:
    print("\nDEBUGGING: 405 with empty body suggests:")
    print("- Possible CORS issue")
    print("- Possible API rate limiting")
    print("- Possible wrong endpoint")
    print("\nTrying with explicit method...")
    
    # Try with requests.request instead of post
    r2 = requests.request(
        "POST",
        "https://openrouter.io/api/v1/chat/completions",
        headers=headers,
        json=payload
    )
    print(f"\nUsing requests.request: {r2.status_code}")
