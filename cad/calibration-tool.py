import cadquery as cq

w = 85
h = 50
d = 20
w1 = 40
w2 = w - w1
h1 = 10
th = 3
hole_inset = 15
hole_2_inset = 50

res = (cq.Workplane("XY")
       .tag("bot")
       # base
       .box(w, d, th, centered=(False, False, False))
       # reinforcement
       .workplaneFromTagged("bot")
       .transformed(offset=(0, d-th, 0))
       .box(w, th, h1, centered=(False, False, False))
       .edges(">Z or |Z")
       .fillet(1)
       # upright part
       .workplaneFromTagged("bot")
       .transformed(offset=(0, d-th, 0))
       .box(w1, th, h, centered=(False, False, False))
       # beam hole
       .workplaneFromTagged("bot")
       .transformed(offset=(w1/2, 0, h/2), rotate=(90, 0, 0))
       .circle(w1*0.4)
       .cutThruAll()
       # mounting hole 1
       .workplaneFromTagged("bot")
       .transformed(offset=(w - hole_inset, d/2, 0))
       .circle(5.5/2)
       .cutThruAll()
       .edges(">Z or |Z")
       # mounting hole 1
       .workplaneFromTagged("bot")
       .transformed(offset=(w - hole_2_inset, d/2, 0))
       .circle(5.5/2)
       .cutThruAll()
       .edges(">Z or |Z")
       .fillet(1)
      )

show_object(res)

inset = 2
hth = 1
paper_th = 0.5
holder = (cq.Workplane("XY")
          .transformed(offset=(inset, d, 0))
          .box(w1 - 2*inset, 2*hth, h - inset, centered=(False, False, False))
          )
cutout1 = (cq.Workplane("XY")
           .transformed(offset=(inset + hth, d, 4*inset - hth))
           .box(w1 - 2*inset - 2*hth, paper_th, h - inset - hth, centered=(False, False, False))
          )
#show_object(cutout1)
cutout2 = (cq.Workplane("XY")
           .transformed(offset=(inset + 3*hth, d, 4*inset))
           .box(w1 - 4*inset - 2*hth, 2*hth, h, centered=(False, False, False))
           .edges("|Y")
           .fillet(2)
          )
#show_object(cutout2)

holder = holder - cutout1 - cutout2
res = res + holder
show_object(res)

cq.exporters.export(res, 'calibration-tool.stl')
