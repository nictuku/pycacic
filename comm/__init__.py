#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides methods for communication with the CACIC server.

Currently it uses HTTP which is the only method supported by
the server.
"""

import sysinfo

import http

net = sysinfo.network()
smb = sysinfo.services.smb()
hw =  sysinfo.hardware.HardWare()

interf = net.interface('eth0')

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
 'te_placa_mae_desc'        : hw.data['Motherboard'][0]['product'],
 'te_placa_mae_fabricante'  : hw.data['Motherboard'][0]['vendor'],
 'te_cpu_serial'            : '',
 'te_cpu_desc'              : hw.data['CPU'][0]['product'],
 'te_cpu_fabricante'        : hw.data['CPU'][0]['vendor'],
 'te_cpu_freq'              : hw.data['CPU'][0]['size'],
 'te_placa_video_desc'      : hw.data['VGA compatible controller'][0]['product'],
 'qt_placa_video_mem'       : hw.data['VGA compatible controller'][0]['size'],
 'qt_placa_video_cores'     : hw.data['VGA compatible controller'][0]['width'],
 'te_placa_som_desc'        : hw.data['Multimedia audio controller'][0]['product'],
 'te_teclado_desc'          : '',
 'te_bios_desc'             : hw.data['BIOS'][0]['vendor'] + ' ' + hw.data['BIOS'][0]['version'],
 'te_bios_fabricante'       : hw.data['BIOS'][0]['vendor'],
 'te_bios_data'             : hw.data['BIOS'][0]['version'],
 'te_cdrom_desc'            : hw.data['DVD reader'][0]['product'],
 'te_modem_desc'            : hw.data['Modem'][0]['vendor'] + ' ' + hw.data['Modem'][0]['product'],
 'te_mouse_desc'            : hw.data['Mouse'][0]['product'] + ' ' + hw.data['Mouse'][0]['vendor'],
 'qt_mem_ram'               : hw.data['System Memory'][0]['size'],
# 'te_mem_ram_desc'          : hw.data['System Memory'][0]['
 'te_placa_rede_desc'       : hw.data['Ethernet interface'][0]['vendor'] + ' ' +
                            hw.data['Ethernet interface'][0]['product'],
 }


if __name__ == '__main__':
    print info
