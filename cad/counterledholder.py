import cadquery as cq

hd = 5.1
cc = 10.668
depth = 5
th = 1

result = (cq.Workplane("XY")
          .tag("o")
          .box(cc + hd + 2*th, depth, hd + 2*th)
          .workplaneFromTagged("o")
          .transformed(rotate=(90, 0, 0))
          .rarray(cc, 1, 2, 1)
          .circle(hd/2)
          .cutThruAll()
          .edges(">Z and |Y")
          .fillet(3)
          .edges(">Z and |X")
          .fillet(0.5)
          )
show_object(result)
