from build123d import *
from ocp_vscode import *
from defs import *

th = 3
height = 15
width = 40
depth = 60
valve_dia = 25
valve_len = 30
valve_h = 3
hole_cc = 20
y_offset = -20

bottom = (Align.CENTER, Align.CENTER, Align.MIN)

with BuildPart() as p:
    # base
    with BuildSketch():
        RectangleRounded(width, depth, 3)
    extrude(amount=th)
    e = p.edges().sort_by(Axis.Z)
    fillet([ e[-1] ], radius=1)    
    # mounting holes
    with BuildSketch(p.faces().sort_by(Axis.Z)[-1]) as sk:
        with Locations([(hole_cc/2, y_offset),
                        (-hole_cc/2, y_offset)]):
            Circle(radius=5.5/2)
    extrude(amount=-20, mode=Mode.SUBTRACT)
    # valve support
    with BuildSketch(p.faces().sort_by(Axis.Z)[-1]) as sk:
        with Locations((0, 10)):
            Rectangle(valve_dia - 5, valve_len)
    extrude(amount=valve_h + 5)
    # cutout
    with BuildSketch(p.faces().sort_by(Axis.Y)[0]) as sk:
        with Locations((0, th + valve_h + valve_dia/2)):
            Circle(valve_dia/2)
    extrude(amount=-depth, mode=Mode.SUBTRACT)
    
show(p)

export_step(p.part, 'valvemount.step')
