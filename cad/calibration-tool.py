import cadquery as cq

w = 85
h = 50
d = 20
w1 = 40
w2 = w - w1
h1 = 10
th = 3
hole_inset = 15

res = (cq.Workplane("XY")
       .tag("bot")
       # base
       .box(w, d, th, centered=(False, False, False))
       # reinforcement
       .workplaneFromTagged("bot")
       .transformed(offset=(0, 0, 0))
       .box(w, th, h1, centered=(False, False, False))
       .edges(">Z or |Z")
       .fillet(1)
       # upright part
       .workplaneFromTagged("bot")
       .transformed(offset=(0, 0, 0))
       .box(w1, th, h, centered=(False, False, False))
       # beam hole
       .workplaneFromTagged("bot")
       .transformed(offset=(w1/2, 0, h/2), rotate=(90, 0, 0))
       .circle(w1*0.4)
       .cutThruAll()
       # mounting hole
       .workplaneFromTagged("bot")
       .transformed(offset=(w - hole_inset, d/2, 0))
       .circle(5.5/2)
       .cutThruAll()
       .edges(">Z or |Z")
       .fillet(1)
      )

show_object(res)
