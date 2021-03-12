#!/usr/bin/env python

import requests
import json
import sys
from pathlib import Path
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from pprint import pprint
from datetime import datetime
from tabulate import tabulate

here = Path(__file__).parent.absolute()
repository_root = (here / ".." ).resolve()
sys.path.insert(0, str(repository_root))

import env

inv_url = env.UMBRELLA.get("inv_url")
inv_token = env.UMBRELLA.get("inv_token")

#Use a domain of your choice
domain = "internetbadguys.com"

# Construct the API request to the Umbrella Investigate API to query for the status 
# of the domain
url = f"{inv_url}/domains/categorization/{domain}?showLabels"
headers = {"Authorization": f'Bearer {inv_token}'}
response = requests.get(url, headers=headers)

#And don't forget to check for errors that may have occured!
response.raise_for_status()

# Make sure the right data in the correct format is chosen, you can use print 
# statements to debug your code
domain_status = response.json()[domain]["status"]

if domain_status == 1:
    print(f"The domain {domain} is found CLEAN")
elif domain_status == -1:
    print(f"The domain {domain} is found MALICIOUS")
elif domain_status == 0:
    print(f"The domain {domain} is found UNDEFINED")

# Add another call here, where you check the historical data for either the domain 
# from the intro or your own domain and print it out in a readable format

url = f"{inv_url}/pdns/domain/{domain}"
response = requests.get(url, headers=headers)
response.raise_for_status()

#pprint(response.json())
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
print(tabulate(resp, headers = theaders))

# url = f"{inv_url}/timeline/{domain}"
# response = requests.get(url, headers=headers)
# response.raise_for_status()

# resp = response.json()
# for item in resp:
#     ts = item['timestamp']/1000
#     item['timestamp'] = datetime.utcfromtimestamp(ts).strftime("%d-%m-%Y %H:%m:%S")

# theaders = {'timestamp': "Time", 'attacks': "Attacks", 'threatTypes': "Threat Types", 'categories': "Categories"}
# print(tabulate(resp, headers = theaders, tablefmt='github'))