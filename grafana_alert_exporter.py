#!/usr/bin/env python

"""Grafana dashboard exporter"""
import json
import os
import requests
import hcl


# get api url and key from .env file
from dotenv import load_dotenv
load_dotenv()

# Grafana ENV VARS
HOST = os.environ.get('GRAFANA_API_URL')
API_KEY = os.environ.get('GRAFANA_API_KEY')

DIR = './grafana-alert-backup-json/'
DIR_HCL = './grafana-alert-backup-hcl/'



def create_root_directories():
    """
    This function creates the root directories for json and hcl.
    """

    print("Creating root directories")

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    if not os.path.exists(DIR_HCL):
        os.makedirs(DIR_HCL)


def get_alerts_json():
    """
    This function gets the alerts in json format.
    """

    print("Getting alerts in json format")

    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    parameters = {
        'format': 'json',
    }
    try:
        print("Calling api for json")
        response = requests.get('%s/api/v1/provisioning/alert-rules/export' % (HOST,), headers=headers, params=parameters)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None
    
    # write response json to a file
    with open(os.path.join(DIR, 'alert_rules.json'), 'w') as f:
        f.write(json.dumps(response.json(), sort_keys=True, indent=4, separators=(',', ': ')))
        f.write('\n')

    return response.json()


def get_alerts_hcl():
    """
    This function gets the alerts in hcl format.
    """

    print("Getting alerts in hcl format")

    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    parameters = {
        'format': 'hcl',
    }
    try:
        print("Calling api for hcl")
        response = requests.get('%s/api/v1/provisioning/alert-rules/export' % (HOST,), headers=headers, params=parameters)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None
    
    # write response text to a file
    with open(os.path.join(DIR_HCL, 'alert_rules.hcl'), 'w') as f:
        f.write(response.text)
        f.write('\n')

    return response.text


def create_folders(blob):
    """
    This function creates a directory for each folder.
    """

    print("Creating folders for json")

    folders = []
    for alert in blob['groups']:
        folder = alert['folder']
        if folder not in folders:
            folders.append(folder)
            # create a directory for each folder
            folder_path = os.path.join(DIR, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)

    return folders


def create_folders_hcl(blob):
    """
    This function creates a directory for each folder from hcl text file.
    """
    print("Creating folders for hcl")
    folders = []

    # Load the hcl data
    data = hcl.loads(blob)

    # Extract the resources
    resources = data['resource']['grafana_rule_group']

    # Iterate over each resource
    for resource_name, resource in resources.items():
        # Get the folder_uid
        folder = resource['folder_uid']

        # If the folder is not already in the list, add it
        if folder not in folders:
            folders.append(folder)

            # Create a directory for each folder
            folder_path = os.path.join(DIR_HCL, folder)
            if not os.path.exists(folder_path):
                os.makedirs(folder_path)


def add_alerts_to_folders(blob):
    """
    This function adds the alerts to the respective folders.
    """
    print("Adding alerts to folders for json")
    for alert in blob['groups']:
        folder = alert['folder']
        alert_name = alert['name']
        alert_path = os.path.join(DIR, folder, alert_name + '.json')

        saved_alert = {
            "apiVersion": 1,
            "groups": [alert]
        }

        with open(alert_path, 'w') as f:
            f.write(json.dumps(saved_alert, sort_keys=True, indent=4, separators=(',', ': ')))
            f.write('\n')


def add_alerts_to_folders_hcl(blob):
    """
    This function adds the alerts to the respective folders from hcl text file.
    """
    print("Adding alerts to folders for hcl")
    # Load the hcl data
    data = hcl.loads(blob)

    # Extract the resources
    resources = data['resource']['grafana_rule_group']

    # Iterate over each resource
    for resource_name, resource in resources.items():
        # Get the folder_uid
        folder = resource['folder_uid']
        alert_name = resource['name']
        alert_path = os.path.join(DIR_HCL, folder, alert_name + '.hcl')

        with open(alert_path, 'w') as f:
            f.write(json.dumps(resource, sort_keys=True, indent=4, separators=(',', ': ')))
            f.write('\n')
 

def main():
    """
    This function gets the alerts json and hcl, creates a directory for each folder, and adds the alerts to the respective folders.
    """
    # Create root directories if they don't exist
    create_root_directories()

    # Get alerts json
    alerts_blob = get_alerts_json()
    # Get alerts directory
    create_folders(alerts_blob)
    # Add alerts to folders
    add_alerts_to_folders(alerts_blob)

    # Get alerts hcl
    alerts_blob_hcl = get_alerts_hcl()
    # Get alerts directory
    create_folders_hcl(alerts_blob_hcl)

    # Add alerts to folders
    add_alerts_to_folders_hcl(alerts_blob_hcl)


if __name__ == '__main__':
    main()