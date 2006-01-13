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

"""Provides methods to communicate with the CACIC web server using HTTP

It tries to follow the recommendations of diveintopython[1], including:
- Compression
- User-agents

[1] http://diveintopython.org/http_web_services/http_features.html
"""

import urllib2
import httplib
import base64
import logging

logger = logging.getLogger("cacic.agent.http")

def post_info(putinfo,server,path):
    """Send pre-formated 'putinfo' string  to the 'destination' in the http server
    """
    #FIXME: quebrar essa função em outras

    logger.debug("Posting info to the CACIC server")
    debug = urllib2.HTTPHandler()

    url = 'http://' + server + '/' + path

    #FIXME: isso deve ser configuravel
    base64string = base64.encodestring('%s:%s' % ('USER_CACIC', 'PW_CACIC'))[:-1]

    logger.debug("Building request object")
    request = urllib2.Request(url) 
    request.add_header('User-Agent', 'AGENTE_CACIC')   
    request.add_header('Pragma', 'no-cache')   
    request.add_header('Accept-encoding', 'gzip')  

    request.add_header("Authorization", "Basic %s" % base64string)

    request.add_data(formatInfo(putinfo))
#   Método não funcionou, assim como http://user:pass@server
#   authinfo = urllib2.HTTPPasswordMgrWithDefaultRealm()

#   authinfo.add_password(None, 'cacic', 'USER_CACIC', 'PW_CACIC')

    opener = urllib2.build_opener(debug) # +authinfo

    logger.debug("POSTing request to the server")
    f = opener.open(request)

    #FIXME: criar funcao para "handledata"
    if f.headers.get('Content-Encoding') == 'gzip':
        import StringIO
        compresseddata = f.read()
        compressedstream = StringIO.StringIO(compresseddata)
        import gzip
        gzipper = gzip.GzipFile(fileobj=compressedstream)  
        feeddata = gzipper.read()  
    else:
        feeddata = opener.open(request).read()
    
#    print feeddata

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

    #print x
    te_ip=10.68.8.195&te_node_address=00-0D-60-E0-A6-3C&id_ip_rede=10.68.8.0&\
    id_so=8&te_nome_computador=INF24GO&te_versao_cacic=2.0.0.23&
    """

    info_string = ''

    for key, value in info_dict.iteritems():
        info_string += key + '=' + value + '&'

    return info_string
        
