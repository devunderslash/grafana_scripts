#!/usr/bin/env python

"""Grafana notifications template exporter"""
import os
import requests



# get api url and key from .env file
from dotenv import load_dotenv
load_dotenv()

# Grafana ENV VARS
HOST = os.environ.get('GRAFANA_API_URL')
API_KEY = os.environ.get('GRAFANA_API_KEY')

DIR_HCL = './grafana-alert-backup-hcl/'


def create_root_directories():
    """
    This function creates the root directories for hcl.
    """

    print("Creating root directories")

    if not os.path.exists(DIR_HCL):
        os.makedirs(DIR_HCL)


def get_alerts_hcl():
    """
    This function gets the alert notification templates.
    """

    print("Getting alert notifications")

    headers = {'Authorization': 'Bearer %s' % (API_KEY,)}
    parameters = {
        'format': 'hcl',
    }
    try:
        print("Calling api for alert notifications hcl")
        response = requests.get('%s/api/v1/provisioning/templates' % (HOST,), headers=headers, params=parameters)
        response.raise_for_status()
    except requests.exceptions.HTTPError as err:
        print(err)
        return None
    
    # write response text to a file
    with open(os.path.join(DIR_HCL, 'notification_templates.hcl'), 'w') as f:
        f.write(response.text)
        f.write('\n')

    return response.text


if __name__ == '__main__':
    create_root_directories()
    get_alerts_hcl()