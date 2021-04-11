#!/bin/bash

sleep 10
iwlist wlan1 scan > /tmp/networks.txt
sleep 30
iwlist wlan1 scan > /tmp/networks.txt
