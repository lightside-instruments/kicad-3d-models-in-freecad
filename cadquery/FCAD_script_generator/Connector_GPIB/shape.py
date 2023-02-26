import cadquery as cq

delta=0.1

#Part 1 of 6

for i in range(0,12):
	pin = cq.Workplane("XZ", origin=0)\
                   .rect(2.16, 2+delta).extrude(9)
	hole = cq.Workplane("XZ", origin=0)\
                   .rect(1, 0.6).extrude(9+delta)
	pin.cut(hole)
	pin_high = pin.translate((i*2.16,0,1))
	pin_low = pin.translate((i*2.16,0,-1))
	print(i)
	if(i==0):
		pins = pin_high.union(pin_low)
	else:
		pins = pins.union(pin_high.union(pin_low))

oshell1 = cq.Workplane("XZ", origin=0)\
                   .rect(28+delta, 4+delta).extrude(9)


oshell2 =cq.Workplane("XZ", origin=0)\
                   .rect(28+delta, 4+delta).extrude(9+delta).edges("|Z").fillet(0.2)
oshell2 =oshell2.edges("#Z").fillet(0.2)

oshell3 = cq.Workplane("XZ", origin=0)\
                   .rect(28+delta, 4+delta).extrude(9+delta)
oshell4 = cq.Workplane("XZ", origin=0)\
                   .rect(28+delta, 4+delta).extrude(9+delta).cut(cq.Workplane("XZ", origin=0)\
                   .rect(25+delta, 4+delta).extrude(9+delta))

oshell1 = oshell1.cut(oshell2)

oshell3 = oshell3.cut(oshell1)

pins = pins.translate((2.16/2-12*2.16/2,0,00)).union(oshell4).cut(oshell1)
part1 = pins.translate((0,9+delta,0))


#Part 2 of 6
part2 = cq.Workplane("XY", origin=0)\
                   .rect(54.7+delta, 15.1+delta)
part2 = part2.center(23.4, -(10.70-15.10/2)).circle(2)
part2 = part2.center(-2*23.4,0).circle(2)
part2 = part2.extrude(4).translate((0,-8,4))

reductor_side = cq.Workplane("XY", origin=0).rect(6-4*delta, 15.6+delta).extrude(2)
part2 = part2.cut(reductor_side.translate((23.4,-6,4))).cut(reductor_side.translate((-23.4,-6,4)))


#Part 3 of 6
part3 = cq.Workplane("XZ", origin=0)\
                   .rect(54.7+delta, 15.6+delta).rect(28,15.6+delta).center(-23.4,0).circle(2).center(2*23.4,0).circle(2).extrude(6)
reductor_side = cq.Workplane("XZ", origin=0).rect(6-4*delta, 15.6+delta).extrude(4)
reductor_center = cq.Workplane("XZ", origin=0)\
                   .rect(28, 15.6+2*delta).extrude(6)
part3 = part3.cut(reductor_side.translate((23.4,-2.4,0))).cut(reductor_side.translate((-23.4,-2.4,0))).cut(reductor_center)


#Part 4 of 6
part4 = cq.Workplane("XZ", origin=0).moveTo(-13.5,6.5)\
.threePointArc((-15,6),(-16.5, 4)).lineTo(-18,-2).threePointArc((-18,-4.5),(-14, -6)).lineTo(14,-6)\
.threePointArc((18,-4.5),(18, -2)).lineTo(16.5,4).threePointArc((15,6),(13.5, 6.5))\
.lineTo(-13.5,6.5).close().extrude(8).translate((0,2,0))

#Part 5 of 6
part5_1 = cq.Workplane("YZ", origin=0)\
                   .moveTo(0,0).lineTo(0,-12).lineTo(-8,0).close().extrude(2).translate((-16,-6,4))
part5_2 = cq.Workplane("YZ", origin=0)\
                   .moveTo(0,0).lineTo(0,-12).lineTo(-8,0).close().extrude(2).translate((16-4/2,-6,4))

#Part 6 of 6
part6 = cq.Workplane("XZ", origin=0).box(28,2,2)
part6 = part6.translate((0,-7,4))

show_object(part6.union(part5_1.union(part5_2.union(part4.union(part3.union(part2.union(part1)))))))

