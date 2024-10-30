"""
This is an example of how to control a strip of WS2812B strip lights on a stairway. There are two motion detectors: one
at the top of the stairs and one at the bottom. A light sensor controls them to detect if it's dark enough to justify
having the stairs lit.
"""
import time

from machine import Pin
from neopixel import NeoPixel


def top_to_bottom(strip, pixel_count, color):
    """
    Function to control lighting from top to bottom.
    :param strip: The WS2812B strip
    :param pixel_count: The number of pixels in the strip
    :param color: The color to set on the strip
    """
    for i in range(pixel_count):
        strip[i] = color
        strip.write()


def bottom_to_top(strip, pixel_count, color):
    """
    Function to control lighting from bottom to top.
    :param strip: The WS2812B strip
    :param pixel_count: The number of pixels in the strip
    :param color: The color to set on the strip
    """
    for i in range(pixel_count - 1, -1, -1):
        strip[i] = color
        strip.write()


# Number of pixels in the strip
PIXEL_COUNT = 300

# Duration to keep the light on (in minutes)
LIGHT_MINUTES = 3

# GPIO pins (adjust these according to your ESP32-C3 pinout)
PIXEL_PIN_NUM = 0  # GPIO4 for the NeoPixel strip
DOWN_MOTION_DETECTION_PIN_NUM = 1  # GPIO5 for the bottom motion detector
UP_MOTION_DETECTION_PIN_NUM = 2  # GPIO6 for the top motion detector
DARKNESS_DETECTION_PIN_NUM = 3  # GPIO7 for the light sensor

# Define colors
WHITE = (16, 16, 16)  # Adjust brightness as needed
OFF = (0, 0, 0)

# Time to keep the lights on after motion is detected (in seconds)
SHINE_TIME = 60 * LIGHT_MINUTES

# Initialize NeoPixel strip
PIXEL_PIN = Pin(PIXEL_PIN_NUM, Pin.OUT)
pixels = NeoPixel(PIXEL_PIN, PIXEL_COUNT)

# Initialize sensors
down = Pin(DOWN_MOTION_DETECTION_PIN_NUM, Pin.IN, Pin.PULL_DOWN)
up = Pin(UP_MOTION_DETECTION_PIN_NUM, Pin.IN, Pin.PULL_DOWN)
dark = Pin(DARKNESS_DETECTION_PIN_NUM, Pin.IN, Pin.PULL_DOWN)

# Turn off all pixels initially
pixels.fill(OFF)
pixels.write()

while True:
    if dark.value():
        if down.value():
            top_to_bottom(pixels, PIXEL_COUNT, WHITE)
            time.sleep(SHINE_TIME)
            top_to_bottom(pixels, PIXEL_COUNT, OFF)
        elif up.value():
            bottom_to_top(pixels, PIXEL_COUNT, WHITE)
            time.sleep(SHINE_TIME)
            bottom_to_top(pixels, PIXEL_COUNT, OFF)
