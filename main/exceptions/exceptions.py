#!/usr/bin/env python
# Base Exceptions

class Error(Exception):
    """Base class for other exceptions"""
    def __init__(self, arg=None):
        if arg is None:
            arg = 'An error ocurred with coco'
        self.msg = arg
        super(Error, self).__init__(arg)

    pass

# Custom Exceptions

class UrlValueException(Error):
    def __init__(self):
        super(UrlValueException, self).__init__(arg="URL ERROR")
