from dataclasses import dataclass, field
from typing import List, Dict, Any

@dataclass
class InputItem:
    id: str
    appeal_raw: str
    meta: Dict[str, Any] | None = None

@dataclass
class Recommendation:
    department: str
    action: str
    timeframe: str

@dataclass
class Plan:
    id: str
    incident_type: list        # 27-dim one-hot / multi-hot
    cause_analysis: str
    recommendations: List[Recommendation]
    debug: Dict[str, Any] = field(default_factory=dict)

# Output schema returned to the user-facing agent
@dataclass
class AgentOutput:
    incident_type: str
    cause_analysis: str
    recommendations: List[Recommendation]
    severity_level: str
