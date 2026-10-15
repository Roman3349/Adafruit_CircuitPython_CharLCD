# SPDX-FileCopyrightText: 2026 Roman Ondráček
#
# SPDX-License-Identifier: MIT

"""
`adafruit_character_lcd.i2c_expanders`
====================================================

Wrappers for I2C GPIO expanders used on character LCD backpacks.

Each wrapper presents a common API to `Character_LCD_I2C` and describes how
the LCD signals are wired to the expander pins. Every expander lives in its own
submodule, so only the library for the expander actually in use is loaded
into RAM.

The default pin mapping of each wrapper matches the common backpack for that
expander. For a backpack wired differently, pass the pin numbers to the wrapper
constructor:

.. code-block:: python

    from adafruit_character_lcd.i2c_expanders.pcf8574 import PCF8574_Expander

    expander = PCF8574_Expander(i2c, reset=0, enable=2, data=(4, 5, 6, 7), backlight=3)

* Author(s): Roman Ondráček

"""

try:
    from typing import Optional, Sequence

    import digitalio
except ImportError:
    pass

__version__ = "0.0.0+auto.0"
__repo__ = "https://github.com/adafruit/Adafruit_CircuitPython_CharLCD.git"


class I2C_Expander:
    """Base class for 8-bit I2C GPIO expanders driving a character LCD in 4-bit mode.

    Subclasses set the default pin mapping in the `RESET`, `ENABLE`, `DATA` and
    `BACKLIGHT` class attributes and implement `get_pin()` and `write_gpio()`.

    :param int reset: Expander pin wired to the LCD reset (RS) line.
    :param int enable: Expander pin wired to the LCD enable (E) line.
    :param data: Expander pins wired to the LCD data lines D4, D5, D6 and D7.
    :param int backlight: Expander pin wired to the backlight control.

    Pins which are not specified use the default mapping of the subclass.
    """

    RESET: int
    """Default expander pin wired to the LCD reset (RS) line."""
    ENABLE: int
    """Default expander pin wired to the LCD enable (E) line."""
    DATA: Sequence[int]
    """Default expander pins wired to the LCD data lines D4, D5, D6 and D7."""
    BACKLIGHT: int
    """Default expander pin wired to the backlight control."""

    def __init__(
        self,
        reset: Optional[int] = None,
        enable: Optional[int] = None,
        data: Optional[Sequence[int]] = None,
        backlight: Optional[int] = None,
    ) -> None:
        self.reset_pin = self.RESET if reset is None else reset
        self.enable_pin = self.ENABLE if enable is None else enable
        self.data_pins = tuple(self.DATA if data is None else data)
        self.backlight_pin = self.BACKLIGHT if backlight is None else backlight

        if len(self.data_pins) != 4:
            raise ValueError("data must specify exactly 4 pins (D4, D5, D6, D7)")
        pins = (self.reset_pin, self.enable_pin, self.backlight_pin) + self.data_pins
        if len(set(pins)) != len(pins) or any(not 0 <= pin <= 7 for pin in pins):
            raise ValueError("pins must be unique and in range 0-7")

    def get_pin(self, pin: int) -> digitalio.DigitalInOut:
        """Return a :class:`~digitalio.DigitalInOut`-like object for the specified expander pin."""
        raise NotImplementedError

    def write_gpio(self, value: int) -> None:
        """Set the state of all 8 expander pins at once from a single byte."""
        raise NotImplementedError
