"""
Accuracy Judge Agent (LLM-based).

Compares the AI response against a reference answer / retrieved chunk
to check factual correctness. Must never invent evidence -- grounding
comes strictly from the provided reference/evidence text, and if the
evidence doesn't actually address the response's claim, accuracy
cannot be verified and must be scored low.
"""

from src.agents.llm_client import call_judge

SYSTEM_PROMPT = """You are a strict fact-checking evaluator. Your only job is to judge \
ACCURACY: does the response factually match the provided evidence \
(reference answer / retrieved chunk)?

CRITICAL RULES -- follow these exactly:
- You must rely ONLY on the provided evidence text. Do not use outside \
knowledge, training data, or general world facts, even if you believe \
them to be true.
- If the evidence is about a completely different topic than the response \
and does not address the response's claim at all, you CANNOT verify the \
response as correct -- score it low (1 or 2), since accuracy cannot be \
confirmed from irrelevant evidence.
- Only score high (4 or 5) if the evidence explicitly confirms the \
response's claim.
- If the response contradicts the evidence, score low (1 or 2).

Score using this scale:
1 = completely incorrect / contradicts evidence / evidence is unrelated and cannot verify the claim
2 = mostly incorrect or unverifiable
3 = partially correct
4 = mostly correct, evidence supports most of the claim
5 = fully correct, evidence explicitly confirms the claim

Respond ONLY with a JSON object in this exact format:
{"score": <integer 1-5>, "reasoning": "<one or two sentence explanation, stating explicitly whether the evidence actually addresses the response's topic>", "evidence_used": "<the exact evidence text you compared against>"}
"""


def evaluate(ai_response, evidence):
    """
    Args:
        ai_response (str): the AI-generated response being evaluated
        evidence (str): reference answer or retrieved RAG chunk

    Returns:
        dict: {"score": int (1-5), "reasoning": str, "evidence_used": str,
               "normalized_score": float (0-1)}
    """
    user_prompt = f"Evidence: {evidence}\n\nResponse to evaluate: {ai_response}"

    result = call_judge(SYSTEM_PROMPT, user_prompt)

    score = int(result["score"])
    score = max(1, min(score, 5))

    return {
        "score": score,
        "reasoning": result.get("reasoning", ""),
        "evidence_used": result.get("evidence_used", evidence),
        "normalized_score": round((score - 1) / 4, 2),
    }


if __name__ == "__main__":
    # Test case from your mentor's example
    evidence = "Canberra is the capital city of Australia."
    response = "Sydney"

    result = evaluate(response, evidence)
    print(f"Evidence: {evidence}")
    print(f"Response: {response}")
    print(f"Score: {result['score']}/5")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Evidence used: {result['evidence_used']}")
    print(f"Normalized (0-1): {result['normalized_score']}")

    print()

    # Mismatch test -- evidence completely unrelated to the response
    evidence2 = "The watermelon seeds pass through your digestive system"
    response2 = "capital of india is New Delhi"

    result2 = evaluate(response2, evidence2)
    print(f"Evidence: {evidence2}")
    print(f"Response: {response2}")
    print(f"Score: {result2['score']}/5")
    print(f"Reasoning: {result2['reasoning']}")