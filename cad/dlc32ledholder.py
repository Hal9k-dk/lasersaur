# %%
from build123d import *
from ocp_vscode import *

# LED holes
led_dia = 5.2
led_cc = 8.47
led_depth = 8
led_offset = 0
fiber_dia = 2.8
# Screw holes
hole_cc = 58.7 - 33.2486
hole_dia = 3.2
hole_x_offset = led_cc/2
hole_y_offset = -3.5
# Overall
depth = led_depth + 5
plate_depth = 15
block_th = 1
plate_th = 2

block_l = hole_cc + 1.5*led_cc
block_w = depth
block_h = led_dia + 2*block_th

#length, width, thickness = 80.0, 60.0, 10.0

led_locs = []
for i in range(0, 4):
    led_locs.append((0, -block_l / 2 + led_offset + i * led_cc))
    
with BuildPart() as ex11:
    # basic shape
    Box(block_l, block_w, block_h, align=Align.MIN)
    # fillet
    fillet(ex11.edges().filter_by(Axis.Z), radius=1)
    #fillet(ex11.edges().sort_by(Axis.X)[0], radius=0.5)
    # LED holes
    with BuildSketch(ex11.faces().sort_by(Axis.Y)[-1]) as ex11_sk:
        with GridLocations(1, led_cc, 1, 4):
            Circle(radius=led_dia/2)
    extrude(amount=-led_depth, mode=Mode.SUBTRACT)
    # fiber holes
    with BuildSketch(ex11.faces().sort_by(Axis.Y)[-1]) as ex11_sk:
        with GridLocations(1, led_cc, 1, 4):
            Circle(radius=fiber_dia/2)
    extrude(amount=-depth, mode=Mode.SUBTRACT)
    # screw holes
    with BuildSketch(ex11.faces().sort_by(Axis.Z)[-1]) as ex11_sk:
        with Locations([
            (-hole_cc/2 + hole_x_offset, hole_y_offset), 
            (hole_cc/2 + hole_x_offset, hole_y_offset)]):
            Circle(radius=hole_dia/2)
    extrude(amount=-50, mode=Mode.SUBTRACT)
    # cutout
    with BuildSketch(ex11.faces().sort_by(Axis.Z)[-1]) as ex11_sk:
        with Locations([(19, 3)]):
            RectangleRounded(5, 7, 1)
    extrude(amount=-50, mode=Mode.SUBTRACT)

show(ex11)    
