"""
Enable or disable printing of stdout.

enable_stdout -> bool: Enable printing.
disable_stdout -> bool: Disable printing.
"""

import sys
import os


def disable_stdout():
    setattr(sys, "stdout", open(os.devnull, "w"))


def enable_stdout():
    setattr(sys, "stdout", sys.__stdout__)
