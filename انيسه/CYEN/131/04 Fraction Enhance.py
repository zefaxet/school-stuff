######################################################################################################################
# Name: Anisah Alahmed
# Date: 12/22/2018
# Description: Fraction class that can do math on itself
######################################################################################################################

# the fraction class
class Fraction(object):

    def __init__(self, numerator=0, denominator=1):

        self._num = numerator
        self.den = denominator
    
    @property
    def num(self):
        return self._num
    
    @num.setter
    def num(self, value):
        self._num = value
        self.reduce()

    @property
    def den(self):
        return self._den
    
    @den.setter
    def den(self, value):
        if value == 0:
            self._den = 1
        else:
            self._den = value
        self.reduce()
    
    def reduce(self):
        if self.num == 0:
            self._den = 1
            return
        for i in range(self.num, 1, -1):
            if self.num % i == 0 and self.den % i == 0:
                self._num /= i
                self._den /= i
                self.reduce()
                break
    
    def float(self):

        return float(self.num) / float(self.den)

    def __str__(self):

        return "{}/{} ({})".format(self.num, self.den, self.float())
    
    def __add__(self, fraction):

        thisnum = self.num * fraction.den
        thatnum = fraction.num * self.den

        newnum = thisnum + thatnum
        newden = self.den * fraction.den

        return Fraction(newnum, newden)
    
    def __sub__(self, fraction):

        temp = Fraction(- fraction.num, fraction.den)
        return self + temp

    def __mul__(self, fraction):

        num = self.num * fraction.num
        den = self.den * fraction.den
        return Fraction(num, den)
    
    def __div__(self, fraction):

        num = self.num * fraction.den
        den = self.den * fraction.num
        return Fraction(num, den)

    


# ***DO NOT MODIFY OR REMOVE ANYTHING BELOW THIS POINT!***
# the main part of the program
# create some fractions
f1 = Fraction()
f2 = Fraction(5, 8)
f3 = Fraction(3, 4)
f4 = Fraction(1, 0)

# display them
print "f1:", f1
print "f2:", f2
print "f3:", f3
print "f4:", f4

# play around
f3.num = 5
f3.den = 8
f1 = f2 + f3
f4.den = 88
f2 = f1 - f1
f3 = f1 * f1
f4 = f4 / f3

# display them again
print
print "f1:", f1
print "f2:", f2
print "f3:", f3
print "f4:", f4

