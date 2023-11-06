import asyncio
import os
import string
import sys

from rich import print as printmd
from rich.markdown import Markdown


def initializeColorCodes():
    if sys.platform == "win32":
        os.system('')


def separator():
    print("-" * os.get_terminal_size().columns)


color = {
    'red': '\033[31m',
    'blue': '\033[34m',
    'aqua': '\033[36m',
    'green': '\033[32m',
    'dark_green': '\033[38;5;2m',
    'yellow': '\033[33m',
    'orange': '\033[38;5;202m',
    'purple': '\033[35m',
    'light_purple': '\033[38;5;93m',
    'dark_purple': '\033[38;5;54m',
    'gray': '\033[37m',
    'light_gray': '\033[38;5;250m',
    'dark_blue': '\033[38;5;18m'
}

# ansi style codes for the style parameter in processStyle()
style = {
    'bold': '\033[1m',
    'italic': '\033[3m',
    'underlined': '\033[4m'
}


# Takes in a string, processes it into a colored or style formatted string, then returns it
def processStyle(content: string, color_name=None, style_name=None):
    color_code = color[color_name] if color_name else ''
    style_code = style[style_name] if style_name else ''
    # Reset code
    reset = '\033[0m'
    return f"{color_code}{style_code}{content}{reset}"


def clearScreen():
    # if the Operating System is Windows
    if sys.platform == "win32":
        os.system("cls")
    # if the Operating System is Linux or MacOS
    if sys.platform == "linux" or sys.platform == "linux2" or sys.platform == "darwin":
        os.system("clear") # Clears the terminal screen.


def pause(): # A simple pause function
    input(processStyle("Press return to continue...", style_name='italic'))


def delayedPrint(content: string, delay: float = 0, afterDelay: float = 0, returnLine: bool = True):
    asyncio.run(__delayedPrint__(content, delay, afterDelay, returnLine)) # uses Asyncio to run the asynchronous function. mimics the effects of sys.sleep(0)


def loader(duration: float = 2, placeholder: string = "Processing"):
    asyncio.run(__loaderText__(duration, placeholder)) # uses Asyncio to run the asynchronous function. mimics the effects of sys.sleep(0)


async def __delayedPrint__(content: string, delay: float, afterDelay: float, returnLine: bool):
    temp = float(delay / len(content)) # Calculates the duration needed for pause between printing out each letter.
    for i in content: # Prints out the content letter by letter.
        print(i, end='')
        await asyncio.sleep(temp) # Uses an asynchronous await to sleep. similar to sys.sleep().
    if returnLine:
        print() # Returns the Line.
    await asyncio.sleep(afterDelay) # Delays the function after printing out the content. For custom purposes.


# The core function of loader().
async def __loaderText__(duration: float, placeholder: string):
    for _ in range(3):  # Adjust the range for the desired number of cycles
        for dot_count in range(4):  # The number of dot_count will cycle from 0 to 3, with each index representing a character in a loop
            print(f'\r{placeholder}...  [ {__loaderSpinner__(dot_count)} ]', end='')
            await asyncio.sleep(duration / 12)


# The function that returns the characters representing the indexes in the spinner.
def __loaderSpinner__(index: int):
    temp = index % 4
    return processStyle("|" if temp == 0 else "/" if temp == 1 else "-" if temp == 2 else "\\", 'aqua', 'bold')


def parse_markdown_native(text):
    return Markdown(text)


def parse_markdown(text):
    md = Markdown(text)
    printmd(md)
