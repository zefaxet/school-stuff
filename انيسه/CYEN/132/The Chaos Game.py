######################################################################################################################
# Name: Anisah Alahmed
# Date: 4/4/2019
# Description: Build a sierpenski triangle out of 50000 points
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

# the chaos game class: (0,0) is in the top-left corner
# inherits from the Canvas class of Tkinter
class ChaosGame(Canvas):

	def __init__(self, master):
		Canvas.__init__(self, master)
		#create the vertex Point objects
		self.vertices = [Point(MID_X, MIN_Y), Point(MIN_X, MAX_Y), Point(MAX_X, MAX_Y)]
		#plot the vertices
		[self.plotPoint(x, 2, 'red') for x in self.vertices]
		#add to tkinter window, take all available space
		self.pack(fill=BOTH, expand=True)

	#plot a number of points on this canvas
	def plotPoints(self, numPoints):
		#choose a random vertex to start with
		lastPoint = self.vertices[randint(0,2)]
		for x in xrange(numPoints):
			#plot the midpoint between the last point and a random vertex
			lastPoint = lastPoint.midpt(self.vertices[randint(0,2)])
			self.plotPoint(lastPoint, 0, "pink")

	def plotPoint(self, point, radius, color):
		#use the radius to get the corner coordinates of the bounding box
		pointXFirst = point.x - radius
		pointYFirst = point.y - radius
		pointXLast = point.x + radius
		pointYLast = point.y + radius
		#add point to canvas with bounding box coordinates and color
		self.create_oval(pointXFirst, pointYFirst, pointXLast, pointYLast, outline=color, fill=color)

##########################################################
# the default size of the canvas is 700x700
WIDTH = 700
HEIGHT = 700

MIN_X = 4
MIN_Y = 4
MAX_X = 695
MAX_Y = 695

MID_X = (MAX_X + MIN_X) / 2
MID_Y = (MAX_Y + MIN_Y) / 2
# the number of points to plot
NUM_POINTS = 50000

# create the window
window = Tk()
window.geometry("{}x{}".format(WIDTH, HEIGHT))
window.title("The Chaos Game")
# create the coordinate system as a Tkinter canvas inside the window
s = ChaosGame(window)
# plot some random points
s.plotPoints(NUM_POINTS)
# wait for the window to close
window.mainloop()
