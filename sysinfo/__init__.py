#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides methods for collecting system information in
a portable way, for both Linux and Windows.
"""

# The current structure will be replaced by the following:
# 
# sysinfo.network().dnsdomains = list
# sysinfo.network().default_gateway = str
# sysinfo.network().interfaces = list
# sysinfo.network().interface() = method
# sysinfo.network().interface('eth0').ip_addresses = list
# sysinfo.network().interface('eth0').mac_address = str
# sysinfo.network().interface('eth0').product = str
# sysinfo.network().interface('eth0').vendor = str
# sysinfo.services.smb.workgroup = str
# sysinfo.services.smb.winsservers = list
# sysinfo.hardware.motherboard.product
# sysinfo.hardware.motherboard.vendor
# sysinfo.hardware.videoboard.product
# sysinfo.hardware.videoboard.vendor
#
# All data must be populated, even with empty values.
#
# Planned modules strucuture:
#
# sysinfo/
#           __init__.py
#           linux/
#                   __init__.py
#                   network.py      network class
#                   services.py     services class
#                   hardware.py     provides hardware class
#
#

import sys

if sys.platform == 'linux2':
    from linux.network import network
    from linux.hardware import hardware
    from linux import services

elif sys.platform == 'win32':
    from win32 import network
