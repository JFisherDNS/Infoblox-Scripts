from infoblox_client import connector, objects
import sys

# Infoblox Grid connection parameters
GRID_HOST = 'gridmaster.example.com'  # Change to your Grid Master IP or hostname
USERNAME = 'admin'                   # Change to your username
PASSWORD = 'infoblox'                # Change to your password
WAPI_VERSION = '2.10'                # Adjust to your Infoblox WAPI version

ZONE_NAME = 'test.net'
DNS_SERVER_NAME = 'ns1.lab.local'

def main():
    opts = {
        'host': GRID_HOST,
        'username': USERNAME,
        'password': PASSWORD,
        'wapi_version': WAPI_VERSION,
        'ssl_verify': False
    }

    conn = connector.Connector(opts)

    # Find the authoritative zone
    zones = objects.ZoneAuth.search(conn, fqdn=ZONE_NAME)
    zone = next(zones, None)
    if not zone:
        print(f"Zone '{ZONE_NAME}' not found.")
        sys.exit(1)

    # Remove the DNS server from the zone's list of authoritative servers
    orig_grid_primary = zone.grid_primary
    if not orig_grid_primary:
        print(f"No grid primary servers found for zone '{ZONE_NAME}'.")
        sys.exit(1)

    # Filter out the server to remove
    new_grid_primary = [
        server for server in orig_grid_primary
        if server.get('name') != DNS_SERVER_NAME
    ]

    if len(new_grid_primary) == len(orig_grid_primary):
        print(f"Server '{DNS_SERVER_NAME}' not found in zone '{ZONE_NAME}'.")
        sys.exit(1)

    # Update the zone with the new list
    zone.grid_primary = new_grid_primary
    zone.update()
    print(f"Removed '{DNS_SERVER_NAME}' from zone '{ZONE_NAME}'.")

if __name__ == '__main__':
    main()