from typing import List
from memory import MemoryItem

SYSTEM_HEADER = (
    "System: You are an urban emergency response expert. "
    "Think step by step and return only valid JSON as specified—no extra text."
)

OUTPUT_FORMAT = """\
{
  "incident_type": "string",
  "cause_analysis": "string",
  "recommendations": [
    {"department": "string", "action": "string", "timeframe": "string"},
    {"department": "string", "action": "string", "timeframe": "string"}
  ],
  "severity_level": "Level I | Level II | Level III"
}"""

def build_prompt_cot(appeal_clean: str, examples: List[MemoryItem]) -> str:
    lines = [SYSTEM_HEADER, "", "Steps:",
             "1) Incident type → choose N1–N27 category; add a brief rationale.",
             "2) Cause analysis → direct causes, contributing factors, background.",
             "3) Recommendations → at least 2, each with department/action/timeframe.",
             "4) Severity scoring → estimate impact and map to severity rules.",
             "", "Format: Return a JSON object with the fields exactly as:", OUTPUT_FORMAT, ""]
    if examples:
        lines.append("Examples:")
        for ex in examples:
            lines.append(f"- Request: {ex.q_text}")
            lines.append(f"  → Solution: {ex.a_solution}")
            lines.append(f"  → Types: {ex.incident_type}")
            lines.append("")
    lines.append("New Request:")
    lines.append(appeal_clean)
    return "\n".join(lines)
