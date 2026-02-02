#!/usr/bin/env python3
"""Debug the app by testing imports and endpoints directly"""
import sys
import traceback

print("=" * 60)
print("ISABELLA APP DEBUG")
print("=" * 60)

# Test 1: Import the app
print("\n[1] Testing app import...")
try:
    from app.main import app
    print("✓ App imported successfully")
except Exception as e:
    print(f"✗ Error importing app:")
    traceback.print_exc()
    sys.exit(1)

# Test 2: Check routes
print("\n[2] Checking routes...")
try:
    routes = [(r.path, r.methods) for r in app.routes]
    for path, methods in sorted(routes):
        if 'story' in path or path == '/':
            print(f"  {path}: {methods}")
    print(f"✓ Total routes: {len(routes)}")
except Exception as e:
    print(f"✗ Error checking routes:")
    traceback.print_exc()

# Test 3: Test status endpoint directly
print("\n[3] Testing status endpoint directly...")
try:
    from starlette.testclient import TestClient
    client = TestClient(app)
    response = client.get("/story/status")
    print(f"✓ Status code: {response.status_code}")
    print(f"✓ Response: {response.json()}")
except Exception as e:
    print(f"✗ Error testing status:")
    traceback.print_exc()

# Test 4: Test root endpoint
print("\n[4] Testing root endpoint...")
try:
    from starlette.testclient import TestClient
    client = TestClient(app)
    response = client.get("/")
    print(f"✓ Status code: {response.status_code}")
    print(f"✓ Response keys: {list(response.json().keys())}")
except Exception as e:
    print(f"✗ Error testing root:")
    traceback.print_exc()

print("\n" + "=" * 60)
print("DEBUG COMPLETE")
print("=" * 60)
