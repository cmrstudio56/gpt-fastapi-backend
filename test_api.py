#!/usr/bin/env python3
"""Test Google Drive API connection"""
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
import json

# Load token
with open('token.json', 'r') as f:
    creds_data = json.load(f)

creds = Credentials.from_authorized_user_info(creds_data, ['https://www.googleapis.com/auth/drive'])
drive = build('drive', 'v3', credentials=creds)

# Test basic call
print("Testing Drive API connection...")
try:
    results = drive.files().list(q="trashed=false", spaces='drive', pageSize=5, fields='files(id, name)').execute()
    print(f'✓ Files found: {len(results.get("files", []))}')
    for f in results.get('files', []):
        print(f"  - {f['name']} ({f['id']})")
except Exception as e:
    print(f'✗ Error: {e}')

# Test our specific folder
DRIVE_FOLDER_ID = "1UNIpr8fEWbGccnyAAu01kwXa6xwPdkFk"
try:
    results = drive.files().list(
        q=f"'{DRIVE_FOLDER_ID}' in parents and trashed=false",
        spaces='drive',
        pageSize=10,
        fields='files(id, name, mimeType)'
    ).execute()
    print(f'\n✓ ISA_BRAIN folder contents: {len(results.get("files", []))}')
    for f in results.get('files', []):
        ftype = "📁" if f['mimeType'] == "application/vnd.google-apps.folder" else "📄"
        print(f"  {ftype} {f['name']} ({f['id']})")
except Exception as e:
    print(f'✗ Error reading ISA_BRAIN: {e}')
