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

"""Configurations manager and interface to sysinfo.

Basically this is the CACIC agent core.

Its job is to get the configuration from the server,
from local files and parameters, then populate informational
objects that will be accessed by other modules.
"""

import re
import urllib2
import httplib
import base64
import logging
import sys

import http
import sysinfo

import StringIO
import gzip

sys.path.append('/etc/pycacic')
sys.path.append('/usr/local/etc/pycacic')

logger = logging.getLogger("cacic.agent.config")

try:
    import cacic
except ImportError:
    logger.error("'cacic.py' config file not found")
    raise Exception, "'cacic.py' config file not found" 

class cfg:
    """Builds a dict of configuration, in the following
    order of preference:
    - command arguments
    - local configurations
    - fallback values
    """
    cacic_cfg = {}

    def __init__(self):
        logger.debug("Instantiating agent.cfg")

        self.cacic_cfg = { 'server':'cacic', 
                       'cache_path':'/var/cache/cacic',
                       'force_send':0, 
                       'interface':'eth0', 
                       'log_path':'/var/log/cacic', 
                       'test_mode':0, 
                       'verbose':0,
        }

        local_parameters = dir(cacic)

        # local values overriding default values
        logger.debug("Loading local config")
        for def_parameter, def_value in self.cacic_cfg.iteritems():
            if def_parameter in local_parameters:
                logger.debug("Local config: " + str(def_parameter) + "=" + 
                    str(def_value))
                self.cacic_cfg[def_parameter] = def_value

cur_cacic = cfg()
cur_config = cur_cacic.cacic_cfg

def parse_remote_raw_cfg(cfg, cfg_regex, remote_raw_cfg, mode):
    """It parses the remote_raw_cfg string, looking for the cfg_regex and return the
    results found.
    """
    logger.debug("Looking for " + cfg + " setting in the remote config data")
    x = re.compile(cfg_regex, re.I)
    w = x.search(remote_raw_cfg)

    if w:
        if mode == 'boolean':
            return True

        elif mode == 'string':
            setting = w.groups('mac_invalidos')
            return setting
    else:
        logger.warning("Could not find the configuration respective to " + cfg + " in the server")
        return False

def get_config(data):
    """Asks the server the current setting for this computer, as explicited in the
    'data' dictionary. 
    
    This dictionary provides enough information required by ws/get_config.php.
    """
    logger.debug("Getting config data from the CACIC server")

    if type(data) is not dict:
        logger.error("get_config needs a dict argument")
        raise Exception, "get_config requires a dict argument"
        return ''

    path = 'cacic2/ws/get_config.php'
    server = cur_config['server']

    debug = urllib2.HTTPHandler(debuglevel=0)

    url = 'http://' + server + '/' + path
    base64string = base64.encodestring('%s:%s' % ('USER_CACIC', 'PW_CACIC'))[:-1]

    logger.debug("Building request object")
    request = urllib2.Request(url)
    request.add_header('User-Agent', 'AGENTE_CACIC')
    request.add_header('Pragma', 'no-cache')
    request.add_header('Accept-encoding', 'gzip')

    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_data(http.formatInfo(data))
    opener = urllib2.build_opener(debug) # +authinfo

    logger.debug("Submitting request to the server")
    f = opener.open(request)
    if f.headers.get('Content-Encoding') == 'gzip':
        logger.debug("Content provided by the server is gzip-encoded.")
        compresseddata = f.read()
        compressedstream = StringIO.StringIO(compresseddata)
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        logger.debug("Reading compressed data.")
        feeddata = gzipper.read()
    else:
        logger.debug("Reading data.")
        feeddata = opener.open(request).read()

    return feeddata

# FIXME: these should come from either local configuration or set
# by the calling method, as required.

get_hard = True
get_services = True

class load:
    info = {}
    config_info = {}
    remote_cfg = {}
    remote_raw_cfg = ''
    logger.debug("Loading config.load class")

    def __init__(self):
        logger.debug("Instantiating config.load")

        net = sysinfo.network()
        interf = net.interface('eth0')
        last = net.last_logon()
        
        self.remote_raw_cfg = get_config(self.config_info)
        logger.debug("remote_raw_cfg populated")

        logger.debug("LAST LOGON:" + last.user)

        #print "Remote raw config:", remote_raw_cfg

        self.remote_cfg['patrimony_collection'] = parse_remote_raw_cfg(
         'patrimony_collection', '<cs_coleta_patrimonio>\s*s\s*<\/cs_coleta_patrimonio>', 
         self.remote_raw_cfg, 'boolean')

        self.remote_cfg['hardware_collection'] = parse_remote_raw_cfg(
         'hardware_collection', '<cs_coleta_hardware>\s*S\s*<\/cs_coleta_hardware>', 
         self.remote_raw_cfg, 'boolean')

        self.remote_cfg['disk_collection'] = parse_remote_raw_cfg(
         'disk_collection', '<cs_coleta_unid_disc>\s*S\s*<\/cs_coleta_unid_disc>', 
         self.remote_raw_cfg, 'boolean')

        self.remote_cfg['ignore_macs'] = parse_remote_raw_cfg(
         'ignore_macs', 
          '<te_enderecos_mac_invalidos>(?P<mac_invalidos>[^<]*)<\/te_enderecos_mac_invalidos>',
         self.remote_raw_cfg, 'string')

        logger.debug("Getting network data from sysinfo.network()")

        # FIXME: if interf.mac_address is not in remote_cfg['ignore_macs']
        if get_services:
            logger.debug("Getting smb data from sysinfo.services.smb()")
            smb = sysinfo.services.smb()

        if get_hard:
            logger.debug("Getting hardware data from sysinfo.hardware()")
            hw =  sysinfo.hardware()
            # Necessary changes
            ram_size = str(int(hw.memory.size.replace(' bytes', '')) / 1048576)
            video_ram_size = str(int(hw.video_board.memory.replace(' bytes',
            '')) / 1048576)
           

        logger.debug("Populating 'config_info' dictionary")
        self.config_info = {
         'te_node_address'          : interf.mac_address,
         'id_so'                    : '0',
         'id_ip_rede'               : interf.ip_network,
         'te_nome_computador'       : net.hostname,
         'te_ip'                    : interf.ip_addresses[0],
         'te_versao_cacic'          : 'pyc',

        }

        if get_services and get_hard:
            logger.debug("Populating 'info' dictionary")

            self.info =  {
            
             'te_node_address'          : interf.mac_address,
             'id_so'                    : '0',
             'id_ip_rede'               : interf.ip_network,
             'te_nome_computador'       : net.hostname,
             'te_ip'                    : interf.ip_addresses[0],
             'te_versao_cacic'          : 'pyc',
             'te_mascara'               : interf.netmask,
             'te_gateway'               : net.default_gateway,
             'te_serv_dhcp'             : interf.dhcp_server,
             'te_nome_host'             : net.hostname,
             'te_origem_mac'            : 'ifconfig',
             'te_dns_primario'          : net.dnsresolvers[0],
             'te_dns_secundario'        : net.dnsresolvers[1],
             'te_dominio_dns'           : net.dnsdomain,
             'te_dominio_windows'       : last.user,
             'te_wins_primario'         : smb.wins_servers[0],
             'te_wins_secundario'       : smb.wins_servers[0],
             'te_workgroup'             : smb.workgroup,
             #hardware
             'te_placa_mae_desc'        : hw.motherboard.product,
             'te_placa_mae_fabricante'  : hw.motherboard.vendor,
             'te_cpu_serial'            : '',
             'te_cpu_desc'              : hw.cpu.product,
             'te_cpu_fabricante'        : hw.cpu.vendor,
             'te_cpu_freq'              : hw.cpu.frequency,
             'te_placa_video_desc'      : hw.video_board.product,
             'qt_placa_video_mem'       : video_ram_size,
             'qt_placa_video_cores'     : hw.video_board.width,
             'te_placa_som_desc'        : hw.sound_board.product,
             'te_teclado_desc'          : hw.keyboard.model,
             'te_bios_desc'             : hw.bios.vendor + hw.bios.version,
             'te_bios_fabricante'       : hw.bios.vendor,
             'te_bios_data'             : hw.bios.version,
             'te_cdrom_desc'            : hw.dvd_reader.product,
             'te_modem_desc'            : hw.modem.vendor + hw.modem.product,
             'te_mouse_desc'            : hw.mouse.product + hw.mouse.vendor,
             'qt_mem_ram'               : ram_size,
            # 'te_mem_ram_desc'          :
             'te_placa_rede_desc'       : hw.ethernet_board.vendor + hw.ethernet_board.product
             }


