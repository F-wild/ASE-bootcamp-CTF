import requests

from env import config

# Get organisation list from merkai sandbox
headers = {
    "X-Cisco-Meraki-API-Key": config['MERAKI_KEY']
}

orgs_url = f"{config['MERAKI_BASE_URL']}/organizations"
resp = requests.get(orgs_url, headers=headers).json()

# print org id and name for each item in response
for org in resp:
    print('orgID: ' + org['id'] + ', orgName: ' + org['name'])