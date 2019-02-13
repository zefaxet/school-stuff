######################################################################################################################
# Name: Anisah Alahmed
# Date: 2/12/2018
# Description: A variety of sorts applied to a single list, the results of which are displayed on a tkinter bar graph
######################################################################################################################
# bring in the plot() function from the plot.py file
from plot import plot

# creates the list
def getList():

#	the_list = [100, 5, 63, 29, 69, 74, 96, 80, 82, 12]
	the_list = [82, 65, 93, 0, 60, 31, 99, 90, 31, 70]
#	the_list = [63, 16, 78, 69, 36, 36, 3, 66, 75, 100]
#	the_list = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
#	the_list = [10, 9, 8, 7, 6, 5, 4, 3, 2, 1]
#	the_list = [2, 1, 4, 3, 6, 5, 8, 7, 10, 9]

	print("The list:", the_list)
	return the_list

# the bubble sort function
# input: a list of integers
# output: a number of comparisons and swaps
def bubble_sort(list):
	n = len(list)
	comparisons = 0
	swaps = 0
	for i in range(1, n):
		for j in range(1, n - i + 1):
			if (list[j] < list[j - 1]):
				temp = list[j]
				list[j] = list[j - 1]
				list[j - 1] = temp
				swaps += 1
			comparisons += 1
	
	print("After bubble sort:",list)
	return comparisons, swaps

# the optimized bubble sort function
# input: a list of integers
# output: a number of comparisons and swaps
def optimized_bubble_sort(list):
	n = len(list)
	comparisons = 0
	swaps = 0
	for i in range(1, n):
		swap = False
		for j in range(1, n - i + 1):
			if (list[j] < list[j - 1]):
				temp = list[j]
				list[j] = list[j - 1]
				list[j - 1] = temp
				swaps += 1
				swap = True
			comparisons += 1
		if swap == False:
			break
	
	print("After optimized bubble sort:",list)
	return comparisons, swaps

# the selection sort function
# input: a list of integers
# output: a number of comparisons and swaps
def selection_sort(numbers):
	comparisons = 0
	swaps = 0
	n = len(numbers)
	for i in range(0, n - 1):
		minPosition = i
		for j in range(i + 1, n):
			comparisons += 1
			if (numbers[j] < numbers[minPosition]):
				minPosition = j
		swaps += 1
		temp = numbers[i]
		numbers[i] = numbers[minPosition]
		numbers[minPosition] = temp
	
	print("After selection sort:", numbers)
	return comparisons, swaps

# the insertion sort function
# input: a list of integers
# output: a number of comparisons and swaps
def insertion_sort(list):
	comparisons = 0
	swaps = 0
	n = len(list)
	i = 1
	while (i < n):
		comparisons += 1
		if (list[i - 1] > list[i]):
			comparisons += 1
			temp = list[i]
			j = i - 1
			while (j >= 0 and list[j] > temp):
				comparisons += 1
				swaps += 1
				list[j + 1] = list[j]
				j -= 1
			list[j + 1] = temp
		i += 1
	print("After insertion sort:",list)
	return comparisons, swaps

# the main part of the program
comparisons, swaps = bubble_sort(getList())
print("{} comparisons; {} swaps".format(comparisons, swaps))
print()
# save information about bubble sort
bubbleSortStats = [comparisons, swaps]
comparisons, swaps = optimized_bubble_sort(getList())
print("{} comparisons; {} swaps".format(comparisons, swaps))
print()
# save information about optimized bubble sort
optimizedBubbleSortStats = [comparisons, swaps]
comparisons, swaps = selection_sort(getList())
print("{} comparisons; {} swaps".format(comparisons, swaps))
print()
# save information about selection sort
selectionSortStats = [comparisons, swaps]
comparisons, swaps = insertion_sort(getList())
print("{} comparisons; {} swaps".format(comparisons, swaps))
print()
# save information about insertion sort
insertionSortStats = [comparisons, swaps]

# call plot() from the import
plot(bubbleSortStats, optimizedBubbleSortStats, selectionSortStats, insertionSortStats)
