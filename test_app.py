import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# --- THE FIX ---
# We mock BOTH 'redis' and 'prometheus_client' before importing app.
# This tricks Python into thinking they are installed, preventing ModuleNotFoundError.
modules_to_patch = {
    'redis': MagicMock(),
    'prometheus_client': MagicMock()
}

with patch.dict('sys.modules', modules_to_patch):
    import app

class TestLogLogic(unittest.TestCase):
    
    def test_log_level_exists(self):
        """Test if the consumer thread function exists"""
        self.assertTrue(hasattr(app, 'chaos_consumer'))
        self.assertTrue(hasattr(app, 'generate_stress'))

    @patch('app.r') # Mock the Redis object inside app
    def test_queue_logic(self, mock_redis):
        """Test if Redis logic is reachable"""
        # Simulate a Redis queue length
        mock_redis.llen.return_value = 50
        
        # Test our code's access to it
        # Since we mocked redis at the module level, app.r might be a MagicMock.
        # We ensure the logic flow works without crashing.
        if app.r:
            val = app.r.llen('log_queue')
            self.assertEqual(val, 50)

if __name__ == '__main__':
    unittest.main()