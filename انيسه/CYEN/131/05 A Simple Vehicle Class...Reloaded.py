#########################################################
# Name: Anisah Alahmed
# Date: 2018-1-21
# Description: Implements vehicle, truck and car classes.
#########################################################

# the vehicle class
# a vehicle has a year, make, and model
# a vehicle is instantiated with a make and model
# This is all from my assignment 3 work
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
        year = min(value, 2018)
        year = max(value, 2000)
        self._year = year

    def __str__(self):
        # returns a string containing the year, make, and model in that order
        return "{} {} {}".format(self.year, self.make, self.model)

# the truck class
# a truck is a vehicle
# a truck is instantiated with a make and model
class Truck(Vehicle):

	def __init__(self, make, model, year=2000):
		
		Vehicle.__init__(self, make, model, year)

# the car class
# a car is a vehicle
# a car is instantiated with a make and model
class Car(Vehicle):

	def __init__(self, make, model, year=2000):
		
		Vehicle.__init__(self, make, model, year)

# the Dodge Ram class
# a Dodge Ram is a truck
# a Dodge Ram is instantiated with a year
# all Dodge Rams have the same make and model
class DodgeRam(Truck):

	def __init__(self, year=2000):
	
		Truck.__init__(self, 'Dodge', 'Ram', year)

# the Honda Civic class
# a Honda Civic is a car
# a Honda Civic is instantiated with a year
# all Honda Civics have the same make and model
class HondaCivic(Car):

	def __init__(self, year=2000):
	
		Car.__init__(self, 'Honda', 'Civic', year)

# ***DO NOT MODIFY OR REMOVE ANYTHING BELOW THIS POINT!***
# the main part of the program
ram = DodgeRam(2016)
print ram

civic1 = HondaCivic(2007)
print civic1

civic2 = HondaCivic(1999)
print civic2

