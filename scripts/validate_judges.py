"""
Validates the three LLM judge agents against a sample of the
TruthfulQA benchmark data, checking scoring consistency.

For each sample: ask the judges to evaluate the CORRECT answer
(should score high) and re-run twice to check for consistency
(since temperature=0 should give near-identical results each time).
"""

import sys
import os

# Ensure project root is on the path so 'src' imports work when running
# this script directly (python scripts\validate_judges.py)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import json
import random

from src.rag.knowledge_base import load_documents
from src.agents.relevance_judge import evaluate as relevance_judge
from src.agents.accuracy_judge import evaluate as accuracy_judge
from src.agents.hallucination_judge import evaluate as hallucination_judge

SAMPLE_SIZE = 5
RANDOM_SEED = 42


def run_validation():
    documents = load_documents()
    truthfulqa_docs = [d for d in documents if d["source"] == "truthfulqa"]

    random.seed(RANDOM_SEED)
    sample = random.sample(truthfulqa_docs, SAMPLE_SIZE)

    results = []

    for doc in sample:
        question = doc["question"]
        correct_answer = doc["answer"]

        print(f"\n{'='*70}")
        print(f"Question: {question}")
        print(f"Correct answer (used as both response and evidence): {correct_answer}")

        # Run twice to check consistency (temperature=0 should be stable)
        run1_relevance = relevance_judge(question, correct_answer)
        run2_relevance = relevance_judge(question, correct_answer)

        run1_accuracy = accuracy_judge(correct_answer, correct_answer)
        run2_accuracy = accuracy_judge(correct_answer, correct_answer)

        run1_halluc = hallucination_judge(correct_answer, correct_answer)
        run2_halluc = hallucination_judge(correct_answer, correct_answer)

        relevance_consistent = run1_relevance["score"] == run2_relevance["score"]
        accuracy_consistent = run1_accuracy["score"] == run2_accuracy["score"]
        halluc_consistent = run1_halluc["hallucination_detected"] == run2_halluc["hallucination_detected"]

        print(f"Relevance:     {run1_relevance['score']}/5 -> {run2_relevance['score']}/5  [consistent: {relevance_consistent}]")
        print(f"Accuracy:      {run1_accuracy['score']}/5 -> {run2_accuracy['score']}/5  [consistent: {accuracy_consistent}]")
        print(f"Hallucination: {run1_halluc['hallucination_detected']} -> {run2_halluc['hallucination_detected']}  [consistent: {halluc_consistent}]")

        results.append({
            "question": question,
            "relevance_scores": [run1_relevance["score"], run2_relevance["score"]],
            "accuracy_scores": [run1_accuracy["score"], run2_accuracy["score"]],
            "hallucination_results": [run1_halluc["hallucination_detected"], run2_halluc["hallucination_detected"]],
            "relevance_consistent": relevance_consistent,
            "accuracy_consistent": accuracy_consistent,
            "hallucination_consistent": halluc_consistent,
        })

    # Summary
    total = len(results)
    rel_consistent_count = sum(1 for r in results if r["relevance_consistent"])
    acc_consistent_count = sum(1 for r in results if r["accuracy_consistent"])
    hal_consistent_count = sum(1 for r in results if r["hallucination_consistent"])

    print(f"\n{'='*70}")
    print("VALIDATION SUMMARY")
    print(f"{'='*70}")
    print(f"Samples tested: {total}")
    print(f"Relevance Judge consistency:     {rel_consistent_count}/{total}")
    print(f"Accuracy Judge consistency:      {acc_consistent_count}/{total}")
    print(f"Hallucination Judge consistency: {hal_consistent_count}/{total}")

    with open("docs/judge_validation_results.json", "w", encoding="utf-8") as f:
        json.dump(results, f, indent=2)
    print("\nFull results saved to docs/judge_validation_results.json")


if __name__ == "__main__":
    run_validation()