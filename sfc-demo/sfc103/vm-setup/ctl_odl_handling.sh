#!/bin/bash

source general_env.sh 

function stop_odl {
    printf "Stopping karaf ...  "
    spin=('/' '-' '\' '|' '-')
    i=0
    while $HOME/sfc/sfc-karaf/target/assembly/bin/client -u karaf 'system:shutdown -f' &> /dev/null
    do
        printf "\b${spin[$i]}"
        i=$(( (( $i + 1 )) % 5 ))
        # karaf is still running, wait for effective shutdown
        sleep 5
    done
    printf "\bdone\n"
}

function start_sfc {
    cd $HOME/sfc/sfc-karaf/target/assembly/
    sed -i "/^featuresBoot[ ]*=/ s/$/,odl-sfc-provider,odl-sfc-core,odl-sfc-ui,odl-sfc-openflow-renderer,odl-sfc-scf-openflow,odl-sfc-sb-rest,odl-sfc-ovs,odl-sfc-netconf/" etc/org.apache.karaf.features.cfg;
    echo "log4j.logger.org.opendaylight.sfc = DEBUG,stdout" >> etc/org.ops4j.pax.logging.cfg;
    rm -rf journal snapshots; bin/start
    #wait for sfc ready
    retries=3
    while [ $retries -gt 0 ]
    do
        sleep 60
        sfcfeatures=$($HOME/sfc/sfc-karaf/target/assembly/bin/client -u karaf 'feature:list -i' 2>&1 | grep odl-sfc | wc -l)
        if [ $sfcfeatures -eq 9 ]; then
            break
        fi
        retries=$(( $retries - 1 ))
    done
    if [ $retries -eq 0 ]; then
        echo "Karaf not started. Exit immediately"
        exit 1
    fi
}




echo "SFC DEMO: Stop ODL"
stop_odl

echo "SFC DEMO: Start SFC"
start_sfc

echo "SFC DEMO: Give some time to have all things ready..."
sleep 120
echo "done"
