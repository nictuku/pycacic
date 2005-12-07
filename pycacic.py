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

from sysinfo import network
from sysinfo import services
#try: 
a = network.interfaces()
#except:
#    raise 'Off'

print "MAC:", a.getMacAddress('eth0')

print "STATUS:",a.getStatus('eth0')

print "IP:",a.getIpAddress('eth0')

print "Rede:",a.getNetwork('eth0')

print "Hostname:",a.hostname()

print "Default Gateway:",a.getDefaultGateway()

print "DHCP Server:",a.getDHCPServer('eth0')

a.getDNSDomain()
a.getDNSResolvers()
# This seems to be the proper way to handle errors from data collection methods.
try:
    domain = a.getDNSDomain()
except:
    domain = ''
    logging.error('Erro ao consultar domain')
else:
    print "DNS Domain:",domain

try:
    resolvers = a.getDNSResolvers()
except:
    resolvers = [ '', '' ]
    logging.error('Erro ao consultar resolvers')
else:
    print "Resolvers:", resolvers

s = services.smb()

s.getWorkgroup()

s.getWinsServers()
#a.getSambaWorkgroup()

# COMM'unication test.
# It could be a good idea to use the key names for the variable names too,
# like 'te_node_address' : te_node_address, and use a map to build the dict.

info =  {
 'te_node_address'          : a.getMacAddress('eth0'),
 'id_so'                    : '0',
 'id_ip_rede'               : a.getNetwork('eth0'),
 'te_nome_computador'       : a.hostname(),
 'te_ip'                    : a.getIpAddress('eth0'),
 'te_versao_cacic'          : 'pyc',
 'te_mascara'               : a.getNetmask('eth0'),
 'te_gateway'               : a.getDefaultGateway(),
 'te_serv_dhcp'             : a.getDHCPServer('eth0'),
 'te_nome_host'             : a.hostname(),
 'te_origem_mac'            : 'ifconfig',
 'te_dns_primario'          : resolvers[0],
 'te_dns_secundario'        : resolvers[1],
 'te_dominio_dns'           : domain

}

# Desculpe colocar os imports fora de ordem, mas é só pra organizar os testes
from comm import http

helloCACIC = http

print helloCACIC.formatInfo(info)

# get_config cria a maquina, set_tcp_ip manda infos
#helloCACIC.putFormatedInfo(info,'cacic','cacic2/ws/get_config.php')
#helloCACIC.putFormatedInfo(info,'cacic','cacic2/ws/set_tcp_ip.php')

