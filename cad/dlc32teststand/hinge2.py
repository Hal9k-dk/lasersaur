import cadquery as cq

length = 35
hole_cc = 20
hole_dia = 5.1
hole_offset = -12.5
w = 30
th = 3
eps = 0.1
pinhole_dia = th

res = (cq.Workplane("XY")
       .tag("o")
       # flap
       .box(length, w, th, centered=(True, True, False))
       .edges()
       .fillet(1)
       # round part
       .workplaneFromTagged("o")
       .transformed(offset=(length/2 - th/2, w/2, -eps), rotate=(90, 0, 0))
       .tag("r")
       .circle(th+eps)
       .extrude(w)
       # pin hole
       .workplaneFromTagged("r")
       .circle(pinhole_dia/2).cutThruAll()
       # cutouts
       .workplaneFromTagged("o")
       .transformed(offset=(length/2 + w/2 - th/2 - th - 5*eps, w/3, -w/2))
       .rect(w, w/3)
       .cutBlind(w)
       .workplaneFromTagged("o")
       .transformed(offset=(length/2 + w/2 - th/2 - th - 5*eps, -w/3, -w/2))
       .rect(w, w/3)
       .cutBlind(w)
       # mounting holes
       .workplaneFromTagged("o")
       .workplane(th)
       .transformed(offset=(hole_offset, 0, 0))
       .rarray(1, hole_cc, 1, 2)
       .circle(hole_dia/2)
       .cutBlind(-th + 0.5)
       )

show_object(res)
