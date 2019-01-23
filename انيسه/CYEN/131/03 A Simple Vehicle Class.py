######################################################################################################################
# Name: Anisah Alahmed
# Date: 12/17/2018
# Description: Simple vehicle class with year make and model
######################################################################################################################

# the vehicle class
# a vehicle has a year, make, and model
class Vehicle(object):

    #Runs when the class instance is created
    def __init__(self, make, model, year=2000):

        self.make = make
        self.model = model
        self.year = year
    
    #getters and setters for the make variable
    @property
    def make(self):
        return self._make
    
    @make.setter
    def make(self, value):
        self._make = value
    
    #getters and setters for the model variable
    @property
    def model(self):
        return self._model
    
    @model.setter
    def model(self, value):
        self._model = value
    
    #getters and setters for the year variable
    @property
    def year(self):
        return self._year
    
    @year.setter
    def year(self, value):
        #range checking
        if value >= 2000 and value <= 2018:
            self._year = value

# ***DO NOT MODIFY OR REMOVE ANYTHING BELOW THIS POINT!***
# the main part of the program
v1 = Vehicle("Dodge", "Ram")
v2 = Vehicle("Honda", "Odyssey")
print "v1={} {}".format(v1.make, v1.model)
print "v2={} {}".format(v2.make, v2.model)
print

v1.year = 2016
v2.year = 2016
print "v1={} {} {}".format(v1.year, v1.make, v1.model)
print "v2={} {} {}".format(v2.year, v2.make, v2.model)
print

v1.year = 1999
v2.model = "Civic"
v2.year = 2007
print "v1={} {} {}".format(v1.year, v1.make, v1.model)
print "v2={} {} {}".format(v2.year, v2.make, v2.model)

