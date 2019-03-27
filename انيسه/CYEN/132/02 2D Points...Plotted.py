######################################################################################################################
# Name: 
# Date: 
# Description: 
######################################################################################################################

from tkinter import *
from random import randint

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

		# get the string representation of a point in the form (x,y)
		def __str__(self):

			return "({},{})".format(self.x, self.y)

# the coordinate system class: (0,0) is in the top-left corner
# inherits from the Canvas class of Tkinter
class CoordinateSystem(Canvas):

	def __init__(self, master, pointRadius=0):
		Canvas.__init__(self, master)
		self.pointRadius = pointRadius
		self.pack(fill=BOTH, expand=True)

	def plotPoints(self, numPoints):
		for x in xrange(numPoints):
			point = Point(randint(0, WIDTH), randint(0, HEIGHT))
			color = "#%06X" % randint(0, 0xffffff)
			self.plotPoint(point, self.pointRadius, color)

	def plotPoint(self, point, radius, color):
		pointXFirst = point.x - radius
		pointYFirst = point.y - radius
		pointXLast = point.x + radius
		pointYLast = point.y + radius
		self.create_oval(pointXFirst, pointYFirst, pointXLast, pointYLast, outline=color)

##########################################################
# ***DO NOT MODIFY OR REMOVE ANYTHING BELOW THIS POINT!***
# the default size of the canvas is 800x800
WIDTH = 800
HEIGHT = 800
# the number of points to plot
NUM_POINTS = 5000

# create the window
window = Tk()
window.geometry("{}x{}".format(WIDTH, HEIGHT))
window.title("2D Points...Plotted")
# create the coordinate system as a Tkinter canvas inside the window
s = CoordinateSystem(window)
# plot some random points
s.plotPoints(NUM_POINTS)
# wait for the window to close
window.mainloop()
