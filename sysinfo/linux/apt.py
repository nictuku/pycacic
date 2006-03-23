#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright (C) 2006 José de Paula Eufrásio Junior (jose.junior@gmail.com)
#   AND#                      Yves Junqueira (yves.junqueira@gmail.com)
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

"""Provides package management system information
"""


# http://users.sarai.net/shehjar/download/py-apt-tut.txt

import apt_pkg
import os
import sys

class packages:

    installed = []
    installed_ver = {} # package : version
    update_candidates = {} # package : new_version
    
    def __init__(self):
        # FIXME: dup the filehandles and hide messages
        #os.close(1)
        #os.close(2)
        c = cache()
        self.installed_ver = c.installed_packages
        self.installed = self.installed_ver.keys()
        self.installed.sort()
        self.update_candidates = c.update_candidates
        
#        for software in self.installed:
#            self.installed_ver[software] = c.installed_packages[software].VerStr
        

class cache:

    # {'Name' : 'Version'}
    installed_packages = {}
    update_candidates = {}
    
    def __init__(self):

        apt_pkg.init()
        self.cache = apt_pkg.GetCache()
        self.installed_packages, self.update_candidates = \
            self._read_packages(self.cache.Packages)


    def _read_packages(self, packages):
        installed, upgradable = {}, {}

        # from the examples/checkstate.py file in python-apt package
        for package in packages:
                versions = package.VersionList
                if not versions:
                        continue
                version = versions[0]
                for other_version in versions:
                        if apt_pkg.VersionCompare(version.VerStr, other_version.VerStr)<0:
                                version = other_version
                if package.CurrentVer:
                        installed[package.Name] = package.CurrentVer.VerStr
                        current = package.CurrentVer
                        if apt_pkg.VersionCompare(current.VerStr, version.VerStr)<0:
                                upgradable[package.Name] = version.VerStr
#                                break
#                        else:
#                                updated[package.Name] = current
#                else:
#                        uninstalled[package.Name] = version
        #print "installed:", installed
        #print "Update candidates:", upgradable
        return installed, upgradable
      
        
if __name__ == '__main__':
    s = packages()
    #c = cache()
    #print c.update_candidates 
    print "instalados", s.installed
    print "instalados_versao", s.installed_ver
    print "update", s.update_candidates
    
