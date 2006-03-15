#!/usr/bin/env python
from distutils.core import setup
setup(name='PyCACIC',
      version='0.3',
      description='Multi-platform client for CACIC',
      author='Yves Junqueira',
      author_email='yves@cetico.org',
      maintainer='Yves Junqueira',
      maintainer_email='yves@cetico.org',
      url='https://opensvn.csie.org/traccgi/pycacic',
      scripts=['pycacic'],
#      package_dir = {'nwu_agent': 'nwu-agent/nwu_agent', 
	    #'nwu_server': 'nwu-server/nwu_server'},
      packages=['cacic', 'cacic.agent', 'cacic.extensions', 
	'sysinfo', 'sysinfo.linux'],
#      data_files=[('/etc/nwu', ['nwu-agent/sample_conf/agent.conf'])]
     )
