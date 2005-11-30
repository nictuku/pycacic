#!/usr/bin/env python
# -*- coding: utf-8 -*-

import socket 

from sysinfo import network

a = network.interfaces()

print "MAC:", a.mac_address('eth0')

print "STATUS:",a.getStatus('eth0')

print "IP:",a.getIpAddress('eth0')

print "Rede:",a.getNetwork('eth0')

print "Hostname:",a.hostname()

print "Default Gateway:",a.getDefaultGateway()

print "DHCP Server:",a.getDHCPServer('eth0')
