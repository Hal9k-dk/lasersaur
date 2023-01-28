import cadquery as cq

id = 5.2
od = 10
len = 4
slot_w = 1
slot_l = 8

res = (cq.Workplane("XY")
       .circle(od/2)
       .extrude(len)
       .circle(id/2)
       .cutThruAll()
       .rect(slot_w, slot_l)
       .cutThruAll()
      )

show_object(res)
