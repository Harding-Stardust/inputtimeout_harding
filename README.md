This is a modified version of [inputimeout](https://pypi.org/project/inputimeout/)

With the following modifications:
1. correct spelling inputimeout -> inputtimeout
2. docstrings
3. type hints
4. default values
5. each keypress adds time (20 seconds) to the timeout so we won't interupt the user when he/she is typing (Only on Windows)
