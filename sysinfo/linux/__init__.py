#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os 
import logging
import sys

id = str(os.getuid())

if id != '0':
    logging.error("In the current version, sysinfo must be called as root.\
Current uid: " + id)
    sys.exit(1)

