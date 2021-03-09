import requests
import json
from env import config

resp = requests.get("https://webexapis.com/v1/rooms", headers = {'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"})

with open('rooms.json', 'w') as outfile:
    outfile.write(json.dumps(resp.json(), indent=4))

for room in resp.json()['items']:
    if room['title'] == "CSAP Programmability CTF - Team 2":
        room_id = room['id']

print(room_id)