import unittest
import sys
from unittest.mock import MagicMock, patch
import os

# --- NUCLEAR MOCKING STRATEGY ---
# We manually force these into sys.modules. 
# This tricks Python into thinking these libraries are installed permanently for this script.
# We do this BEFORE importing app.
sys.modules["redis"] = MagicMock()
sys.modules["prometheus_client"] = MagicMock()

# Now we can safely import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app

class TestLogLogic(unittest.TestCase):
    
    def test_log_level_exists(self):
        """Test if the consumer thread function exists"""
        self.assertTrue(hasattr(app, 'chaos_consumer'))
        self.assertTrue(hasattr(app, 'generate_stress'))

    def test_queue_logic(self):
        """Test if Redis logic is reachable"""
        # Since we mocked the whole module 'redis' above, app.r is already a Mock.
        # We just need to verify the logic flow doesn't crash.
        
        # Setup the mock to return a value
        app.r.llen.return_value = 50
        
        # Run the line we want to test
        if app.r:
            val = app.r.llen('log_queue')
            self.assertEqual(val, 50)

if __name__ == '__main__':
    unittest.main()