#!/usr/bin/env python3
"""
Generate Google OAuth token and print it for Railway setup
"""
import json
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/drive"]

print("Starting Google OAuth flow...")
print("A browser window will open. Authorize access to your Google Drive.\n")

try:
    flow = InstalledAppFlow.from_client_secrets_file(
        "client_secret.json", SCOPES
    )
    creds = flow.run_local_server(port=8080)
    
    # Print the credentials as JSON
    creds_json = creds.to_json()
    
    print("\n" + "="*80)
    print("COPY THIS ENTIRE JSON TO RAILWAY:")
    print("="*80)
    print(creds_json)
    print("="*80)
    print("\nTo set up Railway:")
    print("1. Go to https://railway.app")
    print("2. Open your project → Variables")
    print("3. Add variable:")
    print("   Name: GOOGLE_OAUTH_TOKEN_JSON")
    print("   Value: [Paste the JSON above]")
    print("\n4. Redeploy your app")
    
    # Also save to token.json
    with open("token.json", "w") as f:
        f.write(creds_json)
    print("\n✅ Token saved to token.json")
    
except Exception as e:
    print(f"Error: {str(e)}")
