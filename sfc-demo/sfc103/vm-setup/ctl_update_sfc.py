#!/usr/bin/python
import argparse
import requests
import json
from requests.auth import HTTPBasicAuth
from subprocess import call
import time
import sys
import os
import ctl_get_env
from ctl_http_methods import put, post


def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:create-rendered-path/"


def get_rendered_service_path_data():
    return {
        "input": {
            "name": "RSP2",
            "parent-service-function-path": "SFP2",
            "symmetric": "true"
        }
    }


def get_service_function_acl_uri():
    return "/restconf/config/ietf-access-control-list:access-lists/"


def get_service_function_acl_data():
    endpoint_net = ctl_get_env.get_endpoint_net()
    return {
        "access-lists": {
            "acl": [
                {
                    "acl-name": "ACL3",
                    "acl-type": "ietf-access-control-list:ipv4-acl",
                    "access-list-entries": {
                        "ace": [
                            {
                                "rule-name": "ACE1",
                                "actions": {
                                    "service-function-acl:rendered-service-path": "RSP2"
                                },
                                "matches": {
                                    "destination-ipv4-network": endpoint_net,
                                    "source-ipv4-network": endpoint_net,
                                    "protocol": "6",
                                    "source-port-range": {
                                        "lower-port": 0
                                    },
                                    "destination-port-range": {
                                        "lower-port": 80
                                    }
                                }
                            }
                        ]
                    }
                },
                {
                    "acl-name": "ACL4",
                    "acl-type": "ietf-access-control-list:ipv4-acl",
                    "access-list-entries": {
                        "ace": [
                            {
                                "rule-name": "ACE2",
                                "actions": {
                                    "service-function-acl:rendered-service-path": "RSP2-Reverse"
                                },
                                "matches": {
                                    "destination-ipv4-network": endpoint_net,
                                    "source-ipv4-network": endpoint_net,
                                    "protocol": "6",
                                    "source-port-range": {
                                        "lower-port": 80
                                    },
                                    "destination-port-range": {
                                        "lower-port": 0
                                    }
                                }
                            }
                        ]
                    }
                }
            ]
        }
    }


def get_service_function_classifiers_uri():
    return "/restconf/config/service-function-classifier:service-function-classifiers/"


def get_service_function_classifiers_data():
    return {
        "service-function-classifiers": {
            "service-function-classifier": [
                {
                    "name": "Classifier1",
                    "scl-service-function-forwarder": [
                        {
                            "name": "Classifier1",
                            "interface": "veth-br"
                        }
                    ],
                    "acl": {
                        "name": "ACL3",
                        "type": "ietf-access-control-list:ipv4-acl"
                    }
                },
                {
                    "name": "Classifier2",
                    "scl-service-function-forwarder": [
                        {
                            "name": "Classifier2",
                            "interface": "veth-br"
                        }
                    ],
                    "acl": {
                        "name": "ACL4",
                        "type": "ietf-access-control-list:ipv4-acl"
                    }
                }
            ]
        }
    }

if __name__ == "__main__":
    controller_info = ctl_get_env.get_controller_info()

    print "sending rendered service path"
    post(controller_info['controller_ip'], controller_info['port'], get_rendered_service_path_uri(),
         get_rendered_service_path_data(), True)
    print "updating service function acl"
    put(controller_info['controller_ip'], controller_info['port'], get_service_function_acl_uri(),
        get_service_function_acl_data(), True)
    print "updating service function classifiers"
    put(controller_info['controller_ip'], controller_info['port'], get_service_function_classifiers_uri(),
        get_service_function_classifiers_data(), True)
