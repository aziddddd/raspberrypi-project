# Import required packages
from webiopi.devices.sensor.onewiretemp import DS18B20
import sys
import pylab
import matplotlib.animation as animation
import datetime
import time

# The function to call each time the plot is updated
def updatePlot(i):
    # Declare the temperature sensors
    tmp = DS18B20(slave="28-000005eb9151")

    # Readout temperature sensor
    temp_water = tmp.getCelsius()

    # Hysteresis loop for temperature measurement
    if temp_water < (temp_set - temp_hys):
        GPIO.output(peltier, GPIO.OUT)

    elif temp_water > (temp_set + temp_hys):
        GPIO.output(peltier, GPIO.HIGH)

    # Store the current time and measurements
    timeValues.append(datetime.datetime.now())
    measurements_water.append(temp_water)

    # Clear the old plot
    plotFigure.clear()

    # Make the new plot
    pylab.xlabel(r'$Real\/Time$')
    pylab.ylabel(r'$Temperature,\/T\//\degree C$')
    pylab.title('PyFridge Temperature Monitor', fontsize='x-large')
    pylab.suptitle('Hysteresis Loop Method', fontsize=12)
    pylab.plot(timeValues, measurements_water, 'b-', label='Water')
    pylab.legend()

# Hide any warnings
GPIO.setwarnings(False)

# GPIO programming by BCM pin numbers
GPIO.setmode(GPIO.BCM) 

# Declare the peltier pin
peltier = 21

# Initialises the pin as output
GPIO.setup(peltier, GPIO.OUT)

# Set up the plot object
plotFigure = pylab.figure()

# Prompt required data for refrigeration
temp_set = float(input('Input the fridge temperature, Tf in centigrade : '))
temp_hys = float(input('Input the hysteresis value, Th in centigrade : '))

# Set the peltier pin output
GPIO.output(peltier, GPIO.HIGH)

# Empty arrays of time and measurement values to plot
timeValues, measurements_water = [ ], [ ]

# Make the animated plot
ani = animation.FuncAnimation(plotFigure, updatePlot, interval=200)
pylab.show()