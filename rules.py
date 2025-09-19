# Incident categories (N1..N27) — example labels; extend as needed.
INCIDENT_LABELS = [
    "Flooding", "PowerOutage", "MedicalShortage", "Wildfire", "TrafficAccident",
    "HazmatSpill", "Earthquake", "GasLeak", "WaterContamination", "Heatwave",
    "ColdSnap", "StormDamage", "BuildingFire", "RoadClosure", "BridgeFailure",
    "Landslide", "Drought", "CyberOutage", "TelecomFailure", "DamFailure",
    "PublicHealthOutbreak", "Evacuation", "ShelterShortage", "SupplyChainDisruption",
    "PublicOrder", "AnimalIncident", "Other"
]

# Severity mapping rules (example; tune per jurisdiction)
INCIDENT_SEVERITY_RULES = {
    "Flooding": "Level II",
    "PowerOutage": "Level I",
    "MedicalShortage": "Level III",
    "Wildfire": "Level II",
    "TrafficAccident": "Level I",
    "HazmatSpill": "Level III",
    "Earthquake": "Level III",
    "GasLeak": "Level II",
    "WaterContamination": "Level III",
    "Heatwave": "Level II",
    "ColdSnap": "Level II",
    "StormDamage": "Level II",
    "BuildingFire": "Level II",
    "RoadClosure": "Level I",
    "BridgeFailure": "Level III",
    "Landslide": "Level II",
    "Drought": "Level II",
    "CyberOutage": "Level I",
    "TelecomFailure": "Level I",
    "DamFailure": "Level III",
    "PublicHealthOutbreak": "Level III",
    "Evacuation": "Level II",
    "ShelterShortage": "Level II",
    "SupplyChainDisruption": "Level II",
    "PublicOrder": "Level I",
    "AnimalIncident": "Level I",
    "Other": "Level I"
}
