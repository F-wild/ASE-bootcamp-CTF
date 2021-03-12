import requests
import json
from pprint import pprint

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                      api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

url = f"{BASE_URL}/ntp/Policies"

response = requests.get(url, auth=auth)

if response.status_code == 200:
    pprint(response.json())
else:
    print(f"{response.status_code}")