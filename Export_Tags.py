import requests
import json
import os
import urllib3

urllib3.disable_warnings()

SOURCE_URL = "https://source-platform-url"
USERNAME = "username"
PASSWORD = "password"

api_url = (
    SOURCE_URL.rstrip("/")
    + "/portal-front/rest/assetview/2.0/tags/list"
)

payload = {
    "root": 7514814,
    "filters": {
        "quickFilter": []
    }
}

response = requests.post(
    api_url,
    auth=(USERNAME, PASSWORD),
    json=payload,
    headers={
        "Content-Type": "application/json",
        "X-Requested-With": "Migration Tool"
    },
    verify=False
)

if response.status_code != 200:
    print("EXPORT FAILED")
    print(response.text)
    exit()

data = response.json()

os.makedirs("exports", exist_ok=True)

filepath = "exports/tags.json"

with open(filepath, "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

total_tags = data.get("total")

if total_tags is None:
    total_tags = len(data.get("tagUIDTOS", []))

print(f"Export Successful")
print(f"Total Tags Exported: {total_tags}")
print(f"Saved to: {filepath}")