# SPDX-FileCopyrightText: 2018 Kattni Rembor for Adafruit Industries
#
# SPDX-License-Identifier: MIT

"""
`adafruit_character_lcd.i2c_expanders.mcp23008`
====================================================

MCP23008 I2C expander wrapper for character LCD backpacks.

* Author(s): Kattni Rembor

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit's MCP230xx library:
  https://github.com/adafruit/Adafruit_CircuitPython_MCP230xx

"""

try:
    from typing import Optional, Sequence

    import busio
    import digitalio
except ImportError:
    pass

from adafruit_mcp230xx.mcp23008 import MCP23008

from adafruit_character_lcd.i2c_expanders import I2C_Expander

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class MCP23008_Expander(I2C_Expander):
    """MCP23008 expander, as used on the Adafruit I2C / SPI character LCD backpack.

    :param ~busio.I2C i2c: The I2C bus.
    :param int address: The I2C address of the MCP23008.
    :param int reset: Expander pin wired to the LCD reset (RS) line.
    :param int enable: Expander pin wired to the LCD enable (E) line.
    :param data: Expander pins wired to the LCD data lines D4, D5, D6 and D7.
    :param int backlight: Expander pin wired to the backlight control.
    """

    RESET = 1
    ENABLE = 2
    DATA = (3, 4, 5, 6)
    BACKLIGHT = 7

    def __init__(
        self,
        i2c: busio.I2C,
        address: int = 0x20,
        *,
        reset: Optional[int] = None,
        enable: Optional[int] = None,
        data: Optional[Sequence[int]] = None,
        backlight: Optional[int] = None,
    ) -> None:
        super().__init__(reset=reset, enable=enable, data=data, backlight=backlight)
        self.device = MCP23008(i2c, address=address)

    def get_pin(self, pin: int) -> digitalio.DigitalInOut:
        return self.device.get_pin(pin)

    def write_gpio(self, value: int) -> None:
        self.device.gpio = value
