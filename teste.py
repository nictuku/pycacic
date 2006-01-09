#!/usr/bin/env python
# -*- coding: utf-8 -*-

import comm

helloCACIC = comm.http
info = comm.info
#print "hw:", hw.__dict__
# get_config cria a maquina, set_tcp_ip manda infos

helloCACIC.putFormatedInfo(info,'cacic','cacic2/ws/get_config.php')
helloCACIC.putFormatedInfo(info,'cacic','cacic2/ws/set_tcp_ip.php')
helloCACIC.putFormatedInfo(info,'cacic','cacic2/ws/set_hardware.php')


print "weee, foi"
