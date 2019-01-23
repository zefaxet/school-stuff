##############################
# NAME: Anisah Alahmed
# DATE: 11/9/2018
# DESC: Use ping sensor and sort results
##############################


import RPi.GPIO as gpio
from time import sleep, time

# constants
DEBUG = False

SETTLE_TIME = 2
CALIBRATIONS = 5

CALIBRATION_DELAY = 1

TRIGGER_TIME = 0.00001

SPEED_OF_SOUND = 343


gpio.setmode(gpio.BCM)

TRIG = 18
ECHO = 27

gpio.setup(TRIG, gpio.OUT)
gpio.setup(ECHO, gpio.IN)

def calibrate():
    print("Calibrating...")

    print("-Place the sensor a measured distance away from an object.")
    known_distance = float(input("-What is the measured distance (cm)? "))

    # measure the distance to the object with the sensor
    # do this several times and get an average
    print("-Getting calibration measurements...")
    distance_avg = 0
    for i in range(CALIBRATIONS):
        distance = getDistance()
        if (DEBUG):
            print("--Got {}cm".format(distance))
        # keep a running sum
        distance_avg += distance
        # delay a short time before using the sensor again
        sleep(CALIBRATION_DELAY)
    # calculate the average of the distances
    distance_avg /= CALIBRATIONS
    if (DEBUG):
        print("--Average is {}cm".format(distance_avg))

    # calculate the correction factor
    correction_factor = known_distance / distance_avg
    if (DEBUG):
        print("--Correction factor is {}".format(correction_factor))

    print("Done.")
    print()

    return correction_factor

# uses the sensor to calculate the distance to an object
def getDistance():
    # trigger the sensor by setting it high for a short time and then setting it low
    gpio.output(TRIG, gpio.HIGH)
    sleep(TRIGGER_TIME)
    gpio.output(TRIG, gpio.LOW)

    # wait for the ECHO pin to read high
    # once the ECHO pin is high, the start time is set
    # once the echo pin is low again, the end time is set
    while (gpio.input(ECHO) == gpio.LOW):
        #print("start run")
        start = time()
    while (gpio.input(ECHO) == gpio.HIGH):
        #print("end run")
        end = time()

    # calculate the duration that the echo pin was high
    # this is how long the pulse took to get from the sensor to the object -- and back again
    duration = end - start
    # calculate the total distance that the pulse traveled by factoring in the speed of sound (m/s)
    distance = duration * SPEED_OF_SOUND
    # the distance from the sensor to the object is half of the total distance traveled
    distance /= 2
    # convert from meters to centimeters
    distance *= 100

    return distance

# simple selection sort for sorting the measurements
def selection_sort(unsorted):

    sorted = []

    # until the unsorted list is empty
    while len(unsorted) != 0:
        # get the smallest value from the unsorted list
        min_value = min(unsorted)
        if DEBUG:
            print("Min value:", min_value)
        # get the index of the smallest value in the unsorted list
        index = unsorted.index(min_value)
        if DEBUG:
            print("Min value index:", index)
        # remove the smallest value from the unsorted list
        pop = unsorted.pop(index)
        if DEBUG:
            print("Popped value:", pop)

        # add it to the end of the sorted list
        sorted.append(pop)
        if DEBUG:
            print("Sorted list:", sorted)
    
    return sorted
    

########
# MAIN #
########
# first, allow the sensor to settle for a bit
print("Waiting for the sensor to settle ({}s)...".format(SETTLE_TIME))
gpio.output(TRIG, gpio.LOW)
sleep(SETTLE_TIME)

# next calibrate the sensor
correction_factor = calibrate()

# measurements will be stored here
measurements = []

# then, measure
input("Press enter to begin...")
print("Getting measurements:")
while (True):
    # get the distance to an object and correct it with the correction factor
    print("Measuring...")
    distance = getDistance() * correction_factor
    sleep(1)

    # and round to four decimal places
    distance = round(distance, 4)

    # display the distance measured/calculated
    print("--Distance measured: {}cm".format(distance))

    # store the measurement
    measurements.append(distance)

    # prompt for another measurement
    i = input("--Get another measurement (Y/n)? ")
    # stop measurig if desired
    if (not i in [ "y", "Y", "yes", "Yes", "YES", "" ]):
        break

# finally, cleanup the GPIO pins
print("Done.")
print()

# display measurements
# unsorted
print("Unsorted measurements:")
print(measurements)

# unsorted
measurements = selection_sort(measurements)
print("Sorted measurements:")
print(measurements)
gpio.cleanup()
