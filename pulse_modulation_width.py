# Import required packages
from webiopi.devices.sensor.onewiretemp import DS18B20
import pylab
import matplotlib.animation as animation
import datetime
import time
import RPi.GPIO as GPIO

# Hide any warnings
GPIO.setwarnings(False)

# GPIO programming by BCM pin numbers
GPIO.setmode(GPIO.BCM) 

# Declare the pins
peltier = 21

# Initialises the pin as output
GPIO.setup(peltier, GPIO.OUT)

# Set up the plot object
plotFigure = pylab.figure()

# The function to call each time the plot is updated
def updatePlot(i):

    # Declare the temperature sensors
    tmp = DS18B20(slave="28-000005eb9151")

    # Readout temperature sensor
    temp_water = tmp.getCelsius()

    # Calculate the current duty cycle
    exp_coefficient = 1000
    duty_cycle = int(exp_coefficient*(temp_water -temp_set))

    # Regulate the duty cycle
    if duty_cycle > 100:
        duty_cycle = 100
    elif duty_cycle < 0:
        duty_cycle = 0

    cool.ChangeDutyCycle(duty_cycle)
	time.sleep(1)

    # Store the current time and measurements
    timeValues.append( datetime.datetime.now() )
    measurements_water.append( temp_water )
    measurements_duty_cycle.append( duty_cycle )

    # Clear the old plot
    plotFigure.clear()

    # Make the new plot
    pylab.subplot(2, 1, 1)
    pylab.xlabel(r'$Real\/Time$')
    pylab.ylabel(r'$Temperature,\/T\//\degree C$')
    pylab.title('PyFridge Temperature Monitor', fontsize='x-large')
    pylab.suptitle('Pulse Modulation Width Method', fontsize=12)
    pylab.plot( timeValues, measurements_water, 'b-', label='Water' )
    pylab.legend()

    pylab.subplot(2, 1, 2)
    pylab.xlabel(r'$Real\/Time$')
    pylab.ylabel(r'$Duty\/Cycle,\/x$')
    pylab.title('PyFridge Duty Cycle Monitor', fontsize='x-large')
    pylab.plot( timeValues, measurements_duty_cycle, 'b-', label='Water' )
    pylab.ylim((0,101))

    pylab.subplots_adjust(hspace=0.6)

# Prompt required data for refrigeration
temp_set = float(input('Input the fridge temperature, Tf in centigrade : '))

# Initialise the Pulse Width Modulation process
cool = GPIO.PWM(peltier, 100)
cool.start(0)

# Empty arrays of time and measurement values to plot
timeValues, measurements_water, measurements_duty_cycle = [ ], [ ], [ ]

# Create a live plot
ani = animation.FuncAnimation(plotFigure, updatePlot, interval=200)
pylab.show()