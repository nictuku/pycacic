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

helloCACIC = agent.http
cacic = agent.config.load()
info = cacic.info
#print "hw:", hw.__dict__
# get_config cria a maquina, set_tcp_ip manda infos

helloCACIC.post_info(info,'cacic','cacic2/ws/get_config.php')
helloCACIC.post_info(info,'cacic','cacic2/ws/set_tcp_ip.php')
helloCACIC.post_info(info,'cacic','cacic2/ws/set_hardware.php')


print "weee, foi"

