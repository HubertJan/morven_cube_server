import sys
import os
import unittest

# set module path for testing
sys.path.insert(0, "path_in_PYTHONPATH")
# repead to include all paths


class TestBase(unittest.TestCase):
    def __init__(self, methodName: str) -> None:
        super().__init__(methodName=methodName)
