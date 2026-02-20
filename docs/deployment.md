# Deployment Guide for Todo Chatbot on Kubernetes

## Overview
This document provides instructions for deploying the Todo Chatbot application on a Kubernetes cluster using Helm charts.

## Prerequisites

### Local Development Environment
- Minikube installed and running
- kubectl configured to connect to Minikube
- Helm 3+ installed
- Docker installed and running
- kubectl-ai and kagent (for AI-powered operations)

### Container Images
The application requires Docker images for both frontend and backend services. These can be built using the provided Dockerfiles:

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

## Deployment Steps

### 1. Prepare the Namespace
Create the namespace for the application:
```bash
kubectl apply -f k8s/todo-chatbot-namespace.yaml
```

### 2. Deploy Using Raw Manifests (Optional)
For initial testing, you can deploy using raw Kubernetes manifests:
```bash
kubectl apply -f k8s/ -n todo-chatbot
```

### 3. Deploy Using Helm
The recommended approach is to use Helm charts:

```bash
# Install the main chart
helm install todo-chatbot-release helm/todo-chatbot/ --namespace todo-chatbot --create-namespace

# Or upgrade an existing installation
helm upgrade todo-chatbot-release helm/todo-chatbot/ --namespace todo-chatbot --install
```

### 4. Verify the Deployment
Check the status of your deployments:
```bash
kubectl get pods -n todo-chatbot
kubectl get services -n todo-chatbot
kubectl get deployments -n todo-chatbot
```

### 5. Access the Application
Get the frontend service URL:
```bash
minikube service todo-frontend-svc -n todo-chatbot --url
```

Or use port forwarding for testing:
```bash
kubectl port-forward -n todo-chatbot svc/todo-frontend-svc 3000:80
```

## Configuration Options

### Helm Values
The chart supports various configuration options defined in `helm/todo-chatbot/values.yaml`:

- `frontend.enabled`: Whether to deploy the frontend service
- `frontend.replicaCount`: Number of frontend replicas
- `frontend.image.repository`: Frontend image repository
- `frontend.image.tag`: Frontend image tag
- `backend.enabled`: Whether to deploy the backend service
- `backend.replicaCount`: Number of backend replicas
- `backend.image.repository`: Backend image repository
- `backend.image.tag`: Backend image tag

### Service Configuration
- Frontend is exposed via NodePort (30080) for external access
- Backend is available internally via ClusterIP
- Port configuration can be adjusted in the respective values files

## Scaling the Application

### Manual Scaling
Increase the number of replicas for either service:
```bash
kubectl scale deployment todo-frontend -n todo-chatbot --replicas=3
kubectl scale deployment todo-backend -n todo-chatbot --replicas=2
```

### Automatic Scaling
The deployment includes Horizontal Pod Autoscaler (HPA) configurations:
```bash
kubectl apply -f k8s/backend-hpa.yaml
kubectl apply -f k8s/frontend-hpa.yaml
```

## Monitoring and Management

### Health Checks
Verify the health of deployed services:
```bash
kubectl get hpa -n todo-chatbot
kubectl top pods -n todo-chatbot
kubectl describe deployment todo-frontend -n todo-chatbot
kubectl describe deployment todo-backend -n todo-chatbot
```

### Using AI Tools
For AI-powered management, you can use kubectl-ai:
```bash
kubectl-ai analyze deployment todo-frontend -n todo-chatbot
kubectl-ai scale deployment todo-backend -n todo-chatbot --replicas=2
```

## Troubleshooting

### Common Issues
1. **Images not found**: Ensure images are loaded into Minikube with `minikube image load`
2. **Service not accessible**: Check if the NodePort is available and the service is running
3. **DNS resolution issues**: Verify that the backend service name is accessible to the frontend

### Debugging Commands
```bash
# Check pod logs
kubectl logs -f deployment/todo-frontend -n todo-chatbot
kubectl logs -f deployment/todo-backend -n todo-chatbot

# Describe resources to see events
kubectl describe pod -l app=todo-frontend -n todo-chatbot
kubectl describe service todo-frontend-svc -n todo-chatbot
```

## Cleanup
To remove the deployment:
```bash
helm uninstall todo-chatbot-release -n todo-chatbot
kubectl delete namespace todo-chatbot
```