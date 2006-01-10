#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides methods for communication with the CACIC server.

Currently it uses HTTP with ini-like data transfer, which is the
only method supported by the server at the moment.
"""

import sysinfo
import sys

import http
import config

get_hard = True
get_services = True

def __init__(self):

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
