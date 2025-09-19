from memory import MemoryStore, MemoryItem
from agent import LLM_AGENT_INFER

def build_demo_memory():
    ms = MemoryStore()
    ms.insert(MemoryItem(
        id="M1",
        q_text="Basement flooding reported near 5th Ave; water backing up through storm drains.",
        a_solution="Public Works deploy pumps; EM posts sandbag sites; alert residents.",
        incident_type=[1]+[0]*26  # not strictly accurate, just a placeholder
    ))
    ms.insert(MemoryItem(
        id="M2",
        q_text="Neighborhood blackout after transformer failure; seniors need cooling center.",
        a_solution="Utility crews dispatched; open community center for cooling if >8h outage.",
        incident_type=[0,1]+[0]*25
    ))
    return ms

if __name__ == "__main__":
    memory = build_demo_memory()
    appeal = "Power is out around Maple Street since last night. Traffic lights are dark; elderly residents in an apartment complex are asking for help."
    plan = LLM_AGENT_INFER(appeal, memory=memory, mode="auto", k=2)
    print(plan)
