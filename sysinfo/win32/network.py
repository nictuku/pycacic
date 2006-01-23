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


"""Provides network information
"""

import commands
import logging
import re
import socket
import struct
import sys

# auxiliary functions
def hex2dec(s):
    """Returns the integer value of a hexadecimal string s
    """
    return int(s, 16)
# Functions based on:
# http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66517
# which is licensed under the BSD license.

def dottedQuadToNum(ip):
    """convert decimal dotted quad string to long integer"""
    return struct.unpack('L',socket.inet_aton(ip))[0]

def numToDottedQuad(n):
    """Convert long int to dotted quad string
    """
    return socket.inet_ntoa(struct.pack('L',n))

def convert_ip_to_net_and_host(ip, maskstring):
    """Returns tuple (network, host) dotted-quad addresses given IP and mask"""
    # (by Greg Jorgensen)

    n = dottedQuadToNum(ip)
    m = dottedQuadToNum(maskstring)

    host = n & m
    net = n - host

    return numToDottedQuad(net), numToDottedQuad(host)


class interface:
    """Retrieves interface specific information
    """
    ip_addresses = []
    mac_address = ''
    netmask = ''
    status = ''
    dhcp_server = ''
    ip_network = ''
    interf_dict = {}

    def __init__(self, interf=None):
        self.interf_dict = ifconfig_instance.interf_dict

        if interf:
            self.ip_addresses = self.get_ip_addresses(interf)
            self.mac_address = self.get_mac_address(interf)
            self.netmask = self.get_netmask(interf)
            self.ip_network = self.get_network(self.ip_addresses[0],self.netmask)
            self.status = self.get_status(interf)
            self.dhcp_server = self.get_dhcp_server(interf)

    def get_ip_addresses(self, interf=None):
        """Shows the interface's respective IP addresses
        """
        # FIXME: get_address currently returns a singleton list.

        h = re.compile(r'inet add?r:(?P<ip_addr>[\w.]+)', re.I)
        w = h.search(self.interf_dict[interf])
        ip_addrs = []
        if w:
            ip_addrs.append(w.group('ip_addr'))
        return ip_addrs

    
    def get_mac_address(self,interf=None):
        """Gives network interfaces hardware address
        """
        mac = ''
        if interf:
            h = re.compile(r'HW(addr)? (?P<mac>[\w:]+) ', re.I)
            w = h.search(self.interf_dict[interf])
            if w:
                mac = w.group('mac')
        return mac

    def get_network(self,ip=None,netmask=None):

        network = ''
        if ip and netmask:
            (host, network) = convert_ip_to_net_and_host(ip, netmask)
        return network

    def get_netmask(self,interf=None):
        """Shows the interface's respective IP netmask
        """
        netmask = ''
        if interf:
            h = re.compile(r'Mask:(?P<netmask>[\w.]+)', re.I)
            w = h.search(self.interf_dict[interf])
            if w:
                netmask = w.group('netmask')
        return netmask

    def get_status(self,interf=None):
        """Shows interface status
        """
        status = ''
        if interf:
            h = re.compile('UP',re.I)
            w = h.search(self.interf_dict[interf])
            if w:
                 return 'UP'
            else:
                 return 'DOWN'
        else:
            return ''

    def get_dhcp_server(self,interf=None):
        """Return the current DHCP Server for the 'interf' interface, by parsing the dhclient.leases file.
        It will try to define if the IP was indeed setup using DHCP by trying to find dhclient in the
        current running process list.
        In case there are many leases stored, it should consider the last one for the given interface.
        """
 
        if interf == None:
            return ''

        # FIXME if there is a better way to define if a machine is using DHCP
        # besides checking dhclient?

        dh = commands.getstatusoutput('ps aux|grep dhclient')

        if dh[0] != 0:
            logging.error("Erro buscando dhclient em execução")
            return ''
        else:
            i = dh[1]
            sp = re.compile('-lf\s+(?P<leases_file>\S+)\s+(?P<interface>[ae]th[\d]+|lo)')
            m = sp.search(dh[1])
            if m:
                leases_file = m.group('leases_file')
            else:
                #FIXME: this should work for other distros and dhclient versions
                leases_file = '/var/lib/dhcp3/dhclient.leases'
            try:
                f = open(leases_file)
            except:
                logging.error("Could not open leases_file (tried from " + leases_file + " )")
                return ''
        dhcp = f.read()
        f.close()

        sp = re.compile('(lease)\s*{')
        leases_list = sp.split(dhcp)

        test_int = re.compile('interface\s*"'+ interf)

        # Removing leases unrelated to 'interf'
        for x in leases_list:
            m = test_int.search(x)
            if not m:
               leases_list.remove(x)
        l = len(leases_list) - 1
        lease = leases_list[l]

        o = re.compile('option\s+dhcp-server-identifier\s+(?P<dhcp_server>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*;')
        k = o.search(lease)
        server = k.group('dhcp_server')

        # Shows the last lease
        return server

class network(resolv, ifconfig, misc):
    """This is the stuff users will access. It inherits data from other 'os' 
    classes so users can access information like network.dnsdomain.
    """

    def __init__(self):
        resolv.__init__(self)
        ifconfig.__init__(self)
        misc.__init__(self)
        self.interface = interface
        



if __name__ == '__main__':

    g = network()

    #print i.interf_dict
    #print d.dnsdomain, d.dnsresolvers
    b = g.interface('eth0')
    print "teste", g.interfaces, b.ip_addresses
