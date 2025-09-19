# City Emergency Agents: Automated Emergency Response Planning with LLM + RAG

This repository implements the framework described in our paper *Automated Emergency Response Planning through a Personalized Large Language Model with Retrieval-Augmented Generation (RAG)*. It provides a practical, lightweight reference system for processing urban resident appeals, classifying needs, analyzing disaster causes, and generating actionable government response plans.

---

## 🚨 Motivation

Cities face increasing challenges from natural disasters and urban disruptions. Government hotlines (e.g., *12345*) receive vast volumes of heterogeneous resident appeals that must be **triaged, classified, and resolved rapidly**. Traditional manual processes struggle with:

* High text volume and redundancy
* Subjectivity in severity grading
* Inconsistent response recommendations

Our framework integrates **Large Language Models (LLMs)** with **Retrieval-Augmented Generation (RAG)** and a **dynamic memory of past cases** to address these challenges.

---

## 🏗 Framework Overview

The system pipeline consists of four major stages:

1. **Data Preprocessing & Representation**

   * Cleans raw appeals (removes noise, normalizes text)
   * Segments into key fields: request, solution, need

2. **Experience Memory Construction**

   * Stores historical request–solution pairs with embeddings
   * Enables semantic retrieval using cosine similarity

3. **Retrieval-Augmented Prompt Generation**

   * Retrieves top-*k* similar cases from memory
   * Composes a Chain-of-Thought (CoT) prompt with:

     * Task definition (expert role, output schema)
     * Common-sense reasoning activation
     * Stepwise need classification (N1–N27 taxonomy)

4. **LLM-based Disaster Evaluation & Strategy Formulation**

   * Produces structured outputs:

     * **Severity Score** (graded response levels)
     * **Cause Analysis** (root cause reasoning)
     * **Strategic Suggestions** (department, action, timeframe)

---

## 📊 Dataset

* **Sources**: *12345 Citizen Hotline*, *12369 Environmental Hotline*, *12320 Health Hotline*, Weibo, WeChat, government portals
* **Scale**: 336,928 resident appeals with paired government resolutions
* **Granularity**: Date, location, department, resolution process
* **Case Study**: 2023 Beijing extreme rainstorm (most severe in 140 years, \$10B+ losses, 1.31M residents affected)

---

## 🧩 Need Taxonomy (N1–N27)

Our model classifies appeals into 27 categories of resident needs, including:

* **Emergency Goods, Communication, Road Access, Water, Electricity, Rescue, Medical Relief, Evacuation, Housing, Compensation, Epidemic Prevention, Education**, etc.

Each appeal is first mapped into one or more of these need categories, then used for severity scoring and response generation.

---

## 🔑 Key Contributions

1. **Closed-loop formulation**: From appeal → response plan → government feedback
2. **Methodological innovation**: Fusing CoT reasoning with retrieval-based memory (dense embeddings instead of static knowledge graphs)
3. **Effectiveness**: RAG-enhanced LLM reduces hallucination and improves factual accuracy, validated via *LLM-as-judge* and expert review

---

## 📂 Repository Structure

```
city_emergency_agents/
  ├── __init__.py
  ├── agent.py              # Core inference pipeline
  ├── heuristics_llm.py     # Offline LLM heuristic stub
  ├── memory.py             # Memory store (RAG retrieval)
  ├── preprocessing.py      # Text cleaning
  ├── prompting.py          # CoT + RAG prompt builder
  ├── rules.py              # N1–N27 taxonomy, severity rules
  ├── schemas.py            # Data schemas (Plan, Output, etc.)
  ├── eval.py               # BLEU/ROUGE evaluation
  ├── demo.py               # Quick demo
  └── README.md
```

---

## 🚀 Quick Start

```bash
git clone <repo_url>
cd city_emergency_agents
python -m city_emergency_agents.demo
```

Example output:

```text
Plan(
  id='auto',
  incident_type=[0,1,0,...],
  cause_analysis="Likely power outage ...",
  recommendations=[
    {'department': 'Utility', 'action': 'Dispatch crews', 'timeframe': '4h'},
    {'department': 'Emergency Mgmt', 'action': 'Open cooling centers', 'timeframe': 'contingent'}
  ],
  debug={'mode': 'auto', 'retrieved_k': 2, ...}
)
```

---

## 📈 Evaluation

We evaluate generated outputs along three axes:

* **Severity grading accuracy** (compared to labeled data)
* **Recommendation quality** via *LLM-as-judge* auto-scorer
* **Human expert review** for factual consistency and actionability

Metrics: **BLEU-1/2**, **ROUGE-L**, and task-specific accuracy.

---

## 📜 Citation

If you use this repository or its methodology, please cite our paper:

> *Automated Emergency Response Planning through a Personalized Large Language Model with Retrieval-Augmented Generation (RAG)*, 2025.
