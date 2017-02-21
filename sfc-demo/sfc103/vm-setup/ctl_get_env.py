#!/usr/bin/python

import sys
from os import environ


def get_credential():
    user = ''
    passwd = ''
    try:
        user = environ["USERNAME"]
        passwd = environ["PASSWORD"]
    except KeyError:
        print "Please set the environment variables first!"
        sys.exit(1)
    return {'user': user, 'passwd': passwd}


def get_controller_info():
    controller_ip = ''
    default_port = ''
    try:
        controller_ip = environ["CONTROLLER_IP"]
        default_port = environ["DEFAULT_PORT"]
    except KeyError:
        print "Please set the environment variables first!"
        sys.exit(1)
    return {'controller_ip': controller_ip, 'port': default_port}


def get_service_nodes_ip():
    (classifier1_ip, classifier2_ip, sff1_ip, sff2_ip, sf1_ip,
     sf2_ip, sf1_uri, sf2_uri) = ('', '', '', '', '', '', '', '')
    try:
        (classifier1_ip, classifier2_ip, sff1_ip, sff2_ip, sf1_ip, sf2_ip, sf1_uri, sf2_uri) = (environ["CLASSIFIER1_IP"], environ[
            "CLASSIFIER2_IP"], environ["SFF1_IP"], environ["SFF2_IP"], environ["SF1_IP"], environ["SF2_IP"], environ["SF1_URI"], environ["SF2_URI"])
    except KeyError:
        print "Please set the environment variables first!"
        sys.exit(1)
    return {'classifier1': classifier1_ip, 'classifier2': classifier2_ip, 'sff1': sff1_ip, 'sff2': sff2_ip, 'sf1': sf1_ip, 'sf2': sf2_ip, 'sf1_uri': sf1_uri, 'sf2_uri': sf2_uri}


def get_endpoint_net():
    endpoint_net = ''
    try:
        endpoint_net = environ["ENDPOINT_NET"]
    except KeyError:
        print "Please set the environment variables first!"
        sys.exit(1)
    return endpoint_net
