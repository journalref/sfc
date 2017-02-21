#!/usr/bin/python
import requests
import json
from requests.auth import HTTPBasicAuth
import time
import sys
import os
from ctl_get_env import get_credential


def put(host, port, uri, data, debug=False):
    credential_info = get_credential()

    '''Perform a PUT rest operation, using the URL and data provided'''

    url = 'http://' + host + ":" + port + uri

    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "PUT %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.put(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(
        credential_info['user'], credential_info['passwd']))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)


def post(host, port, uri, data, debug=False):
    credential_info = get_credential()

    '''Perform a POST rest operation, using the URL and data provided'''

    url = 'http://' + host + ":" + port + uri
    headers = {'Content-type': 'application/yang.data+json',
               'Accept': 'application/yang.data+json'}
    if debug == True:
        print "POST %s" % url
        print json.dumps(data, indent=4, sort_keys=True)
    r = requests.post(url, data=json.dumps(data), headers=headers, auth=HTTPBasicAuth(
        credential_info['user'], credential_info['passwd']))
    if debug == True:
        print r.text
    r.raise_for_status()
    time.sleep(5)


def delete(host, port, uri):
    credential_info = get_credential()
    url = 'http://' + host + ":" + port + uri
    r = requests.delete(url, auth=HTTPBasicAuth(
        credential_info['user'], credential_info['passwd']))
    # r.raise_for_status()
