#!/bin/bash

mkdir -p acoustic_node/logs
mkdir -p /home/pi/acoustic_node/tasks
mkdir -p /home/pi/acoustic_node/done

sudo apt-get install python3-pip
sudo pip3 install paramiko
#? sudo apt-get install openssh-server
sudo apt-get install rpi.gpio
sudo apt-get install libatlas-base-dev
sudo apt-get install python3-numpy
sudo apt-get install python3-scipy
