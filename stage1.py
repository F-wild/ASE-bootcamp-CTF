import requests
import json

from env import config

# Get organisation list from meraki sandbox
headers = {
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

# Get device info for specified organization (env variable)
url = f"{config['MERAKI_BASE_URL']}/organizations/{config['MERAKI_ORG_ID']}/devices"
resp = requests.get(url, headers=headers).json()

devices = {}
devices['devices'] = []
for device in resp:
    devices['devices'].append({
        'name': device['name'],
        'mac': device['mac'],
        'serial': device['serial'],
        'type': device['model']
    })

# Write dictionary of devices to json file
with open('devicelist.json', 'w') as outfile:
    json.dump(devices, outfile, indent=4)