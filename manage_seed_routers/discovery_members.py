import os
import requests
from dotenv import load_dotenv

def load_env_variables():
    """
    Loads environment variables from a .env file and returns the required Infoblox connection parameters.
    Returns:
        tuple: (host_fqdn, wapi_version, username, password)
    """
    load_dotenv()
    WAPI_HOST_FQDN = os.getenv("WAPI_HOST_FQDN")
    WAPI_VERSION = os.getenv("WAPI_VERSION")
    WAPI_USER = os.getenv("WAPI_USER")
    WAPI_PASS = os.getenv("WAPI_PASS")

    if not all([WAPI_HOST_FQDN, WAPI_VERSION, WAPI_USER, WAPI_PASS]):
        print("❌ Missing required environment variables in .env file.")
        exit(1)
    return WAPI_HOST_FQDN, WAPI_VERSION, WAPI_USER, WAPI_PASS

def normalize_host_and_version(host_fqdn, wapi_version):
    """
    Strips 'https://' from the host if present and removes a leading 'v' from the version if present.
    Args:
        host_fqdn (str): The host FQDN, possibly with protocol.
        wapi_version (str): The WAPI version, possibly with leading 'v'.
    Returns:
        tuple: (host, version)
    """
    # Remove 'https://' if present
    if host_fqdn.startswith("https://"):
        host = host_fqdn[len("https://"):]
    else:
        host = host_fqdn
    # Remove leading 'v' if present
    version = wapi_version[1:] if wapi_version.startswith("v") else wapi_version
    return host, version

def get_discovery_members(host, version, username, password):
    """
    Queries the Infoblox WAPI for discovery member properties and prints each member's name and GUID.
    Args:
        host (str): The Infoblox Grid host (without protocol).
        version (str): The WAPI version (without leading 'v').
        username (str): Infoblox username.
        password (str): Infoblox password.
    """
    url = f"https://{host}/wapi/v{version}/discovery:memberproperties"
    response = requests.get(
        url,
        auth=(username, password),
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

if __name__ == "__main__":
    # Load environment variables
    WAPI_HOST_FQDN, WAPI_VERSION, WAPI_USER, WAPI_PASS = load_env_variables()
    # Normalize host and version
    host, version = normalize_host_and_version(WAPI_HOST_FQDN, WAPI_VERSION)
    # Query and print discovery members
    get_discovery_members(host, version,