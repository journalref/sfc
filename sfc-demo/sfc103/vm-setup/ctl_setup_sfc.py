#!/usr/bin/python
import argparse
import requests
import json
import time
import sys
import os
import ctl_get_env
from requests.auth import HTTPBasicAuth
from subprocess import call
from ctl_http_methods import put, post


def get_service_nodes_uri():
    return "/restconf/config/service-node:service-nodes"


def get_service_nodes_data():
    service_nodes_ip = ctl_get_env.get_service_nodes_ip()
    return {
        "service-nodes": {
            "service-node": [
                {
                    "name": "classifier1",
                    "service-function": [
                    ],
                    "ip-mgmt-address": service_nodes_ip['classifier1']
                },
                {
                    "name": "sff1",
                    "service-function": [
                    ],
                    "ip-mgmt-address": service_nodes_ip['sff1']
                },
                {
                    "name": "sf1",
                    "service-function": [
                        "dpi-1"
                    ],
                    "ip-mgmt-address": service_nodes_ip['sf1']
                },
                {
                    "name": "sf2",
                    "service-function": [
                        "firewall-1"
                    ],
                    "ip-mgmt-address": service_nodes_ip['sf2']
                },
                {
                    "name": "sff2",
                    "service-function": [
                    ],
                    "ip-mgmt-address": service_nodes_ip['sff2']
                },
                {
                    "name": "classifier2",
                    "service-function": [
                    ],
                    "ip-mgmt-address": service_nodes_ip['classifier2']
                }
            ]
        }
    }


def get_service_functions_uri():
    return "/restconf/config/service-function:service-functions"


def get_service_functions_data():
    service_nodes_ip = ctl_get_env.get_service_nodes_ip()
    return {
        "service-functions": {
            "service-function": [
                {
                    "name": "dpi-1",
                    "ip-mgmt-address": service_nodes_ip['sf1'],
                    "rest-uri": service_nodes_ip['sf1_uri'],
                    "type": "dpi",
                    "nsh-aware": "true",
                    "sf-data-plane-locator": [
                        {
                            "name": "dpi-1-dpl",
                            "port": 6633,
                            "ip": service_nodes_ip['sf1'],
                            "transport": "service-locator:vxlan-gpe",
                            "service-function-forwarder": "SFF1"
                        }
                    ]
                },
                {
                    "name": "firewall-1",
                    "ip-mgmt-address": service_nodes_ip['sf2'],
                    "rest-uri": service_nodes_ip['sf2_uri'],
                    "type": "firewall",
                    "nsh-aware": "true",
                    "sf-data-plane-locator": [
                        {
                            "name": "firewall-1-dpl",
                            "port": 6633,
                            "ip": service_nodes_ip['sf2'],
                            "transport": "service-locator:vxlan-gpe",
                            "service-function-forwarder": "SFF2"
                        }
                    ]
                }
            ]
        }
    }


def get_service_function_forwarders_uri():
    return "/restconf/config/service-function-forwarder:service-function-forwarders"


def get_service_function_forwarders_data():
    service_nodes_ip = ctl_get_env.get_service_nodes_ip()
    return {
        "service-function-forwarders": {
            "service-function-forwarder": [
                {
                    "name": "Classifier1",
                    "service-node": "classifier1",
                    "service-function-forwarder-ovs:ovs-bridge": {
                        "bridge-name": "br-sfc",
                    },
                    "sff-data-plane-locator": [
                        {
                            "name": "sff0-dpl",
                            "data-plane-locator": {
                                "transport": "service-locator:vxlan-gpe",
                                "port": 6633,
                                "ip": service_nodes_ip['classifier1']
                            },
                            "service-function-forwarder-ovs:ovs-options": {
                                "remote-ip": "flow",
                                "dst-port": "6633",
                                "key": "flow",
                                "exts": "gpe",
                                "nsp": "flow",
                                "nsi": "flow",
                                "nshc1": "flow",
                                "nshc2": "flow",
                                "nshc3": "flow",
                                "nshc4": "flow"
                            }
                        }
                    ],
                },
                {
                    "name": "SFF1",
                    "service-node": "sff1",
                    "service-function-forwarder-ovs:ovs-bridge": {
                        "bridge-name": "br-sfc",
                    },
                    "sff-data-plane-locator": [
                        {
                            "name": "sff1-dpl",
                            "data-plane-locator": {
                                "transport": "service-locator:vxlan-gpe",
                                "port": 6633,
                                "ip": service_nodes_ip['sff1']
                            },
                            "service-function-forwarder-ovs:ovs-options": {
                                "remote-ip": "flow",
                                "dst-port": "6633",
                                "key": "flow",
                                "exts": "gpe",
                                "nsp": "flow",
                                "nsi": "flow",
                                "nshc1": "flow",
                                "nshc2": "flow",
                                "nshc3": "flow",
                                "nshc4": "flow"
                            }
                        }
                    ],
                    "service-function-dictionary": [
                        {
                            "name": "dpi-1",
                            "sff-sf-data-plane-locator": {
                                "sf-dpl-name": "dpi-1-dpl",
                                "sff-dpl-name": "sff1-dpl"
                            }
                        }
                    ],
                },
                {
                    "name": "SFF2",
                    "service-node": "sff2",
                    "service-function-forwarder-ovs:ovs-bridge": {
                        "bridge-name": "br-sfc",
                    },
                    "sff-data-plane-locator": [
                        {
                            "name": "sff2-dpl",
                            "data-plane-locator": {
                                "transport": "service-locator:vxlan-gpe",
                                "port": 6633,
                                "ip": service_nodes_ip['sff2']
                            },
                            "service-function-forwarder-ovs:ovs-options": {
                                "remote-ip": "flow",
                                "dst-port": "6633",
                                "key": "flow",
                                "exts": "gpe",
                                "nsp": "flow",
                                "nsi": "flow",
                                "nshc1": "flow",
                                "nshc2": "flow",
                                "nshc3": "flow",
                                "nshc4": "flow"
                            }
                        }
                    ],
                    "service-function-dictionary": [
                        {
                            "name": "firewall-1",
                            "sff-sf-data-plane-locator": {
                                "sf-dpl-name": "firewall-1-dpl",
                                "sff-dpl-name": "sff2-dpl"
                            }
                        }
                    ]
                },
                {
                    "name": "Classifier2",
                    "service-node": "classifier2",
                    "service-function-forwarder-ovs:ovs-bridge": {
                        "bridge-name": "br-sfc",
                    },
                    "sff-data-plane-locator": [
                        {
                            "name": "sff3-dpl",
                            "data-plane-locator": {
                                "transport": "service-locator:vxlan-gpe",
                                "port": 6633,
                                "ip": service_nodes_ip['classifier2']
                            },
                            "service-function-forwarder-ovs:ovs-options": {
                                "remote-ip": "flow",
                                "dst-port": "6633",
                                "key": "flow",
                                "exts": "gpe",
                                "nsp": "flow",
                                "nsi": "flow",
                                "nshc1": "flow",
                                "nshc2": "flow",
                                "nshc3": "flow",
                                "nshc4": "flow"
                            }
                        }
                    ],
                }
            ]
        }
    }


def get_service_function_chains_uri():
    return "/restconf/config/service-function-chain:service-function-chains/"


def get_service_function_chains_data():
    return {
        "service-function-chains": {
            "service-function-chain": [
                {
                    "name": "SFC1",
                    "symmetric": "true",
                    "sfc-service-function": [
                        {
                            "name": "dpi-abstract1",
                            "type": "dpi"
                        },
                        {
                            "name": "firewall-abstract1",
                            "type": "firewall"
                        }
                    ]
                },
                {
                    "name": "SFC2",
                    "symmetric": "true",
                    "sfc-service-function": [
                        {
                            "name": "dpi-abstract1",
                            "type": "dpi"
                        }
                    ]
                }
            ]
        }
    }


def get_service_function_paths_uri():
    return "/restconf/config/service-function-path:service-function-paths/"


def get_service_function_paths_data():
    return {
        "service-function-paths": {
            "service-function-path": [
                {
                    "name": "SFP1",
                    "service-chain-name": "SFC1",
                    "starting-index": 255,
                    "symmetric": "true",
                    "context-metadata": "NSH1",
                    "service-path-hop": [
                        {
                            "hop-number": 0,
                            "service-function-name": "dpi-1"
                        }
                    ]
                },
                {
                    "name": "SFP2",
                    "service-chain-name": "SFC2",
                    "starting-index": 255,
                    "symmetric": "true",
                    "context-metadata": "NSH1",
                    "service-path-hop": [
                        {
                            "hop-number": 0,
                            "service-function-name": "dpi-1"
                        }
                    ]
                }
            ]
        }
    }


def get_service_function_metadata_uri():
    return "/restconf/config/service-function-path-metadata:service-function-metadata/"


def get_service_function_metadata_data():
    return {
        "service-function-metadata": {
            "context-metadata": [
                {
                    "name": "NSH1",
                    "context-header1": "1",
                    "context-header2": "2",
                    "context-header3": "3",
                    "context-header4": "4"
                }
            ]
        }
    }


def get_rendered_service_path_uri():
    return "/restconf/operations/rendered-service-path:create-rendered-path/"


def get_rendered_service_path_data():
    return {
        "input": {
            "name": "RSP1",
            "parent-service-function-path": "SFP1",
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
                    "acl-name": "ACL1",
                    "acl-type": "ietf-access-control-list:ipv4-acl",
                    "access-list-entries": {
                        "ace": [
                            {
                                "rule-name": "ACE1",
                                "actions": {
                                    "service-function-acl:rendered-service-path": "RSP1"
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
                    "acl-name": "ACL2",
                    "acl-type": "ietf-access-control-list:ipv4-acl",
                    "access-list-entries": {
                        "ace": [
                            {
                                "rule-name": "ACE2",
                                "actions": {
                                    "service-function-acl:rendered-service-path": "RSP1-Reverse"
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
                        "name": "ACL1",
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
                        "name": "ACL2",
                        "type": "ietf-access-control-list:ipv4-acl"
                    }
                }
            ]
        }
    }

if __name__ == "__main__":
    controller_info = ctl_get_env.get_controller_info()

    print "sending service nodes"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_nodes_uri(), get_service_nodes_data(), True)
    print "sending service functions"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_functions_uri(), get_service_functions_data(), True)
    print "sending service function forwarders"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_function_forwarders_uri(), get_service_function_forwarders_data(), True)
    print "sending service function chains"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_function_chains_uri(), get_service_function_chains_data(), True)
    print "sending service function metadata"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_function_metadata_uri(), get_service_function_metadata_data(), True)
    print "sending service function paths"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_function_paths_uri(), get_service_function_paths_data(), True)
    print "sending service function acl"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_function_acl_uri(), get_service_function_acl_data(), True)
    print "sending rendered service path"
    post(controller_info['controller_ip'], controller_info[
         'port'], get_rendered_service_path_uri(), get_rendered_service_path_data(), True)
    print "sending service function classifiers"
    put(controller_info['controller_ip'], controller_info[
        'port'], get_service_function_classifiers_uri(), get_service_function_classifiers_data(), True)
