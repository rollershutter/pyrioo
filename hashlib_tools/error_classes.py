#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#
#  error_classes.py (hashlib_tools)
#  python 2.7 / 3.5 - tested
#
#  Copyright 2018 sebastian rollershutter
##


class Error(Exception):
    """Base class for exceptions in this module."""
    pass


class VerbosErr(Error):
    """Exception raised for situations where a verbose error info needed.
    Attributes:
        expression -- input expression in which the error occurred
        message -- explanation of the error
    """

    def __init__(self, expression, message):
        self.expression = expression
        self.message = message
