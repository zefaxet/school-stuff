###########################################################################################
# Name: Anisah Alahmed
# Date: 10/43/2018
# Description: Prompts the user for their name and age. Provides a greeting and the value equal to twice their age. Implementation is done in functions.
###########################################################################################

# function that prompts the user for a name and returns it
def name():

    a = input("Please enter your name:") #asks for the name and gives the person types in
    return a

# function that receives the user's name as a parameter, and prompts the user for an age and returns it
def age(nameofperson):

    b = input("How old are you, {}?".format(nameofperson)) #asks for the age
    return (int(b)) #changes the age from a string to a integer


# function that receives the user's name and age as parameters and displays the final output
def twice(nameagain, ageofperson):
    print("Hi, {}. You are {} years old. Twice you age is {}.".format(nameagain, ageofperson, ageofperson * 2)) #prints with the name and age and twice the age

###############################################
# MAIN PART OF THE PROGRAM
# implement the main part of your program below
# comments have been added to assist you
###############################################
# get the user's name
thename = name()

# get the user's age
theage = age(thename)

# display the final output
twice(thename, theage)
