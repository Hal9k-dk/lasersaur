# %%
from build123d import *
from ocp_vscode import *

length, height, width = 25, 22, 40
bend_radius = 1
thickness = 3

with BuildPart() as bracket:
    with BuildSketch() as sketch:
        with BuildLine() as profile:
            FilletPolyline(
                (0, 0), (length, 0), (length, height), radius=bend_radius
            )
            offset(amount=thickness, side=Side.LEFT)
        make_face()
    extrude(amount=width)
    fillet(bracket.edges().filter_by(Axis.Z), radius=1)
    fillet(bracket.edges().filter_by(Axis.Y), radius=1)
    # ridges
    with BuildSketch(bracket.faces().sort_by(Axis.Y)[0]) as h_sk:
        with GridLocations(1, 20, 1, 2):
            Rectangle(length - 5, 5)
    extrude(amount = 1)
    # side screw hole
    with BuildSketch(bracket.faces().sort_by(Axis.Y)[-1]) as h_sk:
        with Locations([(15, -10)]):
            Circle(radius=5.2/2)
    extrude(amount=-50, mode=Mode.SUBTRACT)
    # bottom screw hole
    with BuildSketch(bracket.faces().sort_by(Axis.X)[0]) as h_sk:
        with Locations([(length/2+2.5, 4 + 8)]):
            Circle(radius=3.2/2)
    extrude(amount=-50, mode=Mode.SUBTRACT)


show(bracket)
export_step(bracket.part, "sensorbracket.step")
