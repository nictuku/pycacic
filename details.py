#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Protótipo para gerenciamento de informações de 
patrimônio e - futuramente - comentários etc.
"""

import urllib2
import httplib
import base64
import re

# Precisamos montar um dicionário com os detalhes, a partir de
# diversas fontes, dependendo da situação.
#
# 1: Diálogo de coleta dos dados
# 2: Cache da configuração
# 
# Para preparar as coletas, é preciso obter no gerente
# as seguintes informações:
# 1: A coleta está ativa para a rede desta máquina?
# 2: Quais são os rótulos da coleta de PATRIMONIO?


#$patrimony_collection =
#      ( ( $result =~ 
#/<cs_coleta_patrimonio>\s*S\s*<\/cs_coleta_patrimonio>/i 
#          || ( $Config::testmode == 1 ) )
# FIXME do gerente:
# Quando desabilitado, o tag "cs_coleta_patrimonio" *NAO APARECE*, ao invés de aparecer
# com "N".

def get_config(data):
    """Consulta no servidor a atual configuração da rede atual
    """
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
    request.add_data(formatInfo(data))
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

# lixo, só pra funfar.

from sysinfo import network
from sysinfo import services
from sysinfo import hardware
from comm import http

def handleDictErrorsWithEmptyString(source):
    if source:
        return source
    else:
        return ''

def handleErrorsWithEmptyString(source, argument_list):
    """Handles errors for the given function call. Always returns a string - or
     an empty one if an exception occurs.

    Usage:
        handleErrors(function, tuple_args)

    Note that 'function' must not have the parenthesis and tuple_args
    is actually a tuple.

    Example:
        handleErrors(a.getMacAddress, ( 'eth0' ) )
    """

    arg = argument_list[:]

    if len(arg) > 0:
        try:
            output = source(arg)
        except:
            return ''
        else:
            return output
    else:
        try:
            output = source()
        except:
            return ''
        else:
            return output

def handleErrorsUsingList(source, argument_list, item):
    """Handles errors for the given function call which would return a list.
    You must also specify the element and it will always return a string.

    If an exception occurs it returns an empty string.

    Usage:
        handleErrors(function, tuple_args, item)

    Note that 'function' must not have the parenthesis and tuple_args is
    actually a tuple.

    Example:
        handleErrorsUsingList(s.getWinsServers, ( 'eth0' ), 1 )
    """

    arg = argument_list[:]

    if len(arg) > 0:
        try:
            output = source(arg)[item]
        except:
            return ''
        else:
            return output
    else:
        try:
            output = source()[item]
        except:
            return ''
        else:
            return output



def formatInfo(info_dict):
    """Formats the 'info_dict' to the required format by putFormatedInfo()

    Important: as it uses dictionaries to organize the data, it won't return
    it in the original order of the pairs.

    Example:

    info = {
        'te_node_address' : '00-0D-60-E0-A6-3C',
        'id_so' : '8',
        'id_ip_rede' : '10.68.8.0',
        'te_nome_computador' : 'INF24GO',
        'te_ip' :   '10.68.8.195',
        'te_versao_cacic' : '2.0.0.23'
        }

    x = formatInfo(info)

    print x
    te_ip=10.68.8.195&te_node_address=00-0D-60-E0-A6-3C&id_ip_rede=10.68.8.0&\
    id_so=8&te_nome_computador=INF24GO&te_versao_cacic=2.0.0.23&
    """

    info_string = ''

    for key, value in info_dict.iteritems():
        info_string += key + '=' + value + '&'

    return info_string

a = network.interfaces()
s = services.smb()

hw =  hardware.HardWare()


info =  {
  # falta: last log, serial da cpu, detalhes da RAM, teclado

 'te_node_address'          : handleErrorsWithEmptyString(a.getMacAddress, ('eth0')),
 'id_so'                    : '0',
 'id_ip_rede'               : handleErrorsWithEmptyString(a.getNetwork, ('eth0')),
 'te_nome_computador'       : handleErrorsWithEmptyString(a.hostname, ()),
 'te_ip'                    : handleErrorsWithEmptyString(a.getIpAddress, ('eth0')),
 'te_versao_cacic'          : 'pyc',
 'te_mascara'               : handleErrorsWithEmptyString(a.getNetmask, ('eth0')),
 'te_gateway'               : handleErrorsWithEmptyString(a.getDefaultGateway, ()),
 'te_serv_dhcp'             : handleErrorsWithEmptyString(a.getDHCPServer, ('eth0')),
 'te_nome_host'             : handleErrorsWithEmptyString(a.hostname, ()),
 'te_origem_mac'            : 'ifconfig',
 'te_dns_primario'          : handleErrorsWithEmptyString(a.getDNSResolvers, ())[0],
 'te_dns_secundario'        : handleErrorsWithEmptyString(a.getDNSResolvers, ())[1],
 'te_dominio_dns'           : handleErrorsWithEmptyString(a.getDNSDomain, ()),
 'te_wins_primario'         : handleErrorsUsingList(s.getWinsServers, (), 0),
 'te_wins_secundario'       : handleErrorsUsingList(s.getWinsServers, (), 1),
 'te_workgroup'             : handleErrorsWithEmptyString(s.getWorkgroup, ()),
 #hardware
 'te_placa_mae_desc'        : hw.data['Motherboard'][0].get('product', ''),
 'te_placa_mae_fabricante'  : hw.data['Motherboard'][0].get('vendor', ''),
 'te_cpu_serial'            : '',
# 'te_cpu_desc'              : hw.data['CPU'][0].get('product', ''),
# 'te_cpu_fabricante'        : hw.data['CPU'][0].get('vendor', ''),
# 'te_cpu_freq'              : hw.data['CPU'][0].get('size', ''),
# 'te_placa_video_desc'      : hw.data['VGA compatible controller'][0].get('product', ''),
# 'qt_placa_video_mem'       : hw.data['VGA compatible controller'][0].get('size',''),
# 'qt_placa_video_cores'     : hw.data['VGA compatible controller'][0].get('width', ''),
# 'te_placa_som_desc'        : hw.data['Multimedia audio controller'][0].get('product', ''),
# 'te_teclado_desc'          : '',
# 'te_bios_desc'             : hw.data['BIOS'][0]['vendor'] + ' ' + hw.data['BIOS'][0]['version'],
# 'te_bios_fabricante'       : hw.data['BIOS'][0]['vendor'],
# 'te_bios_data'             : hw.data['BIOS'][0]['version'],
# 'te_cdrom_desc'            : hw.data['DVD reader'][0]['product'],
# 'te_modem_desc'            : hw.data['Modem'][0]['vendor'] + ' ' + hw.data['Modem'][0]['product'],
# 'te_mouse_desc'            : hw.data['Mouse'][0]['product'] + ' ' + hw.data['Mouse'][0]['vendor'],
# 'qt_mem_ram'               : hw.data['System Memory'][0]['size'],
# 'te_mem_ram_desc'          : hw.data['System Memory'][0]['
# 'te_placa_rede_desc'       : hw.data['Ethernet interface'][0]['vendor'] + ' ' +
#                            hw.data['Ethernet interface'][0]['product'],
 }


config = get_config(info)

print "config:", config
