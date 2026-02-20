---
id: 1
title: Phase II Web App Spec
stage: spec
date: 2026-01-08
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-phase2-web-app
branch: 001-phase2-web-app
user: user
command: /sp.specify
labels: [phase2,web-app,todo,specification,fullstack]
links:
  spec: specs/001-phase2-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
 - specs/001-phase2-web-app/spec.md
 - specs/001-phase2-web-app/CLAUDE-FRONTEND.md
 - specs/001-phase2-web-app/CLAUDE-BACKEND.md
 - specs/001-phase2-web-app/crud-spec.md
 - specs/001-phase2-web-app/api-endpoints-spec.md
 - specs/001-phase2-web-app/database-schema-spec.md
 - specs/001-phase2-web-app/authentication-spec.md
 - specs/001-phase2-web-app/project-structure-spec.md
 - specs/001-phase2-web-app/agents-spec.md
 - specs/001-phase2-web-app/checklists/requirements.md
tests:
 - none
---

## Prompt

```
I am starting Phase II for our Todo project.

Follow the original project constitution rules strictly,
but present this as a new implementation for Phase II.

Phase II Objective:
Upgrade the CLI-based Todo app from Phase I
into a web application supporting multiple users
with persistent storage.

Technology Stack:
Frontend: Next.js 16+ (App Router)
Backend: Python FastAPI
ORM: SQLModel
Database: Neon Serverless PostgreSQL
Authentication: Better Auth with JWT
Spec-Driven: Claude Code + Spec-Kit Plus

Development Approach:
Spec → Plan → Task Breakdown → Implementation
No manual coding is allowed.

Tasks for this phase:
1. Design monorepo layout suitable for full-stack web app
2. Generate CLAUDE.md files for frontend and backend
3. Create all specification documents, including:
   - CRUD feature specs
   - REST API endpoints spec
   - Database schema spec
   - Authentication (JWT) spec
   - Project structure/organization spec
4. Define reusable agents:
   - Planner Agent
   - Builder Agent
   - Reviewer
```

## Response snapshot

Successfully created comprehensive specifications for Phase II of the Todo application. Created a full set of specification documents including:
- Main feature specification (spec.md)
- Frontend and backend CLAUDE.md files
- CRUD operations specification
- REST API endpoints specification
- Database schema specification
- Authentication specification
- Project structure specification
- Reusable agents specification
- Quality checklist

All specifications follow the spec-driven development approach and are organized in a monorepo structure suitable for full-stack web development with Next.js and FastAPI.

## Outcome

- ✅ Impact: Complete specification suite for Phase II web application development
- 🧪 Tests: none
- 📁 Files: Created 10 specification files and 1 checklist across the specs/001-phase2-web-app/ directory
- 🔁 Next prompts: Ready for planning phase with /sp.plan
- 🧠 Reflection: All required specification documents created according to project constitution

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): N/A
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Proceed to planning phase