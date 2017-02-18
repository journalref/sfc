#!/bin/bash
echo "setup paramiko for sfc-agent"
tar xzvf paramiko-1.15.0.tar.gz
cd paramiko-1.15.2/
sudo python3 setup.py install
