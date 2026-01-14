import redis
import time
import os

# Connect to Redis
# Note: We will run this container in the SAME network, so it can find 'redis-store'
r = redis.Redis(host='redis-store', port=6379, db=0)

def start_police():
    print(f"👮 Police (Consumer) Started PID: {os.getpid()}", flush=True)
    print("Waiting for suspicious logs...", flush=True)
    
    while True:
        # BRPOP = Blocking Right POP
        # Queue la data varuvaraikum wait pannum (Blocks). Empty loop suthadhu (Efficient).
        # Data vandha udane 'pop' pannidum.
        data = r.brpop('log_queue', timeout=5)
        
        if data:
            # data format: (b'queue_name', b'message')
            queue_name, message = data
            message_str = message.decode('utf-8')
            
            # Simple Logic: Only Alert on CRITICAL
            if "CRITICAL" in message_str:
                print(f"🚨 ALERT! Critical Issue Found: {message_str}", flush=True)
            else:
                print(f"✅ Processed: {message_str}", flush=True)

if __name__ == "__main__":
    start_police()