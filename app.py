import time
import random
import os
import redis
import math  # New import

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