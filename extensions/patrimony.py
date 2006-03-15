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

"""CACIC extension for patrimony collection
"""
import re

from agent import http

class patrimony:

    labels = {
        'te_etiqueta1' : '',
	'te_help_etiqueta1' : '',
        'te_etiqueta2' : '',
	'te_help_etiqueta2' : '',
        'te_etiqueta3' : '', 
	'te_help_etiqueta3' : '',
        'te_etiqueta4' : '',
	'te_help_etiqueta4' : '',
        'te_etiqueta5' : '',
	'te_help_etiqueta5' : '',
        'te_etiqueta6' : '',
	'te_help_etiqueta6' : '',
        'te_etiqueta7' : '',
	'te_help_etiqueta7' : '',
        'te_etiqueta8' : '',
	'te_help_etiqueta8' : '',
        'te_etiqueta9' : '',
	'te_help_etiqueta9' : '', }

    def __init__(self):
	self.labels_xml = self.get_labels_xml()
	self.labels = self.get_labels(self.labels_xml)


    def get_labels_xml(self):
	labels_xml = http.get_info('cacic',
	    'cacic2/ws/get_patrimonio.php?tipo=config')
	return labels_xml

    def get_uon1_xml(self):
	uon1_xml = http.get_info('cacic', 
	'cacic2/ws/get_patrimonio.php?tipo=itens_uon1')
	return uon1_xml

    def get_labels(self, labels_xml):
	#labels_xml.replace('<STATUS>OK<\/STATUS>','')

	l = {}
	for k in self.labels.keys():
	    s = '<' + k + '>(?P<value>[^<]*)<\/' + k + '>'
	    m = re.compile(s,re.I|re.M)
            p = m.search(labels_xml)

	    value = ''
	    try:
		value = p.group('value')
	    except:
		pass
	    l[k] = value 

	return l
