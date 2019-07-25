######################################################################################################################
# Name: Anisah Alahmed
# Date: 5/13/2019
# Description: Builds various fractals in a tkinter canvas
######################################################################################################################

from tkinter import *
from random import randint
from Fractal import *

# the chaos game class: (0,0) is in the top-left corner
# inherits from the Canvas class of Tkinter
class ChaosGame(Canvas):

	def __init__(self, master, dimensions, vertex_radius=2, vertex_color="red", point_radius=0, point_color="black"):
		Canvas.__init__(self, master)
		# calculate dimensions
		self.dimensions = dimensions
		self.vertex_radius = 2
		self.vertex_color = "red"
		self.point_radius = 0
		self.point_color = "black"
		self.pack(fill=BOTH, expand=True)

	#plot a number of points on this canvas
	def plotPoints(self, fractal):
		#choose a random vertex to start with
		lastPoint = fractal.vertices[randint(0, len(fractal.vertices) - 1)]
		#plot as many points as defined by the fractal subclass
		for x in xrange(fractal.num_points):
			lastPoint = lastPoint.interpt(fractal.vertices[randint(0, len(fractal.vertices) - 1)], fractal.r)
			self.plotPoint(lastPoint, self.point_radius, self.point_color)

	def plotPoint(self, point, radius, color):
		#use the radius to get the corner coordinates of the bounding box
		pointXFirst = point.x - radius
		pointYFirst = point.y - radius
		pointXLast = point.x + radius
		pointYLast = point.y + radius
		#add point to canvas with bounding box coordinates and color
		self.create_oval(pointXFirst, pointYFirst, pointXLast, pointYLast, outline=color, fill=color)

	def make(self, f):
		#create the fractal represented by the given string
		exec "fractal = {}(self.dimensions)".format(f)
		#plot the fractal's vertices
		for vertex in fractal.vertices:
			self.plotPoint(vertex, self.vertex_radius, self.vertex_color)
		#plot the fractal
		self.plotPoints(fractal)


##########################################################
# the default size of the canvas is 700x700
dimensions = {
	"width": 700,
	"height": 700,
	"min_x": 4,
	"min_y": 4,
	"max_x": 695,
	"max_y": 695
}
# calculate the midpoints
dimensions["mid_x"] = (dimensions["max_x"] + dimensions["min_x"]) / 2
dimensions["mid_y"] = (dimensions["max_y"] + dimensions["min_y"]) / 2

# the implemented fractals
FRACTALS = ["SierpinskiTriangle", "SierpinskiCarpet", "Pentagon", "Hexagon", "Octagon"]

# create the fractals in individual (sequential) windows
for f in FRACTALS:
	window = Tk()
	window.geometry("{}x{}".format(dimensions["width"], dimensions["height"]))
	window.title("The Chaos Game...Reloaded")
	# create the game as a Tkinter canvas inside the window
	s = ChaosGame(window, dimensions)
	# make the current fractal
	s.make(f)
	# wait for the window to close
	window.mainloop()
