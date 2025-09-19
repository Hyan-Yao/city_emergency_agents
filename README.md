# City Emergency Agents (Reference Implementation)

Minimal, dependency‑free Python implementation of the pipeline described in the project spec:
- Input/Output schemas
- Memory (RAG) with simple bag‑of‑words and cosine search
- CoT prompt builder
- Deterministic heuristics "LLM" stub (no external API) for classification and recommendations
- Evaluation helpers (BLEU‑1/2 and ROUGE‑L)

> This code follows the interfaces and steps outlined in the project description (sections on I/O schema, Memory, preprocessing, CoT+RAG, pseudocode, and evaluation).

## Quick Start

```bash
python -m city_emergency_agents.demo
```

## Structure
```
city_emergency_agents/
  __init__.py
  agent.py
  heuristics_llm.py
  memory.py
  preprocessing.py
  prompting.py
  rules.py
  schemas.py
  eval.py
  demo.py
```

## Notes
- The `heuristics_llm.py` module replaces a real LLM with keyword heuristics to keep the demo fully offline.
- To plug a real LLM, swap in your API call and parse JSON, then pass through the same validation.
