import time
import random
import os
import redis
import math  # New import

# app.py (Add this function at the top)

def get_log_level_id(level):
    """
    Simple logic to convert Log Level to a numeric ID.
    Used for filtering priority.
    """
    levels = {
        "INFO": 1,
        "WARNING": 2,
        "ERROR": 3,
        "CRITICAL": 4
    }
    return levels.get(level, 0) # Return 0 if unknown

# Connect to Redis using the Service Hostname
r = redis.Redis(host='redis-store', port=6379, db=0)

def generate_stress():
    print(f"🔥 STRESS AGENT PID: {os.getpid()} Starting CPU Burn...", flush=True)
    while True:
        # 1. Heavy Calculation to spike CPU
        x = 0.0001
        for i in range(1000000):
            x += math.sqrt(i)
        
        # 2. Push log after burning CPU
        levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
        log_msg = f"{random.choice(levels)}: CPU Burn at {x:.2f} - {time.ctime()}"
        
        try:
            r.lpush('log_queue', log_msg)
            # print(f"Sent: {log_msg}", flush=True) # Comment print to run faster
        except:
            pass
            
        # No Sleep! Run as fast as possible!

if __name__ == "__main__":
    generate_stress()