import cadquery as cq

w = 40
h = 15
th = 3
edge = 3

res = (cq.Workplane("XY")
       .tag("bot")
       .box(w, h, th, centered=(True, True, False))
       .edges(">Z or |Z")
       .fillet(2)
      )

block = (cq.Workplane("XY")
       .transformed(offset=(0, 0, -2*th))
       .box(w-2*edge, h-2*edge, 2*th, centered=(True, True, False))
       .edges("|Z")
       .fillet(1)
       )

res = res.union(block)
res = (res
       .workplaneFromTagged("bot")
       .rarray(10, 1, 4, 1)
       .circle(1.9/2)
       .cutThruAll()
       )

show_object(res)
