# Name: Edward Auttonberry
# CWID: 102-48-286
# DATE: 12//2018
# Assignment 2 -- In-Place 3-D Transformations in a Multi Object Environment
# Desc: This produces a set of wire-frime objects in a pseduo-three-dimensional environment.
    # Rendered are two cubes and two pyramids, each with in-place translation, uniform scaling, nad
    # rotation.

import math
from tkinter import *
from statistics import mean

canvas_width = 400
canvas_height = 400
d = 500

# ***************************** Initialize Pyramid Object ***************************

# This is a superclass that defines all transformation procedures and initial point clouds and faces
    # for any object that we draw on the canvas.
class Polyhedron:
	
	def __init__(self, centered_shape, point_cloud, initial_pos):
		
		self.offset = initial_pos
		self.polygons = centered_shape
		self.point_cloud = point_cloud
		self.translate(initial_pos)
	
	# This function performs a simple uniform scale of an object assuming the object is
	# centered at the origin.  The scalefactor is a scalar.
	def scale(self, scale_factor):
		# Take each point in the point cloud and multiply the components by the scale factor
		center = get_visual_center(self.point_cloud)
		inverted_center = [-x for x in center]  # negate the center for translation
		self.translate(inverted_center)
		for point in self.point_cloud:
			point[0] *= scale_factor
			point[1] *= scale_factor
			point[2] *= scale_factor
		self.translate(center)
	
	# This function translates an object by some displacement.  The displacement is a 3D
	# vector so the amount of displacement in each dimension can vary.
	def translate(self, displacement):
		
		for point in self.point_cloud:
			# Add the displacement vector to each point in the pyramid's point cloud
			point[0] += displacement[0]
			point[1] += displacement[1]
			point[2] += displacement[2]
	
	# This function performs a rotation of an object about the Z axis (from +X to +Y)
	# by 'degrees', assuming the object is centered at the origin.  The rotation is CCW
	# in a LHS when viewed from -Z [the location of the viewer in the standard postion]
	def rotate_z(self, degrees):
		# Take the xy projection of each point and apply the rotation to the resulting plane's axes
		# Python's trig functions take radian inputs
		# Input stays positive to preserve counter-clockwise rotation
		center = get_visual_center(self.point_cloud)
		inverted_center = [-x for x in center]
		self.translate(inverted_center)
		for point in self.point_cloud:
			x = point[0]
			y = point[1]
			point[0] = x * math.cos(math.radians(degrees)) - y * math.sin(math.radians(degrees))
			point[1] = x * math.sin(math.radians(degrees)) + y * math.cos(math.radians(degrees))
		self.translate(center)
			
	# This function performs a rotation of an object about the Y axis (from +Z to +X)
	# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
	# in a LHS when viewed from +Y looking toward the origin.
	def rotate_y(self, degrees):
		# Take the xz projection of each point and apply the rotation to the resulting plane's axes
		# Python's trig functions take radian inputs
		# Input should be negated to produce clockwise rotation on positive values
		center = get_visual_center(self.point_cloud)
		inverted_center = [-x for x in center]  # negate the center for translation
		self.translate(inverted_center)
		degrees *= -1
		for point in self.point_cloud:
			x = point[0]
			z = point[2]
			point[0] = x * math.cos(math.radians(degrees)) - z * math.sin(math.radians(degrees))
			point[2] = x * math.sin(math.radians(degrees)) + z * math.cos(math.radians(degrees))
		self.translate(center)
	
		# This function performs a rotation of an object about the X axis (from +Y to +Z)
	# by 'degrees', assuming the object is centered at the origin.  The rotation is CW
	# in a LHS when viewed from +X looking toward the origin.
	def rotate_x(self, degrees):
		# Take the yz projection of each point and apply the rotation to the resulting plane's axes
		# Python's trig functions take radian inputs
		# Input should be negated to produce clockwise rotation on positive values
		degrees *= -1
		center = get_visual_center(self.point_cloud)
		inverted_center = [-x for x in center]  # negate the center for translation
		self.translate(inverted_center)
		for point in self.point_cloud:
			z = point[2]
			y = point[1]
			point[2] = z * math.cos(math.radians(degrees)) - y * math.sin(math.radians(degrees))
			point[1] = z * math.sin(math.radians(degrees)) + y * math.cos(math.radians(degrees))
		self.translate(center)
	
# Implementation of the Polyhedron superclass that models the pyramid as it was in assignment 1
class Pyramid(Polyhedron):

	def __init__(self, initial_pos):
		
		# Definition  of the five underlying points
		self.apex = [0, 50, 100]
		self.base1 = [-50, -50, 50]
		self.base2 = [50, -50, 50]
		self.base3 = [50, -50, 150]
		self.base4 = [-50, -50, 150] 

		# Definition of the five polygon faces using the meaningful point names
		# Polys are defined in counter clockwise order when viewed from the outside
		front_poly = [self.apex, self.base1, self.base2]
		right_poly = [self.apex, self.base2, self.base3]
		back_poly = [self.apex, self.base3, self.base4]
		left_poly = [self.apex, self.base4, self.base1]
		bottom_poly = [self.base4, self.base3, self.base2, self.base1]
		
		# Definition of the object
		pyramid = [bottom_poly, front_poly, right_poly, back_poly, left_poly]
		
		# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
		pyramid_point_cloud = [self.apex, self.base1, self.base2, self.base3, self.base4]
		
		Polyhedron.__init__(self, pyramid, pyramid_point_cloud, initial_pos)

	# This function resets the pyramid to its original size and location in 3D space
	# Note that shortcuts like "apex = [0,50,100]" will not work as they build new
	# structures rather than modifying the existing Pyramid / PyramidPointCloud
	def reset(self):
		# The pyramid object is a list whose elements are references to sub-lists
		# These sub-lists are used in the other methods. This method will not replace the sub-lists, but will instead
		# 	modify the existing references by replacing the current values with the values that were present when the
		# 	program began.
		self.apex[0] = 0
		self.apex[1] = 50
		self.apex[2] = 100
		self.base1[0] = -50
		self.base1[1] = -50
		self.base1[2] = 50
		self.base2[0] = 50
		self.base2[1] = -50
		self.base2[2] = 50
		self.base3[0] = 50
		self.base3[1] = -50
		self.base3[2] = 150
		self.base4[0] = -50
		self.base4[1] = -50
		self.base4[2] = 150
		self.translate(self.offset)

# Implementation of the Polyhedron superclass that models a new cube object
class Cube(Polyhedron):

	def __init__(self, initial_pos):
		# Definition  of the eight underlying points
		# first letter: u or l for upper or lower
		# second letter: r or l for right or left
		# third letter: f or b for front or back
                # TODO: Ensure clockwiseness
		self.ulb = [-50, 50, 50]
		self.urb = [50, 50, 50]
		self.urf = [50, 50, 150]
		self.ulf = [-50, 50, 150]
		self.llb = [-50, -50, 50]
		self.lrb = [50, -50, 50]
		self.lrf = [50, -50, 150]
		self.llf = [-50, -50, 150]

		# Definition of the six polygon faces using the meaningful point names
		top_poly = [self.ulb, self.urb, self.urf, self.ulf]
		front_poly = [self.urf, self.ulf, self.llf, self.lrf]
		right_poly = [self.urf, self.urb, self.lrb, self.lrf]
		back_poly = [self.ulb, self.urb, self.lrb, self.llb]
		left_poly = [self.ulb, self.ulf, self.llf, self.llb]
		bottom_poly = [self.llf, self.lrf, self.lrb, self.llb]

		# Definition of the object
		cube = [bottom_poly, front_poly, right_poly, back_poly, left_poly, top_poly]

		# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
		cube_point_cloud = [self.ulf, self.urf, self.urb, self.ulb, self.llb, self.lrb, self.llf, self.lrf]

		Polyhedron.__init__(self, cube, cube_point_cloud, initial_pos)

	# This function resets the cube to its original size and location in 3D space
	def reset(self):
		# The pyramid object is a list whose elements are references to sub-lists
		# These sub-lists are used in the other methods. This method will not replace the sub-lists, but will instead
		# 	modify the existing references by replacing the current values with the values that were present when the
		# 	program began.
		self.ulf[0] = -50
		self.ulf[1] = 50
		self.ulf[2] = 150
		self.ulb[0] = -50
		self.ulb[1] = 50
		self.ulb[2] = 50
		self.urb[0] = 50
		self.urb[1] = 50
		self.urb[2] = 50
		self.urf[0] = 50
		self.urf[1] = 50
		self.urf[2] = 150
		self.lrb[0] = 50
		self.lrb[1] = -50
		self.lrb[2] = 50
		self.llb[0] = -50
		self.llb[1] = -50
		self.llb[2] = 50
		self.lrf[0] = 50
		self.lrf[1] = -50
		self.lrf[2] = 150
		self.llf[0] = -50
		self.llf[1] = -50
		self.llf[2] = 150
		self.translate(self.offset)


# ************************************************************************************
objects = [Pyramid([-20, -20, 20]), Pyramid([100, 300, 500]), Cube([100, -100, 200]), Cube([-600, 400, 3000])]
current_object_index = 0


# The function will draw an object by repeatedly callying drawPoly on each polygon in the object
def draw_objects(objects):
	# Draw each face of the pyramid individually
	for polyhedron in objects:
		color = 'green' if polyhedron is objects[current_object_index] else 'black'
		for poly in polyhedron.polygons:
			draw_poly(poly, color)


# This function will draw a polygon by repeatedly calling drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def draw_poly(poly, color):
	# Assuming the points are aligned in an order that would traverse the polygon's perimeter, draw points between each
	# duple of consecutive points in the polygon
	# The modulo guarantees that the last point will connect to the first point
	points = len(poly)
	for i in range(points):
		draw_line(poly[i], poly[(i + 1) % points], color)


# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
def draw_line(start, end, color):
	# for the start and end points, calculate their projections and convert those points to points representative of the
	# 	tkinter canvas layout, then draw the line
	start_display = convert_to_display_coordinates(project(start))
	end_display = convert_to_display_coordinates(project(end))
	w.create_line(start_display[0], start_display[1], end_display[0], end_display[1], fill=color)


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


# This function takes the point cloud of a shape and calculates the visual center to be used as a reference point for
	# performing transformations on the shapes in place
def get_visual_center(cloud):
	x = []
	y = []
	z = []
	for point in cloud:
		x.append(point[0])
		y.append(point[1])
		z.append(point[2])
	return [mean(x), mean(y), mean(z)]
	

# **************************************************************************
# Everything below this point implements the interface
def reset():
	w.delete(ALL)
	objects[current_object_index].reset()
	draw_objects(objects)


def larger():
	w.delete(ALL)
	objects[current_object_index].scale(1.1)
	draw_objects(objects)


def smaller():
	w.delete(ALL)
	objects[current_object_index].scale(.9)
	draw_objects(objects)


def forward():
	w.delete(ALL)
	objects[current_object_index].translate([0, 0, 5])
	draw_objects(objects)


def backward():
	w.delete(ALL)
	objects[current_object_index].translate([0, 0, -5])
	draw_objects(objects)


def left():
	w.delete(ALL)
	objects[current_object_index].translate([-5, 0, 0])
	draw_objects(objects)


def right():
	w.delete(ALL)
	objects[current_object_index].translate([5, 0, 0])
	draw_objects(objects)


def up():
	w.delete(ALL)
	objects[current_object_index].translate([0, 5, 0])
	draw_objects(objects)


def down():
	w.delete(ALL)
	objects[current_object_index].translate([0, -5, 0])
	draw_objects(objects)


def x_plus():
	w.delete(ALL)
	objects[current_object_index].rotate_x(5)
	draw_objects(objects)


def x_minus():
	w.delete(ALL)
	objects[current_object_index].rotate_x(-5)
	draw_objects(objects)


def y_plus():
	w.delete(ALL)
	objects[current_object_index].rotate_y(5)
	draw_objects(objects)


def y_minus():
	w.delete(ALL)
	objects[current_object_index].rotate_y(-5)
	draw_objects(objects)


def z_plus():
	w.delete(ALL)
	objects[current_object_index].rotate_z(5)
	draw_objects(objects)


def z_minus():
	w.delete(ALL)
	objects[current_object_index].rotate_z(-5)
	draw_objects(objects)


def select():
	w.delete(ALL)
	global current_object_index
	current_object_index = (current_object_index + 1) % len(objects)
	draw_objects(objects)


root = Tk()
outer_frame = Frame(root)
outer_frame.pack()

w = Canvas(outer_frame, width=canvas_width, height=canvas_height)
draw_objects(objects)
w.pack()

control_panel = Frame(outer_frame)
control_panel.pack()

reset_controls = Frame(control_panel, height=100, borderwidth=2, relief=RIDGE)
reset_controls.pack(side=LEFT)

reset_controls_label = Label(reset_controls, text="Reset")
reset_controls_label.pack()

resetButton = Button(reset_controls, text="Reset", fg="green", command=reset)
resetButton.pack(side=LEFT)

selectButton = Button(reset_controls, text="Select", command=select)
selectButton.pack(side=LEFT)

scale_controls = Frame(control_panel, borderwidth=2, relief=RIDGE)
scale_controls.pack(side=LEFT)

scale_controls_label = Label(scale_controls, text="Scale")
scale_controls_label.pack()

largerButton = Button(scale_controls, text="Larger", command=larger)
largerButton.pack(side=LEFT)

smallerButton = Button(scale_controls, text="Smaller", command=smaller)
smallerButton.pack(side=LEFT)

translate_controls = Frame(control_panel, borderwidth=2, relief=RIDGE)
translate_controls.pack(side=LEFT)

translate_controls_label = Label(translate_controls, text="Translation")
translate_controls_label.pack()

forwardButton = Button(translate_controls, text="FW", command=forward)
forwardButton.pack(side=LEFT)

backwardButton = Button(translate_controls, text="BK", command=backward)
backwardButton.pack(side=LEFT)

leftButton = Button(translate_controls, text="LF", command=left)
leftButton.pack(side=LEFT)

rightButton = Button(translate_controls, text="RT", command=right)
rightButton.pack(side=LEFT)

upButton = Button(translate_controls, text="UP", command=up)
upButton.pack(side=LEFT)

upButton = Button(translate_controls, text="DN", command=down)
upButton.pack(side=LEFT)

rotation_controls = Frame(control_panel, borderwidth=2, relief=RIDGE)
rotation_controls.pack(side=LEFT)

rotation_controls_label = Label(rotation_controls, text="Rotation")
rotation_controls_label.pack()

xPlusButton = Button(rotation_controls, text="X+", command=x_plus)
xPlusButton.pack(side=LEFT)

xMinusButton = Button(rotation_controls, text="X-", command=x_minus)
xMinusButton.pack(side=LEFT)

yPlusButton = Button(rotation_controls, text="Y+", command=y_plus)
yPlusButton.pack(side=LEFT)

yMinusButton = Button(rotation_controls, text="Y-", command=y_minus)
yMinusButton.pack(side=LEFT)

zPlusButton = Button(rotation_controls, text="Z+", command=z_plus)
zPlusButton.pack(side=LEFT)

zMinusButton = Button(rotation_controls, text="Z-", command=z_minus)
zMinusButton.pack(side=LEFT)

root.mainloop()
