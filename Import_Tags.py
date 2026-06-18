import requests
import json
import urllib3

urllib3.disable_warnings()

TARGET_URL = "https://target-platform-url"
USERNAME = "username"
PASSWORD = "password"

JSON_FILE = "exports/tags.json"

with open(JSON_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

tags = data.get("tagUIDTOS", [])

imported = 0
failed = 0
skipped = 0

old_to_new = {}
parent_queue = []


def int_to_hex_color(value):
    if value is None:
        return None

    return format(value & 0xFFFFFF, "06x")


print("=" * 60)
print("PASS 1 - CREATE TAGS")
print("=" * 60)

for tag in tags:

    if tag.get("reservedType"):
        skipped += 1
        continue

    payload = {
        "name": tag.get("name", ""),
        "description": tag.get("description", ""),
        "favorite": tag.get("favorite", False),
        "ruleSet": True
    }

    if tag.get("criticalityScore") is not None:
        payload["criticalityScore"] = tag["criticalityScore"]

    payload["rule"] = tag.get("dynamicTagRule", "")
    payload["engine"] = tag.get("dynamicTagEngine", "")

    bg = (
        tag.get("display", {})
        .get("backgroundColor")
    )

    if bg is not None:
        payload["bgColor"] = int_to_hex_color(bg)

    create_url = (
        TARGET_URL.rstrip("/")
        + "/portal-front/rest/assetview/1.0/tags/create"
    )

    response = requests.post(
        create_url,
        auth=(USERNAME, PASSWORD),
        headers={
            "Content-Type": "application/json",
            "X-Requested-With": "Migration Tool"
        },
        json=payload,
        verify=False
    )

    if response.status_code != 200:
        failed += 1
        print(f"FAILED : {tag.get('name')}")
        continue

    imported += 1
    print(f"Imported : {tag.get('name')}")

    try:
        created = response.json()

        if "tagId" in created:
            old_to_new[tag["id"]] = created["tagId"]

    except Exception:
        pass

    if tag.get("parentId"):
        parent_queue.append({
            "child_old_id": tag["id"],
            "parent_old_id": tag["parentId"],
            "name": tag["name"]
        })

print("\n")
print("=" * 60)
print("PASS 2 - REBUILD HIERARCHY")
print("=" * 60)

for item in parent_queue:

    if (
        item["child_old_id"] not in old_to_new
        or item["parent_old_id"] not in old_to_new
    ):
        print(f"Skipped Hierarchy : {item['name']}")
        continue

    child_new_id = old_to_new[item["child_old_id"]]
    parent_new_id = old_to_new[item["parent_old_id"]]

    update_url = (
        TARGET_URL.rstrip("/")
        + f"/portal-front/rest/assetview/1.0/tags/update/{child_new_id}"
    )

    response = requests.put(
        update_url,
        auth=(USERNAME, PASSWORD),
        headers={
            "Content-Type": "application/json",
            "X-Requested-With": "Migration Tool"
        },
        json={
            "parentId": parent_new_id
        },
        verify=False
    )

    if response.status_code == 200:
        print(f"Parent Assigned : {item['name']}")
    else:
        print(f"Parent Failed : {item['name']}")

print("\n")
print("=" * 60)
print(f"Imported : {imported}")
print(f"Failed : {failed}")
print(f"Skipped System Tags : {skipped}")
print("=" * 60)