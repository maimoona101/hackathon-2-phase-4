# Quickstart Guide: Todo Chatbot on Kubernetes

## Overview
Quickstart guide to deploy the Todo Chatbot application on a local Minikube cluster using Helm charts.

## Prerequisites
- Minikube installed and running
- kubectl installed and configured
- Helm installed
- Docker installed and running
- kubectl-ai installed (or available for cluster management)
- kagent installed (or available for cluster optimization)

## Setup Instructions

### 1. Start Minikube
```bash
minikube start
```

### 2. Verify Kubernetes cluster
```bash
kubectl cluster-info
kubectl get nodes
```

### 3. Build Docker images for backend and frontend
```bash
# Build backend image
cd backend
docker build -t todo-backend:latest .
cd ..

# Build frontend image
cd frontend
docker build -t todo-frontend:latest .
cd ..

# Load images into Minikube
minikube image load todo-backend:latest
minikube image load todo-frontend:latest
```

### 4. Deploy using Helm
```bash
# Install the main Helm chart
helm install todo-chatbot-release helm/todo-chatbot/ --namespace todo-chatbot --create-namespace
```

### 5. Verify deployment
```bash
# Check pods
kubectl get pods -n todo-chatbot

# Check services
kubectl get services -n todo-chatbot

# Check deployment status
kubectl get deployments -n todo-chatbot
```

### 6. Access the application
```bash
# Get the NodePort URL for frontend
minikube service todo-frontend-svc -n todo-chatbot --url
```

## Management Commands

### Scaling
```bash
# Scale backend replicas
kubectl scale deployment todo-backend -n todo-chatbot --replicas=2

# Using kubectl-ai (AI-powered scaling)
kubectl-ai scale deployment todo-backend -n todo-chatbot --replicas=2
```

### Monitoring
```bash
# Check pod status
kubectl get pods -n todo-chatbot -w

# Check logs
kubectl logs -f deployment/todo-frontend -n todo-chatbot

# Using kagent for cluster optimization
kagent analyze --namespace todo-chatbot
```

### Cleanup
```bash
# Uninstall Helm release
helm uninstall todo-chatbot-release -n todo-chatbot

# Delete namespace
kubectl delete namespace todo-chatbot
```

## Verification Steps
1. Confirm both frontend and backend pods are running
2. Verify the frontend service is accessible via NodePort
3. Check that the backend service is running internally (ClusterIP)
4. Test application functionality through the frontend interface