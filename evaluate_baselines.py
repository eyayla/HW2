import json
from api_basics import query_llm
from config import DATASET_PATH


# -----------------------------
# Load dataset
# -----------------------------

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

qa_test_data = [(item["question"], "Yes" if item["answer"] else "No") for item in data]


# -----------------------------
# Extract Yes/No
# -----------------------------

def extract_answer(text):

    text = text.lower()

    if "yes" in text:
        return "yes"

    if "no" in text:
        return "no"

    return "unknown"


# -----------------------------
# Direct QA baseline
# -----------------------------

def direct_qa(question):

    prompt = f"""
Answer the following question.

Question:
{question}

Respond ONLY in this format:

Answer: Yes or No
Reason: one short sentence
"""

    result = query_llm(prompt)

    if result:
        return result["text"]

    return "ERROR"


# -----------------------------
# Self-consistency baseline
# -----------------------------

def self_consistency(question, n=7):

    answers = []

    for _ in range(n):

        prompt = f"""
Answer the following question.

Question:
{question}

Respond ONLY:

Answer: Yes or No
"""

        result = query_llm(prompt)

        if result:

            ans = extract_answer(result["text"])

            if ans != "unknown":
                answers.append(ans)

    if len(answers) == 0:
        return "unknown"

    return max(set(answers), key=answers.count)


# -----------------------------
# Run experiments
# -----------------------------

def run_baselines():

    total = len(qa_test_data)

    correct_direct = 0
    correct_sc = 0

    for question, truth in qa_test_data:

        print("\n====================")
        print("QUESTION:", question)

        # Direct QA
        direct_result = direct_qa(question)

        direct_answer = extract_answer(direct_result)

        print("\nDirect QA:", direct_answer)

        if direct_answer == truth.lower():
            correct_direct += 1

        # Self Consistency
        sc_answer = self_consistency(question)

        print("Self Consistency:", sc_answer)

        if sc_answer == truth.lower():
            correct_sc += 1

    acc_direct = round(correct_direct / total, 2)
    acc_sc = round(correct_sc / total, 2)

    print("\n============================")
    print("BASELINE RESULTS")

    print("\nDirect QA Accuracy:", acc_direct)
    print("Self Consistency Accuracy:", acc_sc)


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    run_baselines()