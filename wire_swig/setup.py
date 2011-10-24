#!/usr/bin/env python
#
# setup.py for WIRE

from distutils.core import setup, Extension

import os
import re

def get_libs(cmdline):
    s = os.popen(cmdline).read()
    return re.findall(r'-l(\w+)', s)

def get_includes(cmdline):
    s = os.popen(cmdline).read()
    return re.findall(r'-I([\w/]+)', s)

home_dir = "/home/egraells/proyectos/cpp"
wire_dir = home_dir + "/WIRE-0.22"

include_dirs =  get_includes("xml2-config --cflags")
include_dirs.append( home_dir )
include_dirs.append( wire_dir )
include_dirs.append( wire_dir + "/lib" )
include_dirs.append( wire_dir + "/bot" )
include_dirs.append( wire_dir + "/search" )
include_dirs.append( wire_dir + "/wirudiko" )
include_dirs.append( wire_dir + "/universalchardet" )

library_dirs = []
library_dirs.append( wire_dir + "/lib" )
library_dirs.append( wire_dir + "/universalchardet" )
library_dirs.append( wire_dir + "/bot" )
library_dirs.append( wire_dir + "/search" )
library_dirs.append( wire_dir + "/wirudiko" )

module1 = Extension('_Wire',
                    sources = ['Wire.i'],
                    include_dirs = include_dirs,
		    library_dirs = library_dirs,
                    libraries = [] + ['wire', 'univchardet', 'wirudiko', 'stdc++'] + get_libs('xml2-config --libs'),
		    swig_opts = ['-c++'])
                    

setup(
    name = "Wire",
    version = "0.22",
    py_modules = ['Wire'],
    description = "Wrapper for WIRE, an implementation of Web crawler",
    ext_modules = [module1,])
