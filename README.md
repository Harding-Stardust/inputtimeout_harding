This is a modified version of inputimeout (https://pypi.org/project/inputtimeout)
With the following mods:
correct spelling inputimeout -> inputtimeout
docstrings
type hints
default values
each keypress adds time (20 seconds) to the timeout so we won't interupt the user when he/she is typing (Only on Windows)
