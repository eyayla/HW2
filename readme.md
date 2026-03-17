# LLM Debate System – NLP Assignment

## Overview

This project implements a **multi-agent debate system using Large Language Models (LLMs)** for reasoning tasks.
Two agents argue opposing positions (Yes / No) about a question, and a **judge model evaluates the debate and decides the final answer**.

The goal of this project is to explore whether **structured debate between LLM agents can improve reasoning performance** on complex question-answering tasks.

The system was evaluated using the **StrategyQA dataset**, which contains questions requiring multi-step commonsense reasoning.

---

## Dataset

This project uses the **StrategyQA dataset**:

Geva et al., 2021
*Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies*

StrategyQA contains **yes/no questions that require implicit reasoning**.

For this assignment:

* **100 questions** were sampled from the dataset
* Each question includes a **ground truth answer (Yes/No)**

Example question:

> Did the Roman Empire exist at the same time as the Mayan civilization?

---

## Model

The debate system uses:

**Qwen3-8B**

The model is accessed through the **UTSA LLM API endpoint**.

Each debate consists of:

* Debater A (argues **YES**)
* Debater B (argues **NO**)
* Judge agent (decides the final answer)

---

## Debate Process

For every question:

1. Debater A produces an argument supporting **YES**
2. Debater B produces a counterargument supporting **NO**
3. The debate runs for **multiple rounds**
4. The judge reviews the entire transcript
5. The judge outputs:

Final Answer: Yes / No
Confidence: 1–5
Reason: short explanation

---

## Project Structure

```
HW2_ELIF_ERCEK/

api_basics.py        # LLM API interface
debate_pipeline.py   # debate orchestration
config.py            # hyperparameters and paths

data/
    strategyqa_100.json   # dataset

prompts/
    debater_a.txt
    debater_b.txt
    judge.txt

logs/
    debate_logs.json      # saved debate transcripts

requirements.txt
README.md
```

---

## Configuration

All important hyperparameters are stored in **config.py**.

Example configuration:

* model name
* temperature
* max tokens
* number of debate rounds
* dataset path
* log file path

This ensures **reproducibility and clean code structure**.

---

## Prompt Templates

All prompts are stored in the **prompts/** directory as editable templates.

Examples:

* debater_a.txt
* debater_b.txt
* judge.txt

Variables such as `{question}` and `{history}` are dynamically inserted during execution.

---

## Logging

All debate transcripts are automatically saved as JSON.

Output file:

```
logs/debate_logs.json
```

Each entry contains:

* question
* debate rounds
* arguments from each debater
* judge decision
* ground truth answer

Example log entry:

```
{
  "question": "...",
  "rounds": [
    {
      "round": 1,
      "debater_a": "...",
      "debater_b": "..."
    }
  ],
  "judge": "...",
  "ground_truth": "Yes"
}
```

---

## Installation

Install required dependencies:

```
pip install -r requirements.txt
```

---

## Running the Debate System

To run the full experiment:

```
python debate_pipeline.py
```

The script will:

* run debates for all questions
* display debate rounds in the terminal
* compute final accuracy
* save debate transcripts to JSON logs

---

## Evaluation

Accuracy is computed by comparing:

**Judge Final Answer vs Ground Truth**

Example output:

```
FINAL RESULTS
Questions: 100
Correct: 69
Accuracy: 0.69
```

---

## Reproducibility

All experiments can be reproduced by:

1. Installing dependencies
2. Running the debate pipeline

```
python debate_pipeline.py
```

---

## References

Geva, M., Khashabi, D., Segal, E., Khot, T., Roth, D., & Berant, J. (2021).

*Did Aristotle Use a Laptop? A Question Answering Benchmark with Implicit Reasoning Strategies.*

Transactions of the Association for Computational Linguistics (TACL).
