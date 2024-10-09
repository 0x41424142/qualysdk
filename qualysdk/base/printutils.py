"""
Enable or disable printing of stdout.

enable_stdout -> bool: Enable printing.
disable_stdout -> bool: Disable printing.
"""

import sys, os

disable_stdout = lambda: setattr(sys, "stdout", open(os.devnull, "w"))
enable_stdout = lambda: setattr(sys, "stdout", sys.__stdout__)
