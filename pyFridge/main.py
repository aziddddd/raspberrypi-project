# Import required packages
from webiopi.devices.sensor.onewiretemp import DS18B20
import sys
import pylab
import matplotlib.animation as animation
import datetime
import time

# The function to call each time the plot is updated
def updatePlot( i ):
    # Declare the temperature sensors
    tmp0 = DS18B20(slave="28-000005ead278")
    tmp1 = DS18B20(slave="28-000005eb9151")

    # Readout temperature sensor
    temp_water, temp_peltier = tmp0.getCelsius(), tmp1.getCelsius()

    if (GPIO.input(switch) == GPIO.HIGH):
        print('Peltier Temperature in centigrade    :   {}'.format(temp_peltier))
        if temp_peltier < measurements_peltier[-1]:
            print('Peltier status                   :   Cooling')
        elif temp_peltier >= measurements_peltier[-1]:
            print('Peltier status                   :   Not Cooling')
        return

    # Hysteresis loop for temperature measurement
    if temp_water < (temp_set - temp_hys):
        GPIO.output(peltier, GPIO.OUT)

    elif temp_water > (temp_set + temp_hys):
        for x in range(duty_cycle):                 # Execute loop for 'duty cycle' times
            cool.ChangeDutyCycle(x)                 # Change duty cycle for varying the cooling power
            time.sleep(0.1)                         # Sleep for 100m second
        
        for x in range(duty_cycle):
            cool.ChangeDutyCycle(duty_cycle-x)
            time.sleep(0.1)

    # Store the current time and measurements
    timeValues.append( datetime.datetime.now() )
    measurements_water.append( temp_water )
    measurements_peltier.append( temp_peltier )

    # Clear the old plot
    plotFigure.clear()

    # Make the new plot
    pylab.plot( timeValues, measurements_water, 'b-', label='Temperature of water' )
    pylab.plot( timeValues, measurements_peltier, 'r-', label='Temperature of Peltier' )

def main():
    # Hide any warnings
    GPIO.setwarnings(False)

    # GPIO programming by BCM pin numbers
    GPIO.setmode(GPIO.BCM) 

    # Declare the pins
    peltier     = 21            # Your peltier pin
    fan         = 20            # Your fan pin
    switch      = 19            # Your switch pin

    # Verify duty cycle
    if duty_cycle < 0 or duty_cycle > 100:
        print('Invalid Duty Cycle value given, please try again.')
        sys.exit()

    # Initialises the pin as output
    GPIO.setup(peltier, GPIO.OUT)
    GPIO.setup(fan, GPIO.OUT)
    GPIO.setup(switch, GPIO.OUT)

    # Set the output
    GPIO.output(fan, GPIO.HIGH)
    GPIO.output(switch, GPIO.HIGH)
    cool = GPIO.PWM(peltier, frequency)
    cool.start(0)

    # Empty arrays of time and measurement values to plot
    timeValues = [ ]
    measurements_water = [ ]
    measurements_peltier = [ ]

    # Set up the plot object
    plotFigure = pylab.figure()

    # Loop forever
    while True:
        if (GPIO.input(switch) == GPIO.LOW):
            # Prompt required data for refrigeration
            frequency   = float(input('Input the frequency of cooling power variation in Hz : '))
            duty_cycle  = float(input('Input the duty cycle [ 0-100 ] : '))
            temp_set    = float(input('Input the fridge temperature, Tf in centigrade : '))
            temp_hys    = float(input('Input the hysteresis value, Th in centigrade : '))

            # Make the animated plot
            ani = animation.FuncAnimation( plotFigure, updatePlot, interval=1000 )
            pylab.xlabel('Real time in seconds')
            pylab.ylabel('Temperature in centigrade')
            pylab.title('Temperature Sensor')
            pylab.legend()
            pylab.show()

main()
