import os
import requests

from lxml import etree

def main():

    try:

        import getpass
 #==========================================================
 # Target Qualys Platform Details
 #==========================================================       

        username = "your_username"
        password = "your_password"
        target_url = ""

        xml_file = "sogei_tags_01.xml"
# ======================================================================
# READ XML FILE
# ======================================================================
        tree = etree.parse(xml_file)

        root = tree.getroot()

        tags = root.findall(".//Tag")
        parsed_tags = []
        
        root_tags = 0
        child_tags = 0
        dynamic_tags = 0
        print("\nScanning XML...")

        for tag in tags:
            parent = tag.findtext("parentTagId")
            rule = tag.findtext("ruleType")
            if parent:
                child_tags += 1
            else:
                root_tags += 1
            if rule:
                dynamic_tags += 1
        print("\n====================================")
        print("XML Statistics")
        print("====================================")

        print(f"Total Tags     : {len(tags)}")
        print(f"Root Tags      : {root_tags}")
        print(f"Child Tags     : {child_tags}")
        print(f"Dynamic Tags   : {dynamic_tags}")

        print("====================================")

        print("\nBuilding Tag Objects...")
        parsed_tags = []
        for tag in tags:
            tag_object = {
                "old_id": tag.findtext("id"),
                "name": tag.findtext("name"),
                "parent_id": tag.findtext("parentTagId"),
                "description": tag.findtext("description"),
                "criticality": tag.findtext("criticalityScore"),
                "rule_type": tag.findtext("ruleType"),
                "rule_text": tag.findtext("ruleText")
            }
            parsed_tags.append(tag_object)    
        print(f"Created {len(parsed_tags)} Python Tag Objects.")
        print("\nFirst Parsed Object")
        print("=" * 40)
        print(parsed_tags[0])

        imported = 0
        failed = 0
        skipped = 0

        old_to_new = {}
        parent_queue = []

        output = ""

        def int_to_hex_color(value):

            if value is None:
                return None

            return format(
                value & 0xFFFFFF,
                "06x"
            )

        output += (
            "=====================================\n"
        )

        output += (
            "PASS 1 - CREATE TAGS\n"
        )

        output += (
            "=====================================\n\n"
        )

        # ====================================
        # PASS 1 - CREATE TAGS
        # ====================================

        for tag in parsed_tags:

            #if tag.get("reservedType"):

            #    skipped += 1
            #    continue

            payload = {

                "name":
                    tag(
                        "name", 
                        ""
                    ),

                "description":
                    tag(
                        "description",
                        ""
                    ),

                "favorite":
                    tag(
                        "favorite",
                        False
                    ),

                "ruleSet":
                    True
            }

            # Criticality Score

            if tag.get(
                "criticalityScore"
            ) is not None:

                payload[
                    "criticalityScore"
                ] = tag[
                    "criticalityScore"
                ]

            # Dynamic Tag Rule

            payload["rule"] = tag.get(
                "ruleText",
                ""
            )

            payload["engine"] = tag.get(
                "ruleType",
                ""
            )

            # Color

            bg = (
                tag.get(
                    "display",
                    {}
                ).get(
                    "backgroundColor"
                )
            )

            if bg is not None:

                payload[
                    "bgColor"
                ] = int_to_hex_color(
                    bg
                )

            create_url = (

                target_url.rstrip("/")

                + "/portal-front/rest/assetview/1.0/tags/create"

            )

            response = requests.post(

                create_url,

                auth=(
                    username,
                    password
                ),

                headers={
                    "Content-Type":
                        "application/json",

                    "X-Requested-With":
                        "Migration Tool"
                },

                json=payload,

                verify=False

            )

            if response.status_code != 200:

                failed += 1

                output += (
                    f"FAILED : "
                    f"{tag.findtext('name')}\n"
                )

                continue

            imported += 1

            output += (
                f"Imported : "
                f"{tag.findtext('name')}\n"
            )

            try:

                created = response.json()

                if "tagId" in created:

                    old_to_new[
                        tag["id"]
                    ] = created[
                        "tagId"
                    ]

            except Exception:

                pass

            if tag.findtext(
                "parentTagId"
            ):

                parent_queue.append({

                    "child_old_id":
                        tag["id"],

                    "parent_old_id":
                        tag["parentId"],

                    "name":
                        tag["name"]
                })

        # ====================================
        # PASS 2 - REBUILD HIERARCHY
        # ====================================

        output += "\n"

        output += (
            "=====================================\n"
        )

        output += (
            "PASS 2 - REBUILD HIERARCHY\n"
        )

        output += (
            "=====================================\n\n"
        )

        for item in parent_queue:

            child_old_id = item[
                "child_old_id"
            ]

            parent_old_id = item[
                "parent_old_id"
            ]

            if (
                child_old_id not in old_to_new
                or
                parent_old_id not in old_to_new
            ):

                output += (
                    f"Skipped Hierarchy : "
                    f"{item['name']}\n"
                )

                continue

            child_new_id = old_to_new[
                child_old_id
            ]

            parent_new_id = old_to_new[
                parent_old_id
            ]

            update_url = (

                target_url.rstrip("/")

                + f"/portal-front/rest/assetview/1.0/tags/update/{child_new_id}"

            )

            hierarchy_payload = {

                "parentId":
                    parent_new_id

            }

            response = requests.put(

                update_url,

                auth=(
                    username,
                    password
                ),

                headers={
                    "Content-Type":
                        "application/json",

                    "X-Requested-With":
                        "Migration Tool"
                },

                json=hierarchy_payload,

                verify=False

            )

            if response.status_code == 200:

                output += (
                    f"Parent Assigned : "
                    f"{item['name']}\n"
                )

            else:

                output += (
                    f"Parent Failed : "
                    f"{item['name']}\n"
                )

        output += "\n"

        output += (
            "=====================================\n"
        )

        output += (
            f"Imported : {imported}\n"
        )

        output += (
            f"Failed : {failed}\n"
        )

        output += (
            f"Skipped System Tags : {skipped}\n"
        )

        output += (
            "=====================================\n"
        )

        return output

    except Exception as e:

        return (
            "IMPORT FAILED\n\n"
            + str(e)
        )
if __name__ == "__main__":
    main()