from build123d import *
from ocp_vscode import *

axle_d = 5
bearing_od = 7
od = 8
th = 4.2
crush_dia = 1

with BuildPart() as p:
    # main body
    with BuildSketch():
        Circle(od/2)
    extrude(amount=th - (od - bearing_od))
    # conical part
    with BuildSketch(p.faces().group_by(Axis.Z)[0][0]):
        Circle(od/2)
    with BuildSketch(p.faces().group_by(Axis.Z)[0][0].offset(od - bearing_od)):
        Circle(bearing_od/2)
    loft()
    # through hole
    with BuildSketch(p.faces().group_by(Axis.Z)[0][0]):
        Circle(axle_d/2 + 0.1)
    extrude(amount=-th, mode=Mode.SUBTRACT)
    # crush ribs
    with BuildSketch(p.faces().sort_by(Axis.Z)[-1]):
        with PolarLocations(radius=axle_d/2 + crush_dia/2, count=4):
            Circle(crush_dia/2)
    extrude(amount=-th)

    
show(p)

export_step(p.part, 'idlerspacer.step')
