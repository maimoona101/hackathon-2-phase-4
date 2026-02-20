<!-- SYNC IMPACT REPORT
Version change: 1.0.0 → 1.1.0
Modified principles:
- Added "AI-Powered Chat Interface" principle
- Updated "No Manual Coding Constraint" to emphasize Phase III restrictions
- Updated "Progressive Evolution" to include AI/ML considerations
Added sections: None
Removed sections: None
Templates requiring updates:
- ✅ .specify/templates/plan-template.md (updated)
- ✅ .specify/templates/spec-template.md (updated)
- ✅ .specify/templates/tasks-template.md (updated)
- ⚠️ .specify/templates/commands/*.md (pending manual review)
Follow-up TODOs: None
-->

# The Evolution of Todo – From Console App to Cloud-Native AI System Constitution

## Core Principles

### Spec-Driven Development
All code must be generated strictly from written specifications. No manual coding is allowed; only specification refinement is permitted. This ensures deterministic behavior and maintainable code across all phases of the project.

### Progressive Evolution
Each phase must build logically on the previous phase without breaking architectural integrity. The system must maintain backward compatibility where possible and follow clean architecture principles throughout all phases. Phase III specifically extends existing functionality with AI-powered features while preserving all Phase II capabilities.

### Reusable Intelligence
Sub-agents, skills, and templates must be explicitly defined and applied across all phases. Agents (Planner, Builder, Reviewer) and skills (Task Management, Spec Parsing, CLI Interaction) must be reusable without modification between phases.

### AI-Powered Chat Interface
Phase III introduces an AI-powered chat interface using MCP tools and OpenAI Agent SDK to manage todos via natural language. The system must implement natural language processing for task management operations while maintaining clear separation between traditional UI and AI chat features. All conversation and task state must be stored persistently in the database.

### MCP Server Integration
MCP tools must be exposed as backend services to enable AI orchestration of task operations. The system must implement proper tool specifications in `specs/mcp-tools-spec.md` and ensure secure, reliable communication between AI agents and backend services.

### No Manual Coding Constraint
Developers may not write or edit code manually at any point in any phase, particularly during Phase III implementation. All implementation must be driven by specifications through automated agents and tools. Existing backend APIs for todos and auth must remain unchanged during Phase III development. This ensures consistency and adherence to spec-driven development.

### Deterministic Behavior
System outputs must be predictable and testable at every phase. All phases must have clear acceptance criteria, explicit error paths, and testable functionality to ensure reliable evolution from one phase to the next.

### Clean Architecture
Clear separation of concerns must be maintained throughout all phases. Business logic, interfaces, and infrastructure must remain decoupled to enable smooth transitions between phases and technologies. Phase III must maintain clear separation between existing Phase-2 UI and new AI chat features.

## Additional Constraints
- Technology progression follows a defined path: Phase I (Python/CLI) → Phase II (Next.js/FastAPI/SQLModel) → Phase III (AI/Chatbot/MCP/OpenAI Agent) → Phase IV (Kubernetes) → Phase V (Cloud-Native/Dapr)
- All phases must maintain core Todo functionality: Add/View/Update/Delete/Complete tasks
- In-memory storage in Phase I evolves to persistent storage in Phase II and beyond
- Security, performance, and observability requirements increase with each phase
- Phase III constraints: No manual coding allowed for Phase III; existing backend APIs must remain unchanged; clear separation between Phase-2 UI and Phase-3 AI chat features

## Development Workflow
- Specifications drive all implementation through Planner → Builder → Reviewer agent pipeline
- Each phase must pass validation before advancing to the next phase
- Code generation must follow established templates and patterns
- All changes must be testable and verifiable against specification requirements
- Continuous integration and testing required at each phase
- Phase III specific: Generate all necessary backend folders/files for AI and MCP tools; implement MCP tools specification file

## Governance
This constitution governs all development activities across all five phases. All code generation, architectural decisions, and implementation choices must align with these principles. Deviations require formal amendment procedures. All agents, skills, and templates must comply with these principles throughout the project lifecycle.

**Version**: 1.1.0 | **Ratified**: 2026-01-08 | **Last Amended**: 2026-01-29
