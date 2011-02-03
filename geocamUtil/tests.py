
import os
import unittest

thisDir = os.path.abspath(os.path.dirname(__file__))
suite = unittest.TestLoader().discover(thisDir, '*.py')
