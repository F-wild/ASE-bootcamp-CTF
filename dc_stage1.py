import requests
import json
from pprint import pprint
from tabulate import tabulate

from utils.auth import IntersightAuth, get_authenticated_aci_session
from env import config

auth=IntersightAuth(secret_key_filename=config['INTERSIGHT_CERT'],
                    api_key_id=config['INTERSIGHT_API_KEY'])

BASE_URL='https://www.intersight.com/api/v1'

def getAlarms(f):
    url = f"{BASE_URL}/cond/Alarms"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        for alarm in response.json()['Results']:
            f.write(f"{alarm['Description']}\n")
    else:
        print(f"Alarm request status code{response.status_code}")

def getInfra(f):
    url = f"{BASE_URL}/compute/PhysicalSummaries"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        # define variables for making a table of data collected
        tableData = []
        theaders = {'ManagementMode': 'Management Mode',
            'MgmtIpAddress': 'Management IP',
            'Name': 'Name',
            'NumCpus': 'CPUs',
            'NumCpuCores': 'Cores',
            'OperPowerState': 'PowerState',
            'Firmware': 'Firmware',
            'Model': 'Model',
            'Serial': 'Serial',
            'L': 'License Tier'}
        for item in response.json()['Results']:
            # append desired data as dict to tableData[]
            tableData.append({'ManagementMode': f"{item['ManagementMode']}",
                                'MgmtIpAddress': f"{item['MgmtIpAddress']}",
                                'Name': f"{item['Name']}",
                                'NumCpus': f"{item['NumCpus']}",
                                'NumCpuCores': f"{item['NumCpuCores']}",
                                'OperPowerState': f"{item['OperPowerState']}",
                                'Firmware': f"{item['Firmware']}",
                                'Model': f"{item['Model']}",
                                'Serial': f"{item['Serial']}"})
        # Write data as table to file
        f.write(tabulate(tableData, headers = theaders))
    else:
        print(f"Infra request status code{response.status_code}")

def getHCL(f):
    url = f"{BASE_URL}/cond/HclStatuses"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        # define variables for making a table of data collected
        tableData = []
        theaders = {'Moid': 'Managed Object ID',
            'HclOsVendor': 'HCL OS Vendor',
            'HclOsVersion': 'HCL OS Version'}
        for item in response.json()['Results']:
            tableData.append({'Moid': f"{item['Moid']}",
                                'HclOsVendor': f"{item['HclOsVendor']}",
                                'HclOsVersion': f"{item['HclOsVersion']}"})
        f.write(tabulate(tableData, headers = theaders))
    else:
        print(f"HCL request status code{response.status_code}")

def getKubernetes(f):
    url = f"{BASE_URL}/kubernetes/Clusters"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        for item in response.json()['Results']:
            f.write(f"\n{item['Name']}")
    else:
        print(f"* request status code{response.status_code}")

def getDeployments():
    url = f"{BASE_URL}/kubernetes/Deployments"

    response = requests.get(url, auth=auth)

    if response.status_code == 200:
        return int(len(response.json()['Results']))
    else:
        print(f"* request status code{response.status_code}")

def main():
    with open('output.txt', 'w') as f:
        f.write("Alarms:")
        getAlarms(f)
        f.write("\n\nInfrastructure")
        getInfra(f)
        f.write("\n\nHardware Compliance")
        getHCL(f)
        f.write("\n\nKubernetes Clusters:")
        getKubernetes(f)
        f.write(f"\n\nKubernetes Deployments: {getDeployments()}")

if __name__ == '__main__':
    main()