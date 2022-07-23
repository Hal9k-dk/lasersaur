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

case_w = 59
case_h = 53
case_w2 = case_w + 6
case_h2 = case_h + 6
case_d1 = 13
case_d2 = 15
case_th = 2
coil_sup_l = 3
coil_sup_d = 3
# Inner diameter of coil
coil_sup_w = 43
coil_sup_h = 31
e = 0.001

def coil_sup():
    return cylinder(coil_sup_d/2, coil_sup_l)

def coil_sups():
    s1 = translate([-(coil_sup_w-coil_sup_d)/2, -(coil_sup_h-coil_sup_d)/2, 0])(coil_sup())
    s2 = translate([(coil_sup_w-coil_sup_d)/2, -(coil_sup_h-coil_sup_d)/2, 0])(coil_sup())
    s3 = translate([(coil_sup_w-coil_sup_d)/2, (coil_sup_h-coil_sup_d)/2, 0])(coil_sup())
    s4 = translate([-(coil_sup_w-coil_sup_d)/2, (coil_sup_h-coil_sup_d*2)/2, 0])(coil_sup())
    return s1+s2+s3+s4

def bottom():
    return translate([-case_w/2, -case_h/2, 0])(cube([case_w, case_h, case_th]))

# The part that fits into the pocket part
def frame1():
    outer = translate([-case_w/2, -case_h/2, case_th])(cube([case_w, case_h, case_d1]))
    iw = case_w-2*case_th
    ih = case_h-2*case_th
    inner = translate([-iw/2, -ih/2, case_th])(cube([iw, ih, case_d1+1]))
    return outer-inner

def frame2():
    outer = translate([-case_w2/2, -case_h2/2, case_th])(cube([case_w2, case_h2, case_d2]))
    iw = case_w-2*case_th
    ih = case_h-2*case_th
    inner = translate([-iw/2, -ih/2, case_th])(cube([iw, ih, case_d2+1]))
    return outer-inner

def frame3():
    h = 10
    ow = case_w-2*case_th
    oh = case_h-2*case_th
    outer = translate([-(ow+e)/2, -(oh+e)/2, 0])(cube([ow+e, oh+e, h]))
    iw = ow - 4
    ih = oh
    inner = translate([-iw/2, -ih/2, -1])(cube([iw, ih, h+2]))
    return outer-inner

def screw_support():
    return cylinder(5, 4)

switch_offset = -22

def switch_hole():
    flap_hole = cube([5, 18, 5])
    sw_w = 6.25
    return translate([-sw_w/2, switch_offset, -0.5])(cube([sw_w, 24, 10]) +
                                    translate([.5, 3, -4.5])(flap_hole))

def switch_mount():
    return translate([-5, switch_offset+5, 1])(cube([10, 15, 8]))

def screw_hole():
    return up(case_d1 + case_d2 - 5)(left(5)(rotate([90, 0, 90])(cylinder(r=1.5, h = 10))))

def front_screw_hole(invert):
    th = 1
    offset = 8.5-th
    if invert:
        offset = 6.5+th
    return left(10)(rotate([90, 0, 90])(cylinder(d=3.2, h = 20) +
                                        translate([0, 0, offset])(cylinder(d=4.5, h = 5))))

def assembly():
    bt = bottom()
    cs = up(case_th)(forward(switch_offset/2+5)(coil_sups()))
    fr1 = frame1()
    fr2 = up(case_d1-0.1)(frame2())
    fr3 = frame3()

    swm = switch_mount()
    swh = switch_hole()
    sh1 = translate([-case_w/2, -15, 0])(screw_hole())
    sh2 = translate([-case_w/2, 15, 0])(screw_hole())
    sh3 = translate([case_w/2, -15, 0])(screw_hole())
    sh4 = translate([case_w/2, 15, 0])(screw_hole())

    # Front screw holes (for inserts)
    fsh_x = 26
    fsh_dist = 35
    fsh_offset = -1
    fsh_z = 5
    fsh1 = translate([-fsh_x, fsh_offset - fsh_dist/2, fsh_z])(front_screw_hole(True))
    fsh2 = translate([-fsh_x, fsh_offset + fsh_dist/2, fsh_z])(front_screw_hole(True))
    fsh3 = translate([fsh_x, fsh_offset - fsh_dist/2, fsh_z])(front_screw_hole(False))
    fsh4 = translate([fsh_x, fsh_offset + fsh_dist/2, fsh_z])(front_screw_hole(False))
    fscrewholes = fsh1 + fsh2 + fsh3 + fsh4

    return cs + fr1 + fr2 + fr3 + bt + translate([0, 0, 0])(swm) - translate([0, 0, 1])(swh) - sh1 - sh2 - sh3 - sh4 - fscrewholes

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a, file_header='$fn = %s;' % SEGMENTS, include_orig_code=False)
