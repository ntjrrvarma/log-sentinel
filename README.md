# 🛡️ LogSentinel: From Python Script to Kubernetes Cluster

**A complete journey of building a Fault-Tolerant, Distributed Log Ingestion System.**
* **Author:** Rahul N R
* **Tech Stack:** Python, Redis, Docker, Kubernetes (Minikube), Terraform.

---

## 📖 Project Overview
LogSentinel is a simulation of a high-traffic logging infrastructure. It demonstrates how modern SREs build systems that are:
1.  **Decoupled:** Producers and Consumers don't talk directly (using Redis Queue).
2.  **Scalable:** Can handle traffic spikes by creating more containers automatically.
3.  **Resilient:** If a component dies, the system heals itself.

---

## 🏗️ Phase 1: Docker & Distributed Systems
**Goal:** Containerize the application and set up basic networking.

### 🧩 Components
1.  **Log Agent (`app.py`):** A Python script that generates synthetic logs (INFO, WARNING, CRITICAL) and pushes them to a Redis List.
2.  **Redis Store:** A message broker that buffers logs.
3.  **Consumer (`consumer.py`):** A "Police" service that reads from Redis and alerts on CRITICAL errors.

### 💡 Key Concepts Learned
* **Docker Networking:** Created `sentinel-net` so containers can talk by name (`host='redis-store'`).
* **Docker Compose:** Orchestrated the entire stack with one command (`docker-compose up`).
* **Persistence:** Used Redis to ensure logs aren't lost even if the Python app crashes.

### ⚡ Commands

# Start the stack
docker-compose up -d --scale log-agent=5

# Check logs
docker logs -f redis-store



## ☸️ Phase 2: Kubernetes Migration (The Big Boss)
**Goal:** Move from a single machine (Docker Compose) to a Cluster (Kubernetes) for Orchestration.

### 🚀 Why Kubernetes?
Docker Compose is great for local dev, but Kubernetes provides Self-Healing and Auto-Scaling.

### 🛠️ Architecture Changes

Feature,Docker Compose,Kubernetes (Minikube)
Process Manager,Container,Deployment (Restarts dead pods)
Networking,Automatic Bridge,Service (ClusterIP to provide stable DNS)
Scaling,Manual (--scale),Horizontal Pod Autoscaler (HPA)


### 📂 Manifests Explained
# k8s/redis.yaml:
Deployment: Keeps 1 Redis Pod running.
Service: Maps the DNS name redis-store to the Pod's IP. Crucial for Service Discovery.

# k8s/agent.yaml:
Deployment: Manages the Python Agents.
Resources: Defined CPU limits (200m) so HPA knows when to scale.

### 📈 Auto-Scaling (The "Black Friday" Test)
We implemented HPA to watch CPU usage.

Metric: If CPU usage > 50%.
Action: Scale from 1 replica to max 10 replicas.
Stress Test: We updated app.py to burn CPU, and observed pods scaling from 2 -> 8 -> 10 automatically.

### ⚡ Commands

# Apply Configs
kubectl apply -f k8s/

# Watch Auto-Scaling
kubectl get hpa --watch

# Update Image (Rolling Update)
kubectl set image deployment/log-agent-deploy agent=log-sentinel:v3

## 🏗️ Phase 3: Infrastructure as Code (Terraform)
**Goal:** Stop "ClickOps". Automate infrastructure creation using Code.

### 💡 Why Terraform?
Instead of typing docker run, we write main.tf. This allows us to version control our infrastructure just like our application code.

### 🛠️ What we built
A Terraform script to provision a Docker Container (Nginx) automatically.

### Learned the workflow: Init -> Plan -> Apply.

### ⚡ Commands

cd terraform-lab
terraform init   # Download providers
terraform plan   # Preview changes
terraform apply  # Create infrastructure


### 🎓 Summary of Skills Mastered
Containerization: Docker, Dockerfile best practices.
Orchestration: Kubernetes Pods, Deployments, Services, HPA.
Infrastructure as Code: Terraform basics.
Scripting: Python for Automation & Stress Testing.
Git Ops: Handling large files, .gitignore, and commit discipline.
