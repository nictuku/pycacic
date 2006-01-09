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
        # FIXME: hmm what's the string for CD reader?
        for element in ['CPU', 'BIOS', 'System Memory', 'Motherboard', 'VGA compatible controller', 
                'Multimedia audio controller', 'DVD-RAM writer', 'DVD reader', 'Modem' ,'Mouse',
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


class get_hardware:
 
    data = {}

    def __init__(self):
        parser = make_parser()
        handler = LshwDataParser()
        parser.setContentHandler(handler)
        logging.warning("Calling lshw")
        lshwxml = commands.getstatusoutput("export LANGUAGE=C; /usr/sbin/lshw -xml 2>&1|grep -v WARNING")
        logging.warning("Done with lshw")
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



class motherboard:
    product = ''
    vendor = ''

    def __init__(self, hw, index=0):
        if hw.data.has_key('Motherboard'):
            self.product = hw.data['Motherboard'][index].get('product', '')
            self.vendor = hw.data['Motherboard'][index].get('vendor', '')


class memory:
    size = ''

    def __init__(self, hw):
        if hw.data.has_key('System Memory'):
            self.size = hw.data['System Memory'][0].get('size', '')

class mouse:
    product = ''
    vendor = ''

    def __init__(self, hw, index=0):
        if hw.data.has_key('Mouse'):
            self.product = hw.data['Mouse'][index].get('product', '')
            self.vendor = hw.data['Mouse'][index].get('vendor', '')


class modem:
    product = ''
    vendor = ''

    def __init__(self, hw, index=0):
        if hw.data.has_key('Modem'):
            self.product = hw.data['Modem'][index].get('product', '')
            self.vendor = hw.data['Modem'][index].get('vendor', '')

class dvd_reader:
    product = ''
    
    def __init__(self, hw, index=0):
        if hw.data.has_key('DVD reader'):
            self.product = hw.data['DVD reader'][index].get('product', '')

class dvd_ram_writer:
    product = ''
    serial = ''
    version = ''
    
    def __init__(self, hw, index=0):
        if hw.data.has_key('DVD-RAM writer'):
            self.product = hw.data['DVD-RAM writer'][index].get('product', '')
            self.serial = hw.data['DVD-RAM writer'][index].get('serial', '')
            self.version = hw.data['DVD-RAM writer'][index].get('version', '')

class bios:
    product = ''
    vendor = ''
    version = ''
    
    def __init__(self, hw):
        if hw.data.has_key('BIOS'):
            self.product = hw.data['BIOS'][0].get('product', '')
            self.vendor = hw.data['BIOS'][0].get('vendor', '')
            self.version = hw.data['BIOS'][0].get('version', '')



class video_board:
    product = ''
    vendor = ''
    memory = ''
    width = ''
    
    def __init__(self, hw, index=0):
        if hw.data.has_key('VGA compatible controller'):
            self.product = hw.data['VGA compatible controller'][index].get('product')
            self.memory = hw.data['VGA compatible controller'][index].get('size')
            self.width = hw.data['VGA compatible controller'][index].get('width')
            self.vendor = hw.data['VGA compatible controller'][index].get('vendor')

class sound_board:
    product = ''
    
    def __init__(self, hw, index=0):
        if hw.data.has_key('Multimedia audio controller'):
            self.product = hw.data['Multimedia audio controller'][index].get('product')

class ethernet_board:
    product = ''
    width = ''
    version = ''
    vendor = ''
    serial = ''

    def __init__(self, hw, index=0):
        if hw.data.has_key('Ethernet interface'):
            self.product = hw.data['Ethernet interface'][index].get('product', '')
            self.width = hw.data['Ethernet interface'][index].get('width', '')
            self.vendor = hw.data['Ethernet interface'][index].get('vendor', '')
            self.version = hw.data['Ethernet interface'][index].get('version', '')
            self.serial = hw.data['Ethernet interface'][index].get('serial', '')
       
class cpu:
    product = ''
    vendor = ''
    frequency = ''
    serial = ''
    
    def __init__(self, hw, index=0):
        if hw.data.has_key('CPU'):
            self.product = hw.data['CPU'][index].get('product', '')
            self.vendor = hw.data['CPU'][index].get('vendor', '')
            self.frequency = hw.data['CPU'][index].get('size', '')

class hardware:
    """This is the interfaced accessed by the user. It provides
    hardware data collected through get_hardware.
    """
    # FIXME: motherboard, cpu, etc need support to multiple values. Currently
    # uses index=0

    # Tá certo iniciar o objeto assim, com string em branco? Ele nao vai ser string
    hw = ''
    motherboard = ''
    cpu = ''
    ethernet_board = ''
    video_board = ''
    sound_board = ''
    bios = ''
    dvd_reader = ''
    modem = ''
    mouse = ''
    memory = ''
    
    def __init__(self):
        self.hw = get_hardware()
        self.motherboard = motherboard(self.hw, 0)
        self.cpu = cpu(self.hw, 0)
        self.ethernet_board = ethernet_board(self.hw, 0)
        self.video_board = video_board(self.hw, 0)
        self.sound_board = sound_board(self.hw, 0)
        self.bios = bios(self.hw) # BIOS is always index=0
        self.dvd_reader = dvd_reader(self.hw, 0)
        self.modem = modem(self.hw, 0)
        self.mouse = mouse(self.hw, 0)
        self.memory = memory(self.hw)

if __name__ == '__main__':
#    a = get_hardware()
#    print a.data
    x = hardware()
    y = x.motherboard
    print "h", x.motherboard.vendor, x.ethernet_board.product, x.video_board.product, x.video_board.vendor,\
        x.dvd_reader.product, x.memory.size
