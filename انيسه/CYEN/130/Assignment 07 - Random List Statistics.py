###########################################################################################
# Name: Anisah Alahmed
# Date: 11/14/2018
# Description: Manually calculates some statistics about a list
###########################################################################################
from random import randint

# function that prompts the user for a list size, minimum and maximum values, creates the list, and returns it
# you must use the list functions discussed in class to add integers to the list

# fills a list with random numbers. the size of the list is given by user
# i didnt see a space for this function in the template so im doing it here
def fillList():

	list = []
	listsize = int(input("How many random integers would you like to add to the list? "))
	rangemin = int(input("What would you like the minimum value to be? "))
	rangemax = int(input("What would you like the maximum value to be? "))
	for i in range(listsize):
		list.append(randint(rangemin, rangemax))
	return list

# function that receives the list as a parameter, and calculates and returns the mean
def mean(list):

	total = 0
	for int in list:
		total += int
	return total / len(list)

# function that receives the list as a parameter, and calculates and returns the median
def median(list):

	list.sort()
	listsize = len(list)
	# if list is even number length
	if listsize % 2 == 0:
		# get the average of the middle 2
		left = list[int(listsize / 2) - 1]
		right = list[int(listsize / 2)]
		return (left + right) / 2
	else:
		return list[int(listsize / 2)]


# function that receives the list as a parameter, and calculates and returns the range
def listrange(list):

	return max(list) - min(list)

###############################################
# MAIN PART OF THE PROGRAM
# implement the main part of your program below
# comments have been added to assist you
###############################################
# create the list
nums = fillList()
# display the list
# there is no need to write/call your own function for this part
print("The list:", nums)

# calculate and display the mean
print("The mean of the list is {}.".format(mean(nums)))

# calculate and display the median
print("The median of the list is {}.".format(median(nums)))

# calculate and display the range
print("The range of the list is {}.".format(listrange(nums)))
