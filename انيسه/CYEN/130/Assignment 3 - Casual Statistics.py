###########################################################################################
# Name: Anisah Alahmed
# Date: 10/12/18
# Description: Script that does basic math functions on three user-sourced inputs
###########################################################################################

# function that prompts the user to enter an integer and returns it
def prompt():

    return int(input("Enter an integer: "))

# function that receives three integers as parameters and returns the minimum of the three
def minimum(i, j, k):

    minimum = i

    if j < minimum:

        minimum = j

    if k < minimum:

        minimum = k

    return minimum

# function that receives three integers as parameters and returns the maximum of the three
def maximum(i, j, k):

    maximum = i

    if j > maximum:

        maximum = j

    if k > maximum:

        maximum = k

    return maximum

# function that receives three integers as parameters, and calculates and returns the mean
def mean(i, j, k):

    return float(i+j+k)/3

# function that receives three integers as parameters, and calculates and returns the median
def median(i, j, k):

    numbers = [i,j,k]
    numbers.sort()

    return numbers[1]

# function that receives three integers as parameters, and calculates and returns the mode
def mode(i, j, k):

    if i == j or i == k:

        return i

    if j == k:

        return j

    return "undefined"

# function that receives three integers as parameters, and calculates and returns the range
def range3(i, j, k):

    ma = maximum(i, j, k)
    mi = minimum(i, j, k)

    return ma - mi

###############################################
# MAIN PART OF THE PROGRAM
# implement the main part of your program below
# comments have been added to assist you
###############################################
# get three integers from the user

i = prompt()
j = prompt()
k = prompt()

# determine and display the minimum value
print("The minimum value is " + str(minimum(i,j,k)) + ".")

# determine and display the maximum value
print("The maximum value is " + str(maximum(i,j,k)) + ".")

# calculate and display the mean
print("The mean is " + str(mean(i,j,k)) + ".")

# calculate and display the median
print("The median is " + str(median(i,j,k)) + ".")

# calculate and display the mode
print("The mode is " + str(mode(i,j,k)) + ".")

# calculate and display the range
print("The range is " + str(range3(i,j,k)) + ".")

