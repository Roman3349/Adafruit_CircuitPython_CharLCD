# SPDX-FileCopyrightText: 2026 Roman Ondráček
# SPDX-License-Identifier: MIT

"""Simple test for 16x2 character lcd connected to a PCF8574 I2C LCD backpack."""

import time

import board

import adafruit_character_lcd.character_lcd_i2c as character_lcd
from adafruit_character_lcd.i2c_expanders.pcf8574 import PCF8574_Expander

# Modify this if you have a different sized Character LCD
lcd_columns = 16
lcd_rows = 2

# Initialise I2C bus.
i2c = board.I2C()  # uses board.SCL and board.SDA
# i2c = board.STEMMA_I2C()  # For using the built-in STEMMA QT connector on a microcontroller

# Initialise the lcd class
# Most PCF8574 backpacks use address 0x27, PCF8574A ones use 0x3F
expander = PCF8574_Expander(i2c, address=0x27)
# For a backpack wired differently, specify the pins, e.g.:
# expander = PCF8574_Expander(i2c, address=0x27, reset=0, enable=2, data=(4, 5, 6, 7), backlight=3)
lcd = character_lcd.Character_LCD_I2C(i2c, lcd_columns, lcd_rows, expander=expander)

# Turn backlight on
lcd.backlight = True
# Print a two line message
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
lcd.clear()
# Print two line message right to left
lcd.text_direction = lcd.RIGHT_TO_LEFT
lcd.message = "Hello\nCircuitPython"
# Wait 5s
time.sleep(5)
# Return text direction to left to right
lcd.text_direction = lcd.LEFT_TO_RIGHT
# Display cursor
lcd.clear()
lcd.cursor = True
lcd.message = "Cursor! "
# Wait 5s
time.sleep(5)
# Display blinking cursor
lcd.clear()
lcd.blink = True
lcd.message = "Blinky Cursor!"
# Wait 5s
time.sleep(5)
lcd.blink = False
lcd.clear()
# Create message to scroll
scroll_msg = "<-- Scroll"
lcd.message = scroll_msg
# Scroll message to the left
for i in range(len(scroll_msg)):
    time.sleep(0.5)
    lcd.move_left()
lcd.clear()
lcd.message = "Going to sleep\nCya later!"
time.sleep(5)
# Turn backlight off
lcd.backlight = False
time.sleep(2)
