#!/usr/bin/env python
"""
Complete Railway startup diagnostic
Tests everything that could fail on Railway
"""

import sys
import os

print("=" * 60)
print("ISABELLA RAILWAY STARTUP DIAGNOSTIC")
print("=" * 60)

# TEST 1: Check Python version
print("\n[1] Python Version Check")
print(f"Python: {sys.version}")
print(f"Version match: {sys.version.startswith('3.11')}")

# TEST 2: Check all required files exist
print("\n[2] Required Files Check")
required_files = [
    "requirements.txt",
    "runtime.txt",
    "nixpacks.toml",
    "app/main.py",
    "openrouter_key.txt",
    "token.json"
]
for f in required_files:
    exists = os.path.exists(f)
    status = "✓" if exists else "✗"
    print(f"{status} {f}")

# TEST 3: Try importing all dependencies
print("\n[3] Dependencies Import Check")
deps = [
    "fastapi",
    "uvicorn",
    "pydantic",
    "google.oauth2.credentials",
    "google_auth_oauthlib.flow",
    "googleapiclient.discovery",
    "requests"
]

for dep in deps:
    try:
        __import__(dep)
        print(f"✓ {dep}")
    except ImportError as e:
        print(f"✗ {dep}: {e}")

# TEST 4: Try importing the main app
print("\n[4] App Import Check")
try:
    from app.main import app
    print(f"✓ app.main imported")
    print(f"✓ FastAPI app object created")
    
    # Check routes
    routes = [r.path for r in app.routes]
    print(f"✓ Routes available: {len(routes)}")
    for r in routes:
        if 'story' in r:
            print(f"  - {r}")
except Exception as e:
    print(f"✗ CRITICAL ERROR: {type(e).__name__}: {e}")
    import traceback
    traceback.print_exc()

# TEST 5: Check environment variables
print("\n[5] Environment Variables Check")
env_vars = ["OPENROUTER_API_KEY", "GOOGLE_OAUTH_TOKEN_JSON"]
for var in env_vars:
    value = os.environ.get(var)
    status = "✓ SET" if value else "✗ MISSING"
    print(f"{status}: {var}")

# TEST 6: Check key files are readable
print("\n[6] Key Files Readability Check")
try:
    with open("openrouter_key.txt", "r") as f:
        key = f.read().strip()
        print(f"✓ openrouter_key.txt readable ({len(key)} chars)")
except Exception as e:
    print(f"✗ openrouter_key.txt: {e}")

try:
    with open("token.json", "r") as f:
        token = f.read()
        print(f"✓ token.json readable ({len(token)} chars)")
except Exception as e:
    print(f"✗ token.json: {e}")

print("\n" + "=" * 60)
print("DIAGNOSTIC COMPLETE")
print("=" * 60)
