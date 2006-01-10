#!/usr/bin/env python
# -*- coding: utf-8 -*-
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

import agent
import agent.config

import logging

logger = logging.getLogger("cacic")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - \
%(message)s")
ch.setFormatter(formatter)
logger.addHandler(ch)
logger.debug("debug message")
logger.info("info message")
logger.warn("warn message")
logger.error("error message")
logger.critical("critical message")

logger.debug("Loading agent.http")

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

