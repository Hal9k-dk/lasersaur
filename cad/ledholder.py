import cadquery as cq

depth = 30
plate_th = 3
hd = 5.1
th = 1
width = 15
offset = 18
result = (cq.Workplane("XY")
          .tag("o")
          # Plate
          .box(width, depth, plate_th, centered=(True, False, False))
          .edges(">Z")
          .fillet(0.5)
          .workplaneFromTagged("o")
          .transformed(offset=(0, offset, plate_th))
          .box(5, 10, hd + 2*th, centered=(True, False, False))
          .workplaneFromTagged("o")
          .transformed(offset=(0, 10, 0))
          .circle(5.5/2)
          .cutThruAll()
          .workplaneFromTagged("o")
          .transformed(offset=(0, offset + 5, plate_th + hd/2 + th), rotate=(90, 90, 0))
          .circle(hd/2)
          .cutThruAll()
          .edges(">Z")
          .fillet(0.5)
          )
show_object(result)
