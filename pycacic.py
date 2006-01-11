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

"""Atualmente utilizado apenas para testar módulos e testar
metodologias e estruturas.
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


import logging

format = "%(asctime)s cacic[%(process)d] %(levelname)s %(name)s:%(lineno)d: %(message)s"
#format = "%(asctime)s %(levelname)s %(message)s"

logger = logging.getLogger("cacic")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(format)
ch.setFormatter(formatter)
logger.addHandler(ch)

sysinfo_logger = logging.getLogger("sysinfo")
sysinfo_logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter(format)
ch.setFormatter(formatter)
sysinfo_logger.addHandler(ch)
  

logger.info("Starting PyCACIC.")
logger.debug("Loading agent.http")

import agent
import agent.config


helloCACIC = agent.http

logger.debug("Loading agent.config.load()")
cacic = agent.config.load()
info = cacic.info
#print "hw:", hw.__dict__
# get_config cria a maquina, set_tcp_ip manda infos

logger.info("Getting configuration from the server")
helloCACIC.post_info(info,'cacic','cacic2/ws/get_config.php')
logger.info("Posting network information")
helloCACIC.post_info(info,'cacic','cacic2/ws/set_tcp_ip.php')
logger.info("Posting hardware information")
helloCACIC.post_info(info,'cacic','cacic2/ws/set_hardware.php')

logger.info("Finished execution sucessfuly")

