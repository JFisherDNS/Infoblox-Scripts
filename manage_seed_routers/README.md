for the manage seed routers script, the GUID for the discovery appliance will need to be referenced.
The GUID is enumerated at the discovery:memberproperties wapi endpoint.

The easiest way to discover this is with a CURL command
curl -k -u <username>:<password> "https://<gridmaster_fqdn>/wapi/v2.13.6/discovery:memberproperties"
[
    {
        "_ref": "discovery:memberproperties/ZGlzY292ZXJ5Lm1lbvszvrfassa9kaXNjb3ZlcnlfcHJvcGVydGllcyQz:discoverymember-01.lab",
        "discovery_member": "discoverymember-01.lab"
    }
]

