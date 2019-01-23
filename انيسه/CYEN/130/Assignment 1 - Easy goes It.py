###########################################################################################
# Name: Anisah Alahmed
# Date: 9/28/2018
# Description: Prompts the user for their name and age. Provides a greeting and the value equal to twice their age.
###########################################################################################

# prompt the user for a name and an age
name = input("Please enter your name: ")
string_age = input("How old are you, {}? ".format(name)) #insert the given name into the age prompt
age = int(string_age) #age above comes in as a string, so I turn it into an integer for multiplying later

# display the final output
print("Hi, {}. You are {} years old. Twice your age is {}.".format(name, age, age * 2))
#the format inserts the given name, age, and the double of the age into the final response

