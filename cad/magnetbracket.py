# %%
from build123d import *
from ocp_vscode import *

length, height, width = 20, 20, 40
bend_radius = 1
thickness = 4

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
    # ridge
    with BuildSketch(bracket.faces().sort_by(Axis.Y)[-1].offset(-20)) as h_sk:
        with Locations((10, -10)):
            Rectangle(5, 15)
    extrude(amount = -2)
    # side screw hole
    with BuildSketch(bracket.faces().sort_by(Axis.Y)[-1]) as h_sk:
        with Locations([(10, -10)]):
            Circle(radius=5.2/2)
    extrude(amount=-50, mode=Mode.SUBTRACT)
    # magnet hole
    with BuildSketch(bracket.faces().sort_by(Axis.X)[-1]) as h_sk:
        with Locations([(-height/2 + 13.5, 10)]):
            Circle(radius=5.2/2)
    extrude(amount=-2, mode=Mode.SUBTRACT)


show(bracket)
export_step(bracket.part, "magnetbracket.step")
