#!/usr/bin/env python3
"""Silent exception handler test."""

try:
    result = 1 / 0
except:
    pass

try:
    x = undefined_variable
except Exception:
    pass
