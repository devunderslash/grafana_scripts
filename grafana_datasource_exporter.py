# Original Bash command to export datasources:
# 
# for i in datasources/*; do \
#     curl -X "POST" "http://{grafana-hostname}:{grafana-port}/api/datasources" \
#     -H "Content-Type: application/json" \
#      --user {grafana-user}:{grafana-password} \
#      --data-binary @$i
# done

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

DIR = './grafana-datasource-backup/'


def create_root_directories():
    """
    This function creates the root directories for 
    json files to be stored.
    """
    print("Creating root directories")
    if not os.path.exists(DIR):
        os.makedirs(DIR)


def get_datasources():
    """
    This function gets the datasources in json format.
    """

    print(f"Getting datasources from {HOST}")
    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    response = requests.get('%s/api/datasources' % (HOST,), headers=headers)
    response.raise_for_status()

    data = response.json()
    names = [datasource['name'] for datasource in data]

    datasources = json.dumps(data, sort_keys=True, indent=4, separators=(',', ': '))

    # save whole datatsource json to a file
    with open(os.path.join(DIR, 'datasources.json'), 'w') as f:
        f.write(datasources)
        f.write('\n')

    # for each datasource in the datasources list create a file and save the individual datasource
    for name in names:
        print("Saving: " + name)
        with open(os.path.join(DIR, name + '.json'), 'w') as f:
            f.write(json.dumps(data[names.index(name)], sort_keys=True, indent=4, separators=(',', ': ')))
            f.write('\n')


if __name__ == "__main__":

    create_root_directories()
    get_datasources()

