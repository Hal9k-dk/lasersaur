#! /usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import division
import os
import sys
import re

# Assumes SolidPython is in site-packages or elsewhwere in sys.path
from solid import *
from solid.utils import *

SEGMENTS = 32

card_pocket_w = 54
card_pocket_h = 50
card_pocket_d = 2

fob_pocket_inside_dia = 35
fob_pocket_inside_h = 6.5
fob_pocket_inside_radius = 1
fob_pocket_thickness = 2
fob_pocket_displacement = 10
epsilon = 0.001

step = 3

def fob_hole():
    s = sphere(1)
    cyl = cylinder(fob_pocket_inside_dia/2, fob_pocket_inside_h-2*fob_pocket_inside_radius)
    rounded_cyl = minkowski()(cyl, s)
    return rounded_cyl

def fob_cuts():
    # remove top half of fob pocket
    fob_cut1 = translate([-card_pocket_w/2, 
                          -fob_pocket_inside_dia, 
                          -(fob_pocket_inside_h*2+2*fob_pocket_thickness+2)/2])(
                              cube([card_pocket_w+2,
                                    fob_pocket_inside_dia, 
                                    fob_pocket_inside_h*4]))
    cw = card_pocket_w + 3
    fob_cut2 = translate([-cw/2-1, -card_pocket_h-3, -10])(
        cube([cw+2, card_pocket_h*2+step*2, 10]))
    return fob_cut1+fob_cut2

def card_pocket():
    return down(1)(back(1)(left(card_pocket_w/2)(cube([card_pocket_w, 
                                                       card_pocket_h+1, 
                                                       card_pocket_d+1]))))

def half_sphere(r):
    return rotate([-90, 0, 0])(difference()(sphere(r), 
                                            down(r)(left(r)(cube([r*2,r*2,r*2])))))

def half_cylinder(r):
    return rotate([-90, 0, 0])(difference()(cylinder(r,r), 
                                            down(r-1)(left(r)(cube([r*2,r*2,r*2])))))

def card_cover():
    d = 3
    r = 4
    h = 10
    card_cover_w = card_pocket_w + 2*d + 2*step
    card_cover_d = card_pocket_d+d
    
    left_s = translate([card_cover_w/2-r, card_pocket_h+step-1, card_cover_d])(half_sphere(r))
    right_s = translate([-(card_cover_w/2-r), card_pocket_h+step-1, card_cover_d])(half_sphere(r))

    left_c = translate([card_cover_w/2-r, 0, card_cover_d])(half_cylinder(r))
    right_c = translate([-(card_cover_w/2-r), 0, card_cover_d])(half_cylinder(r))
    w2 = card_cover_w

    left_bc = translate([-w2/2 + r, card_pocket_h-step+d + 2, -h+epsilon])(cylinder(r = r, h = h+card_cover_d))
    right_bc = translate([w2/2 - r, card_pocket_h-step+d + 2, -h+epsilon])(cylinder(r = r, h = h+card_cover_d))
    left_bcu = translate([-w2/2, -step+d, -h+epsilon])(cube([r, r, h+card_cover_d]))
    right_bcu = translate([w2/2 - r, -step+d, -h+epsilon])(cube([r, r, h+card_cover_d]))
    brim = hull()(left_bcu + right_bcu + left_bc + right_bc)

    return hull()(left_c+right_c+left_s+right_s) + brim

def screw_hole(invert):
    cone = cylinder(r1=1.6, r2=3, h=2.3)
    offset = 10
    if invert:
        cone = rotate([180, 0, 0])(cone)
        offset = 0
    return left(5)(rotate([90, 0, 90])(cylinder(r=1.6, h = 10) + translate([0, 0, offset])(cone)))

def assembly():
    fh1 = fob_hole()
    fh2 = translate([0, fob_pocket_displacement, 0])(fh1)
    fh = hull()(fh1+fh2)
    fc = fob_cuts()
    cp = card_pocket()
    cc = card_cover()

    sh_x = 26
    sh_dist = 35
    sh_offset = 25
    sh_z = -5
    sh1 = translate([-sh_x, sh_offset - sh_dist/2, sh_z])(screw_hole(True))
    sh2 = translate([-sh_x, sh_offset + sh_dist/2, sh_z])(screw_hole(True))
    sh3 = translate([sh_x, sh_offset - sh_dist/2, sh_z])(screw_hole(False))
    sh4 = translate([sh_x, sh_offset + sh_dist/2, sh_z])(screw_hole(False))
    screwholes = sh1 + sh2 + sh3 + sh4
    
    return cc-fh-cp-fc - screwholes

if __name__ == '__main__':
    a = assembly()
    scad_render_to_file(a, file_header='$fn = %s;' % SEGMENTS, include_orig_code=False)
