import os
import json

# Read the key
with open("fastapi openrouter .txt", "r") as f:
    api_key = f.read().strip()

# Write a test Python script that will make the exact request with debugging
code = '''
import requests
import json

api_key = "{}"

headers = {{
    "Authorization": "Bearer {{}}".format(api_key),
    "Content-Type": "application/json",
    "HTTP-Referer": "https://test.app",
    "X-Title": "TestApp"
}}

payload = {{
    "model": "openai/gpt-3.5-turbo",
    "messages": [{{"role": "user", "content": "test"}}],
    "max_tokens": 100
}}

print("Full Headers:")
print(json.dumps(headers, indent=2))

r = requests.post("https://openrouter.io/api/v1/chat/completions", 
                  headers=headers, 
                  json=payload)

print(f"\\nStatus: {{r.status_code}}")
print(f"Response Headers: {{dict(r.headers)}}")
print(f"Response Body: {{r.text}}")

# Try with different endpoint variations
endpoints = [
    "https://api.openrouter.io/v1/chat/completions",
    "https://openrouter.io/api/v1/completions",
    "https://openrouter.io/v1/chat/completions",
]

for ep in endpoints:
    print(f"\\nTrying {{ep}}...")
    try:
        r = requests.post(ep, headers=headers, json=payload, timeout=3)
        print(f"Status: {{r.status_code}}")
    except Exception as e:
        print(f"Error: {{e}}")
'''.format(api_key)

with open("_test_post.py", "w") as f:
    f.write(code)

print("Created test script")
