#!/usr/bin/env python
# -*- coding: utf-8 -*-
from xml.sax import ContentHandler
from xml.sax import make_parser
from xml.sax import parseString

import StringIO
import xml.sax

import commands
import logging
import string 
import sys

# FIXME: teste feito em MDS500 mostrou que lshw às vezes gera um XML com caracteres
# estranhos, como ^E^D^D^C

class LSHWRunError(Exception):
    pass

class LshwDataParser(ContentHandler):
    """Parse a XML file that was created using 'lshw -xml'. You need another
    function to parse it and copy the contents of "HardWare". The class
    "HardWare" below does that.
    """

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
        # FIXME: this is returning the WRONG unit
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
            #print "Hey this shouldn't happen.", self.CurrentTag[-1]['name'], tag
            sys.exit(1)

        else:
            self.CurrentTag.pop()
            if tag == 'node':
            # Node closing. We should get all that and store somewhere, then pop it
            # from the self.Nodes list.
                node = self.Nodes[-1]

                if node.has_key('physid') and node.has_key('description'):
                    #print "Physid:", node['physid']
                    #print "Description:", node['description']

                    self.setHardWare(node)

                else:
                    #print "Strange. Node lacks physid and/or description"
                    pass
                    
                if len(self.Nodes) > 1:
         #       print "closing", tag
                    self.Nodes.pop()
    
    def characters(self, ch):

        # This will populate self.Nodes[-1] with relevant data.
        # Not that it would only work for unique data (like physid)
        for x in ['description', 'physid', 'product', 'vendor', 'version', 'size', 'slot', 'width', 'serial']:

            if self.CurrentTag[-1]['name'] == x:
 
                if self.Nodes[-1].has_key(x):
                    self.Nodes[-1][x] += ch
                else:
                    self.Nodes[-1][x] = ch

    def setHardWare(self, node):
        """Argh. This is ugly.
        """

        for element in ['CPU', 'BIOS', 'System Memory', 'Motherboard', 'VGA compatible controller', 
                'Multimedia audio controller', 'DVD reader', 'Modem' ,'Mouse',
                'Ethernet interface']:

            if node['description'] == element:
                if not self.HardWare.has_key(element):
                    self.HardWare[element] = []
    
                self.HardWare[element].append({})
    
                for info in ['product', 'vendor', 'size','version', 'slot', 'width', 'serial']:
                    if node.has_key(info):
                        set = node[info]
                        if info == 'size' and len(self.CurrentTagUnits) > 1:
                           unit = self.CurrentTagUnits
                           set += ' ' + unit
        
                        self.HardWare[element][-1][info] = set


#if __name__ == '__main__':
class HardWare:
 
    data = {}

    def __init__(self):
        parser = make_parser()
        handler = LshwDataParser()
        parser.setContentHandler(handler)

        lshwxml = commands.getstatusoutput("export LANGUAGE=C; /usr/sbin/lshw -xml 2>&1|grep -v WARNING")
        if lshwxml[0] != 0:
            # This would kill this module instance. Should we handle it instead?
            raise LSHWRunError, "could not run /usr/sbin/lshw"
        else:
            xmldata = lshwxml[1]

        #print dir(parser)
        #sys.exit(1)
        #print "="*80
        #print xmldata
        #print "="*80
        input = StringIO.StringIO(xmldata)
        #print "input", input
        parser.parse(input)
#        parser.parse('lshw.xml')

#        parser.parse('lshw.xml')
        self.data = handler.HardWare

if __name__ == '__main__':
#print handler.HardWare['BIOS'][0]['version']
    a = HardWare()
    
    print a.data
    print a.data['BIOS'][0]['version']
