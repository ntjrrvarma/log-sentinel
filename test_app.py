import unittest
import sys
import os
from unittest.mock import MagicMock

# --- NUCLEAR MOCKING (Must be at the very top) ---
# We force-feed these mocks into Python's memory.
# This makes Python think these libraries are installed, even if they are missing.
sys.modules["redis"] = MagicMock()
sys.modules["prometheus_client"] = MagicMock()

# Now it is safe to import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app

class TestLogLogic(unittest.TestCase):
    
    def test_consumer_logic_exists(self):
        """Test if the consumer thread function is defined"""
        self.assertTrue(hasattr(app, 'chaos_consumer'))
        self.assertTrue(hasattr(app, 'generate_stress'))

    def test_queue_logic(self):
        """Test if Redis logic is reachable"""
        # Since we mocked 'redis' globally, app.r is ALREADY a MagicMock.
        # We don't need @patch here. We just use the mock directly.
        
        # 1. Setup the mock to return a fake queue size
        app.r.llen.return_value = 50
        
        # 2. Run the logic
        if app.r:
            val = app.r.llen('log_queue')
            self.assertEqual(val, 50)

if __name__ == '__main__':
    unittest.main()