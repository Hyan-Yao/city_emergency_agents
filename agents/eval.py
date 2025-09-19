from typing import List
from collections import Counter

def _tok(s: str) -> List[str]:
    import re
    return [t for t in re.findall(r"[a-zA-Z0-9']+", s.lower()) if t]

def bleu_n(reference: str, candidate: str, n: int = 2) -> float:
    """Simple BLEU-n (no BP)."""
    ref = _tok(reference)
    cand = _tok(candidate)
    if n == 1:
        ref_counts = Counter(ref)
        match = sum(min(ref_counts[w], cand.count(w)) for w in set(cand))
        return match / max(len(cand), 1)
    elif n == 2:
        ref_bi = Counter(list(zip(ref, ref[1:])))
        cand_bi = list(zip(cand, cand[1:]))
        match = sum(min(ref_bi[p], cand_bi.count(p)) for p in set(cand_bi))
        return match / max(len(cand_bi), 1)
    else:
        raise ValueError("Only BLEU-1 and BLEU-2 supported")

def rouge_l(reference: str, candidate: str) -> float:
    """Very simple ROUGE-L (LCS / ref_len)."""
    ref = _tok(reference)
    cand = _tok(candidate)
    # LCS dynamic programming
    dp = [[0]*(len(cand)+1) for _ in range(len(ref)+1)]
    for i in range(1, len(ref)+1):
        for j in range(1, len(cand)+1):
            if ref[i-1] == cand[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    lcs = dp[-1][-1]
    return lcs / max(len(ref), 1)
