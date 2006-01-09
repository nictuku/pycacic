#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gestor de configurações do CACIC.
"""

import re
import urllib2
import httplib
import base64
import logging
import sys

import http
import sysinfo

def parse_remote_raw_cfg(cfg, cfg_regex, remote_raw_cfg, mode):

    x = re.compile(cfg_regex, re.I)
    w = x.search(remote_raw_cfg)

    if w:
        if mode == 'boolean':
            return True

        elif mode == 'string':
            setting = w.groups('mac_invalidos')
            return setting
    else:
        logging.warning("Could not find the configuration respective to " + cfg + " in the server")
        return False

def get_config(data):
    """Consulta no servidor a atual configuração da rede atual
    "data" deve ser um dicionário contendo certas informações
    essenciais ao ws/get_config.php
    """
    if type(data) is not dict:
        logging.error("get_config needs a dict argument")
        raise Exception, "get_config requires a dict argument"
        return ''
    path = 'cacic2/ws/get_config.php'
    server = 'cacic'

    debug = urllib2.HTTPHandler(debuglevel=0)

    url = 'http://' + server + '/' + path
    base64string = base64.encodestring('%s:%s' % ('USER_CACIC', 'PW_CACIC'))[:-1]

    request = urllib2.Request(url)
    request.add_header('User-Agent', 'AGENTE_CACIC')
    request.add_header('Pragma', 'no-cache')
    request.add_header('Accept-encoding', 'gzip')

    request.add_header("Authorization", "Basic %s" % base64string)
    request.add_data(http.formatInfo(data))
    opener = urllib2.build_opener(debug) # +authinfo
    f = opener.open(request)
    if f.headers.get('Content-Encoding') == 'gzip':
        import StringIO
        compresseddata = f.read()
        compressedstream = StringIO.StringIO(compresseddata)
        import gzip
        gzipper = gzip.GzipFile(fileobj=compressedstream)
        feeddata = gzipper.read()
    else:
        feeddata = opener.open(request).read()

    return feeddata

"""Provides methods for communication with the CACIC server.

Currently it uses HTTP with ini-like data transfer, which is the
only method supported by the server at the moment.
"""

get_hard = True
get_services = True

net = sysinfo.network()

if get_services:
    smb = sysinfo.services.smb()

if get_hard:
    hw =  sysinfo.hardware()

interf = net.interface('eth0')

config_info = {
 'te_node_address'          : interf.mac_address,
 'id_so'                    : '0',
 'id_ip_rede'               : interf.ip_network,
 'te_nome_computador'       : net.hostname,
 'te_ip'                    : interf.ip_addresses[0],
 'te_versao_cacic'          : 'pyc',

}

if get_services and get_hard:

    info =  {
    
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
     'qt_placa_video_mem'       : hw.video_board.memory,
     'qt_placa_video_cores'     : hw.video_board.width,
     'te_placa_som_desc'        : hw.sound_board.product,
     'te_teclado_desc'          : '',
     'te_bios_desc'             : hw.bios.vendor + hw.bios.version,
     'te_bios_fabricante'       : hw.bios.vendor,
     'te_bios_data'             : hw.bios.version,
     'te_cdrom_desc'            : hw.dvd_reader.product,
     'te_modem_desc'            : hw.modem.vendor + hw.modem.product,
     'te_mouse_desc'            : hw.mouse.product + hw.mouse.vendor,
     'qt_mem_ram'               : hw.memory.size,
    # 'te_mem_ram_desc'          :
     'te_placa_rede_desc'       : hw.ethernet_board.vendor + hw.ethernet_board.product
     }

remote_raw_cfg = config.get_config(config_info)

#print "Remote raw config:", remote_raw_cfg

remote_cfg = {}

remote_cfg['patrimony_collection'] = config.parse_remote_raw_cfg(
 'patrimony_collection', '<cs_coleta_patrimonio>\s*s\s*<\/cs_coleta_patrimonio>', 
 remote_raw_cfg, 'boolean')

remote_cfg['hardware_collection'] = config.parse_remote_raw_cfg(
 'hardware_collection', '<cs_coleta_hardware>\s*S\s*<\/cs_coleta_hardware>', 
 remote_raw_cfg, 'boolean')

remote_cfg['disk_collection'] = config.parse_remote_raw_cfg(
 'disk_collection', '<cs_coleta_unid_disc>\s*S\s*<\/cs_coleta_unid_disc>', 
 remote_raw_cfg, 'boolean')

remote_cfg['ignore_macs'] = config.parse_remote_raw_cfg(
 'ignore_macs', 
  '<te_enderecos_mac_invalidos>(?P<mac_invalidos>[^<]*)<\/te_enderecos_mac_invalidos>',
 remote_raw_cfg, 'string')


if __name__ == '__main__':
    print info
    print remote_cfg
