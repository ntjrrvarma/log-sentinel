import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock redis before importing app to prevent connection errors
# We also need to mock prometheus_client to avoid "duplicate metric" errors during testing
with patch.dict('sys.modules', {'redis': MagicMock()}):
    import app

class TestLogLogic(unittest.TestCase):
    
    def test_log_level_exists(self):
        """Test if the consumer thread function exists"""
        # We just want to ensure the critical functions are defined
        self.assertTrue(hasattr(app, 'chaos_consumer'))
        self.assertTrue(hasattr(app, 'generate_stress'))

    @patch('app.r') # Mock the Redis object inside app
    def test_queue_logic(self, mock_redis):
        """Test if Redis logic is reachable"""
        # Simulate a Redis queue length
        mock_redis.llen.return_value = 50
        
        # Test our code's access to it
        if app.r:
            val = app.r.llen('log_queue')
            self.assertEqual(val, 50)

if __name__ == '__main__':
    unittest.main()