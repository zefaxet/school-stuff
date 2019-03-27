######################################################################################################################
# Name: Anisah Alahmed
# Date: 3/27/2019
# Description: Randomly plots some points in tkinter
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

	def __init__(self, master, pointRadius=0, pointColor=None):
		Canvas.__init__(self, master)
		#set class variables
		self.pointRadius = pointRadius
		self.pointColor = pointColor
		#list of colors to choose from randomly
		self.colors = ["black", "red", "green", "blue", "cyan", "yellow", "magenta"]
		#add to tkinter window, take all available space
		self.pack(fill=BOTH, expand=True)

	#plot a number of points on this canvas
	def plotPoints(self, numPoints):
		for x in xrange(numPoints):
			#create the point with random x and y coordinates
			point = Point(randint(0, WIDTH), randint(0, HEIGHT))
			#if a color is set, use that one
			if not self.pointColor == None:
				color = self.pointColor
			#otherwise use a random one
			else:
				color = self.colors[randint(0, len(self.colors) - 1)]
			#plot the point with the set radius
			self.plotPoint(point, self.pointRadius, color)

	def plotPoint(self, point, radius, color):
		#use the radius to get the corner coordinates of the bounding box
		pointXFirst = point.x - radius
		pointYFirst = point.y - radius
		pointXLast = point.x + radius
		pointYLast = point.y + radius
		#add point to canvas with bounding box coordinates and color
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
