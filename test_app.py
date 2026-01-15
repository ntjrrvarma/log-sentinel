import unittest
from app import get_log_level_id

class TestLogLogic(unittest.TestCase):
    
    # Test 1: Check if CRITICAL returns 4
    def test_critical_level(self):
        result = get_log_level_id("CRITICAL")
        self.assertEqual(result, 4)

    # Test 2: Check if INFO returns 1
    def test_info_level(self):
        result = get_log_level_id("INFO")
        self.assertEqual(result, 1)

    # Test 3: Check unknown level (Should be 0)
    def test_unknown_level(self):
        result = get_log_level_id("UNKNOWN_STUFF")
        self.assertEqual(result, 0)

if __name__ == '__main__':
    unittest.main()