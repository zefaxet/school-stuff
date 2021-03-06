# Name: Edward Auttonberry
# CWID: 102-48-286
# DATE: 2/7/2019
# Assignment 4 -- Lighting and Shading
# Desc: This program draws a hollow cylindrical tube in a pseudo-three dimensional environemnt. The environment
# simulates a light source, which is reflected off of the surfaces of the tube.

import math
from tkinter import *
from statistics import mean
from copy import deepcopy

DEBUG = False
DRAW_DEBUG = 0  # 0 is off, 1 draws scan line bounds, -1 fills polygons with lines
# Program constants
canvas_width = 400
canvas_height = 400
d = 500

# toggleable values defining how shapes should be rendered
cull_backface = True
polygon_draw_mode = 0
z_buffering = True
lighting_model_state = 0
shading_model_state = 0

# ***************************** Initialize Pyramid Object ***************************


# This is a superclass that defines all transformation procedures and initial point clouds and faces
# for any object that we draw on the canvas.
class Polyhedron:
	def __init__(self, centered_shape, point_cloud, initial_pos,
				base_color, reflection_color):

		self.offset = initial_pos
		self.polygons = centered_shape
		self.point_cloud = point_cloud
		self.translate(initial_pos)
		self.base_color = base_color
		self.reflection_color = reflection_color

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

	# The function will draw the polyhedron by repeatedly calling drawPoly on each polygon in the object
	def draw(self):
		edge_color = 'red' if self is objects[current_object_index] else 'blue'
		for poly in self.polygons:
			poly.refresh_normal()
		for poly in self.polygons:
			# Filter visible faces with backface culling
			if not cull_backface or poly.draw:
				draw_poly(poly, edge_color, self)


# Implementation of the Polyhedron superclass that models the pyramid as it was in assignment 1
class Pyramid(Polyhedron):

	def __init__(self, initial_pos, fill_color_lambda=None):
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

		if fill_color_lambda:
			Polyhedron.__init__(self, pyramid, pyramid_point_cloud, initial_pos, fill_color_lambda)
		else:
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

	def __init__(self, initial_pos, fill_color_lambda=None):
		# Definition  of the eight underlying points
		# first letter: u or l for upper or lower
		# second letter: r or l for right or left
		# third letter: f or b for front or back
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
		front_poly = [self.ulf, self.urf, self.lrf, self.llf]
		right_poly = [self.urf, self.urb, self.lrb, self.lrf]
		back_poly = [self.urb, self.ulb, self.llb, self.lrb]
		left_poly = [self.ulb, self.ulf, self.llf, self.llb]
		bottom_poly = [self.llf, self.lrf, self.lrb, self.llb]

		# Definition of the object
		cube = [bottom_poly, front_poly, right_poly, back_poly, left_poly, top_poly]

		# Definition of the Pyramid's underlying point cloud.  No structure, just the points.
		cube_point_cloud = [self.ulf, self.urf, self.urb, self.ulb, self.llb, self.lrb, self.llf, self.lrf]

		if fill_color_lambda:
			Polyhedron.__init__(self, cube, cube_point_cloud, initial_pos, fill_color_lambda)
		else:
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


# Implementation of the polyhedron superclass that models the approximation of a hollow cylindrical tube
class Tube(Polyhedron):

	def __init__(self, initial_pos, outer_base_color, inner_fill_color):

		tube_point_cloud = self.generate_approximation_points(32)
		outer_tube, inner_tube = self.build_tube_faces(tube_point_cloud)

		Polyhedron.__init__(self, outer_tube, tube_point_cloud, initial_pos, outer_base_color, [200, 152, 255-0xBB])

		self.inner_polyhedron = Polyhedron(inner_tube, tube_point_cloud, initial_pos, inner_fill_color, [255, 0, 0])

	# This function resets the cube to its original size and location in 3D space
	def reset(self):
		# The pyramid object is a list whose elements are references to sub-lists
		# These sub-lists are used in the other methods. This method will not replace the sub-lists, but will instead
		# 	modify the existing references by replacing the current values with the values that were present when the
		# 	program began.

		tube_point_cloud = self.generate_approximation_points(32)
		for i in range(len(self.point_cloud)):
			self.point_cloud[i] = tube_point_cloud[i]

		self.translate(self.offset)
	
	def draw(self):
		
		super().draw()
		self.inner_polyhedron.draw()

	# Generate the approximation points assuming a tube height of 100 Tkinter units and tube radius of 50 units
	@staticmethod
	def generate_approximation_points(detail):

		R = 25  # radius constant
		theta_interval = (2 * math.pi) / detail
		upper_points, lower_points = [], []
		for i in range(detail):

			x = R*math.cos(theta_interval * i)
			z = R*math.sin(theta_interval * i)  # if backface culling breaks its because of this
			upper_points.append([x, 50, z])
			lower_points.append([x, -50, z])

		return upper_points + lower_points

	# This method builds the approximation faces and associates them for lighting models
	@staticmethod
	def build_tube_faces(point_cloud):

		face_count = len(point_cloud) / 2
		assert(face_count % 1 == 0)
		face_count = int(face_count)
		print(face_count)

		outer_tube = []
		inner_tube = []
		for i in range(face_count):
			upper_right = point_cloud[i % face_count]
			lower_right = point_cloud[face_count + i % face_count]
			lower_left = point_cloud[face_count + (i + 1) % face_count]
			upper_left = point_cloud[(i + 1) % face_count]
			outer_tube.append(Polygon([upper_right, lower_right, lower_left, upper_left]))
			inner_tube.append(Polygon([upper_left, lower_left, lower_right, upper_right]))

		for i in range(face_count):
			# add left and right faces as neighbours
			current_outer_face = outer_tube[i]
			left_outer_face = outer_tube[(i + 1) % face_count]
			right_outer_face = outer_tube[(i - 1) % face_count]
			current_outer_face.add_neighbour(right_outer_face)
			current_outer_face.add_neighbour(right_outer_face)
			current_outer_face.add_neighbour(left_outer_face)
			current_outer_face.add_neighbour(left_outer_face)

			# do the same for the inner faces
			current_inner_face = inner_tube[i]
			left_inner_face = inner_tube[(i + 1) % face_count]
			right_inner_face = inner_tube[(i - 1) % face_count]
			current_inner_face.add_neighbour(left_inner_face)
			current_inner_face.add_neighbour(left_inner_face)
			current_inner_face.add_neighbour(right_inner_face)
			current_inner_face.add_neighbour(right_inner_face)

		return outer_tube, inner_tube

# This class contains information about the faces of a polyhedron
class Polygon(object):

	def __init__(self, vertices):

		self.vertices = vertices
		self.neighbours = []
		self.draw, self.unit_normal = should_draw_polygon(self.vertices)
		self.__iterator = 0

	def add_neighbour(self, polygon):
		assert(type(polygon) is Polygon)
		self.neighbours.append(polygon)

	def refresh_normal(self):

		self.draw, self.unit_normal = should_draw_polygon(self.vertices)

	def __getitem__(self, i):

		return self.vertices[i]

	def __len__(self):

		return len(self.vertices)


# This object represents the edge made by the path between two points and the attributes of that line
class Edge(object):

	def __init__(self, p1, p2):
		self.start = min(p1, p2, key=lambda point: point[1])
		self.end = p2 if (p1 is self.start) else p1

	def set_vertex_normals(self, v1, v2, color, reflection_color):

		self.v1 = v1
		self.v2 = v2
		self.i1 = get_lit_color(color, v1, reflection_color)
		self.i2 = get_lit_color(color, v2, reflection_color)

	@property
	def x_start(self):
		return self.start[0]

	@property
	def y_start(self):
		return self.start[1]

	@property
	def z_start(self):
		return self.start[2]

	@property
	def x_end(self):
		return self.end[0]

	@property
	def y_end(self):
		return self.end[1]

	@property
	def z_end(self):
		return self.end[2]

	# dy/dx
	@property
	def slope(self):
		try:

			return (self.y_end - self.y_start)/(self.x_end - self.x_start)

		except ZeroDivisionError:

			return "undefined"

	# dx/dy
	@property
	def dx(self):
		try:

			return (self.x_end - self.x_start)/(self.y_end - self.y_start)

		except ZeroDivisionError:

			return 0

	# dz/dy
	@property
	def dz(self):
		try:

			return (self.z_end - self.z_start)/(self.y_end - self.y_start)

		except ZeroDivisionError:

			return 0

	# LIGHTING DELTAS

	# dr/dy
	@property
	def di(self):
		try:

			return list(map(lambda i: i / (self.y_end - self.y_start), vector_subtract(self.i2, self.i1)))

		except ZeroDivisionError:

			return [0.0, 0.0, 0.0]

	# dn/dy
	@property
	def dn(self):
		try:

			return list(map(lambda n: n / (self.y_end - self.y_start), vector_subtract(self.v2, self.v1)))

		except ZeroDivisionError:

			return [0.0, 0.0, 0.0]

	def __str__(self):
		return "Edge starting at " + str(self.start) + " and ending at " + str(self.end) + ".\n" \
																			"Slope is " + str(self.slope) + "\n"\
																			+ "Dx is " + str(self.dx) + "\n"\
																			+ "Dz is " + str(self.dz)

# Contains basic information about point light sources
class PointLightSource(object):

	def __init__(self, position, color):

		self.position = position
		self.color = color


# ************************************************************************************

# Determines whether or not a polygon should be subject to backface culling
def should_draw_polygon(poly):
	# Backface removal occurs here
	# Compute surface normal using first three points of polygon
	edge_1 = vector_subtract(poly[0], poly[1])
	edge_2 = vector_subtract(poly[0], poly[2])
	unit_normal = get_unit_normal(edge_1, edge_2)
	anchor_constant = vector_dot(unit_normal, poly[0])
	return vector_dot(unit_normal, [0, 0, d]) + anchor_constant > 0, unit_normal


# This creates an Edge object from a starting and an ending point given in Cartesian coordinates
# The coordinates are projected and converted to canvas coordinates to build the edge
def generate_projected_edge(start_point, end_point):

	projected_start = convert_to_display_coordinates(project(start_point))
	projected_end = convert_to_display_coordinates(project(end_point))

	# Floor the x and y values to keep calculations discrete and prevent the fill from doing wicked overflows
	projected_start[0] = math.floor(projected_start[0])
	projected_start[1] = math.floor(projected_start[1])
	projected_end[0] = math.floor(projected_end[0])
	projected_end[1] = math.floor(projected_end[1])
	
	return Edge(projected_start, projected_end)

	
# This is just shorthand for calling draw() on all polygons in the scene
def draw_objects(scene_objects):
	global pixel_drawing_canvas
	global z_buffer
	z_buffer = [[None for y in range(canvas_height)] for x in range(canvas_width)]  # 2D array of NoneType
	pixel_drawing_canvas = PhotoImage(width=canvas_width, height=canvas_height)
	w.create_image((canvas_width / 2, canvas_height / 2), image=pixel_drawing_canvas)
	for polyhedron in scene_objects:
		polyhedron.draw()


# This function will draw a polygon by repeatedly calling drawLine on each pair of points
# making up the object.  Remember to draw a line between the last point and the first.
def draw_poly(poly, color, polyhedron):

	global z_buffer
	edge_table = []
	points = len(poly)

	# Only fill if polygon filling is enabled
	if polygon_draw_mode < 2:

		# calculate color for polygon here if lambert shading is active
		if shading_model_state == 0:
			final_color_values = get_lit_color(polyhedron.base_color, poly.unit_normal, polyhedron.reflection_color)

		# Generate all of the edges in the polygon
		if DEBUG:
			print('Drawing polygon with {} points.'.format(points))
		for point in range(points):
			next_i = (point + 1) % points
			edge = generate_projected_edge(poly[point], poly[(point + 1) % points])
			if shading_model_state > 0:
				# calculate vertex normals
				# TODO maybe update for other polyhedrons
				vertex_normal1 = normalize_vector(vector_add(poly.unit_normal, poly.neighbours[point].unit_normal))
				vertex_normal2 = normalize_vector(vector_add(poly.unit_normal, poly.neighbours[next_i].unit_normal))
				edge.set_vertex_normals(vertex_normal1, vertex_normal2, polyhedron.base_color, polyhedron.reflection_color)
			# Ignore horizontal edges
			if edge.slope != 0:
				if DEBUG:
					print('Edge added')
				edge_table.append(edge)

		# sort edges by y value
		edge_table.sort(key=lambda edge_obj: edge_obj.y_start)

		if DEBUG:
			for end_edge in edge_table:
				print(end_edge)

		# compute starting y and ending y
		y_min = edge_table[0].y_start
		y_max = edge_table[-1].y_end

		if DEBUG:
			print("Vertical Distance:", y_max - y_min)
			if DRAW_DEBUG > 1:
				w.create_line(0, y_min, canvas_width, y_min)
				w.create_line(0, y_max, canvas_width, y_max)

		start_edge = edge_table.pop(0)
		end_edge = edge_table.pop(0)

		# if the first two active edges start from the same point, make sure that the first edge has the lower dx
		if start_edge.x_start == end_edge.x_start:
			if start_edge.dx > end_edge.dx:
				start_edge, end_edge = end_edge, start_edge
		elif start_edge.x_start > end_edge.x_start:
			start_edge, end_edge = end_edge, start_edge

		# offset from where to start drawing and on which to iterate with dx/dy partial
		first_edge_x = start_edge.x_start
		end_edge_x = end_edge.x_start

		if shading_model_state == 1:
			first_edge_i = start_edge.i1
			end_edge_i = end_edge.i1
		elif shading_model_state == 2:
			first_edge_n = start_edge.v1
			end_edge_n = end_edge.v1

		# same offset but for dz/dy
		first_edge_z = start_edge.z_start
		end_edge_z = end_edge.z_start

		# go down the polygon and fill it
		for scan_y in range(int(y_min), int(y_max)):
			if DEBUG:
				print('Ticking scan line...')
			if DRAW_DEBUG < 0:
				w.create_line(first_edge_x, scan_y, end_edge_x, scan_y)
			else:
				start_value = int(first_edge_x)
				end_value = int(end_edge_x)
				if shading_model_state == 1:
					start_intensity = start_edge.i1
					end_intensity = end_edge.i2
				elif shading_model_state == 2:
					start_normal = start_edge.v1
					end_normal = end_edge.v2
				# calculate the change in z over the horizontal line
				try:
					dx = float(end_value - start_value)
					z_partial_x = (end_edge_z - first_edge_z) / dx
					if shading_model_state == 1:
						i_partial_x = list(map(lambda i: i / dx, vector_subtract(end_intensity, start_intensity)))
					elif shading_model_state == 2:
						n_partial_x = list(map(lambda n: n / dx, vector_subtract(end_normal, start_normal)))
				except ZeroDivisionError:
					z_partial_x = 0
					if shading_model_state == 1:
						i_partial_x = [0, 0, 0]
					elif shading_model_state == 2:
						n_partial_x = [0, 0, 0]
				current_z = first_edge_z
				if shading_model_state == 1:
					current_i = start_intensity
				elif shading_model_state == 2:
					current_n = start_normal
				# fill the polygon on the current scan line
				for x in range(start_value, end_value):
					# calculate immediate z position using dx partial of z
					if DEBUG:
						print('Buffer values:\n\tx: {}\n\ty: {}\n\tBuffer value at coordinates: {}\n\tCurrent Z: {}'
							.format(x, scan_y, z_buffer[x][scan_y], current_z))
					# if buffer slot is empty or the current object dot is closer (-z) or z-buffering is disabled
					if z_buffer[x][scan_y] is None or current_z < z_buffer[x][scan_y] or not z_buffering:
						z_buffer[x][scan_y] = current_z

						if shading_model_state == 1:
							final_color_values = current_i
						elif shading_model_state == 2:
							final_color_values = get_lit_color(polyhedron.base_color, current_n, polyhedron.reflection_color)

						# Build color string
						# print(final_color_values)
						color_value_strings = list(
							map(
								lambda i: '00' if len(i) == 0 else (('0' + i) if len(i) == 1 else i),
								map(
									lambda i: str(hex(int(i)))[2::], final_color_values
								)
							)
						)
						color_string = "#{}{}{}".format(*color_value_strings)
						# The PhotoImage class doesn't like negative coordinates
						if x >= 0 and scan_y >= 0:
							pixel_drawing_canvas.put(color_string, (x, scan_y))
					current_z += z_partial_x
					if shading_model_state == 1:
						current_i = vector_add(current_i, i_partial_x)
					elif shading_model_state == 2:
						current_n = vector_add(current_n, n_partial_x)

			popped = False
			# Check and update leftmost edge
			if scan_y >= math.floor(start_edge.y_end):
				if DEBUG:
					print("Popping table to first edge.")
				start_edge = edge_table.pop(0)
				popped = True
			# Check and update rightmost edge
			if scan_y >= math.floor(end_edge.y_end):
				if DEBUG:
					print("Popping table to end edge.")
				end_edge = edge_table.pop(0)
				popped = True

			# Ensure that the correct edges have been assigned at the bottom of the polygon
			if popped:
				if start_edge.x_end == end_edge.x_end and start_edge.dx < end_edge.dx:
					start_edge, end_edge = end_edge, start_edge

			# Increment the drawing bounds
			first_edge_x += start_edge.dx
			end_edge_x += end_edge.dx

			# Increment the z-values
			first_edge_z += start_edge.dz
			end_edge_z += end_edge.dz

			if shading_model_state == 1:
				first_edge_i = vector_add(first_edge_i, start_edge.di)
				end_edge_i = vector_add(end_edge_i, end_edge.di)
			elif shading_model_state == 2:
				first_edge_n = vector_add(first_edge_n, start_edge.dn)
				end_edge_n = vector_add(end_edge_n, end_edge.dn)

			if DEBUG:
				print('First edge x changed by {} to {}. End edge x changed by {} to {}.\n'
					.format(start_edge.dx, first_edge_x, end_edge.dx, end_edge_x)
					+ 'First edge z changed by {} to {}. End edge z changed by {} to {}'
					.format(start_edge.dz, first_edge_z, end_edge.dz, end_edge_z))

	# Draw edges if enabled
	if polygon_draw_mode > 0:
		for scan_y in range(len(poly)):
			draw_line(poly[scan_y], poly[(scan_y + 1) % points], color)


# Project the 3D endpoints to 2D point using a perspective projection implemented in 'project'
# Convert the projected endpoints to display coordinates via a call to 'convertToDisplayCoordinates'
# draw the actual line using the built-in create_line method
# Method returns an edge object with information about projected coordinates
def draw_line(start, end, color):
	# for the start and end points, calculate their projections and convert those points to points representative of the
	# 	tkinter canvas layout, then draw the line
	start_display = convert_to_display_coordinates(project(start))
	end_display = convert_to_display_coordinates(project(end))
	w.create_line(start_display[0], start_display[1], end_display[0], end_display[1], fill=color)

	if DRAW_DEBUG:
		w.create_text(start_display[0], start_display[1],
					text=str([math.floor(start_display[0]), math.floor(start_display[1])]), fill='green', font='bold')


# This function converts from 3D to 2D (+ depth) using the perspective projection technique.  Note that it
# will return a NEW list of points.  We will not want to keep around the projected points in our object as
# they are only used in rendering
def project(point):
	# Calculate the projection of the point on the display surface based on an assumed perspective distance from the
	# 	viewport, d, and the z position of the point
	ps = [d * point[0] / (d + point[2]),
		d * point[1] / (d + point[2]),
		point[2] / (d + point[2])]

	return ps


# This function converts a 2D point to display coordinates in the tk system.  Note that it will return a
# NEW list of points.  We will not want to keep around the display coordinate points in our object as 
# they are only used in rendering.
def convert_to_display_coordinates(point):
	# Based on the dimensions of the canvas, calculate the coordinates on the canvas that match the two-dimensional
	# 	cartesian coordinates of the point
	origin_x = canvas_width / 2
	origin_y = canvas_height / 2
	display_coordinate = [point[0] + origin_x, origin_y - point[1], point[2]]  # y = 0 is top
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


# Returns the result of subtracting two vectors of any dimension
def vector_subtract(minuend, subtrahend):
	# This will throw an error if the two vectors are of varying lengths
	assert len(minuend) == len(subtrahend)
	return [minuend[i] - subtrahend[i] for i in range(len(minuend))]


def vector_add(addend1, addend2):
	assert len(addend1) == len(addend2)
	return list(map(lambda i, j: i + j, addend1, addend2))


# Calculates the unit surface normal of a plane defined by two lines
def get_unit_normal(v1, v2):
	normal = [
		v1[1] * v2[2] - v1[2] * v2[1],
		v1[2] * v2[0] - v1[0] * v2[2],
		v1[0] * v2[1] - v1[1] * v2[0]
	]

	return normalize_vector(normal)


def normalize_vector(vector):

	magnitude = math.sqrt(vector[0] ** 2 + vector[1] ** 2 + vector[2] ** 2)

	return list(map(lambda i: i / magnitude, vector))


# Calculates the dot product of two vectors in any dimension
def vector_dot(v1, v2):
	# Ensure the two vectors are the same lengths
	assert len(v1) == len(v2)
	product = 0
	for i in range(len(v1)):
		product += v1[i] * v2[i]

	return product


# Calculates the color based on the current lighting model and some variable parameteres
def get_lit_color(base_color, normal, specular_reflectivity):
	# start with the ambient component
	final_lighting = map(lambda k, i: k * i, base_color, ambient_light_intensity)

	if lighting_model_state > 0:
		# TODO using the color of the source for intensity, have the intensity decrease using exp() as object moves away?
		# calculate point diffuse component when applicable
		for source in light_sources:
			point_intensity = source.color
			light_position = normalize_vector(list(map(lambda i: -i, source.position)))  # L
			point_diffuse_component = map(lambda i, k: max(i * k * vector_dot(normal, light_position), 0),
										point_intensity, base_color)
			final_lighting = map(lambda a, b: a + b, final_lighting, point_diffuse_component)
			if lighting_model_state == 2:
				view_vector = normalize_vector([0, 0, d])
				cos_fi = vector_dot(normal, light_position)
				if cos_fi == 0:
					reflection_vector = map(lambda l: -l, light_position)
				elif cos_fi > 0:
					reflection_vector = map(lambda n, l: n - (l / (2*cos_fi)), normal, light_position)
				else:
					reflection_vector = map(lambda n, l: -n + (l / (2*cos_fi)), normal, light_position)
				cos_theta = vector_dot(view_vector, normalize_vector(list(reflection_vector)))
				specular_component = map(lambda i, k: i * k * cos_theta ** n, point_intensity, specular_reflectivity)
				final_lighting = list(map(lambda a, b: a + b, final_lighting, specular_component))
				# print(final_lighting)

	return list(map(lambda i, k: max(min(k, i), 0), final_lighting, base_color))


# Program globals
objects = [
	Tube([0, 0, 0], [0xBB, 0xBB, 0xBB], [0xBB, 0x00, 0x00])
	# Pyramid([0, 0, 0], lambda i: "#{}00{}".format(i, str(hex(0xFF - int("0x" + i, 16)))[2::])),  # red pyramid
	# Pyramid([100, 300, 500], lambda i: "#00{}00".format(i)),  # green pyramid
	# Cube([200, -100, 200], lambda i: "#0000{}".format(i)),  # blue cube
	# Cube([-600, 400, 3000], lambda i: "#{}{}{}".format(i, i, i))  # gray cube

]
current_object_index = 0
pixel_drawing_canvas = None
z_buffer = None  # initialize for global use
ambient_light_intensity = [0.3, 0.3, 0.3]
light_sources = [PointLightSource([1.0, 1.0, -1.0], [1.0, 1.0, 1.0])]
n = 1

# **************************************************************************
# Everything below this point implements the interface

ANSI_RED = "\033[1;31m"
ANSI_END = "\033[0;0m"


def reset():
	w.delete(ALL)
	objects[current_object_index].reset()
	draw_objects(objects)
	print(ANSI_RED + "Object {} reset.".format(current_object_index) + ANSI_END)


def larger():
	w.delete(ALL)
	objects[current_object_index].scale(1.1)
	draw_objects(objects)
	print(ANSI_RED + "Object {} scaled up.".format(current_object_index) + ANSI_END)


def smaller():
	w.delete(ALL)
	objects[current_object_index].scale(.9)
	draw_objects(objects)
	print(ANSI_RED + "Object {} scaled down.".format(current_object_index) + ANSI_END)


def forward():
	w.delete(ALL)
	objects[current_object_index].translate([0, 0, 20])
	draw_objects(objects)
	print(ANSI_RED + "Object {} moved forward.".format(current_object_index) + ANSI_END)


def backward():
	w.delete(ALL)
	objects[current_object_index].translate([0, 0, -20])
	draw_objects(objects)
	print(ANSI_RED + "Object {} moved backward.".format(current_object_index) + ANSI_END)


def left():
	w.delete(ALL)
	objects[current_object_index].translate([-20, 0, 0])
	draw_objects(objects)
	print(ANSI_RED + "Object {} moved left.".format(current_object_index) + ANSI_END)


def right():
	w.delete(ALL)
	objects[current_object_index].translate([20, 0, 0])
	draw_objects(objects)
	print(ANSI_RED + "Object {} moved right.".format(current_object_index) + ANSI_END)


def up():
	w.delete(ALL)
	objects[current_object_index].translate([0, 20, 0])
	draw_objects(objects)
	print(ANSI_RED + "Object {} moved up.".format(current_object_index) + ANSI_END)


def down():
	w.delete(ALL)
	objects[current_object_index].translate([0, -20, 0])
	draw_objects(objects)
	print(ANSI_RED + "Object {} moved down.".format(current_object_index) + ANSI_END)


def x_plus():
	w.delete(ALL)
	objects[current_object_index].rotate_x(10)
	draw_objects(objects)
	print(ANSI_RED + "Object {} rotated clockwise (+) about x-axis.".format(current_object_index) + ANSI_END)


def x_minus():
	w.delete(ALL)
	objects[current_object_index].rotate_x(-10)
	draw_objects(objects)
	print(ANSI_RED + "Object {} rotated counterclockwise (-) about x-axis.".format(current_object_index) + ANSI_END)


def y_plus():
	w.delete(ALL)
	objects[current_object_index].rotate_y(10)
	draw_objects(objects)
	print(ANSI_RED + "Object {} rotated clockwise (+) about y-axis.".format(current_object_index) + ANSI_END)


def y_minus():
	w.delete(ALL)
	objects[current_object_index].rotate_y(-10)
	draw_objects(objects)
	print(ANSI_RED + "Object {} rotated counterclockwise (-) about y-axis.".format(current_object_index) + ANSI_END)


def z_plus():
	w.delete(ALL)
	objects[current_object_index].rotate_z(10)
	draw_objects(objects)
	print(ANSI_RED + "Object {} rotated counterclockwise (+) about z-axis.".format(current_object_index) + ANSI_END)


def z_minus():
	w.delete(ALL)
	objects[current_object_index].rotate_z(-10)
	draw_objects(objects)
	print(ANSI_RED + "Object {} rotated clockwise (-) about z-axis.".format(current_object_index) + ANSI_END)


def select():
	global current_object_index
	current_object_index = (current_object_index + 1) % len(objects)
	print(ANSI_RED + 'Selection changed to index {}.'.format(current_object_index) + ANSI_END)
	if polygon_draw_mode > 0:
		w.delete(ALL)
		draw_objects(objects)


def change_ambient_intensity(value):
	global ambient_light_intensity
	ambient_light_intensity = list(map(lambda i: min(1, max(i + value, 0)), ambient_light_intensity))
	print(ANSI_RED + "Changed ambient light intensity by {} ".format(value) +
		"to {}".format(ambient_light_intensity) + ANSI_END)
	w.delete(ALL)
	draw_objects(objects)


def change_n(value):
	global n
	n += value
	w.delete(ALL)
	draw_objects(objects)


def change_rgb(i, value):
	global light_sources
	old = light_sources[0].color[i]
	light_sources[0].color[i] = min(1.0, max(0, old + value))
	w.delete(ALL)
	draw_objects(objects)


# toggles backface culling of objects and redraws them
# Bound to the 'B' key
def toggle_backface_culling(event):
	global cull_backface
	cull_backface = not cull_backface
	print("Toggled backface culling " + ("on" if cull_backface else "off"))
	w.delete(ALL)
	draw_objects(objects)


# toggles filling of object faces and redraws them
# Bound to the 'F' key
def toggle_polygon_filling(event):
	global polygon_draw_mode
	polygon_draw_mode = (polygon_draw_mode + 1) % 3
	modes = ["'polygon fill only", "'polygon fill and wire-frame", "'wire-frame only"]
	print("Polyhedron render mode set to {}.'".format(modes[polygon_draw_mode]))
	w.delete(ALL)
	draw_objects(objects)


# toggles z-buffering objects and redraws them
# Bound to the 'Z' key
def toggle_zbuffering(event):
	global z_buffering
	z_buffering = not z_buffering
	print("Toggled z-buffering " + ("on" if z_buffering else "off"))
	w.delete(ALL)
	draw_objects(objects)


def rotate_lighting_model(event):
	global lighting_model_state
	lighting_model_state = (lighting_model_state + 1) % 3
	print("Rotated lighting model to " +
		  ["ambient diffuse only",
		   "ambient diffuse + point diffuse",
		   "ambient diffuse + point diffuse + point specular"
		   ][lighting_model_state] + ".")
	w.delete(ALL)
	draw_objects(objects)


def toggle_shading_model(event):
	global shading_model_state
	shading_model_state = (shading_model_state + 1) % 3
	print("Toggled shading model to " +
		  ["faceted shading",
		   "Goraud shading",
		   "Phong shading"
		   ][shading_model_state] + ".")
	w.delete(ALL)
	draw_objects(objects)


root = Tk()
# bind toggles
root.bind('b', toggle_backface_culling)
root.bind('f', toggle_polygon_filling)
root.bind('z', toggle_zbuffering)
root.bind('l', rotate_lighting_model)
root.bind('s', toggle_shading_model)
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

lighting_controls = Frame(control_panel, borderwidth=2, relief=RIDGE)
lighting_controls.pack(side=LEFT)

lighting_controls_label = Label(lighting_controls, text="Lighting")
lighting_controls_label.pack(side=TOP)

ambientPlusButton = Button(lighting_controls, text="I+", command=lambda: change_ambient_intensity(0.1))
ambientPlusButton.pack(side=LEFT)

ambientMinusButton = Button(lighting_controls, text="I-", command=lambda: change_ambient_intensity(-0.1))
ambientMinusButton.pack(side=LEFT)

nminus = Button(lighting_controls, text="n-", command=lambda: change_n(-2))
nminus.pack(side=LEFT)
nplus = Button(lighting_controls, text="n+", command=lambda: change_n(2))
nplus.pack(side=LEFT)

rminus = Button(lighting_controls, text="r-", command=lambda: change_rgb(0, -0.1))
rminus.pack(side=LEFT)
rplus = Button(lighting_controls, text="r+", command=lambda: change_rgb(0, 0.1))
rplus.pack(side=LEFT)

gminus = Button(lighting_controls, text="g-", command=lambda: change_rgb(1, -0.1))
gminus.pack(side=LEFT)
gplus = Button(lighting_controls, text="g+", command=lambda: change_rgb(1, 0.1))
gplus.pack(side=LEFT)

bminus = Button(lighting_controls, text="b-", command=lambda: change_rgb(2, -0.1))
bminus.pack(side=LEFT)
bplus = Button(lighting_controls, text="b+", command=lambda: change_rgb(2, 0.1))
bplus.pack(side=LEFT)

root.mainloop()
