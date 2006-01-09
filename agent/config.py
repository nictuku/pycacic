#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Gestor de configurações do CACIC.
"""

import re
import urllib2
import httplib
import base64
import logging

import http

def parse_remote_raw_cfg(cfg, cfg_regex, remote_raw_cfg, mode):
    x = re.compile(cfg_regex, re.I)
    w = x.search(remote_raw_cfg)

    if w:
        if mode == 'boolean':
            return True

        elif mode == 'string':
            setting = w.groups('mac_invalidos')
            return setting
    else:
        logging.warning("Could not find the configuration respective to " + cfg + " in the server")
        return False

def get_config(data):
    """Consulta no servidor a atual configuração da rede atual
    "data" deve ser um dicionário contendo certas informações
    essenciais ao ws/get_config.php
    """
    if type(data) is not dict:
        logging.error("get_config needs a dict argument")
        raise Exception, "get_config requires a dict argument"
        return ''
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
    request.add_data(http.formatInfo(data))
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
