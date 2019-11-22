"""
https://www.geeksforgeeks.org/print-colors-python-terminal/
https://stackoverflow.com/questions/287871/how-to-print-colored-text-in-terminal-in-python
"""

# Python program to print
# colored text and background
def prRed(skk): print("\033[31m {}\033[00m" .format(skk))
def prGreen(skk): print("\033[92m {}\033[00m" .format(skk))
def prDarkGreen(skk): print("\033[42m {}\033[00m" .format(skk))
def prYellow(skk): print("\033[33m {}\033[00m" .format(skk))
def prLightPurple(skk): print("\033[94m {}\033[00m" .format(skk))
def prPurple(skk): print("\033[95m {}\033[00m" .format(skk))
def prCyan(skk): print("\033[96m {}\033[00m" .format(skk))
def prLightGray(skk): print("\033[97m {}\033[00m" .format(skk))
def prBlack(skk): print("\033[98m {}\033[00m" .format(skk))
