import time
import random
import os
import redis  # New Import

# Connect to Redis Container by NAME
# Hostname 'redis-store' works because they are in the same Docker Network
r = redis.Redis(host='redis-store', port=6379, db=0)

def generate_log():
    print(f"LogSentinel Agent PID: {os.getpid()} Connecting to Redis...", flush=True)
    while True:
        levels = ["INFO", "WARNING", "ERROR", "CRITICAL"]
        log_msg = f"{random.choice(levels)}: System load at {random.randint(10, 100)}% - {time.ctime()}"
        
        # Push to Redis List named 'log_queue'
        try:
            r.lpush('log_queue', log_msg)
            print(f"Sent to Redis: {log_msg}", flush=True)
        except redis.ConnectionError:
            print("Redis Connection Failed! Retrying...", flush=True)
            
        time.sleep(2)

if __name__ == "__main__":
    generate_log()