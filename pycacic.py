#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Atualmente utilizado apenas para testar módulos
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

from sysinfo import network

a = network.interfaces()

print "MAC:", a.mac_address('eth0')

print "STATUS:",a.getStatus('eth0')

print "IP:",a.getIpAddress('eth0')

print "Rede:",a.getNetwork('eth0')

print "Hostname:",a.hostname()

print "Default Gateway:",a.getDefaultGateway()

print "DHCP Server:",a.getDHCPServer('eth0')


# Teste do COMM:
info = {
 'te_node_address'          : a.mac_address('eth0'),
 'id_so'                    : '8',
 'id_ip_rede'               : a.getNetwork('eth0'),
 'te_nome_computador'       : a.hostname(),
 'te_ip'                    : a.getIpAddress('eth0'),
 'te_versao_cacic'          : 'pyc',
 'te_mascara'               : a.getNetmask('eth0'),
 'te_gateway'               : a.getDefaultGateway(),
 'te_serv_dhcp'             : a.getDHCPServer('eth0'),
 'te_nome_host'             : a.hostname(),
 'te_origem_mac'            : 'ifconfig'

}

# Desculpe colocar os imports fora de ordem, mas é só pra organizar os testes
from comm import http

format = http

print format.formatInfo(info)


# Original em Perl:
# set_tcp_ip
#        te_node_address => $info{'te_node_address'},
#        id_so           => $linux_id,
#        id_ip_rede => $request{'CONTENT'}{'NETWORKS'}[$interface]{'NETWORK'}[0],
#        te_nome_computador => $Device,
#        te_ip => $request{'CONTENT'}{'NETWORKS'}[$interface]{'IPADDRESS'}[0],
#        te_mascara => $request{'CONTENT'}{'NETWORKS'}[$interface]{'IPMASK'}[0],
#        te_gateway =>
#          $request{'CONTENT'}{'NETWORKS'}[$interface]{'IPGATEWAY'}[0],
#        te_serv_dhcp =>
#          $request{'CONTENT'}{'NETWORKS'}[$interface]{'IPDHCP'}[0],
#        te_dns_primario =>
#          $request{'CONTENT'}{'NETWORKS'}[$interface]{'RESOLVER1'}[0],
#        te_dns_secundario =>
#          $request{'CONTENT'}{'NETWORKS'}[$interface]{'RESOLVER2'}[0],
#        te_wins_primario   => '',
#        te_wins_secundario => '',
#        te_nome_host       => $Device,
#        te_dominio_dns     =>
#         $request{'CONTENT'}{'NETWORKS'}[$interface]{'DNSDOMAIN'}[0],
#       te_origem_mac      => "ifconfig",
#       te_dominio_windows => '',

