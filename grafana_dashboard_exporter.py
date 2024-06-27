#!/usr/bin/env python
"""Grafana dashboard exporter"""

import json
import os
import requests


# get api url and key from .env file
from dotenv import load_dotenv
load_dotenv()

# Grafana API URL
HOST = os.environ.get('GRAFANA_API_URL')

# Service account credentials (API Key or Token)
API_KEY = os.environ.get('GRAFANA_API_KEY')

DIR = './grafana-dash-backup/'


def create_root_directories():
    """
    This function creates the root directories for json and hcl.
    """
    print("Creating root directories")

    if not os.path.exists(DIR):
        os.makedirs(DIR)


def create_folder_structure():
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get('%s/api/folders' % (HOST,), headers=headers)
    response.raise_for_status()

    folders = response.json()

    if not os.path.exists(DIR):
        os.makedirs(DIR)

    folder_list = []

    # for each folder in the folders list create a directory
    for folder in folders:
        folder_name = folder['title']
        folder_uuid = folder['uid']
        folder_path = os.path.join(DIR, folder_name)
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)

        print(folder_name, folder_uuid)

        # make a key value pair of folder name and folder uuid
        folder_list.append({"title": folder_name, "uid" : folder_uuid})

    return folder_list
    

def export_dashboards(folder_map):
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get('%s/api/search?query=&' % (HOST,), headers=headers)
    response.raise_for_status()
    dashboards = response.json()

    for dash in dashboards:
        print("Saving: " + dash['title'])
        response = requests.get('%s/api/dashboards/uid/%s' % (HOST, dash['uid']), headers=headers)
        data = response.json()['dashboard']
        print(data)

        folder_ref_id = response.json()['meta']['folderUid'] if 'folderUid' in response.json()['meta'] else None
        print(f"Folder ref id: {folder_ref_id}")
        dash = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))
        name = data['title'].replace(' ', '').replace('/', '').replace(':', '').replace('[', '').replace(']', '')

        folder_path = DIR  # default to DIR
        
        for folder in folder_map:
            print(folder['uid'], folder_ref_id)
            if folder_ref_id == folder['uid']:
                folder_path = os.path.join(DIR, folder['title'])  # set folder_path to the path of the matching folder
                break

        with open(os.path.join(folder_path, name + '.json'), 'w') as f:
            f.write(dash)
            f.write('\n')


# not used
def call_api(query):
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get(query % (HOST,), headers=headers)
    response.raise_for_status()
    return response.json()    


def main():

    create_root_directories()
    folder_map = create_folder_structure() # list of folder dictionaries
    export_dashboards(folder_map)


if __name__ == '__main__':
    main()
