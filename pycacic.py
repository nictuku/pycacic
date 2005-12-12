#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Atualmente utilizado apenas para testar módulos e testar
metodologias e estruturas
"""

# Algoritmo:

# x) MAIN: Verificar parâmetros de execução
#
# x) COMM: Consultar no servidor quais informações
# devem ser enviadas
#
# x) MAIN: Se necessário (conforme x e x), iniciar modo de coleta de informações
# de hardware
#
# x.1) COMM: Consultar no servidor o nome dos campos de patrimônio
#
# x) SYSINFO: Coletar informações de sistema
#
# - Caso haja alteração, marcar como "updated"
#
# x.1) Rede
# x.2) Hardware
# x.3) Software
#
# x) COMM: Enviar informações se forem novas ou atualizadas
#

import socket 
import logging 
import sys
from sysinfo import network
from sysinfo import services
from comm import http

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

a = network.interfaces()
s = services.smb()

# COMM'unication test.
# It could be a good idea to use the key names for the variable names too,
# like 'te_node_address' : te_node_address, and use a map to build the dict.

# Guido doesn't like extra spaces to align variables list, but I don't care!!!

info =  {
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
 }

# Desculpe colocar os imports fora de ordem, mas é só pra organizar os testes

helloCACIC = http

print helloCACIC.formatInfo(info)

# get_config cria a maquina, set_tcp_ip manda infos
#helloCACIC.putFormatedInfo(info,'cacic','cacic2/ws/get_config.php')
#helloCACIC.putFormatedInfo(info,'cacic','cacic2/ws/set_tcp_ip.php')

