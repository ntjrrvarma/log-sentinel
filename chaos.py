import docker
import time
import random

# --- CONFIGURATION ---
# IMPORTANT: Run 'docker ps' to get your EXACT Redis container name.
# It is usually 'log-sentinel-redis-1' or 'log-sentinel_redis_1'
CONTAINER_NAME = "redis_store" 
OUTAGE_DURATION_SECONDS = 45

def connect_docker():
    try:
        # Connect to the local Docker engine
        client = docker.from_env()
        print("✅ Connected to Docker Engine.")
        return client
    except Exception as e:
        print(f"❌ Failed to connect to Docker: {e}")
        print("💡 Hint: Is Docker Desktop running? Try running as Admin/Sudo.")
        exit(1)

def kill_redis(client):
    try:
        container = client.containers.get(CONTAINER_NAME)
        if container.status != 'running':
            print(f"⚠️  Container {CONTAINER_NAME} is already stopped/dead.")
            return

        print(f"\n🎯 Target Acquired: {CONTAINER_NAME}")
        print(f"💥 KILLING REDIS CONTAINER...")
        
        # Stop the container (Simulates a crash)
        container.stop()
        
        print(f"💀 REDIS IS DEAD. Services should be failing now.")
        print(f"📉 Watch your Grafana Dashboard FLATLINE.")
    except docker.errors.NotFound:
        print(f"❌ Error: Container '{CONTAINER_NAME}' not found. Check 'docker ps'.")
        exit(1)

def revive_redis(client):
    print(f"\n⏳ Waiting {OUTAGE_DURATION_SECONDS} seconds for chaos to settle...")
    time.sleep(OUTAGE_DURATION_SECONDS)
    
    print(f"\n🚑 INITIATING RECOVERY PROTOCOL...")
    try:
        container = client.containers.get(CONTAINER_NAME)
        container.start()
        print(f"✅ REDIS RESTARTED. System should self-heal.")
        print(f"📈 Check Grafana for recovery spikes.")
    except Exception as e:
        print(f"❌ Failed to revive Redis: {e}")

if __name__ == "__main__":
    print("--- 🌪️ CHAOS MONKEY: INITIATED 🌪️ ---")
    client = connect_docker()
    
    kill_redis(client)
    revive_redis(client)
    
    print("\n--- 🏁 CHAOS DRILL COMPLETE ---")