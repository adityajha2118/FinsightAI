# Agent Orchestrator

## Purpose
Coordinates multiple domain-specific agents to handle complex, cross-functional queries.

## Architecture
```mermaid
graph TD
    USER[User Query] --> ORCH[Orchestrator]
    ORCH --> CA[Customer Agent]
    ORCH --> CMA[Campaign Agent]
    ORCH --> COA[Compliance Agent]
    ORCH --> CPA[Complaint Agent]
    CA & CMA & COA & CPA --> ORCH
    ORCH --> RESP[Unified Response]
```

## Current Implementation
The orchestrator currently dispatches to the complaint agent directly.
Future versions will implement query classification and multi-agent routing.

## Entry Point
- `src/agents/orchestrator.py`
