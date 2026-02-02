import requests

with open('openrouter_key.txt') as f:
    key = f.read().strip()

# Try OPTIONS first to see what methods are allowed
print("Checking OPTIONS endpoint...")
r = requests.options("https://openrouter.io/api/v1/chat/completions")
print(f"OPTIONS Status: {r.status_code}")
print(f"Allow header: {r.headers.get('Allow', 'Not specified')}")

# Try with redirects disabled
print("\nTesting POST without redirects...")
r = requests.post(
    "https://openrouter.io/api/v1/chat/completions",
    headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
    json={"model": "openai/gpt-3.5-turbo", "messages": [{"role": "user", "content": "hi"}]},
    allow_redirects=False
)
print(f"Status: {r.status_code}")
if r.status_code >= 300 and r.status_code < 400:
    print(f"Location header: {r.headers.get('Location', 'None')}")

print(f"Full response: {r.text}")
