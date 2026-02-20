---
id: 001
title: Adopt Phase IV Constitution
stage: constitution
date: 2026-02-20
surface: agent
model: Claude-Opus-4-6
feature: none
branch: main
user: user
command: /sp.constitution
labels: ["constitution","phase-iv","kubernetes"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
 - .specify/memory/constitution.md
tests:
 - none
---

## Prompt

Adopt the following Phase IV System Prompt Constitution for this project:

Phase IV – Local Kubernetes Deployment (Minikube, Helm Charts, kubectl-ai, Kagent, Docker Desktop, and Gordon)

Rules:
1. Use the Agentic Dev Stack workflow: Write spec → Generate plan → Break into tasks → Implement via Claude Code. No manual coding allowed.
2. Containerize backend and frontend applications using Docker AI Agent (Gordon). If Gordon is unavailable, generate Docker commands via AI.
3. Generate Helm charts for deployment using kubectl-ai or kagent. No manual YAML creation.
4. Deploy applications only on local Minikube cluster.
5. Use kubectl-ai to handle deployments, scaling, debugging, and monitoring.
6. Use kagent to analyze cluster health and optimize resource allocation.
7. Preserve all AI-generated prompts, outputs, and iterations for judging.
8. Frontend must be exposed via NodePort; backend must remain internal.
9. All decisions and generated artifacts must follow this constitution strictly.

## Response snapshot

Updated the project constitution at .specify/memory/constitution.md to reflect the Phase IV Kubernetes deployment requirements. The new constitution now includes specific principles for:

- Kubernetes Deployment Principles (local Minikube deployment, Helm charts, NodePort exposure)
- Containerization Principles (Docker AI Agent usage)
- Agent Orchestration Principles (kubectl-ai and kagent usage)
- Updated Technology Stack and Phase Requirements to reflect Phase IV

Version was updated from 1.1.0 to 1.2.0 following semantic versioning (MINOR update for new principles).

## Outcome

- ✅ Impact: Updated project constitution for Phase IV Kubernetes deployment
- 🧪 Tests: none
- 📁 Files: .specify/memory/constitution.md
- 🔁 Next prompts: none
- 🧠 Reflection: Constitution successfully updated to reflect Phase IV requirements with appropriate Kubernetes, containerization, and agent orchestration principles.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): N/A