import time
import unittest

def test_0sec():
    time.sleep(0)

def test_halfsec():
    time.sleep(0.5)

def test_1sec():
    time.sleep(1)

def test_2sec():
    time.sleep(2)

def nada():
    pass

class MyTestClass(unittest.TestCase):
    def test_1sec_method(self):
        time.sleep(1)
