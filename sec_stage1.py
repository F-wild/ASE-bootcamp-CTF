#!/usr/bin/env python

import requests
import json
import sys
import re
import json
from time import time
from pathlib import Path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from datetime import datetime
from tabulate import tabulate

here = Path(__file__).parent.absolute()
repository_root = (here / ".." ).resolve()
sys.path.insert(0, str(repository_root))

import env

inv_url = env.UMBRELLA.get("inv_url")
inv_token = env.UMBRELLA.get("inv_token")
en_url = env.UMBRELLA.get("en_url")
en_key = env.UMBRELLA.get("en_key")

domains = ["internetbadguys.com", "icanhazdadjoke.com"]

for domain in domains:
    url = f"{inv_url}/domains/categorization/{domain}?showLabels"
    headers = {"Authorization": f'Bearer {inv_token}'}
    response = requests.get(url, headers=headers)

    # check for errors
    response.raise_for_status()
    domain_status = response.json()[domain]["status"]

    # Sanitize URL
    s_url = re.sub("\.", "(dot)", domain)

    if domain_status == 1:
        print(f"The domain {s_url} is found CLEAN")
    elif domain_status == -1:
        print(f"The domain {s_url} is found MALICIOUS")
        current_time = datetime.utcfromtimestamp(time()).strftime("%Y-%m-%dT%H:%m:%SZ")
        payload = {"alertTime": f"{current_time}",
                    "deviceId": "ba6a59f4-e692-4724-ba36-c28132c761de",
                    "deviceVersion": "13.7a",
                    "dstDomain": f"{domain}",
                    "dstUrl": f"{domain}",
                    "eventTime": f"{current_time}",
                    "protocolVersion": "1.0a",
                    "providerName": "Security Platform"}
        payload = json.dumps(payload)
        block = requests.post(f"{en_url}events?customerKey={en_key}", headers={'Content-Type': 'application/json'}, data=payload)
        block.raise_for_status()
        if block.status_code == 202:
            print(f"Domain {s_url} successfully posted to Umbrella Events.")
    elif domain_status == 0:
        print(f"The domain {s_url} is found UNDEFINED")

    url = f"{inv_url}/pdns/domain/{domain}"
    response = requests.get(url, headers=headers)
    response.raise_for_status()

    resp = response.json()['records']
    for record in resp:
        record.pop('firstSeen')
        record.pop('lastSeen')
        record['contentCategories'] = '\n'.join(record['contentCategories'])
        record['securityCategories'] = '\n'.join(record['securityCategories'])    
    theaders = {'contentCategories': 'Content\nCategories', 
                'firstSeen': 'First Seen\n(epoch)', 
                'firstSeenISO': 'First Seen', 
                'lastSeen': 'Last Seen\n(epoch)',
                'lastSeenISO': 'Last Seen',
                'maxTtl': 'Max. TTL',
                'minTtl': 'Min. TTL',
                'name': 'Domain',
                'rr': 'Resource Record',
                'securityCategories': 'Security\nCategories',
                'type': 'Type'
                }
    print("Historical data:\n")
    print(tabulate(resp, headers = theaders))

    # url = f"{inv_url}/timeline/{domain}"
    # response = requests.get(url, headers=headers)
    # response.raise_for_status()

    # resp = response.json()
    # for item in resp:
    #     ts = item['timestamp']/1000
    #     item['timestamp'] = datetime.utcfromtimestamp(ts).strftime("%d-%m-%Y %H:%m:%S")

    # theaders = {'timestamp': "Time", 'attacks': "Attacks", 'threatTypes': "Threat Types", 'categories': "Categories"}
    # print("Historical data:\n")
    # print(tabulate(resp, headers = theaders, tablefmt='github'))