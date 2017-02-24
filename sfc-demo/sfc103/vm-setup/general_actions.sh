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
        ./ctl_setup_sfc.py
    fi
    # wait for openflow effective
    sleep 60
}

function update_sfc {
    # dynamic insert & remove sf
    host=`hostname`
    if [ $host  == 'controller'  ]; then
        ./ctl_update_sfc.py
    fi    
    # wait for openflow effective
    sleep 60
}

printf "Choose one of the following actions:\n1 - Install sfc(for controller node)\n2 - Update sfc(for controller node)\n3 - Dump flows on bridge(for service nodes)\nYour action: "

read option 

if [ $option == 1 ]; then
    echo "Setup SFC" 
    setup_sfc
elif [ $option == 2 ]; then
    echo "Update SFC"
    update_sfc
elif [ $option == 3 ]; then
    echo "Dump flows"
    dump_flows
else 
    exit 1
fi
