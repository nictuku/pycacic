#!/usr/bin/env python
# -*- coding: utf-8 -*-

import getpass
import logging
import sys

if getpass.getuser() != 'root':
    logging.error("In the current version, sysinfo must be called as root")
    sys.exit(1)

