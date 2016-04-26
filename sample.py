#!/usr/bin/env python
"""
Copyright (c) 2016 Mobily.ws
Code by Lucas Thompson

Script showing how to import a class from the library and use it.

For more examples, read the manual (README.md)

"""
from mobily.sms import MobilySMS

if MobilySMS.can_send():
    print 'Service is available!'
else:
    print 'Service is not available!'
