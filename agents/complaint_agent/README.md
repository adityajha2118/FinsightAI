# Complaint Agent

## Purpose
Processes raw customer complaint narratives through a 6-node LangGraph state machine pipeline.

## Architecture
```
Input → Summarize → Classify → Detect Emotion → Score Escalation → Route → Generate Response → Output
```

## Nodes
1. **Summarize**: LLM condenses 200-500 word narratives into 1-2 sentences
2. **Classify**: LLM maps text to financial complaint categories
3. **Detect Emotion**: LLM identifies customer emotional state
4. **Score Escalation**: XGBoost predicts escalation probability (0.0-1.0)
5. **Route**: Business rules assign priority level and team
6. **Generate Response**: LLM drafts empathetic customer response

## Implementation
- State Machine: `src/agents/complaint_agent.py`
- Orchestrator: `src/agents/orchestrator.py`
- API Endpoint: `POST /api/complaints/process`
