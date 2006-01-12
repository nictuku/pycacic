#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2006 José de Paula Eufrásio Junior (jose.junior@gmail.com) AND
#                      Yves Junqueira (yves.junqueira@gmail.com)
#
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

"""Provides specific services information
"""

import re
import logging

logger = logging.getLogger("sysinfo.linux.services")

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
                logger.error("Error while opening smb.conf")
                return ''

        smbconf = f.read()
        f.close()
        if not smbconf:
                logger.error("Empty smb.conf")
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
            logger.error("Could not find WINS server setting")
        else:
            if wins_string:
                wins = wins_string.split(' ')
            else:
                logger.error("Could not find WINS server setting")
        l = len(wins)
        repeat = 2 - l
        for foo in range(repeat):
            wins.append('')
        return wins

if __name__ == '__main__':

    s = smb()

    #print i.interf_dict
    #print d.dnsdomain, d.dnsresolvers
    print "teste", s.workgroup,s.wins_servers


