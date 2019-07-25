######################################################################################################################
# Name: Anisah Alahmed
# Date: 3/19/2019
# Description: 2D point class that can calcuate distance and midpoint with another Point
######################################################################################################################

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

##########################################################
# ***DO NOT MODIFY OR REMOVE ANYTHING BELOW THIS POINT!***
# create some points
p1 = Point()
p2 = Point(3, 0)
p3 = Point(3, 4)
# display them
print "p1:", p1
print "p2:", p2
print "p3:", p3
# calculate and display some distances
print "distance from p1 to p2:", p1.dist(p2)
print "distance from p2 to p3:", p2.dist(p3)
print "distance from p1 to p3:", p1.dist(p3)
# calculate and display some midpoints
print "midpt of p1 and p2:", p1.midpt(p2)
print "midpt of p2 and p3:", p2.midpt(p3)
print "midpt of p1 and p3:", p1.midpt(p3)
# just a few more things...
p4 = p1.midpt(p3)
print "p4:", p4
print "distance from p4 to p1:", p4.dist(p1)
