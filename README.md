## MicroPython example for ubitlogger.com
This python example should work with ubitlogger.com. It has been tested with https://python.microbit.org/v/2.0

The custom send() function is necessarry because ubitlogger.com expects data to be sent in the same format as makecode. At some point i might make a pull-request to BBC's MicroPython implementation to include functions that does the same trick. 