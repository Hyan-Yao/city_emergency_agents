from dataclasses import dataclass
from typing import List, Dict, Tuple
import math

def _tokenize(text: str) -> List[str]:
    import re
    return re.findall(r"[a-zA-Z0-9_]+", text.lower())

def _bow_vector(tokens: List[str]) -> Dict[str, int]:
    from collections import Counter
    return dict(Counter(tokens))

def _cosine(a: Dict[str, int], b: Dict[str, int]) -> float:
    if not a or not b:
        return 0.0
    # dot
    dot = sum(a.get(k,0)*b.get(k,0) for k in set(a)|set(b))
    # norms
    na = math.sqrt(sum(v*v for v in a.values()))
    nb = math.sqrt(sum(v*v for v in b.values()))
    if na==0 or nb==0:
        return 0.0
    return dot/(na*nb)

@dataclass
class MemoryItem:
    id: str
    q_text: str
    a_solution: str
    incident_type: list        # 27-dim 0/1

class MemoryStore:
    def __init__(self):
        self.items: List[MemoryItem] = []
        self._vecs: List[Dict[str,int]] = []

    def insert(self, item: MemoryItem) -> None:
        self.items.append(item)
        self._vecs.append(_bow_vector(_tokenize(item.q_text)))

    def encode(self, text: str) -> Dict[str,int]:
        return _bow_vector(_tokenize(text))

    def search(self, query_vec: Dict[str,int], k: int = 5) -> List[MemoryItem]:
        scores: List[Tuple[float,int]] = []
        for i, vec in enumerate(self._vecs):
            s = _cosine(query_vec, vec)
            scores.append((s, i))
        scores.sort(reverse=True)
        out = []
        for s, idx in scores[:k]:
            out.append(self.items[idx])
        return out
