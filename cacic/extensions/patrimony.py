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

from cacic.agent import http

class patrimony:

    uon1 = {}
	uon2 = {}

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
	self.labels = self._get_labels()
	self.uon1 = self._get_uon1()
	self.uon2 = self._get_uon2()

    def _get_patr_xml(self, info):
	patr_xml = http.get_info('cacic',
	    'cacic2/ws/get_patrimonio.php?tipo=' + info)
	return patr_xml

    def _get_labels(self):
	labels_xml = self._get_patr_xml('config')
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

    def _get_uon1(self):

	uon1_xml = self._get_patr_xml('itens_uon1')

	uon1_list = uon1_xml.split('<ITEM>')

	uon1 = {}

	for item in uon1_list:
	    s = '<ID1>(?P<id>\d+)<\/ID1><VALOR>(?P<valor>[^>]+)<\/VALOR><\/ITEM>'
	    m = re.compile(s,re.I|re.M)
	    p = m.search(item)
	    id = ''
	    value = ''
	    try:
		value = p.group('valor')
	    except:
		continue	
	    try:
		id = p.group('id')
	    except:
		continue

	    uon1[id]=value

	return uon1

    def _get_uon2(self):

	uon2_xml = self._get_patr_xml('itens_uon2')

	uon2_list = uon2_xml.split('<ITEM>')

	uon2 = {}

	for item in uon2_list:
	    s = '<ID1>(?P<id1>\d+)<\/ID1><ID2>(?P<id2>\d+)<\/ID2><VALOR>(?P<valor>[^>]+)<\/VALOR><\/ITEM>'
	    m = re.compile(s,re.I|re.M)
	    p = m.search(item)
	    id1 = ''
	    id2 = ''
	    value = ''
	    try:
		value = p.group('id2')
	    except:
		continue	
	    try:
		id1 = p.group('id1')
	    except:
		continue

	    try:
		id2 = p.group('id2')
	    except:
		continue

	    try:
		value = p.group('valor')
	    except:
		continue

	    if not uon2.has_key(id1):
		uon2[id1] = {}
	    
	    uon2[id1][id2]=value  

	return uon2
    
    def	ask(self, label):
	
	for k, v in self.uon1.iteritems():
	    
	    print v

