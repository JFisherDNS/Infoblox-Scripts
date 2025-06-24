import os
from dotenv import load_dotenv
from infoblox_client import connector, objects

# Load environment variables from .env
load_dotenv()

GRID_HOST = os.getenv("WAPI_HOST")
USERNAME = os.getenv("WAPI_USER")
PASSWORD = os.getenv("WAPI_PASS")
WAPI_VERSION = os.getenv("WAPI_VERSION")

if not all([GRID_HOST, USERNAME, PASSWORD, WAPI_VERSION]):
    print("❌ Missing required environment variables in .env file.")
    exit(1)

def main():
    opts = {
        'host': GRID_HOST,
        'username': USERNAME,
        'password': PASSWORD,
        'wapi_version': WAPI_VERSION,
        'ssl_verify': False
    }

    conn = connector.Connector(opts)

    print("Discovery Member Properties:")
    for member in objects.DiscoveryMemberProperties.search(conn):
        print("-" * 40)
        for k, v in member.items():
            print(f"{k}: {v}")

if __name__ == "__main__":
    main()