#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides specific services information
"""

import re
import logging

class smb:
    """Provides information from the SMB service using information from the smb.conf file.
    That may not be an exact science, but it's the best method available.
    """

    # FIXME, add "SHARES" collections


    smbconf = ''
    workgroup = ''
    wins_servers = []

    def __init__(self):
        self.smbconf = self.get_smbconf()
        self.workgroup = self.get_workgroup()
        self.wins_servers = self.get_wins_servers()

    def get_smbconf(self):
        try:
            # In Debian-like distros
            f = open('/etc/samba/smb.conf','r')
        except:
           try:
                f = open('/etc/smb/smb.conf','r')
           except:
                logging.error("Error while opening smb.conf")
                return ''

        smbconf = f.read()
        f.close()
        if not smbconf:
                logging.error("Empty smb.conf")
                return ''
        else:
                return smbconf
    


    def get_workgroup(self):
        """Gets the workgroup from which the machine is a member
        """

        m = re.compile(r'^\s*workgroup\s*=\s*(?P<workgroup>.*)',re.I|re.M)

        p = m.search(self.smbconf)

        workgroup = ''
        try: 
            workgroup = p.group('workgroup')
        except:
            pass

        return workgroup
        

    def get_wins_servers(self):
        """Gets the WINS servers in use by the machine
        """
        
        m = re.compile(r'^\s*wins server\s*=\s*(?P<wins>.*)',re.I|re.M)

        p = m.search(self.smbconf)
        wins = []

        try:
            wins_string = p.group('wins')
        except:
            logging.error("Could not find WINS server setting")

        if wins_string:
            wins = wins_string.split(' ')
        else:
            logging.error("Could not find WINS server setting")

        return wins

if __name__ == '__main__':

    s = smb()

    #print i.interf_dict
    #print d.dnsdomain, d.dnsresolvers
    print "teste", s.workgroup,s.wins_servers


