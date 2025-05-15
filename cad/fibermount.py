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
       .fillet(2)
       )

res = res.union(block)
hd = 7
res = (res
       .workplaneFromTagged("bot")
       .rarray(hd, 1, 5, 1)
       .circle(1/2)
       .cutThruAll()
       .workplaneFromTagged("bot")
       .transformed(offset=(2*hd, 0, 0))
       .circle(2/2)
       .cutThruAll()
       )

show_object(res)
