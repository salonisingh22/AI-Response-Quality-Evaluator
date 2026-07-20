"""
Relevance Judge Agent (LLM-based).

Evaluates whether the AI response actually answers the user's
question -- not whether it's factually correct, just whether it
addresses what was asked.
"""

from src.agents.llm_client import call_judge

SYSTEM_PROMPT = """You are an expert evaluator. Your only job is to judge \
RELEVANCE: does the response actually answer the user's question? \
Do not judge factual correctness -- only whether the response addresses \
what was asked.

Score using this scale:
1 = completely irrelevant
2 = mostly irrelevant
3 = partially relevant
4 = mostly relevant
5 = fully answers the question

Respond ONLY with a JSON object in this exact format:
{"score": <integer 1-5>, "reasoning": "<one or two sentence explanation>"}
"""


def evaluate(question, ai_response):
    """
    Returns:
        dict: {"score": int (1-5), "reasoning": str, "normalized_score": float (0-1)}
    """
    user_prompt = f"Question: {question}\n\nResponse: {ai_response}"

    result = call_judge(SYSTEM_PROMPT, user_prompt)

    score = int(result["score"])
    score = max(1, min(score, 5))  # safety clamp in case model drifts out of range

    return {
        "score": score,
        "reasoning": result.get("reasoning", ""),
        "normalized_score": round((score - 1) / 4, 2),  # maps 1-5 to 0-1
    }


if __name__ == "__main__":
    # Test case from your mentor's example
    q = "Who invented Python?"
    r = "Python is a programming language used in AI."

    result = evaluate(q, r)
    print(f"Question: {q}")
    print(f"Response: {r}")
    print(f"Score: {result['score']}/5")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Normalized (0-1): {result['normalized_score']}")