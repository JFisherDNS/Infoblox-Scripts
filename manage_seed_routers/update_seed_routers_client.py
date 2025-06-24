#!/usr/bin/env python3

import csv
import requests
import json
import os
from dotenv import load_dotenv

# --- Load environment variables from .env ---
load_dotenv()

WAPI_HOST_FQDN = os.getenv("WAPI_HOST_FQDN")
WAPI_VERSION = os.getenv("WAPI_VERSION")
WAPI_USER = os.getenv("WAPI_USER")
WAPI_PASS = os.getenv("WAPI_PASS")
MEMBERPROPERTIES_REF = os.getenv("MEMBERPROPERTIES_REF")
CSV_FILE = os.getenv("CSV_FILE", "seed_routers.csv")

if not all([WAPI_HOST_FQDN, WAPI_VERSION, WAPI_USER, WAPI_PASS, MEMBERPROPERTIES_REF]):
    print("❌ Missing required environment variables in .env file.")
    exit(1)

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
url = f"{WAPI_HOST_FQDN}/wapi/{WAPI_VERSION}/discovery:memberproperties/{MEMBERPROPERTIES_REF}"
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