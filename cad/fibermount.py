import cadquery as cq

w = 50
h = 30
th = 3
edge = 3

res = (cq.Workplane("XY")
       .tag("bot")
       .box(w, h, th, centered=(True, True, False))
       .edges(">Z or |Z")
       .fillet(2)
       .workplaneFromTagged("bot")
       .transformed(offset=(0, 0, -2*th))
       .box(w-2*edge, h-2*edge, 2*th, centered=(True, True, False))
       .rarray(15, 1, 3, 1)
       .circle(1)
       .cutThruAll()
      )

show_object(res)
