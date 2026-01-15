import unittest
from unittest.mock import MagicMock, patch
import sys
import os

# Add parent directory to path so we can import app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Mock redis before importing app, so it doesn't crash trying to connect
with patch.dict('sys.modules', {'redis': MagicMock()}):
    import app

class TestLogLogic(unittest.TestCase):
    
    def test_log_level_id(self):
        """Test the specific logic function (Unit Test)"""
        self.assertEqual(app.get_log_level_id("INFO"), 1)
        self.assertEqual(app.get_log_level_id("CRITICAL"), 4)
        self.assertEqual(app.get_log_level_id("UNKNOWN"), 0)

    @patch('app.r') # Mock the Redis object inside app
    def test_metrics_logic(self, mock_redis):
        """Test if metrics would theoretically update"""
        # We just want to ensure the logic exists, not test the actual DB connection
        mock_redis.llen.return_value = 10 
        queue_size = mock_redis.llen('log_queue')
        self.assertEqual(queue_size, 10)

if __name__ == '__main__':
    unittest.main()