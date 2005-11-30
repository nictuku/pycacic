#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Provides methods to communicate with the CACIC web server using HTTP
"""

def putFormatedInfo(self,putinfo,destination):
    """Send pre-formated 'putinfo' string  to the 'destination' in the http server
    """

def formatInfo(self,info_dict):
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

    intro_string = None

    for key, value in info_dict.iteritems():
        info_string += key + '=' + value + '&'

    return info_string
        
