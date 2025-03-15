import cadquery as cq

w = 30
pinhole_dia = 2.9

res = (cq.Workplane("XY")
       .circle(pinhole_dia/2).extrude(w)
       )

show_object(res)
