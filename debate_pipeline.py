import json
from api_basics import query_llm
from config import ROUNDS, DATASET_PATH, LOG_PATH


# -----------------------------
# Load dataset
# -----------------------------

with open(DATASET_PATH, "r", encoding="utf-8") as f:
    data = json.load(f)

qa_test_data = [(item["question"], "Yes" if item["answer"] else "No") for item in data]


# -----------------------------
# Prompt loader
# -----------------------------

def load_prompt(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# -----------------------------
# Extract Yes / No
# -----------------------------

def extract_answer(text):

    text = text.lower()

    if "yes" in text:
        return "yes"

    if "no" in text:
        return "no"

    return "unknown"


# -----------------------------
# Parse Judge Output
# -----------------------------

def parse_judge_output(text):

    verdict = "unknown"
    confidence = None
    reason = ""

    for line in text.split("\n"):

        line_clean = line.strip().lower()

        if "final answer" in line_clean:
            if "yes" in line_clean:
                verdict = "yes"
            elif "no" in line_clean:
                verdict = "no"

        if "confidence" in line_clean:
            try:
                confidence = int(line_clean.split(":")[-1].strip())
            except:
                confidence = None

        if "reason" in line_clean:
            reason = line.split(":", 1)[-1].strip()

    return verdict, confidence, reason


# -----------------------------
# Debater A
# -----------------------------

def debater_a(question, transcript):

    template = load_prompt("prompts/debater_a.txt")

    prompt = template.format(
        question=question,
        history=transcript
    )

    result = query_llm(prompt)

    if result:
        return result["text"]

    return "ERROR"


# -----------------------------
# Debater B
# -----------------------------

def debater_b(question, transcript):

    template = load_prompt("prompts/debater_b.txt")

    prompt = template.format(
        question=question,
        history=transcript
    )

    result = query_llm(prompt)

    if result:
        return result["text"]

    return "ERROR"


# -----------------------------
# Judge
# -----------------------------

def judge(question, transcript):

    template = load_prompt("prompts/judge.txt")

    prompt = template.format(
        question=question,
        history=transcript
    )

    result = query_llm(prompt)

    if result:
        return result["text"]

    return "ERROR"


# -----------------------------
# Debate Runner
# -----------------------------

def run_debate():

    correct = 0
    total = len(qa_test_data)

    logs = []

    for question, truth in qa_test_data:

        print("\n============================")
        print("QUESTION:", question)

        # -----------------------------
        # Phase 1 — Initial Positions
        # -----------------------------

        print("\n--- INITIAL POSITIONS ---")

        initial_A = debater_a(question, "")
        print("\nDebater A initial:")
        print(initial_A)

        initial_B = debater_b(question, "")
        print("\nDebater B initial:")
        print(initial_B)

        answer_A = extract_answer(initial_A)
        answer_B = extract_answer(initial_B)

        # Transcript starts with initial positions
        transcript = f"""
Initial Position A:
{initial_A}

Initial Position B:
{initial_B}
"""

        debate_log = {
            "question": question,
            "initial_positions": {
                "A": initial_A,
                "B": initial_B
            },
            "rounds": [],
            "transcript": "",
            "judge": {},
            "ground_truth": truth
        }

        # -----------------------------
        # Phase 1.5 — Consensus Check
        # -----------------------------

        if answer_A == answer_B and answer_A != "unknown":

            print("\nCONSENSUS DETECTED — Skipping debate")

        else:

            # -----------------------------
            # Phase 2 — Multi-Round Debate
            # -----------------------------

            prev_answer_A = None
            prev_answer_B = None

            for r in range(ROUNDS):

                print(f"\n--- ROUND {r+1} ---")

                A = debater_a(question, transcript)

                print("\nDebater A:")
                print(A)

                transcript += f"\nRound {r+1} - Debater A:\n{A}\n"

                B = debater_b(question, transcript)

                print("\nDebater B:")
                print(B)

                transcript += f"\nRound {r+1} - Debater B:\n{B}\n"

                debate_log["rounds"].append({
                    "round": r + 1,
                    "debater_a": A,
                    "debater_b": B
                })

                current_A = extract_answer(A)
                current_B = extract_answer(B)

                # -----------------------------
                # Adaptive Stopping
                # -----------------------------

                if current_A == current_B and current_A != "unknown":

                    if prev_answer_A == current_A and prev_answer_B == current_B:
                        print("\nADAPTIVE STOPPING — Agents converged")
                        break

                prev_answer_A = current_A
                prev_answer_B = current_B

        # Save transcript
        debate_log["transcript"] = transcript

        # -----------------------------
        # Phase 3 — Judge
        # -----------------------------

        J = judge(question, transcript)

        verdict, confidence, reason = parse_judge_output(J)

        debate_log["judge"] = {
            "raw_output": J,
            "verdict": verdict,
            "confidence": confidence,
            "reason": reason
        }

        if verdict == truth.lower():
            correct += 1

        print("\nJudge:")
        print(J)

        print("\nGround Truth:", truth)

        logs.append(debate_log)

    accuracy = round(correct / total, 2)

    print("\n============================")
    print("FINAL RESULTS")
    print("Questions:", total)
    print("Correct:", correct)
    print("Accuracy:", accuracy)

    # -----------------------------
    # Save Logs
    # -----------------------------

    with open(LOG_PATH, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)


# -----------------------------
# Main
# -----------------------------

if __name__ == "__main__":
    run_debate()