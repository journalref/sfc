SFC103 Demo
===========

Overview
--------

SFC103 demo is to show standalone SFC classifier including dynamic insert
& remove service function.

Ubuntu 14.04.3 server! 
Note
----

It takes long time to complete the demo including vagrant box download,
SFC download/build and ovs with NSH installation. The duration depends
On your network. Normally, it takes several hours.

Global Topology
---------------
```sh
                           +-----------------+
                           |       SFC       |
                           |   10.20.0.5     |
                           +-----------------+
                       /      |          |     \
                    /         |          |         \
                /             |          |             \
+---------------+  +--------------+   +--------------+  +---------------+
|  Classifier1  |  |    SFF1      |   |     SFF2     |  |  Classifier2  |
|  10.20.0.10   |  | 10.20.0.20   |   | 10.20.0.50   |  |  10.20.0.60   |
+---------------+  +--------------+   +--------------+  +---------------+
                              |          |
                              |          |
                   +---------------+  +--------------+
                   |     DPI-1     |  |     FW-1     |
                   | 10.20.0.30    |  | 10.20.0.40   |
                   +---------------+  +--------------+
```

Classifiers Topology
--------------------
```sh
            +---------------------------------+
            |            ARP Cache            |
            + - - - - - - - - - - - - - - - - +
            | 192.168.1.2 | 00:00:22:22:22:22 |
            +---------------+-----------------+
                            |
+---------------+           |
|               |-----------+------------+                  +-------+
|               | veth-app               +        +---------|       |
| Classifier1   | IP: 192.168.1.1/24     +        +         |       |
| 10.20.0.10    | MAC: 00:00:11:11:11:11 ++------++ veth-br |  app  |
|               | MTU: 1400              +        |         |       |
|               |------------------------+        +---------|       |
+---------------+           ▲                               +-------+
                            |
                            |
                            |
+---------------+           ▼
|               |------------------------+                  +-------+
|               | veth-app               +        +---------|       |
| Classifier2   | IP: 192.168.1.2/24     +        +         |       |
| 10.20.0.60    | MAC: 00:00:22:22:22:22 ++------++ veth-br |  app  |
|               | MTU: 1400              +        |         |       |
|               |------------------------+        +---------|       |
+---------------+           |                               +-------+
                            |
            +---------------+-----------------+
            |            ARP Cache            |
            + - - - - - - - - - - - - - - - - +
            | 192.168.1.1 | 00:00:11:11:11:11 |
            +---------------------------------+
```
Setup Demo
----------
- This setup requires 7 host: 6 hosts for service nodes (2 SFFs, 2 SFs, 2 Classifiers) and 1 host for OpenDaylight SFC Controller
- Set appropriate hostname for each host: sff1, sff2, sf1, sf2, classifier1, classifier2, controller
- Install git client: `sudo apt-get update; sudo apt-get install git -y`
- Clone sfc repo: 

  ```sh
  cd ~/
  git clone https://github.com/thaihust/sfc.git sfc-labs
  ```
  
- Change directory to sfc103 and begin starting setup necessary packages (ODL SFC for controller node and Open vSwitch enabled NSH version 2.6.1 from yyang's repo): 

  ```sh
  cd ~/sfc-labs/sfc-demo/sfc103/vm-setup
  ./general_setup.sh
  ```
  
- Modify file `general_env.sh` to fit your own environment setup.
- On OpenDaylight host, start opendaylight controller with sfc features:

  ```sh
  cd ~/sfc-labs/sfc-demo/sfc103/vm-setup
  ./ctl_odl_handling.sh
  ```
  
- On Service hosts, configure sfc components according to the topo:

  ```sh
  cd ~/sfc-labs/sfc-demo/sfc103/vm-setup
  sudo ./srv_node_start.sh 
  ```
  
- On OpenDaylight host, create and update sfc: `./general_actions.sh`, a message will appear and give 3 actions like this:

  ```sh
  Choose one of the following actions:
  1 - Install sfc(for controller node)
  2 - Update sfc(for controller node)
  3 - Dump flows on bridge(for service nodes)
  Your action:
  ```
  
  Wait for a few minutes until sfc installed or updated successfully. Then go to service nodes and dump flows of `br-sfc` by executing `./general_actions.sh` with action 3.
  That's all! 

Trouble Shooting(TBD)
--------------------
