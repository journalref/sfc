#!/bin/bash

source general_env.sh 

function dump_flows {
    host=`hostname`
    if [ $host  == 'classifier1'  ] || [ $host == 'classifier2' ] || [ $host == 'sff1' ] || [ $host == 'sff2' ]; then
        sudo ovs-ofctl dump-flows -OOpenflow13 br-sfc
        if [ $host  == 'classifier1'  ] ; then
            sudo ip netns exec app wget http://$APP_SERVER_IP
        fi
    fi
}

function setup_sfc {
    host=`hostname`
    if [ $host  == 'controller'  ]; then
        /sfc/sfc-demo/sfc103/ctl_setup_sfc.py
    fi
    # wait for openflow effective
    sleep 60
    dump_flows
}

function update_sfc {
    # dynamic insert & remove sf
    host=`hostname`
    if [ $host  == 'controller'  ]; then
        /sfc/sfc-demo/sfc103/ctl_update_sfc.py
    fi    
    # wait for openflow effective
    sleep 60
    dump_flows
}

echo "SFC DEMO: Setup SFC"
setup_sfc

echo "SFC DEMO: Update SFC"
update_sfc
