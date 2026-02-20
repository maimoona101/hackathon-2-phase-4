# Helm Chart Configuration for Todo Chatbot

## Overview
This document describes the Helm chart configuration for deploying the Todo Chatbot application on Kubernetes.

## Chart Structure

### Main Chart (todo-chatbot)
- **Location**: `helm/todo-chatbot/`
- **Purpose**: Main umbrella chart that includes backend and frontend subcharts
- **Values**: Configures both backend and frontend services

### Backend Subchart
- **Location**: `helm/todo-chatbot/charts/backend/`
- **Purpose**: Deploys the backend API service
- **Service Type**: ClusterIP (internal access only)
- **Port**: 8000

### Frontend Subchart
- **Location**: `helm/todo-chatbot/charts/frontend/`
- **Purpose**: Deploys the frontend web application
- **Service Type**: NodePort (external access)
- **Port**: 80 (NodePort: 30080)

## Installation

### Prerequisites
- Kubernetes cluster (tested with Minikube)
- Helm 3+

### Steps
1. Add the namespace for the application:
   ```bash
   kubectl apply -f k8s/todo-chatbot-namespace.yaml
   ```

2. Install the chart:
   ```bash
   helm install todo-chatbot-release helm/todo-chatbot/ --namespace todo-chatbot
   ```

### Custom Values
You can customize the installation using a values file:

```yaml
frontend:
  enabled: true
  replicaCount: 2
  image:
    tag: "latest"

backend:
  enabled: true
  replicaCount: 1
  image:
    tag: "latest"
```

Then install with:
```bash
helm install todo-chatbot-release helm/todo-chatbot/ --namespace todo-chatbot -f my-values.yaml
```

## Architecture
- The frontend service is exposed via NodePort for external access
- The backend service remains internal (ClusterIP) for security
- Communication between frontend and backend happens internally through Kubernetes DNS