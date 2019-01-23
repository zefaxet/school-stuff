# Name: Edward Auttonberry
# CWID: 102-48-286
# DATE: 12/5/2018
# Assignment 1 -- 3-D Transformations and Perspective Projection
# Desc: This produces a wire-frame 3D square pyramid on a tkinter canvas
# 	Basic uniform scaling, translation, and rotation transformations can be applied to the object at uniform intervals
# 	and will be visibly applied in real time

import math
from tkinter import *

canvas_width = 400
canvas_height = 400
d = 500

# ***************************** Initialize Pyramid Object ***************************
# Definition  of the five underlying points
apex = [0, 50, 100]
base1 = [-50, -50, 50]
base2 = [50, -50, 50]
base3 = [50, -50, 150]
base4 = [-50, -50, 150]

# Definition of the five polygon faces using the meaningful point names
# Polys are defined in counter clockwise order when viewed from the outside
frontpoly = [apex, base1, base2]
rightpoly = [apex, base2, base3]
backpoly = [apex, base3, base4]
leftpoly = [apex, base4, base1]
bottompoly = [base4, base3, base2, base1]

# Definition of the object
pyramid = [bottompoly, frontpoly, rightpoly, backpoly, leftpoly]

# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
pyramid_point_cloud = [apex, base1, base2, base3, base4]
# ************************************************************************************


# This function resets the pyramid to its original size and location in 3D space
# Note that shortcuts like "apex = [0,50,100]" will not work as they build new
# structures rather than modifying the existing Pyramid / PyramidPointCloud
def reset_pyramid():
	# The pyramid object is a list whose elements are references to sub-lists
	# These sub-lists are used in the other methods. This method will not replace the sub-lists, but will instead
	# 	modify the existing references by replacing the current values with the values that were present when the
	# 	program began.
	apex[0] = 0
	apex[1] = 50
	apex[2] = 100
	base1[0] = -50
	base1[1] = -50
	base1[2] = 50
	base2[0] = 50
	base2[1] = -50
	base2[2] = 50
	base3[0] = 50
	base3[1] = -50
	base3[2] = 150
	base4[0] = -50
	base4[1] = -50
	base4[2] = 150


# This function translates an object by some displacement.  The displacement is a 3D
# vector so the amount of displacement in each dimension can vary.
def translate(object, displacement):
	# Add the displacement vector to each point in the pyramid's point cloud
	for point in object:
		point[0] += displacement[0]
		point[1] += displacement[1]
		point[2] += displacement[2]

	
# This function performs a simple uniform scale of an object assuming the object is
# centered at the origin.  The scalefactor is a scalar.
def scale(object, scale_factor):
	# Take each point in the point cloud and multiply the components by the scale factor
	for point in object:
		point[0] *= scale_factor
		point[1] *= scale_factor
		point[2] *= scale_factor


# This function performs a rotation of an object about the Z axis (from +X to +Y)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
def rotate_z(object, degrees):
	# Take the xy projection of each point and apply the rotation to the resulting plane's axes
	# Python's trig functions take radian inputs
	# Input stays positive to preserve counter-clockwise rotation
	for point in object:
		x = point[0]
		y = point[1]
		point[0] = x * math.cos(math.radians(degrees)) - y * math.sin(math.radians(degrees))
		point[1] = x * math.sin(math.radians(degrees)) + y * math.cos(math.radians(degrees))
	
	
# This function performs a rotation of an object about the Y axis (from +Z to +X)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +Y looking toward the origin.
def rotate_y(object, degrees):
	# Take the xz projection of each point and apply the rotation to the resulting plane's axes
	# Python's trig functions take radian inputs
	# Input should be negated to produce clockwise rotation on positive values
	degrees *= -1
	for point in object:
		x = point[0]
		z = point[2]
		point[0] = x * math.cos(math.radians(degrees)) - z * math.sin(math.radians(degrees))
		point[2] = x * math.sin(math.radians(degrees)) + z * math.cos(math.radians(degrees))


# This function performs a rotation of an object about the X axis (from +Y to +Z)
# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
# in a LHS when viewed from +X looking toward the origin.
def rotate_x(object, degrees):
	# Take the yz projection of each point and apply the rotation to the resulting plane's axes
	# Python's trig functions take radian inputs
	# Input should be negated to produce clockwise rotation on positive values
	degrees *= -1
	for point in object:
		z = point[2]
		y = point[1]
		point[2] = z * math.cos(math.radians(degrees)) - y * math.sin(math.radians(degrees))
		point[1] = z * math.sin(math.radians(degrees)) + y * math.cos(math.radians(degrees))


# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def draw_object(object):
	# Draw each face of the pyramid individually
	for poly in object:
		draw_poly(poly)


# This function will draw a polygon by repeatedly callying drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def draw_poly(poly):
	# Assuming the points are aligned in an order that would traverse the polygon's perimeter, draw points between each
	# duple of consecutive points in the polygon
	# The modulo guarantees that the last point will connect to the first point
	points = len(poly)
	for i in range(points):
		draw_line(poly[i], poly[(i + 1) % points])


# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def draw_line(start, end):
	# for the start and end points, calculate their projections and convert those points to points representative of the
	# 	tkinter canvas layout, then draw the line
	start_display = convert_to_display_coordinates(project(start))
	end_display = convert_to_display_coordinates(project(end))
	w.create_line(start_display[0], start_display[1], end_display[0], end_display[1])


# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
	# Calculate the projection of the point on the display surface based on an assumed perspective distance from the
	# 	viewport, d, and the z position of the point
	ps = []
	for axis in point:
		ps.append(d*axis/(d + point[2]))
	return ps


# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convert_to_display_coordinates(point):
	# Based on the dimensions of the canvas, calculate the coordinates on the canvas that match the two-dimensional
	# 	cartesian coordinates of the point
	origin_x = canvas_width / 2
	origin_y = canvas_height / 2
	display_coordinate = [point[0] + origin_x, origin_y - point[1]]  # y = 0 is top
	return display_coordinate
	

# **************************************************************************
# Everything below this point implements the interface
def reset():
	w.delete(ALL)
	reset_pyramid()
	draw_object(pyramid)


def larger():
	w.delete(ALL)
	scale(pyramid_point_cloud, 1.1)
	draw_object(pyramid)


def smaller():
	w.delete(ALL)
	scale(pyramid_point_cloud, .9)
	draw_object(pyramid)


def forward():
	w.delete(ALL)
	translate(pyramid_point_cloud, [0, 0, 5])
	draw_object(pyramid)


def backward():
	w.delete(ALL)
	translate(pyramid_point_cloud, [0, 0, -5])
	draw_object(pyramid)


def left():
	w.delete(ALL)
	translate(pyramid_point_cloud, [-5, 0, 0])
	draw_object(pyramid)


def right():
	w.delete(ALL)
	translate(pyramid_point_cloud, [5, 0, 0])
	draw_object(pyramid)


def up():
	w.delete(ALL)
	translate(pyramid_point_cloud, [0, 5, 0])
	draw_object(pyramid)


def down():
	w.delete(ALL)
	translate(pyramid_point_cloud, [0, -5, 0])
	draw_object(pyramid)


def x_plus():
	w.delete(ALL)
	rotate_x(pyramid_point_cloud, 5)
	draw_object(pyramid)


def x_minus():
	w.delete(ALL)
	rotate_x(pyramid_point_cloud, -5)
	draw_object(pyramid)


def y_plus():
	w.delete(ALL)
	rotate_y(pyramid_point_cloud, 5)
	draw_object(pyramid)


def y_minus():
	w.delete(ALL)
	rotate_y(pyramid_point_cloud, -5)
	draw_object(pyramid)


def z_plus():
	w.delete(ALL)
	rotate_z(pyramid_point_cloud, 5)
	draw_object(pyramid)


def z_minus():
	w.delete(ALL)
	rotate_z(pyramid_point_cloud, -5)
	draw_object(pyramid)


root = Tk()
outerframe = Frame(root)
outerframe.pack()

w = Canvas(outerframe, width=canvas_width, height=canvas_height)
draw_object(pyramid)
w.pack()

controlpanel = Frame(outerframe)
controlpanel.pack()

resetcontrols = Frame(controlpanel, height=100, borderwidth=2, relief=RIDGE)
resetcontrols.pack(side=LEFT)

resetcontrolslabel = Label(resetcontrols, text="Reset")
resetcontrolslabel.pack()

resetButton = Button(resetcontrols, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

scalecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
scalecontrols.pack(side=LEFT)

scalecontrolslabel = Label(scalecontrols, text="Scale")
scalecontrolslabel.pack()

largerButton = Button(scalecontrols, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scalecontrols, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translatecontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
translatecontrols.pack(side=LEFT)

translatecontrolslabel = Label(translatecontrols, text="Translation")
translatecontrolslabel.pack()

forwardButton = Button(translatecontrols, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translatecontrols, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translatecontrols, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translatecontrols, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="UP", command=up)
upButton.pack(side=LEFT)

upButton = Button(translatecontrols, text="DN", command=down)
upButton.pack(side=LEFT)

rotationcontrols = Frame(controlpanel, borderwidth=2, relief=RIDGE)
rotationcontrols.pack(side=LEFT)

rotationcontrolslabel = Label(rotationcontrols, text="Rotation")
rotationcontrolslabel.pack()

xPlusButton = Button(rotationcontrols, text="X+", command=x_plus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotationcontrols, text="X-", command=x_minus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotationcontrols, text="Y+", command=y_plus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotationcontrols, text="Y-", command=y_minus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotationcontrols, text="Z+", command=z_plus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotationcontrols, text="Z-", command=z_minus)
zMinusButton.pack(side=LEFT)

root.mainloop()
