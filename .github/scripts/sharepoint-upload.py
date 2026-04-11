#!/usr/bin/env python3
"""
SharePoint File Bridge - Upload Script
Reads staging/<uuid>/manifest.json + file.b64, decodes, and uploads
to SharePoint via Microsoft Graph API using client credentials flow.
"""

import base64
import json
import os
import sys
import glob
import requests
from pathlib import Path


def get_access_token():
    tenant_id = os.environ["AZURE_TENANT_ID"]
    client_id = os.environ["AZURE_CLIENT_ID"]
    client_secret = os.environ["AZURE_CLIENT_SECRET"]
    url = f"https://login.microsoftonline.com/{tenant_id}/oauth2/v2.0/token"
    data = {
        "grant_type": "client_credentials",
        "client_id": client_id,
        "client_secret": client_secret,
        "scope": "https://graph.microsoft.com/.default",
    }
    resp = requests.post(url, data=data, timeout=30)
    resp.raise_for_status()
    return resp.json()["access_token"]


def upload_file(token, drive_id, folder_path, filename, file_bytes, conflict_behavior="replace"):
    headers = {"Authorization": f"Bearer {token}"}
    folder_path = "/" + folder_path.strip("/")
    file_size = len(file_bytes)
    if file_size <= 4 * 1024 * 1024:
        upload_url = (
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}"
            f"/root:{folder_path}/{filename}:/content"
            f"?@microsoft.graph.conflictBehavior={conflict_behavior}"
        )
        headers["Content-Type"] = "application/octet-stream"
        resp = requests.put(upload_url, headers=headers, data=file_bytes, timeout=120)
        resp.raise_for_status()
        return resp.json()
    else:
        session_url = (
            f"https://graph.microsoft.com/v1.0/drives/{drive_id}"
            f"/root:{folder_path}/{filename}:/createUploadSession"
        )
        session_body = {"item": {"@microsoft.graph.conflictBehavior": conflict_behavior, "name": filename}}
        headers_json = {**headers, "Content-Type": "application/json"}
        resp = requests.post(session_url, headers=headers_json, json=session_body, timeout=30)
        resp.raise_for_status()
        upload_url = resp.json()["uploadUrl"]
        chunk_size = 10 * 1024 * 1024
        result = None
        for start in range(0, file_size, chunk_size):
            end = min(start + chunk_size, file_size)
            chunk = file_bytes[start:end]
            content_range = f"bytes {start}-{end - 1}/{file_size}"
            chunk_headers = {"Content-Length": str(len(chunk)), "Content-Range": content_range}
            resp = requests.put(upload_url, headers=chunk_headers, data=chunk, timeout=120)
            resp.raise_for_status()
            result = resp.json()
            print(f"  Uploaded {end}/{file_size} bytes ({100 * end // file_size}%)")
        return result


def process_staging_directory(staging_dir, token, drive_id):
    manifest_path = os.path.join(staging_dir, "manifest.json")
    if not os.path.exists(manifest_path):
        print(f"  SKIP: No manifest.json in {staging_dir}")
        return False
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    filename = manifest["filename"]
    sharepoint_folder = manifest["sharepoint_folder"]
    source_file = manifest.get("source_file", "file.b64")
    encoding = manifest.get("encoding", "base64")
    source_path = os.path.join(staging_dir, source_file)
    if not os.path.exists(source_path):
        print(f"  ERROR: Source file {source_path} not found")
        return False
    print(f"  File: {filename}")
    print(f"  Destination: {sharepoint_folder}")
    with open(source_path, "r") as f:
        raw = f.read().strip()
    if encoding == "base64":
        file_bytes = base64.b64decode(raw)
    elif encoding == "raw":
        with open(source_path, "rb") as f:
            file_bytes = f.read()
    else:
        print(f"  ERROR: Unknown encoding: {encoding}")
        return False
    print(f"  Size: {len(file_bytes):,} bytes")
    result = upload_file(
        token=token, drive_id=drive_id, folder_path=sharepoint_folder,
        filename=filename, file_bytes=file_bytes,
        conflict_behavior=manifest.get("conflict_behavior", "replace"),
    )
    web_url = result.get("webUrl", "N/A")
    item_id = result.get("id", "N/A")
    print(f"  SUCCESS: {web_url}")
    print(f"  Item ID: {item_id}")
    return True


def main():
    drive_id = os.environ.get(
        "SHAREPOINT_DRIVE_ID",
        "b!wPs8sWIq70Kt7RsL80wFKBqB2HWWzZdAnhoakfwfYIWRgc_-ZgmSTLpthkkQlSJu",
    )
    staging_dirs = sorted(glob.glob("staging/*/"))
    if not staging_dirs:
        print("No staging directories found. Nothing to upload.")
        sys.exit(0)
    print(f"Found {len(staging_dirs)} staging package(s)")
    print()
    print("Authenticating with Microsoft Graph API...")
    token = get_access_token()
    print("Authenticated successfully")
    print()
    success_count = 0
    fail_count = 0
    for staging_dir in staging_dirs:
        dir_name = Path(staging_dir).name
        print(f"Processing: {dir_name}")
        try:
            if process_staging_directory(staging_dir, token, drive_id):
                success_count += 1
            else:
                fail_count += 1
        except Exception as e:
            print(f"  FAILED: {e}")
            fail_count += 1
        print()
    print(f"Done. {success_count} uploaded, {fail_count} failed.")
    if fail_count > 0:
        sys.exit(1)


if __name__ == "__main__":
    main()
