import requests
import json
import os
import urllib3
import json
import requests
import time

urllib3.disable_warnings()

SOURCE_URL = "https://source-platform-url"
USERNAME = "username"
PASSWORD = "password"

api_url = (
    SOURCE_URL.rstrip("/")
    + "/portal-front/rest/assetview/2.0/tags/list"
)

# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

BASE_URL = SOURCE_URL

HEADERS = {
    "Accept": "application/json",
    "Content-Type": "application/json"
}

# use your existing authenticated session
session = requests.Session()

# --------------------------------------------------
# GET CHILD TAGS
# --------------------------------------------------

def get_children(parent_id):
    """
    Returns children under a tag.
    """

    payload = {
        "root": parent_id,
        "filters": {
            "quickFilter": []
        }
    }

    url = f"{BASE_URL}/assetview/1.0/tags"

    try:
        response = session.post(
            url,
            headers=HEADERS,
            json=payload,
            verify=False
        )

        response.raise_for_status()

        data = response.json()

        return data.get("tagUIDTOS", [])

    except Exception as e:
        print(f"Error retrieving children for {parent_id}: {e}")
        return []


# --------------------------------------------------
# BUILD TREE RECURSIVELY
# --------------------------------------------------

def build_tree(tag):
    """
    Recursively discovers all descendants.
    """

    tag_id = tag["id"]

    children = get_children(tag_id)

    tag["children"] = []

    for child in children:

        child_tree = build_tree(child)

        tag["children"].append(child_tree)

    return tag


# --------------------------------------------------
# GET ROOT TAGS
# --------------------------------------------------

def get_root_tags():
    """
    Retrieves top-level tags.
    """

    payload = {
        "root": 0,
        "filters": {
            "quickFilter": []
        }
    }

    url = f"{BASE_URL}/assetview/1.0/tags"

    response = session.post(
        url,
        headers=HEADERS,
        json=payload,
        verify=False
    )

    response.raise_for_status()

    data = response.json()

    return data.get("tagUIDTOS", [])


# --------------------------------------------------
# EXPORT
# --------------------------------------------------

def export_all_tags():

    print("Loading root tags...")

    roots = get_root_tags()

    print(f"Found {len(roots)} root tags")

    export_data = []

    for root in roots:

        print(
            f"Processing: {root['name']} ({root['id']})"
        )

        tree = build_tree(root)

        export_data.append(tree)

        time.sleep(0.2)

    with open(
        "all_tags_export.json",
        "w",
        encoding="utf-8"
    ) as f:

        json.dump(
            export_data,
            f,
            indent=4,
            ensure_ascii=False
        )

    print()
    print("Export completed.")
    print("Output: all_tags_export.json")


# --------------------------------------------------

if __name__ == "__main__":
    export_all_tags()

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