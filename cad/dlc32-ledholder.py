# %%
from build123d import *
from ocp_vscode import *

# LED holes
led_dia = 5.05
led_cc = 8.47
led_depth = 7.5
led_offset = -3
fiber_dia = 2.8
# Screw holes
hole_cc = 58.7 - 33.2486
hole_dia = 3.2
hole_x_offset = led_cc/2 + led_offset
hole_y_offset = -3.5
# Overall
depth = led_depth + 5
plate_depth = 15
block_th = 1
plate_th = 2

block_l = hole_cc + 1.5*led_cc
block_w = depth
block_h = led_dia + 2*block_th

def offset(loc):
    p = loc.position
    p.Y = p.Y + led_offset
    loc.position = p
    return loc
    
with BuildPart() as ex11:
    # basic shape
    Box(block_l, block_w, block_h, align=Align.MIN)
    #fillet(ex11.edges().sort_by(Axis.Z)[-1], radius=0.9)
    # LED holes
    with BuildSketch(ex11.faces().sort_by(Axis.Y)[-1]) as ex11_sk:
        locs = GridLocations(1, led_cc, 1, 4).local_locations
        for loc in locs:
            with Locations(offset(loc)):
                Circle(radius=led_dia/2)
    extrude(amount=-led_depth, mode=Mode.SUBTRACT)
    # fiber holes
    led_offset = -led_cc/2 # weird
    with BuildSketch(ex11.faces().sort_by(Axis.Y)[-1]) as ex11_sk:
        locs = GridLocations(1, led_cc, 1, 4).local_locations
        for loc in locs:
            with Locations(offset(loc)):
                Circle(radius=fiber_dia/2)
    extrude(amount=-depth, mode=Mode.SUBTRACT)
    # screw holes
    with BuildSketch(ex11.faces().sort_by(Axis.Z)[-1]) as ex11_sk:
        with Locations([
            (-hole_cc/2 + hole_x_offset, hole_y_offset), 
            (hole_cc/2 + hole_x_offset, hole_y_offset)]):
            Circle(radius=hole_dia/2)
    extrude(amount=-50, mode=Mode.SUBTRACT)
    # cutout 1
    with BuildSketch(ex11.faces().sort_by(Axis.Z)[-1]) as ex11_sk:
        with Locations([(19, 4.5)]):
            RectangleRounded(10, 10, 1)
    extrude(amount=-50, mode=Mode.SUBTRACT)
    # fillet
    fillet(ex11.edges().filter_by(Axis.Z), radius=1)
    # cutout 2
    with BuildSketch(ex11.faces().sort_by(Axis.Z)[-1]) as ex11_sk:
        with Locations([(-1.6, 3)]):
            RectangleRounded(3, 8, 0.25)
    extrude(amount=-2, mode=Mode.SUBTRACT)

show(ex11)    
export_stl(ex11.part, "dlc32.stl")

