import time
import random
import os
import redis
import math
import threading
from prometheus_client import start_http_server, Counter, Gauge

# --- METRICS ---
LOG_COUNTER = Counter('app_logs_total', 'Total logs generated', ['level'])
QUEUE_GAUGE = Gauge('app_redis_queue_depth', 'Current size of the log queue')

# Connect to Redis
# We use a global variable 'r' so both threads can use it
try:
    r = redis.Redis(host='redis', port=6379, db=0, decode_responses=True, socket_connect_timeout=2)
except Exception as e:
    print(f"⚠️ Redis Connection Failed: {e}")
    r = None

# --- THE CONSUMER (The Drain) ---
def chaos_consumer():
    """
    This thread runs in the background. 
    It wakes up randomly and deletes logs (RPOP) to simulate processing.
    """
    print("📉 Consumer Thread STARTED.", flush=True)
    
    while True:
        if r:
            try:
                # 1. Wait a bit (Let the queue build up)
                sleep_time = random.randint(5, 10)
                time.sleep(sleep_time)
                
                # 2. DELETE a batch of logs (The "Drop")
                # We check the queue length first
                current_len = r.llen('log_queue')
                if current_len > 0:
                    # Remove 30% to 50% of the queue to make a visible drop
                    logs_to_remove = random.randint(int(current_len * 0.3), int(current_len * 0.5))
                    logs_to_remove = max(1, logs_to_remove) # Ensure we remove at least 1
                    
                    pipeline = r.pipeline()
                    for _ in range(logs_to_remove):
                        pipeline.rpop('log_queue')
                    pipeline.execute()
                    
                    print(f"📉 CONSUMER WOKE UP: Removed {logs_to_remove} logs. Queue dropped.", flush=True)
                
                    # 3. Update the Gauge immediately so Grafana sees the drop
                    new_len = r.llen('log_queue')
                    QUEUE_GAUGE.set(new_len)
            except Exception as e:
                print(f"Consumer Error: {e}", flush=True)
        else:
            time.sleep(5)

# --- THE PRODUCER (The Filler) ---
def generate_stress():
    print(f"🔥 Producer Process PID: {os.getpid()} Started.", flush=True)
    
    while True:
        # 1. CPU Stress
        x = 0.0001
        for i in range(100000): 
            x += math.sqrt(i)
            
        # 2. Produce Logs
        if r:
            try:
                # Push 1 to 5 logs rapidly
                for _ in range(random.randint(1, 5)):
                    level = random.choice(["INFO", "WARNING", "ERROR", "CRITICAL"])
                    r.lpush('log_queue', f"{level}: System Load High")
                    LOG_COUNTER.labels(level=level).inc()
                
                # Update Gauge (It goes UP here)
                QUEUE_GAUGE.set(r.llen('log_queue'))
                
            except Exception as e:
                print(f"Producer Error: {e}")
        
        # Run fast!
        time.sleep(0.1)

if __name__ == "__main__":
    # 1. Start Metrics Server
    start_http_server(8000)
    print("📈 Metrics Server Running on port 8000")
    
    # 2. Start the Consumer in a Background Thread
    consumer_thread = threading.Thread(target=chaos_consumer)
    consumer_thread.daemon = True # This ensures it dies when the main app dies
    consumer_thread.start()
    
    # 3. Start the Main Producer Loop
    generate_stress()