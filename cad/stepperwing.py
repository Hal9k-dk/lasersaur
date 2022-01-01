#! /usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import os, sys, re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 48

hole_dia = 5
width = 8
len = 30
th = 5

def assembly():
    cyl = cylinder(h = th, d = width)
    b = hull()(left(len)(cyl) + cyl)
    h = down(1)(cylinder(h = th+2, d = hole_dia))
    return b - h

if __name__ == '__main__':
    a = assembly()    
    scad_render_to_file( a, file_header='$fn = %s;'%SEGMENTS, include_orig_code=True)
