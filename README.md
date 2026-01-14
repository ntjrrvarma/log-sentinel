# 🛡️ LogSentinel (Phase 1)
**A Fault-Tolerant, Distributed Log Ingestion System**

## 📖 Project Overview
LogSentinel is a distributed system designed to simulate a scalable logging infrastructure. It decouples log generation from processing using an **Event-Driven Architecture**.
* **Producers (Agents):** Multiple Python containers generating synthetic logs.
* **Broker (Redis):** Acts as a buffer/queue to ensure zero data loss.
* **Consumer (Police):** A separate Python service that processes logs and alerts on "CRITICAL" events.

## 🏗️ Architecture
**[ Log Agent 1 ]** -->  \
**[ Log Agent 2 ]** -->   **[ Redis Queue ]** -->  **[ Police (Consumer) ]**
**[ Log Agent 3 ]** -->  /
*(Scaled horizontally to N replicas)*

---

## 🚀 Key Concepts Mastered
| Concept | Implementation |
| :--- | :--- |
| **Containerization** | Packaged Python apps into lightweight Docker images (`python:3.12-slim`). |
| **Microservices** | Split the app into Producer (`app.py`), Broker (`redis`), and Consumer (`consumer.py`). |
| **Service Discovery** | Used Docker Networks (`sentinel-net`) allows containers to talk by name (`redis-store`). |
| **Orchestration** | Managed the entire stack using `docker-compose`. |
| **Horizontal Scaling** | Scaled log agents dynamically using `docker-compose up --scale log-agent=5`. |
| **Fault Tolerance** | Decoupled systems using Redis; if the Consumer crashes, logs remain safe in the queue. |

---

## 🛠️ Project Structure
```text
log-sentinel/
├── app.py             # Log Producer (Generates logs -> Pushes to Redis)
├── consumer.py        # Log Consumer (Reads Redis -> Alerts on CRITICAL)
├── Dockerfile         # Blueprint to build the Python image
├── docker-compose.yml # Orchestration file (Services, Networks, Dependencies)
├── requirements.txt   # Dependencies (redis library)
└── README.md          # Documentation

⚡ How to Run
1. Prerequisites
Docker & Docker Compose installed.

2. Start the System (Daemon Mode)
This starts Redis and the Log Agent.

Bash

docker-compose up -d
3. Scale the Producers (Simulate High Load)
Spin up 5 concurrent log agents generating traffic.

Bash

docker-compose up -d --scale log-agent=5
4. Start the Consumer (The "Police")
Run the consumer script inside the network to process logs.

Bash

# Note: Ensure network name matches `docker network ls` (e.g., log-sentinel_sentinel-net)
docker run -it --network log-sentinel_sentinel-net log-sentinel-log-agent python consumer.py
5. Verify Resilience
Check Queue: Exec into Redis and run LLEN log_queue.

Stop Consumer: Logs will pile up in Redis (No data loss).

Restart Consumer: It picks up exactly where it left off.

🧪 Technical Learnings (SRE Perspective)
Immutability: Docker images act as immutable artifacts. Version tagging (v1, v2) allows safe rollbacks.

Buffers are critical: Direct API calls fail if the receiver is down. Using a Queue (Redis) acts as a shock absorber.

Service Names as DNS: In Docker networks, we don't use IPs. We use service names (redis-store) which resolve automatically.


---