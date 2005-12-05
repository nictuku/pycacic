#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides network information
"""

import commands 
import logging
import re
import socket
import struct
import sys

class interfaces:
    """Shows interfaces data. 
    interf_dict provides a list of interfaces and their respective raw
    "ifconfig" data.
    """

    interf_dict = {}

    resolvconf = ''

    def __init__(self):
	ifconfig = commands.getstatusoutput("export LANG=C; /sbin/ifconfig")
	if ifconfig[0] != 0:
	    logging.error("Erro ao executar ifconfig")
	    raise 
	else:
	    i = ifconfig[1]
	    sp = re.compile('([ae]th[\d]+|lo) ')
	    interf_list = sp.split(i)
	    interf_list.pop(0)
	    i = 1
	    for x in interf_list:
		if i % 2 == 0: # PARES
		    self.interf_dict[ interf_list[i - 2] ] = x
		i += 1
    
    try:
        r = open('/etc/resolv.conf','r')
    except:
        logging.error("Erro ao ler /etc/resolv.conf")
    else:
        resolvconf = r.read()
        r.close()

    def getDNSDomain(self):

        h = re.compile( r'.*(domain|search)\s+(?P<domain>.*)\s*',
                        re.I)

        w = h.search(self.resolvconf)
        
        domain = ''

        if w:
            domain = w.group('domain')

        return domain

    def getDNSResolvers(self):

        r = re.compile( r'(nameserver)\s+(?P<resolver>\S+)\s*'
                        r'((nameserver)\s+(?P<resolver2>\S+)\s*)?',
                        re.I)

        x = r.search(self.resolvconf)

        resolvers = []

        if x:
            resolver = x.group('resolver')

            if resolver:
                resolvers.append(resolver)

            resolver2 = x.group('resolver2')

            if resolver2:
                resolvers.append(resolver2)
       
        return resolvers

    def hostname(self):
        """Returns current hostname
        """
        return socket.gethostname()

    def mac_address(self,interf):
        """Gives network interfaces hardware address
        """
        h = re.compile(r'HW(addr)? (?P<mac>[\w:]+) ', re.I)
        w = h.search(self.interf_dict[interf])
        mac = w.group('mac')
        return mac

    def getIpAddress(self,interf):
        """Shows the interface's respective IP addresses
        """
        h = re.compile(r'inet add?r:(?P<ip_addr>[\w.]+)', re.I)
        w = h.search(self.interf_dict[interf])
        ip_addr = w.group('ip_addr')
        return ip_addr

    def getNetmask(self,interf):
        """Shows the interface's respective IP netmask
        """
        h = re.compile(r'Mask:(?P<netmask>[\w.]+)', re.I)
        w = h.search(self.interf_dict[interf])
        netmask = w.group('netmask')
        return netmask

    def getStatus(self,interf):
        """Shows interface status
        """
        h = re.compile('UP',re.I)
        w = h.search(self.interf_dict[interf])
        if w:
             return 'UP'
        else:
             return 'DOWN'

    def getDHCPServer(self,interf):
        """Return the current DHCP Server for the 'interf' interface, by parsing the dhclient.leases file.
        It will try to define if the IP was indeed setup using DHCP by trying to find dhclient in the
        current running process list.
        In case there are many leases stored, it should consider the last one for the given interface.
        """
        dh = commands.getstatusoutput('ps aux|grep dhclient')

	if dh[0] != 0:
	    logging.error("Erro buscando dhclient em execução")
	    raise 
	else:
	    i = dh[1]
	    sp = re.compile('-lf\s+(?P<leases_file>\S+)\s+(?P<interface>[ae]th[\d]+|lo)')

	    m = sp.search(dh[1])
	    leases_file = m.group('leases_file')
        
        try:
            f = open(leases_file)
        except:
            return false
        
        dhcp = f.read()
        
        sp = re.compile('(lease)\s*{')
        leases_list = sp.split(dhcp)

        test_int = re.compile('interface\s*"'+ interf)

        # remove leases unrelated to 'interf'
        for x in leases_list:
            m = test_int.search(x)
            if not m:
               leases_list.remove(x)
        l = len(leases_list) - 1
        lease = leases_list[l]

        o = re.compile('option\s+dhcp-server-identifier\s+(?P<dhcp_server>\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})\s*;')
        k = o.search(lease)
        server = k.group('dhcp_server')

        return server
        # shows the last lease

    def getNetwork(self,interf):
        ip = self.getIpAddress(interf)
        netmask = self.getNetmask(interf)
        (host, network) = self.ipToNetAndHost(ip, netmask)
        return network
 
    def getDefaultGateway(self):
        t1 = self.getDefaultGatewayFromProc()
        if not t1:
            t1 = self.getDefaultGatewayFromBinRoute()
            if not t1:
               return false
        return t1

    # Functions called by getDefaultGateway

    def getDefaultGatewayFromProc(self):
        """"Returns the current default gateway, reading that from /proc'
        """
        try:
            f = open('/proc/net/route','r')
            route = f.read()
        except:
            return false
        else:
            h = re.compile('\n(?P<interface>\w+)\s+00000000\s+(?P<def_gateway>[\w]+)\s+')
            w = h.search(route)
            if w.group('def_gateway'):
                return self.numToDottedQuad(self.hex2dec(w.group('def_gateway')))
            else:
                return false

            logging.warning('Could not read default gateway from /proc')

    def getDefaultGatewayFromBinRoute(self):
        """Get Default Gateway from '/sbin/route -n
        Called by getDefaultGateway and is only used if could not get that from /proc
        """
        routebin = commands.getstatusoutput("export LANG=C; /sbin/route -n")

        if routebin[0] != 0:
            logging.error("Erro while trying to run route")
            return false
        h = re.compile('\n0.0.0.0\s+(?P<def_gateway>[\w.]+)\s+')
        w = h.search(routebin[1])

        def_gateway = w.group('def_gateway')

        if def_gateway:
            return def_gateway

    # getDNSServers

    # getDNSDomain

    # getWINSServers

    # getWindowsDomain

    # Auxiliary functions

    def hex2dec(self,s):
        """Returns the integer value of a hexadecimal string s
        """
        return int(s, 16)

    # Functions based on:
    # http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/66517
    # which is licensed under the BSD license.

    def dottedQuadToNum(self,ip):
        """convert decimal dotted quad string to long integer"""
        return struct.unpack('L',socket.inet_aton(ip))[0]

    def numToDottedQuad(self,n):
        """Convert long int to dotted quad string"""
        return socket.inet_ntoa(struct.pack('L',n))

    def ipToNetAndHost(self,ip, maskstring):
        """Returns tuple (network, host) dotted-quad addresses given IP and mask"""
    # (by Greg Jorgensen)

        n = self.dottedQuadToNum(ip)
        m = self.dottedQuadToNum(maskstring)

        host = n & m
        net = n - host

        return self.numToDottedQuad(net), self.numToDottedQuad(host)


