import cadquery as cq

length = 25
w = 30
th = 3
hole_offset = -2.5

res = (cq.Workplane("XY")
       .tag("o")
       .box(length, w, th, centered=(True, True, False))
       .edges()
       .fillet(0.5)
       .workplaneFromTagged("o")
       .transformed(offset=(hole_offset, 0, 0))
       .circle(2)
       .cutThruAll()
       )

show_object(res)
