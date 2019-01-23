###########################################################################################
# Name: Anisah Alahmed
# Date: 10/17/2018
# Description: Get drunk recursively
###########################################################################################

# the algorithm implemented recursively
def passSomeBeers(n):
	print("{} bottles of beer on the wall.".format(n))
	print("{} bottles of beer.".format(n))
	print("Take one down, pass it around.")
	n = n - 1
	print("{} bottles of beer on the wall.".format(n))
	print()
	if n > 0:
		passSomeBeers(n) # restarts the function with the decremented value

###############################################
# MAIN PART OF THE PROGRAM
###############################################
passSomeBeers(99)

