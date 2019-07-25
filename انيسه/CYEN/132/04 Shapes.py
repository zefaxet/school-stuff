######################################################################################################################
# Name: Anisah Alahmed
# Date: 4/20/2019
# Description: Add parallelogram to shapes
######################################################################################################################

# class shape from textbook
class Shape(object):
	def __init__(self, h=1, w=1):
		self.height = max(h, 1)
		self.width = max(w, 1)
	
	@property
	def height(self):
		return self._height
	
	@height.setter
	def height(self, value):
		if value > 0:
			self._height = value
	
	@property
	def width(self):
		return self._width
	
	@width.setter
	def width(self, value):
		if value > 0:
			self._width = value
	
	#new __str__ function for [rinting rectangle and square
	def __str__(self):
		#lines of shape stored here
		lines = []
		#go down the shape
		for i in range(self.width):
			#build the line and add it to the list of lines
			lines.append( "* " * self.height )
		#join the lines together into a single string
		return "\n".join(lines) + "\n"
	
#rectangle shape from textbook with renamed h parameter
class Rectangle(Shape):
	def __init__(self, h, w):
		Shape.__init__(self, h, w)

#square shape from textbook with renamed h parameter		
class Square(Shape):
	def __init__(self, h):
		Shape.__init__(self, h, h)

#new triangle shape
class Triangle(Shape):
	def __init__(self, h):
		Shape.__init__(self, h, h)
	
	def __str__(self):
		#lines of the triangle stored here
		lines = []
		#go down the triangle, decreasing the length of the lines by one star each time
		for i in range(self.height, 0, -1):
			lines.append( "* " * i )
		#return the shape all together
		return "\n".join(lines) + "\n"

#new parallelogram
class Parallelogram(Shape):
	def __init__(self, l, w):
		Shape.__init__(self, l, w)
	
	def __str__(self):
		#lines of the parallelogram stored here
		lines = []
		#for the number of rows, but from high to low
		for i in range(self.width, 0, -1):
			#the amount of space at the top of the shape is the number of rows - 1, so the for loop will decrement the leading space for us
			line = "  " * (i - 1) + "* " * self.height
			lines.append(line)
		#return the shape all together
		return "\n".join(lines) + "\n"

##########################################################
# ***DO NOT MODIFY OR REMOVE ANYTHING BELOW THIS POINT!***
# create and display several shapes
r1 = Rectangle(12, 4)
print r1
s1 = Square(6)
print s1
t1 = Triangle(7)
print t1
p1 = Parallelogram(10, 3)
print p1
r2 = Rectangle(0, 0)
print r2
p1.width = 2
p1.width = -1
p1.height = 2
print p1

