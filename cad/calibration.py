#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 16

base_size = 18

def block(h):
    c = translate([-base_size/2, -h/2, 0])(cube([base_size, h, base_size]))
    label = translate([0, -1, base_size/2])(rotate([90, 0, 0])(
        linear_extrude(height=3)(text(str(h), halign='center', valign='center', size=6))))
    return c-label

def assembly():
    # b1 = block(10)
    # b2 = block(12)
    # b3 = block(14)
    # b4 = block(8)
    b1 = block(6)
    b2 = block(4)
    b3 = block(2)
    d = 12
    return translate([-d, -d, 0])(b1) + translate([d, -d, 0])(b2) + translate([d, d, 0])(b3)

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a, file_header='$fn = %s;' % SEGMENTS, include_orig_code=False)
