import RPi.GPIO as GPIO
import time
from datetime import datetime
import datetime


from datetime import datetime as dt
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional,CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT, ATARI_FONT, SPECCY_FONT, SEG7_FONT
from datetime import timedelta


serial = spi(port=1, device=0, gpio=noop())
device = max7219(serial, height=8, width=32, block_orientation=-90) #, blocks_arranged_in_reverse_order=True)
device.contrast(1)

GPIO.setmode(GPIO.BOARD)
greenButton = 29
GPIO.setup(greenButton, GPIO.IN, pull_up_down=GPIO.PUD_UP)
buttonPresses = 0

# Define button callback functions
def button_green_callback(channel):
    global buttonPresses    
    today = day_and_time() # Get today's date.
    today = '{:%A, %Y-%m-%d}'.format(today) + ' (' + '{:%H:%M:%S}'.format(today) + ')' # Make the format nicer.
    if buttonPresses % 3 == 0:
        start = dt.now()
        drawTime()
    elif buttonPresses % 3 == 1:
        drawDate()
    elif buttonPresses % 3 == 2:
        counter_up()
    buttonPresses += 1
   
def drawDate():
    today = datetime.datetime.today()
    with canvas(device) as draw:
        text(draw, (0, 1), '{:%d.%m.}'.format(today), fill="white", font=proportional(CP437_FONT))    
def day_and_time():
    today = datetime.datetime.today()
    return today
def drawTime():
    today = datetime.datetime.today()
    with canvas(device) as draw:
        text(draw, (0, 1), '{:%H:%M}'.format(today), fill="white", font=proportional(CP437_FONT))
def counter_up():
    start_time = datetime.datetime.now()
    toggle = False
    while True:
        toggle = not toggle
        current_time = datetime.datetime.now()
        elapsed_time = current_time - start_time
        minutes = elapsed_time.total_seconds() // 60
        seconds = elapsed_time.total_seconds() % 60
        # When you have a timedelta object named elapsed_time, calling elapsed_time.total_seconds() returns the total number of seconds represented by that timedelta object. It calculates the duration of time in seconds, taking into account all the components of the timedelta (days, hours, minutes, and seconds).
        # print("Elapsed time: {} seconds".format(int(seconds)))
        with canvas(device) as draw:
            if minutes < 60:
                display_time = "{:02d}:{:02d}".format(int(minutes), int(seconds))
                text(draw, (1, 0), display_time, fill="white", font=proportional(SINCLAIR_FONT))
            else:
                hours = minutes // 60
                minutes %= 60
                display_time = "{:d} {:02d}".format(int(hours), int(minutes))
                text(draw, (1, 0), display_time, fill="white", font=proportional(SINCLAIR_FONT))
                text(draw, (15, 0), ":" if toggle else " ", fill="white", font=proportional(TINY_FONT))
        time.sleep(1)  # Pause for 1 second before printing the next second

GPIO.add_event_detect(greenButton, GPIO.FALLING, callback=button_green_callback, bouncetime=300)
# Wait for events
try:
    while True:
        time.sleep(0.01)
except KeyboardInterrupt:
    print("INTERRUPT - There was an interrupt and we're cleaning the GPIOs.")
    GPIO.cleanup()
    print("INTERRUPT - Cleanup done.")
