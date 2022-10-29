import cadquery as cq
import math

# shell thickness
th = 3
# shell fillet radius
fillet_r = 5

centerXY = (True, True, False)

mount_h = 12

front_width = 145
front_height = 100
front_y_offset = 23 + mount_h/2
front_depth = 5

bot_depth = 90
top_depth = 60
edge = 2
height = front_height + 5
width = front_width + 2*edge

# make shell
result = (cq.Workplane("XZ")
          .hLine(bot_depth)
          .vLine(height)
          .hLine(-top_depth)
          .lineTo(0, 0)
          .close()
          .extrude(width)
          .faces("<Z")
          .shell(-th)
          # round back edges
          .edges("|Z").fillet(fillet_r)
          # round top
          .faces(">Z")
          .edges().fillet(fillet_r)
          # round front edges
          #.edges('|(30, 0, 70)').fillet(fillet_r)
          )

# mount
mount_th = 5
mount_w = width - th
mount_d = bot_depth - th
log('mount: %d x %d' % (mount_w, mount_d))
mount = (cq.Workplane("XY")
         .transformed(offset=(th/2, -width+(width-mount_w)/2, -(mount_h-th)))
         .box(mount_d, mount_w, mount_h, centered=False)
         .faces("<Z or >Z")
         .shell(-mount_th)
         .edges("|Z").fillet(2)
         )

result = (result + mount)


# workplane aligned with front face
angle = math.degrees(math.atan(height/(bot_depth-top_depth)))
(result
 .faces("<Z")
 .workplane(centerOption="CenterOfMass", invert=True)
 .transformed(offset=(-33.4, 0, 30), rotate=(0, -angle, 0))
 .tag("front")
)

# lip for carrying front plate
result = (result
          .workplaneFromTagged("front")
          .transformed(offset=(front_y_offset, 0, -2))
          .rect(height - th, width-th)
          .extrude(10-5)
          )

# hole for front plate
result = (result
          .workplaneFromTagged("front")
          .transformed(offset=(front_y_offset, 0, 10))
          .rect(front_height, front_width)
          .cutBlind(-5-3)
          )

# hole behind front plate
result = (result
          .workplaneFromTagged("front")
          .transformed(offset=(front_y_offset, 0, -10))
          .rect(front_height - 2*th, front_width - 2*th)
          .cutBlind(50)
          )

# counter dummy
#result = (result
#          .workplaneFromTagged("front")
#          .transformed(offset=(25, 0, -4))
#          .rect(90, 37)
#          .extrude(-50)
#          )

# for debugging
#result = result.workplaneFromTagged("front").box(50, 50, 10, centered=centerXY)

# slots
def make_slot(xo):
    groove_offset = -1
    if xo > 0:
        groove_offset = 1
    return (cq.Workplane("XY")
            .transformed(offset=(bot_depth-7.5, -5/2 - xo*(width-5), 0))
            .box(8, 5, height-fillet_r, centered=centerXY)
            .transformed(offset=(0, groove_offset, height-fillet_r))
            .rect(3, 3)
            .cutBlind(-height)
            )

#result = result + make_slot(0)
#result = result + make_slot(1)

show_object(result)
