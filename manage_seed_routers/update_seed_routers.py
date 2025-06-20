#!/usr/bin/env python3


import csv
import requests
import json

# --- Config ---
WAPI_HOST = "https://<gridmaster_fqdn>"
WAPI_VERSION = "v2.13.6"
WAPI_USER = "<api_username>"
WAPI_PASS = "<api_password>"
MEMBERPROPERTIES_REF = "<discovery_member_guid>"
CSV_FILE = "seed_routers.csv"

# --- Build list of seed routers from CSV ---
seed_routers = []
with open(CSV_FILE, newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        router = {
            "address": row["address"].strip(),
            "network_view": row["network_view"].strip()
        }
        if "comment" in row and row["comment"].strip():
            router["comment"] = row["comment"].strip()
        seed_routers.append(router)

# --- Send PUT request ---
url = f"{WAPI_HOST}/wapi/{WAPI_VERSION}/discovery:memberproperties/{MEMBERPROPERTIES_REF}"
headers = {"Content-Type": "application/json"}

response = requests.put(
    url,
    auth=(WAPI_USER, WAPI_PASS),
    headers=headers,
    data=json.dumps({"seed_routers": seed_routers}),
    verify=False  # ⚠️ Skip SSL verification (consistent with curl -k)
)

# --- Handle response ---
if response.status_code == 200:
    print("✅ Successfully updated seed_routers:")
    print(json.dumps(response.json(), indent=2))
else:
    print(f"❌ Error ({response.status_code}): {response.text}")
