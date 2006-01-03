#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides specific services information
"""

# FIXME, add "SHARES" collections

import re

class GetServicesInfoError(Exception):
    pass

class GetSmbInfoError(GetServicesInfoError):
    pass

class smb:
    """Gets information from the SMB service using information from the smb.conf file.
    That may not be an exact science, but it's the best method available.
    """
    smbconf = ''

    def __init__(self):

        try:
            # In Debian-like distros
            f = open('/etc/samba/smb.conf','r')
        except:
            try:
                f = open('/etc/smb/smb.conf','r')
            except:
                raise GetSmbInfoError, "Error while opening smb.conf"

        self.smbconf = f.read()
        f.close()
        if not self.smbconf:
                raise GetSmbInfoError, "Empty smb.conf"
    
    def getWorkgroup(self):
        """Gets the workgroup from which the machine is a member
        """

        m = re.compile(r'^\s*workgroup\s*=\s*(?P<workgroup>.*)',re.I|re.M)

        p = m.search(self.smbconf)
        try: 
            workgroup = p.group('workgroup')
        except:
            raise GetSmbInfoError, "Could not find workgroup setting"
        
        if workgroup:
            return workgroup
        else:
            raise GetSmbInfoError, "Could not find workgroup setting"

    def getWinsServers(self):
        """Gets the WINS servers in use by the machine
        """
        
        m = re.compile(r'^\s*wins server\s*=\s*(?P<wins>.*)',re.I|re.M)

        p = m.search(self.smbconf)
        try:
            wins_string = p.group('wins')
        except:
            raise GetSmbInfoError, "Could not find WINS server setting"

        if wins_string:
            wins = wins_string.split(' ')
            return wins
        else:
            raise GetSmbInfoError, "Could not find WINS server setting"

