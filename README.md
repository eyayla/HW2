# Multi-Agent Debate System for LLM Reasoning

This repository implements a **multi-agent debate framework** for improving reasoning in Large Language Models (LLMs). The system simulates a structured debate between two AI agents arguing opposite sides of a question, while a third agent acts as a judge.

The project was developed for the **Natural Language Processing (NLP) course assignment** and is inspired by research on multi-agent reasoning and AI debate.

---

# System Overview

The system contains three LLM agents:

### Debater A
Argues **YES** for the given question.

### Debater B
Argues **NO** and provides counterarguments.

### Judge
Observes the debate transcript and determines the final answer.

The pipeline follows four phases:

### Phase 1 — Initialization
Both debaters independently generate an initial answer.

### Phase 2 — Consensus Check
If both debaters agree on the same answer, the debate is skipped.

### Phase 3 — Multi-Round Debate
Agents exchange arguments for multiple rounds.

### Phase 4 — Judgment
The judge evaluates the debate transcript and outputs:

- Final answer
- Confidence score
- Short reasoning

---

# Dataset

The experiments use the **StrategyQA dataset** (Geva et al., 2021), which contains commonsense reasoning questions requiring multi-step inference.

For this assignment, a subset of:

**100 questions**

was used to balance evaluation quality and API cost.

Dataset location:

data/strategyqa_100.json


---

# Model

All agents use the same LLM through the UTSA API.

Model used:

Qwen/Qwen3-8B


---

# Installation

Clone the repository:

git clone https://github.com/eyayla/HW2.git

cd HW2


Install dependencies:

pip install -r requirements.txt


---

# Configuration

All hyperparameters are stored in:

config.py


Example configuration:

ROUNDS = 3
TEMPERATURE = 0.7
MAX_TOKENS = 256

DATASET_PATH = "data/strategyqa_100.json"
LOG_PATH = "logs/debate_logs.json"


This ensures that experiment settings are not hard-coded and can easily be modified.

---

# Running the Experiments

## Baseline Experiments

Run baseline evaluations:

python evaluate_baselines.py


This evaluates:

- Direct QA
- Self-Consistency

Example output:

BASELINE RESULTS

Direct QA Accuracy: 0.64
Self Consistency Accuracy: 0.63


---

## Debate System

Run the full debate pipeline:

python debate_pipeline.py


Example output:

FINAL RESULTS
Questions: 100
Correct: 63
Accuracy: 0.63


All debate transcripts are saved to:
logs/debate_logs.json


---

# Repository Structure

HW2/
│
├── debate_pipeline.py
├── evaluate_baselines.py
├── api_basics.py
├── config.py
├── requirements.txt
│
├── data/
│ └── strategyqa_100.json
│
├── prompts/
│ ├── debater_a.txt
│ ├── debater_b.txt
│ └── judge.txt
│
├── logs/
│ └── debate_logs.json
│
├── README.md
└── REPORT.md


---

# Logging

Each debate run records detailed logs including:

- question
- initial positions
- arguments from each round
- judge reasoning
- final verdict
- ground truth

Logs are stored in:

logs/debate_logs.json


This enables qualitative analysis of debate behavior.

---

# Evaluation Results

Three methods were compared:

| Method | Accuracy |
|------|------|
| Direct QA | 0.64 |
| Self Consistency | 0.63 |
| Debate Framework | 0.63 |

In this experiment, the debate framework performed similarly to self-consistency but did not outperform the direct QA baseline.

---

# Report

The full experimental report is available in:

REPORT.md


The report includes:

- methodology
- experimental results
- qualitative analysis
- prompt engineering discussion

---

# Academic Integrity

This project was completed individually for an NLP course assignment.

LLM tools (such as ChatGPT) were used for **coding assistance and debugging**, but the experimental design, implementation, and written analysis were completed by the author.

---

# Author

Elif Ercek  
UTSA — Natural Language Processing