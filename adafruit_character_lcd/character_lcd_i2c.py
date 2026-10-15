# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_character_lcd.character_lcd_i2c`
====================================================

Module for using I2C with I2C/SPI character LCD backpack

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Hardware:**

* `I2C / SPI character LCD backpack
  <https://www.adafruit.com/product/292>`_ (Product ID: 292)

**Software and Dependencies:**

* Adafruit CircuitPython firmware for the supported boards:
  https://circuitpython.org/downloads

* Adafruit's Bus Device library:
  https://github.com/adafruit/Adafruit_CircuitPython_BusDevice

* Adafruit's MCP230xx library (for the default MCP23008 backpack):
  https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx

* Adafruit's PCF8574 library (for PCF8574 backpacks):
  https://github.com/adafruit/Adafruit_CircuitPython_PCF8574

"""

import time

try:
    from typing import Optional

    import busio
except ImportError:
    pass

from adafruit_character_lcd.character_lcd import Character_LCD_Mono
from adafruit_character_lcd.i2c_expanders import I2C_Expander
from adafruit_character_lcd.i2c_expanders.mcp23008 import MCP23008_Expander

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class Character_LCD_I2C(Character_LCD_Mono):
    """Character LCD connected to I2C/SPI backpack using its I2C connection.
    This is a subclass of `Character_LCD_Mono` and implements all the same
    functions and functionality.

    By default, the Adafruit backpack with an MCP23008 expander is used.
    Other backpacks can be used by passing an expander wrapper from
    `adafruit_character_lcd.i2c_expanders`, optionally with a custom pin mapping.

    To use, import and initialise as follows:

    .. code-block:: python

        import board
        from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C

        i2c = board.I2C()  # uses board.SCL and board.SDA
        lcd = Character_LCD_I2C(i2c, 16, 2)

    or, for a backpack with a PCF8574 expander:

    .. code-block:: python

        import board
        from adafruit_character_lcd.character_lcd_i2c import Character_LCD_I2C
        from adafruit_character_lcd.i2c_expanders.pcf8574 import PCF8574_Expander

        i2c = board.I2C()  # uses board.SCL and board.SDA
        lcd = Character_LCD_I2C(i2c, 16, 2, expander=PCF8574_Expander(i2c))
    """

    def __init__(
        self,
        i2c: busio.I2C,
        columns: int,
        lines: int,
        address: Optional[int] = None,
        backlight_inverted: bool = False,
        expander: Optional[I2C_Expander] = None,
    ) -> None:
        """Initialize character LCD connected to backpack using I2C connection
        on the specified I2C bus with the specified number of columns and
        lines on the display. Optionally specify if backlight is inverted.

        If ``expander`` is given, it is used to drive the LCD and ``i2c`` and
        ``address`` are ignored. Otherwise an MCP23008 expander on ``i2c`` at
        ``address`` (if specified) is used.
        """

        if expander is None:
            if address:
                expander = MCP23008_Expander(i2c, address=address)
            else:
                expander = MCP23008_Expander(i2c)
        self.expander = expander

        # Lookup table mapping a 4-bit nibble to the expander data line bits.
        self._nibble_bits = [
            sum(((nibble >> i) & 1) << pin for i, pin in enumerate(expander.data_pins))
            for nibble in range(16)
        ]

        super().__init__(
            expander.get_pin(expander.reset_pin),
            expander.get_pin(expander.enable_pin),
            expander.get_pin(expander.data_pins[0]),  # data line 4
            expander.get_pin(expander.data_pins[1]),  # data line 5
            expander.get_pin(expander.data_pins[2]),  # data line 6
            expander.get_pin(expander.data_pins[3]),  # data line 7
            columns,
            lines,
            backlight_pin=expander.get_pin(expander.backlight_pin),
            backlight_inverted=backlight_inverted,
        )

    def _write8(self, value: int, char_mode: bool = False) -> None:
        # Sends 8b ``value`` in ``char_mode``.
        # :param value: bytes
        # :param char_mode: character/data mode selector. False (default) for
        # data only, True for character bits.
        #  one ms delay to prevent writing too quickly.
        time.sleep(0.001)

        reset_bit = int(char_mode) << self.expander.reset_pin
        backlight_bit = int(self.backlight ^ self.backlight_inverted) << self.expander.backlight_pin

        # Write char_mode and upper 4 bits of data to the data lines.
        self.expander.write_gpio(reset_bit | backlight_bit | self._nibble_bits[value >> 4])

        #  do command
        self._pulse_enable()

        # Write char_mode and lower 4 bits of data to the data lines.
        self.expander.write_gpio(reset_bit | backlight_bit | self._nibble_bits[value & 0x0F])

        # do command
        self._pulse_enable()
