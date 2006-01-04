#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides methods for collecting system information in
a portable way, for both Linux and Windows.
"""

# The current structure will be replaced by the following:
# 
# sysinfo.network.dnsdomains = list
# sysinfo.network.default_gateway = str
# sysinfo.network.interfaces = list
# sysinfo.network.interface() = method
# sysinfo.network.interface('eth0').ip_addresses = list
# sysinfo.network.interface('eth0').mac_address = str
# sysinfo.network.interface('eth0').product = str
# sysinfo.network.interface('eth0').vendor = str
#
# All data must be populated, even with empty values.

import sys

if sys.platform == 'linux2':
    from linux import network
    from linux import hardware
    from linux import services

elif sys.platform == 'win32':
    from win32 import network
