import re
import requests
from env import config
import json

# create new room space and return ID
room_id="''"
headers = {'Authorization': f"Bearer {config['WEBEX_ACCESS_TOKEN']}"}
payload = {"title": "fwilders-CTF-test"}
resp1 = requests.post(f"{config['WEBEX_BASE_URL']}/v1/rooms", data=payload, headers = headers)
room_id = resp1.json()['id']
print(resp1.status_code)
# add id to env.py

f=open('env.py', 'r')
lines = f.readlines()
f.close()
for index, line in enumerate(lines):
    if re.search("config\['TE*", line):
        lines[index] = "config['TESTING_ROOM'] = '{}'".format(room_id)

f=open('env.py', 'w')
new_contents = "".join(lines)
f.write(new_contents)
f.close()

# Add members to room
emails = ['frewagne@cisco.com', 'mneiding@cisco.com']
for person in emails:
    body = {'roomId': f'{room_id}', 'personEmail': f'{person}'}
    resp2 = requests.post(f"{config['WEBEX_BASE_URL']}/v1/memberships", data = body, headers = headers)
    print(resp2.status_code)

# Post welcome message
message_payload = {'roomId': f'{room_id}', 'text': 'Welcome! (test message with api call)'}
resp3 = requests.post(f"{config['WEBEX_BASE_URL']}/v1/messages", data=message_payload, headers=headers)
print(resp3.status_code)