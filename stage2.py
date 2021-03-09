import requests
import json
from requests.auth import HTTPBasicAuth

from env import config

# Get organisation list from meraki sandbox
headers = {
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

# Get device info for specified organization (env variable)
murl = f"{config['MERAKI_BASE_URL']}/organizations/{config['MERAKI_ORG_ID']}/devices"
mresp = requests.get(murl, headers=headers)

devices = {}
devices['devices'] = []

if mresp.status_code == 200:
    for device in mresp.json():
        devices['devices'].append({
            'name': device['name'],
            'mac': device['mac'],
            'serial': device['serial'],
            'type': device['model'],
            'category': 'Meraki'
        })
else:
    print(f"Meraki error, status code: {mresp.status_code}")


# Get DNAC access token
dnac_auth_url = f"{config['DNAC_BASE_URL']}/dna/system/api/v1/auth/token"
token = requests.post(dnac_auth_url, auth=HTTPBasicAuth(config['DNAC_USER'], config['DNAC_PASSWORD'])).json()['Token']

dna_device_url = f"{config['DNAC_BASE_URL']}/dna/intent/api/v1/network-device"
dna_header = {'X-Auth-Token': f"{token}"}
dna_resp = requests.get(dna_device_url, headers=dna_header)

if dna_resp.status_code == 200:
    for device in dna_resp.json()['response']:
        devices['devices'].append({
            'name': device['hostname'],
            'mac': device['macAddress'],
            'serial': device['serialNumber'],
            'type': device['type'],
            'category': 'DNA'
        })
else:
    print(f"DNA error, status code: {dna_resp.status_code}")

# Write dictionary of devices to json file
with open('devicelist.json', 'w') as outfile:
    json.dump(devices, outfile, indent=4)