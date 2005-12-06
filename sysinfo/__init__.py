#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides methods for collecting system information in
a portable way, for both Linux and Windows.
"""

import sys

if sys.platform == 'linux2':
    from linux import network
    from linux import services

elif sys.platform == 'win32':
    from win32 import network
