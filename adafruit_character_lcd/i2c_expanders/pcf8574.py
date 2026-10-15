# SPDX-FileCopyrightText: 2026 Roman Ondráček
#
# SPDX-License-Identifier: MIT

"""
`adafruit_character_lcd.i2c_expanders.pcf8574`
====================================================

PCF8574 I2C expander wrapper for character LCD backpacks.

* Author(s): Roman Ondráček

Implementation Notes
--------------------

**Software and Dependencies:**

* Adafruit's PCF8574 library:
  https://github.com/adafruit/Adafruit_CircuitPython_PCF8574

"""

try:
    from typing import Optional, Sequence

    import busio
    import digitalio
except ImportError:
    pass

from adafruit_pcf8574 import PCF8574

from adafruit_character_lcd.i2c_expanders import I2C_Expander

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class PCF8574_Expander(I2C_Expander):
    """PCF8574 expander, as used on the common "LCM1602 IIC" character LCD backpacks.

    :param ~busio.I2C i2c: The I2C bus.
    :param int address: The I2C address of the PCF8574.
    :param int reset: Expander pin wired to the LCD reset (RS) line.
    :param int enable: Expander pin wired to the LCD enable (E) line.
    :param data: Expander pins wired to the LCD data lines D4, D5, D6 and D7.
    :param int backlight: Expander pin wired to the backlight control.
    """

    RESET = 0
    ENABLE = 2
    DATA = (4, 5, 6, 7)
    BACKLIGHT = 3

    def __init__(
        self,
        i2c: busio.I2C,
        address: int = 0x27,
        *,
        reset: Optional[int] = None,
        enable: Optional[int] = None,
        data: Optional[Sequence[int]] = None,
        backlight: Optional[int] = None,
    ) -> None:
        super().__init__(reset=reset, enable=enable, data=data, backlight=backlight)
        self.device = PCF8574(i2c, address=address)

    def get_pin(self, pin: int) -> digitalio.DigitalInOut:
        return self.device.get_pin(pin)

    def write_gpio(self, value: int) -> None:
        self.device.write_gpio(value)
