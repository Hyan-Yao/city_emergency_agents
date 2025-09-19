from typing import Dict, Any, List
import re
from rules import INCIDENT_LABELS, INCIDENT_SEVERITY_RULES

KEYWORDS = {
    "Flooding": ["flood", "water level", "inundat", "overflow", "sewage"],
    "PowerOutage": ["power out", "blackout", "no electricity", "transformer", "grid"],
    "MedicalShortage": ["medic", "clinic", "ambulance", "shortage", "pharmacy"],
    "Wildfire": ["wildfire", "brush fire", "smoke plume", "forest fire"],
    "TrafficAccident": ["accident", "collision", "crash", "pileup"],
    "HazmatSpill": ["chemical", "hazmat", "toxic", "spill", "leak"],
    "Earthquake": ["earthquake", "tremor"],
    "GasLeak": ["gas leak", "odor", "methane"],
    "WaterContamination": ["contaminat", "boil water", "e. coli"],
    "Heatwave": ["heatwave", "high temperature", "heat index"],
    "ColdSnap": ["freeze", "cold snap", "hypothermia"],
    "StormDamage": ["storm", "downed", "roof", "debris"],
    "BuildingFire": ["house fire", "apartment fire", "structure fire"],
    "RoadClosure": ["road closed", "closure", "detour"],
    "BridgeFailure": ["bridge", "collapse", "structural"],
    "Landslide": ["landslide", "mudslide"],
    "Drought": ["drought", "water restriction"],
    "CyberOutage": ["cyber", "ransomware", "system down"],
    "TelecomFailure": ["cell tower", "no signal", "telecom"],
    "DamFailure": ["dam", "spillway", "overtop"],
    "PublicHealthOutbreak": ["outbreak", "infection", "flu", "covid"],
    "Evacuation": ["evacuation", "evacuate"],
    "ShelterShortage": ["shelter full", "no beds"],
    "SupplyChainDisruption": ["supply chain", "delivery delay"],
    "PublicOrder": ["protest", "riot", "public order"],
    "AnimalIncident": ["animal", "dog bite", "livestock"],
    "Other": []
}

def _guess_incident(text: str) -> str:
    t = text.lower()
    best_label = "Other"
    best_hit = -1
    for label, kws in KEYWORDS.items():
        hits = sum(1 for kw in kws if kw in t)
        if hits > best_hit:
            best_hit = hits
            best_label = label
    return best_label

def _to_multihot(label: str) -> list:
    arr = [0]*len(INCIDENT_LABELS)
    try:
        idx = INCIDENT_LABELS.index(label)
        arr[idx] = 1
    except ValueError:
        arr[-1] = 1
    return arr

def infer(appeal_clean: str) -> Dict[str, Any]:
    label = _guess_incident(appeal_clean)
    severity = INCIDENT_SEVERITY_RULES.get(label, "Level I")

    # crude cause analysis
    cause = f"Likely {label.lower()} indicated by keyword patterns in the appeal; contributing factors require field verification."

    # simple recs per label
    recs: List[Dict[str,str]] = []
    def add(dep, act, tf): recs.append({"department": dep, "action": act, "timeframe": tf})

    if label == "Flooding":
        add("Public Works", "Deploy pumps and clear storm drains in affected blocks", "within 6 hours")
        add("Emergency Management", "Issue sandbag pickup notice and flood safety advisory", "within 3 hours")
    elif label == "PowerOutage":
        add("Utility", "Dispatch line crews to inspect feeders and restore power", "within 4 hours")
        add("Emergency Management", "Set up cooling/warming centers if outage > 8h", "contingent")
    elif label == "Wildfire":
        add("Fire Dept", "Establish containment lines and conduct structure triage", "immediate")
        add("Public Safety", "Prepare evacuation warnings for at-risk zones", "within 2 hours")
    else:
        add("311 Triage", "Open a work order and route to the responsible agency", "immediate")
        add("Operations", "Provide status update to the requester", "within 24 hours")

    return {
        "label": label,
        "incident_type_vec": _to_multihot(label),
        "severity": severity,
        "cause": cause,
        "recs": recs
    }
