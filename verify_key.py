import requests

# Read the key directly
with open('openrouter_key.txt', 'r') as f:
    key = f.read().strip()

print(f"Key loaded: {key}")
print(f"Key length: {len(key)}")

# Test with explicit accept and user-agent headers
headers = {
    "Authorization": f"Bearer {key}",
    "Content-Type": "application/json",
    "Accept": "application/json",
    "User-Agent": "Mozilla/5.0"
}

payload = {
    "model": "openai/gpt-3.5-turbo",
    "messages": [{"role": "user", "content": "test"}]
}

print("\nAttempting API call...")
resp = requests.post(
    "https://openrouter.io/api/v1/chat/completions",
    headers=headers,
    json=payload
)

print(f"Status: {resp.status_code}")
print(f"Response: {resp.text}")
