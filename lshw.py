#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.sax import ContentHandler
from xml.sax import make_parser

import logging
import string 
import sys

class LshwDataParser(ContentHandler):

    def __init__(self):
        # List of dicts containing Nodes data
        self.Nodes = []
        # Dict containing current tag data.
        self.CurrentTag = [{}]

        # String with the current tag represented unit, if available.
        self.CurrentTagUnits = ''
        # Dict containing relevant machine data.
        # Every item should support multiple values
        self.HardWare = {}

    def startElement(self, tag, attrs):

        self.CurrentTag.append({'name' : tag })
        # If it has a representation unit, set it.
        try:
            unit = attrs.get('units')
        except:
            self.CurrentTagUnits = ''
        else:
            if unit:
                self.CurrentTagUnits = unit

        if tag == 'node':

            self.Nodes.append({'name' : 'node' })

            # Fill node attributes information
            try:
                nodeclass = attrs.get('class','')
            except:
                pass
            else:
                self.Nodes[-1]['class'] = nodeclass

            try:
                nodehandle = attrs.get('handle','')
            except:
                pass
            else:
                self.Nodes[-1]['handle'] = nodehandle


    def endElement(self, tag):
        
        # sanity test
        if self.CurrentTag[-1]['name'] != tag:
            print "Hey this shouldn't happen.", self.CurrentTag[-1]['name'], tag
            sys.exit(1)

        else:
            self.CurrentTag.pop()
            if tag == 'node':
            # Node closing. We should get all that and store somewhere, then pop it
            # from the self.Nodes list.
                node = self.Nodes[-1]

                if node.has_key('physid') and node.has_key('description'):
                    print "Physid:", node['physid']
                    print "Description:", node['description']

                    self.setHardWare(node)

                else:
                    print "Strange. Node lacks physid and/or description"
                    
                if len(self.Nodes) > 1:
         #       print "closing", tag
                    self.Nodes.pop()
    
    def characters(self, ch):

        # This will populate self.Nodes[-1] with relevant data.
        # Not that it would only work for unique data (like physid)
        for x in ['description', 'physid', 'product', 'vendor', 'version', 'size', 'slot']:

            if self.CurrentTag[-1]['name'] == x:
 
                if self.Nodes[-1].has_key(x):
                    self.Nodes[-1][x] += ch
                else:
                    self.Nodes[-1][x] = ch

    def setHardWare(self, node):
        """Argh. This is ugly.
        """

        for element in ['CPU', 'BIOS', 'System Memory']:

            if node['description'] == element:
                if not self.HardWare.has_key(element):
                    self.HardWare[element] = []
    
                self.HardWare[element].append({})
    
                for info in ['product', 'vendor', 'size','version', 'slot']:
                    if node.has_key(info):
                        set = node[info]
                        if info == 'size' and len(self.CurrentTagUnits) > 1:
                            unit = self.CurrentTagUnits
                            set += ' ' + unit
        
                        self.HardWare[element][-1][info] = set


if __name__ == '__main__':

    parser = make_parser()
    handler = LshwDataParser()
    parser.setContentHandler(handler)
    parser.parse('lshw.xml')

    print handler.HardWare
#    print handler.__dict__


