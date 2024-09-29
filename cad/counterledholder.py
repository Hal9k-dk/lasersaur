import cadquery as cq

hd = 5.2
cc = 10.668
depth = 8+5
th = 1

result = (cq.Workplane("XY")
          .tag("o")
          .box(cc + hd + 2*th, depth, hd + 2*th)
          .faces(">Y")
          .workplane()
          .tag("top")
          .rarray(cc, 1, 2, 1)
          .circle(hd/2)
          .cutBlind(-8)
          .workplaneFromTagged("top")
          .rarray(cc, 1, 2, 1)
          .circle(2.8/2)
          .cutThruAll()
          .edges(">Z and |Y")
          .fillet(3)
          .edges(">Z and |X")
          .fillet(0.5)
          )
show_object(result)
