#!/usr/bin/python
"""   
desc:  Setup script for 'pymusic' package.
auth:  Craig Wm. Versek (cversek@physics.umass.edu)
date:  7/12/2009
notes: install with "sudo python setup.py install"
"""

from ez_setup import use_setuptools
use_setuptools()

from setuptools import setup, find_packages

###############################################################################
# run the setup script

setup(
      #metadata
      name         = "pymusic",
      version      = "0.1dev",
      author       = "Craig Versek",
      author_email = "cversek@physics.umass.edu",

      #packages to install
      package_dir  = {'':'src'},
      packages     = find_packages('src'),
      
      #non-code files
      package_data     =   {'': ['*.sng']},

)
