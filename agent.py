from typing import List, Dict, Any
from preprocessing import rewrite_and_clean
from memory import MemoryStore, MemoryItem
from prompting import build_prompt_cot
from heuristics_llm import infer as heuristics_infer
from schemas import Plan, AgentOutput, Recommendation

OUTPUT_SCHEMA_KEYS = {"incident_type", "cause_analysis", "recommendations", "severity_level"}

def choose_mode(appeal_clean: str) -> str:
    # Simple heuristic: use RAG if text is long enough to benefit
    return "rag" if len(appeal_clean.split()) >= 20 else "zero-shot"

def json_parse_and_validate(y: Dict[str, Any]) -> Dict[str, Any]:
    # In real LLM setting, we'd parse JSON; here y is already a dict
    # Validate minimal schema
    if not (set(y.keys()) >= OUTPUT_SCHEMA_KEYS):
        missing = OUTPUT_SCHEMA_KEYS - set(y.keys())
        raise ValueError(f"Missing keys in agent output: {missing}")
    if not isinstance(y.get("recommendations"), list) or not y["recommendations"]:
        raise ValueError("recommendations must be a non-empty list")
    return y

def build_agent_output(raw: Dict[str, Any]) -> AgentOutput:
    # Convert dict to AgentOutput dataclass
    recs = [Recommendation(**r) for r in raw["recommendations"]]
    return AgentOutput(
        incident_type=raw["incident_type"],
        cause_analysis=raw["cause_analysis"],
        recommendations=recs,
        severity_level=raw["severity_level"]
    )

def LLM_AGENT_INFER(appeal_raw: str, memory: MemoryStore | None = None, mode: str = "auto", k: int = 5) -> Plan:
    # Step 0: preprocessing
    appeal_clean = rewrite_and_clean(appeal_raw)

    # Step 1: choose mode
    if mode == "auto":
        mode = choose_mode(appeal_clean)

    # Step 2: build prompt (if we had an external LLM)
    examples = []
    retrieved_ids = []
    if mode == "rag" and memory is not None and memory.items:
        v_new = memory.encode(appeal_clean)
        examples = memory.search(v_new, k)
        retrieved_ids = [ex.id for ex in examples]

    prompt = build_prompt_cot(appeal_clean, examples=examples)

    # Step 3: call LLM (here replaced by deterministic heuristics)
    h = heuristics_infer(appeal_clean)
    agent_out_dict = {
        "incident_type": h["label"],
        "cause_analysis": h["cause"],
        "recommendations": h["recs"],
        "severity_level": h["severity"]
    }

    # Step 4: parse & validate
    _ = json_parse_and_validate(agent_out_dict)
    agent_out = build_agent_output(agent_out_dict)

    # Step 5: pack Plan
    plan = Plan(
        id="auto",
        incident_type=h["incident_type_vec"],
        cause_analysis=agent_out.cause_analysis,
        recommendations=agent_out.recommendations,
        debug={
            "mode": mode,
            "prompt_chars": len(prompt),
            "retrieved_k": len(examples),
            "retrieved_ids": retrieved_ids
        }
    )
    return plan
