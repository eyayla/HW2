# Multi-Agent Debate for Reasoning with Large Language Models

## 1. Methodology

### System Architecture

This project implements a multi-agent debate framework for improving reasoning in Large Language Models (LLMs). The system consists of three agents: **Debater A**, **Debater B**, and a **Judge**. The two debaters argue opposing sides of a question, while the judge evaluates the debate and determines the final answer.

The architecture is inspired by the debate framework proposed by Irving et al. (2018), where adversarial reasoning between two agents is used to expose weaknesses in arguments and improve decision quality.

The system follows a four-phase pipeline:

1. Initialization
2. Multi-round debate
3. Judgment
4. Evaluation

The overall workflow is shown below:

Question → Initial Positions → Consensus Check → Debate Rounds → Judge Decision → Evaluation

---

### Phase 1: Initialization

In the initialization phase, the question is presented independently to both debaters. Each debater generates an **initial position**, consisting of a yes/no answer and a short explanation. Importantly, the two debaters do not see each other’s responses at this stage.

After both initial answers are produced, the system performs a **consensus check**. If both debaters produce the same answer, the system records consensus and skips the debate phase. This mechanism avoids unnecessary computation when the model already agrees on the answer.

---

### Phase 2: Multi-Round Debate

If the initial answers disagree, the system proceeds to a structured multi-round debate. In this phase, Debater A presents an argument supporting its position, and Debater B responds with a counterargument.

The debate runs for a maximum of **N rounds**, where N is set to 3 in our implementation. Each debater receives the full debate transcript from previous rounds as context. This allows the agents to refine their arguments and respond directly to the opponent’s reasoning.

An **adaptive stopping criterion** is implemented to reduce unnecessary computation. If both agents converge to the same answer for two consecutive rounds, the debate stops early.

---

### Phase 3: Judgment

After the debate ends, the judge agent receives the full debate transcript together with the original question. The judge analyzes the arguments presented by both debaters and produces a structured decision.

The judge output includes:

- Analysis of both debaters’ arguments
- Identification of the strongest argument from each side
- Identification of the weakest argument from each side
- Final answer (Yes or No)
- Confidence score from 1 to 5

This structured evaluation allows the debate process to be analyzed and logged for later inspection.

---

### Phase 4: Evaluation

The final answer produced by the judge is compared with the ground-truth answer from the dataset. The overall system performance is measured using **accuracy**, defined as the proportion of correctly answered questions.

All intermediate information, including initial positions, debate arguments, judge reasoning, and final verdicts, is stored in a JSON log file. This enables qualitative analysis of debate behavior and reasoning patterns.

---

### Model and Configuration

All agents in the system use the same underlying language model accessed through the UTSA LLM API.

Model used:

Qwen/Qwen3-8B

The following configuration parameters were used in the experiments:

- Debate rounds: 3
- Temperature: 0.7
- Maximum tokens: 256
- Dataset size: 100 questions

The task domain selected for this project is **commonsense question answering**, using the StrategyQA dataset (Geva et al., 2021). This dataset was chosen because it contains questions requiring multi-step reasoning and world knowledge, making it a suitable benchmark for evaluating debate-based reasoning systems.

## 2. Experiments

### Dataset

The experiments were conducted using the **StrategyQA dataset** (Geva et al., 2021). StrategyQA is a benchmark designed for evaluating multi-step reasoning and commonsense knowledge in question answering systems. Each question in the dataset requires implicit reasoning steps that cannot be answered using simple fact retrieval.

StrategyQA questions are formatted as **yes/no questions** and often require combining multiple pieces of knowledge. For example, answering whether two historical events overlapped in time may require reasoning about dates and historical context.

To keep the computational cost manageable while still obtaining meaningful results, a subset of **100 questions** was randomly sampled from the original dataset. Each question includes a ground-truth answer that is used to evaluate system accuracy.

---

### Experimental Setup

All experiments were conducted using the **Qwen/Qwen3-8B** language model accessed through the UTSA LLM API. The same model was used for all agents in the system, including both debaters and the judge.

The following configuration parameters were used during the experiments:

- Number of debate rounds: **3**
- Temperature: **0.7**
- Maximum tokens per response: **256**
- Dataset size: **100 questions**

Each experiment was executed by running the corresponding Python script:

- `evaluate_baselines.py` for baseline models
- `debate_pipeline.py` for the multi-agent debate framework

For each question, the system recorded the following information:

- initial positions of both debaters
- arguments generated in each round
- the final judge decision
- confidence score
- ground-truth label

All debate transcripts and intermediate outputs were stored in a JSON log file to enable further analysis.

---

### Baseline Methods

To evaluate whether debate improves reasoning performance, two baseline approaches were implemented.

#### Direct Question Answering

The first baseline is **Direct QA**, where the language model answers the question directly without debate.

In this setup, the model receives the question and produces a final answer with a short explanation. The pipeline can be represented as:

Question → LLM → Final Answer

This baseline represents the most common usage of LLMs for question answering tasks.

---

#### Self-Consistency

The second baseline is **Self-Consistency**, introduced by Wang et al. (2023). Instead of generating a single answer, the model produces multiple responses for the same question. The final answer is determined using **majority voting**.

The process works as follows:

1. The model generates multiple answers to the same question.
2. Each answer includes a yes/no prediction.
3. The final answer is selected based on the majority vote among the generated responses.

Self-consistency aims to improve reasoning by sampling different reasoning paths and selecting the most consistent answer.

---

### Debate Framework

The main system evaluated in this project is the **multi-agent debate framework**. In this system, two agents argue opposing sides of a question while a third agent acts as a judge.

The debate protocol consists of the following steps:

1. Each debater produces an initial position independently.
2. If both answers match, the system records consensus and skips the debate phase.
3. If the answers differ, the agents engage in a multi-round debate.
4. The judge analyzes the debate transcript and produces the final verdict.

This framework aims to improve reasoning by exposing weaknesses in arguments through adversarial discussion.

---

### Experimental Results

The results of all experiments are summarized in Table 1.

| Method | Accuracy |
|------|------|
| Direct QA | **0.64** |
| Self Consistency | **0.63** |
| Debate Framework | **0.63** |

Table 1: Accuracy comparison between baseline methods and the debate system.

---

### Discussion of Results

The results show that the Direct QA baseline achieved the highest accuracy at **0.64**. The Self-Consistency approach produced slightly lower accuracy at **0.63**, suggesting that sampling multiple reasoning paths did not significantly improve performance for this dataset.

The debate framework also achieved **0.63 accuracy**, matching the performance of self-consistency but not surpassing the direct QA baseline.

One possible explanation is that both debaters rely on the **same underlying language model**. As a result, the arguments generated by both sides may not provide sufficiently diverse reasoning strategies. Instead of introducing fundamentally different perspectives, the debate often reinforces the model’s original reasoning.

Another factor is that StrategyQA questions rely heavily on **commonsense knowledge**, which the model may already handle effectively in a single forward pass. In such cases, additional debate rounds may not provide a significant advantage.

Despite not improving overall accuracy, the debate framework provides valuable insights into the reasoning process. The generated debate transcripts allow us to observe how arguments evolve over multiple rounds and how the judge evaluates competing claims.

## 3. Analysis of Debate Transcripts

To better understand how the debate framework behaves, several debate transcripts were manually inspected. This section presents qualitative analysis of selected examples, including both successful and failure cases. The goal is to identify when debate improves reasoning and when it fails.

---

### Example 1 – Successful Case (Consensus without Debate)

Question:

Is Drew Carey important to the history of wrestling?

Both debaters produced initial arguments that suggested Drew Carey had some influence on wrestling through media appearances. Since both agents agreed on the same answer, the system detected consensus and skipped the debate phase.

The judge produced the following verdict:

Final Answer: Yes  
Confidence: 4

This example demonstrates how the **consensus mechanism reduces unnecessary computation**. When both agents independently converge to the same answer, running multiple debate rounds provides little additional value. Skipping the debate phase in such cases improves efficiency while maintaining accuracy.

---

### Example 2 – Successful Debate with Multi-Round Arguments

Question:

Is the Louvre in billionaire George Soros's price range?

In this case the initial answers disagreed, triggering the debate phase. Over multiple rounds, both agents refined their arguments regarding the legal and cultural status of the Louvre.

Debater A emphasized the monetary perspective and Soros’s wealth, while Debater B argued that the Louvre is a national institution that cannot be privately purchased.

The judge ultimately concluded:

Final Answer: No  
Confidence: 5

This example illustrates how debate helps clarify **legal and conceptual misunderstandings**. Through repeated counterarguments, the debate converged on the correct interpretation that the Louvre is not a purchasable asset.

---

### Example 3 – Failure Case (Incorrect Reasoning)

Question:

Did a Mediterranean Sea creature kill Steve Irwin?

In this case, Debater A incorrectly claimed that Steve Irwin was killed by a whip snake. Debater B also referenced the whip snake but incorrectly described its geographic origin. Neither debater correctly identified that Steve Irwin died after being pierced by a **stingray barb**.

The judge ultimately answered:

Final Answer: No

However, the ground truth label in the dataset is:

Ground Truth: Yes

This failure demonstrates a key limitation of debate systems: if **both agents share the same incorrect knowledge**, the debate cannot correct the error. Since both arguments relied on incorrect premises, the judge was unable to recover the correct answer.

---

### Example 4 – Argument Repetition During Debate

Question:

Do people who smoke Djarum's like cloves?

In this debate, both agents repeated nearly identical arguments across multiple rounds. Debater A repeatedly emphasized that Djarum cigarettes are flavored with cloves, while Debater B argued that not all smokers necessarily like cloves.

Because neither side introduced new evidence or reasoning, the debate rounds became largely repetitive. The judge ultimately answered:

Final Answer: Yes  
Confidence: 4

This example highlights a common issue in multi-agent debate systems: **argument stagnation**. Without mechanisms encouraging diverse reasoning, agents often repeat the same arguments instead of refining their claims.

---

### Summary of Observations

From the transcript analysis, several patterns emerge:

1. The consensus mechanism effectively reduces unnecessary debate rounds.
2. Debate can help clarify conceptual misunderstandings when agents provide different reasoning paths.
3. Debate cannot correct errors if both agents rely on incorrect knowledge.
4. Multi-round debates sometimes suffer from argument repetition when agents fail to introduce new reasoning.

These observations align with prior research on multi-agent debate systems (Irving et al., 2018; Liang et al., 2024), which suggests that debate can improve reasoning quality but also introduces challenges related to agent diversity and knowledge limitations.

## 4. Prompt Engineering

Prompt design plays a crucial role in controlling the behavior of LLM agents within the debate framework. In this project, separate prompt templates were designed for three different agents: **Debater A**, **Debater B**, and the **Judge**. The prompts were iteratively refined to ensure consistent behavior, reduce verbosity, and produce structured outputs suitable for evaluation.

---

### Debater Prompts

Two debater roles were defined to simulate adversarial reasoning.

Debater A was instructed to argue in favor of the **Yes** position, while Debater B was instructed to argue for the **No** position. Explicit role framing was used to ensure that each agent consistently defended its assigned stance throughout the debate.

The prompt for Debater A included:

- the original question
- the full debate history
- instructions to generate an argument supporting the Yes position

Similarly, Debater B received the same information but was instructed to produce a counterargument supporting the No position.

To maintain clarity and reduce unnecessary verbosity, the following constraints were included in the prompt:

- maximum of three sentences
- no explanation of internal reasoning
- no meta-commentary about the role

These restrictions helped produce concise arguments that could easily be compared and evaluated by the judge.

---

### Debate Context Design

Each debater received the **full debate transcript from previous rounds** as part of the prompt context. This design allowed the agents to respond directly to the opponent’s arguments.

Providing the debate history enables iterative reasoning where agents refine their claims, identify weaknesses in previous arguments, and introduce counterarguments. This mechanism mimics real-world debates where participants adapt their reasoning in response to new information.

However, in practice the transcripts revealed that agents sometimes repeated earlier arguments instead of introducing new evidence. This suggests that further prompt engineering could be used to encourage more diverse reasoning strategies.

---

### Judge Prompt

The judge prompt was designed to produce a **structured evaluation** of the debate. Unlike the debaters, the judge was instructed to analyze both sides objectively before producing a final verdict.

The judge output format was constrained to include:

Final Answer: Yes or No  
Confidence: 1–5  
Reason: short explanation

This structured format was necessary for automatically extracting the verdict and computing accuracy during evaluation.

The judge prompt also instructed the model to evaluate:

- which debater provided stronger arguments
- which arguments were weaker or flawed
- the final decision based on the debate transcript

Using a structured output format ensured that the evaluation script could reliably parse the model's decision.

---

### Prompt Iteration Process

Several prompt iterations were performed during development.

Early prompt versions allowed the model to generate long explanations, which produced overly verbose debate transcripts. These outputs made evaluation difficult and increased API costs.

To address this issue, stricter prompt constraints were introduced:

- limiting arguments to three sentences
- explicitly forbidding role explanations
- removing internal reasoning statements

These adjustments significantly improved the clarity and consistency of the generated debate arguments.

Overall, careful prompt design was essential for ensuring that the agents behaved consistently and produced outputs compatible with the evaluation pipeline.

## Appendix: Full Prompt Templates

This appendix contains the complete prompt templates used for the debate agents and the judge. These prompts are stored in the repository under the `prompts/` directory.

---

### Debater A Prompt

File: `prompts/debater_a.txt`

You are Debater A in a debate.

Your position: YES.

Question:
{question}

Debate history:
{history}

Write ONLY the argument supporting YES.

Rules:
- Maximum 3 sentences
- Do NOT explain your thinking
- Do NOT describe your role
- Do NOT say "Okay"
- Just give the argument

Argument:


---

### Debater B Prompt

File: `prompts/debater_b.txt`

You are Debater B in a debate.

Your position: NO.

Question:
{question}

Debate history:
{history}

Write ONLY the counterargument supporting NO.

Rules:
- Maximum 3 sentences
- Do NOT explain your thinking
- Do NOT describe your role
- Just give the counterargument

Counterargument:

You are Debater B in a debate.

Your position: NO.

Question:
{question}

Debate history:
{history}

Write ONLY the counterargument supporting NO.

Rules:
- Maximum 3 sentences
- Do NOT explain your thinking
- Do NOT describe your role
- Just give the counterargument

Counterargument:

You are the judge of a debate.

Question:
{question}

Debate transcript:
{history}

Decide which answer is correct.

Respond ONLY in this format:

Final Answer: Yes or No
Confidence: 1-5
Reason: one short sentence


---

### Prompt Design Summary

The prompts were designed to enforce clear role separation between agents and ensure structured outputs. Debater prompts emphasize adversarial reasoning, while the judge prompt focuses on evaluation and decision-making.

All prompts are stored as editable templates in the repository to ensure reproducibility and transparency.