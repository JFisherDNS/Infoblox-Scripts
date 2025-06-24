import os
import requests
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

WAPI_HOST_FQDN = os.getenv("WAPI_HOST_FQDN")
WAPI_VERSION = os.getenv("WAPI_VERSION")
WAPI_USER = os.getenv("WAPI_USER")
WAPI_PASS = os.getenv("WAPI_PASS")

if not all([WAPI_HOST_FQDN, WAPI_VERSION, WAPI_USER, WAPI_PASS]):
    print("❌ Missing required environment variables in .env file.")
    exit(1)

# Strip 'https://' from WAPI_HOST_FQDN if present
if WAPI_HOST_FQDN.startswith("https://"):
    host = WAPI_HOST_FQDN[len("https://"):]
else:
    host = WAPI_HOST_FQDN

# Build the URL for the discovery:memberproperties endpoint

url = f"https://{host}/wapi/{WAPI_VERSION}/discovery:memberproperties"

response = requests.get(
    url,
    auth=(WAPI_USER, WAPI_PASS),
    verify=False  # Skip SSL verification like curl -k
)

if response.status_code == 200:
    data = response.json()
    for member in data:
        ref = member.get('_ref', '')
        guid = ref.split('/')[1].split(':')[0] if ref else 'N/A'
        name = member.get('discovery_member', 'N/A')
        print(f"Name: {name}, GUID: {guid}")
else:
    print(f"❌ Error ({response.status_code}): {response.text}")