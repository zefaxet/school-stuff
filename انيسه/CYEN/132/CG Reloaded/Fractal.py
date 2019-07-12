######################################################################################################################
# Name: Anisah Alahmed
# Date: 5/13/2019
# Description: The definitions of the Point class, the Fractal superclass, and the various fractal implementations
######################################################################################################################
from math import sin, cos, pi

# the 2D point class
class Point(object):

	# init point, takes optional x and y parameters
	def __init__(self, x=0.0, y=0.0):
		# set instance variables
		self.x = x
		self.y = y

	# x accessor
	@property
	def x(self):
		return self._x

	# x mutator
	@x.setter
	def x(self, value):
		self._x = float(value)

	# y accessor
	@property
	def y(self):
		return self._y

	# y mutator
	@y.setter
	def y(self, value):
		self._y = float(value)

	# calculates the distance between this point and another point
	def dist(self, other):
		a = self.x - other.x
		b = self.y - other.y
		# sqrt(a^2 - b^2)
		result = (a ** 2 + b ** 2) ** 0.5
		return result

	# calculates the midpoint between this point and another point
	def midpt(self, other):
		x = (self.x + other.x) / 2
		y = (self.y + other.y) / 2
		# { (x1 + x2) / 2, (y1 + y2) / 2 }
		return Point(x, y)

	def interpt(self, other, r):
		# make sure that the distance ratio is expressed from a
		#  smaller component value to a larger one
		# first, the x-component
		rx = r
		if (self.x > other.x):
			rx = 1.0 - r
		# next, the y-component
		ry = r
		if (self.y > other.y):
			ry = 1.0 - r

		# calculate the new point's coordinates
		# the difference in the components (distance between the
		#  points) is first scaled by the specified distance ratio
		# the minimum of the components is then added back in order
		#  to obtain the coordinates in between the two points (and
		#  not with respect to the origin)
		x = abs(self.x - other.x) * rx + min(self.x, other.x)
		y = abs(self.y - other.y) * ry + min(self.y, other.y)

		return Point(x, y)

	# get the string representation of a point in the form (x,y)
	def __str__(self):

		return "({},{})".format(self.x, self.y)

#fractal superclass which will be used later for defining specific fractals
class Fractal:

	def __init__(self, dimensions):
		# the canvas dimensions
		self.dimensions = dimensions
		# the default number of points to plot is 50,000
		self.num_points = 50000
		# the default distance ratio is 0.5 (halfway)
		self.r = 0.5
		self.vertices = []

	def frac_x(self, r):
		return int((self.dimensions["max_x"] - self.dimensions["min_x"]) * r) + \
				self.dimensions["min_x"]

	def frac_y(self, r):
		return int((self.dimensions["max_y"] - self.dimensions["min_y"]) * r) + \
				self.dimensions["min_y"]

# The sierpinski triangle uses the fractal superclass defaults
# we just need to define the vertices
class SierpinskiTriangle(Fractal):

	def __init__(self, dimensions):
		Fractal.__init__(self, dimensions)
		self.vertices.append(Point(self.dimensions["mid_x"], self.dimensions["min_y"]))
		self.vertices.append(Point(self.dimensions["min_x"], self.dimensions["max_y"]))
		self.vertices.append(Point(self.dimensions["max_x"], self.dimensions["max_y"]))

# definition of the sierpinski carpet
class SierpinskiCarpet(Fractal):

	def __init__(self, dimensions):
		Fractal.__init__(self, dimensions)
		self.num_points = 100000
		self.r = 0.66
		self.vertices.append(Point(self.dimensions["min_x"], self.dimensions["min_y"]))
		self.vertices.append(Point(self.dimensions["mid_x"], self.dimensions["min_y"]))
		self.vertices.append(Point(self.dimensions["max_x"], self.dimensions["min_y"]))
		self.vertices.append(Point(self.dimensions["min_x"], self.dimensions["mid_y"]))
		self.vertices.append(Point(self.dimensions["max_x"], self.dimensions["mid_y"]))
		self.vertices.append(Point(self.dimensions["min_x"], self.dimensions["max_y"]))
		self.vertices.append(Point(self.dimensions["mid_x"], self.dimensions["max_y"]))
		self.vertices.append(Point(self.dimensions["max_x"], self.dimensions["max_y"]))

#definition of the pentagonal fractal
class Pentagon(Fractal):

	def __init__(self, dimensions):
		Fractal.__init__(self, dimensions)
		self.r = 0.618
		frac = self.frac_y(0.5375)
		mid_x = self.dimensions["mid_x"]
		mid_y = self.dimensions["mid_y"]
		for i in xrange(2, 12, 2):
			cosValue = cos(i * pi / 5 + 60)
			sinValue = sin(i * pi / 5 + 60)
			self.vertices.append(Point(mid_x + mid_x * cosValue, frac + mid_y * sinValue))

#definition of the hexagonal fractal
class Hexagon(Fractal):

	def __init__(self, dimensions):
		Fractal.__init__(self, dimensions)
		self.r = 0.665
		self.vertices.append(Point(self.dimensions["mid_x"], self.dimensions["min_y"]))
		self.vertices.append(Point(self.dimensions["min_x"], self.frac_y(0.25)))
		self.vertices.append(Point(self.dimensions["max_x"], self.frac_y(0.25)))
		self.vertices.append(Point(self.dimensions["min_x"], self.frac_y(0.75)))
		self.vertices.append(Point(self.dimensions["max_x"], self.frac_y(0.75)))
		self.vertices.append(Point(self.dimensions["mid_x"], self.dimensions["max_y"]))

#definition of the octagonal fractal
class Octagon(Fractal):

	def __init__(self, dimensions):
		Fractal.__init__(self, dimensions)
		self.num_points = 75000
		self.r = 0.705
		self.vertices.append(Point(self.frac_x(0.2925), self.dimensions["min_y"]))
		self.vertices.append(Point(self.frac_x(0.7075), self.dimensions["min_y"]))
		self.vertices.append(Point(self.dimensions["min_x"], self.frac_y(0.2925)))
		self.vertices.append(Point(self.dimensions["max_x"], self.frac_y(0.2925)))
		self.vertices.append(Point(self.dimensions["min_x"], self.frac_y(0.7075)))
		self.vertices.append(Point(self.dimensions["max_x"], self.frac_y(0.7075)))
		self.vertices.append(Point(self.frac_x(0.2925), self.dimensions["max_y"]))
		self.vertices.append(Point(self.frac_x(0.7075), self.dimensions["max_y"]))