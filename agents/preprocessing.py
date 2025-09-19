import re

def rewrite_and_clean(appeal_raw: str) -> str:
    """Normalize user appeal text:
    - Keep key tokens: location, time, objects, counts (rough)
    - Remove emojis, duplicate spaces, profanity (rudimentary)
    - Output short sentences / bullet-ish phrases (simple rules)
    """
    if not appeal_raw:
        return ""
    s = appeal_raw

    # Remove emojis / non-basic symbols
    s = re.sub(r'[\U00010000-\U0010ffff]', ' ', s)  # strip astral plane chars
    s = re.sub(r'[^\w\s,.;:/\-#@()]', ' ', s)

    # Normalize whitespace
    s = re.sub(r'\s+', ' ', s).strip()

    # Split into clauses by punctuation
    parts = re.split(r'[.;]', s)
    parts = [p.strip() for p in parts if p.strip()]

    # Deduplicate simple repeats
    out = []
    seen = set()
    for p in parts:
        key = p.lower()
        if key not in seen:
            out.append(p)
            seen.add(key)

    return "; ".join(out)
