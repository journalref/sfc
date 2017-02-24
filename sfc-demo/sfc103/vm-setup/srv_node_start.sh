#!/bin/bash

set -eux
source general_env.sh

function ovs_start {
    service openvswitch-switch start
    ovs-vsctl set-manager tcp:$CONTROLLER_IP:6640
    ovs-vsctl add-br br-sfc
}

function ovs_add_app_veth-br {
    ip netns add app
    ip link add veth-app type veth peer name veth-br
    ovs-vsctl add-port br-sfc veth-br
    ip link set dev veth-br up
    ip link set veth-app netns app
}

host=`hostname`
if [ $host  == 'classifier1'  ] ; then
    ovs_start
    ovs_add_app_veth-br
    ip netns exec app ifconfig veth-app $APP_CLIENT_CIDR up
    ip netns exec app ip link set dev veth-app  addr $APP_CLIENT_MAC
    ip netns exec app arp -s $APP_SERVER_IP $APP_SERVER_MAC -i veth-app
    ip netns exec app ip link set dev veth-app up
    ip netns exec app ip link set dev lo up
    ip netns exec app ifconfig veth-app mtu 1400
    ovs-vsctl show
elif [ $host  == 'classifier2'  ] ; then
    ovs_start
    ovs_add_app_veth-br
    ip netns exec app ifconfig veth-app $APP_SERVER_CIDR up
    ip netns exec app ip link set dev veth-app  addr $APP_SERVER_MAC
    ip netns exec app arp -s $APP_CLIENT_IP $APP_CLIENT_MAC -i veth-app
    ip netns exec app ip link set dev veth-app up
    ip netns exec app ip link set dev lo up
    ip netns exec app ifconfig veth-app mtu 1400
    nohup ip netns exec app python -m SimpleHTTPServer 80 > /tmp/http_server.log 2>&1  &
    ovs-vsctl show
elif [ $host == 'sff1' ] || [ $host == 'sff2' ]; then
    ovs_start
    ovs-vsctl show
elif [ $host == 'sf1' ] || [ $host == 'sf2' ]; then
    cd ../../../sfc-py;
    pip3 install -r requirements.txt
    nohup python3.4 sfc/sfc_agent.py --rest --odl-ip-port $CONTROLLER_IP:8181 &
fi
/bin/bash
