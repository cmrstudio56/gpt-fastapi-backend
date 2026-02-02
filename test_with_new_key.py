import requests

with open("openrouter_key.txt", "r") as f:
    api_key = f.read().strip()

headers = {
    "Authorization": f"Bearer {api_key}",
    "Content-Type": "application/json"
}

payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "test"}],
    "max_tokens": 50
}

print("Testing OpenRouter API with new setup...")
try:
    r = requests.post("https://openrouter.io/api/v1/chat/completions", headers=headers, json=payload)
    print(f"Status Code: {r.status_code}")
    if r.status_code == 200:
        print("SUCCESS! API is working")
        data = r.json()
        print(f"Response: {data.get('choices', [{}])[0].get('message', {}).get('content', 'N/A')[:100]}")
    else:
        print(f"Error response: {r.text[:200] if r.text else '(empty response)'}")
except Exception as e:
    print(f"Exception: {e}")
