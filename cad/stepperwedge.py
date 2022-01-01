#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import os, sys, re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

th = 4

def assembly():
    r = 11
    cyl = cylinder(h = th, d = 2*r)
    w = 30
    b = translate([-w/2, -r + 2.5, -1])(cube([w, w, th+2]))
    return cyl - b

if __name__ == '__main__':
    a = assembly()    
    scad_render_to_file( a, file_header='$fn = %s;'%SEGMENTS, include_orig_code=True)
