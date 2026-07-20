"""
Hallucination Detection Agent (LLM-based).

Splits the response into individual factual claims and checks each
one against the provided evidence. A claim is "hallucinated" if the
evidence does not explicitly support it -- this is not the same as
being wrong; it means there's no evidence for it either way.
"""

from src.agents.llm_client import call_judge

SYSTEM_PROMPT = """You are a strict fact-checking evaluator. Your job is to \
detect HALLUCINATIONS: statements in the response that are NOT explicitly \
supported by the provided evidence text.

CRITICAL RULES -- follow these exactly:
- You must rely ONLY on the exact evidence text provided below. Do not use \
any outside knowledge, training data, or assumptions about the real world.
- If the evidence text does not explicitly state a detail, that detail is \
UNSUPPORTED -- even if you believe it might be true from general knowledge.
- Do not fill in gaps, infer missing details, or assume plausible-sounding \
facts are correct just because they sound reasonable.

Steps:
1. List every distinct factual claim made in the response.
2. For each claim, check word-for-word whether the evidence text contains \
that specific information.
3. Any claim not explicitly stated in the evidence is unsupported.

Respond ONLY with a JSON object in this exact format:
{
  "claims_checked": ["<claim 1>", "<claim 2>", ...],
  "hallucination_detected": <true or false>,
  "unsupported_claims": ["<claim text>", ...],
  "reasoning": "<brief explanation covering all claims, referencing exactly what the evidence does and does not say>"
}

If every claim is explicitly stated in the evidence, return an empty list \
for unsupported_claims and hallucination_detected: false.
"""


def evaluate(ai_response, evidence):
    """
    Args:
        ai_response (str): the AI-generated response being evaluated
        evidence (str): reference answer or retrieved RAG chunk(s)

    Returns:
        dict: {"claims_checked": list[str], "hallucination_detected": bool,
               "unsupported_claims": list[str], "reasoning": str,
               "normalized_score": float (0-1, 1=no hallucination)}
    """
    user_prompt = f"Evidence (use ONLY this, nothing else): {evidence}\n\nResponse to check: {ai_response}"

    result = call_judge(SYSTEM_PROMPT, user_prompt)

    hallucinated = bool(result.get("hallucination_detected", False))
    unsupported = result.get("unsupported_claims", [])

    return {
        "claims_checked": result.get("claims_checked", []),
        "hallucination_detected": hallucinated,
        "unsupported_claims": unsupported,
        "reasoning": result.get("reasoning", ""),
        # normalized_score: 1.0 = no hallucination (good), 0.0 = hallucination found
        # matches your existing dashboard convention where higher = better
        "normalized_score": 0.0 if hallucinated else 1.0,
    }


if __name__ == "__main__":
    # Test case from your mentor's example
    evidence = "Isaac Newton formulated the theory of gravity."
    response = "Isaac Newton discovered gravity in 1687 while visiting France."

    result = evaluate(response, evidence)
    print(f"Evidence: {evidence}")
    print(f"Response: {response}")
    print(f"Claims checked: {result['claims_checked']}")
    print(f"Hallucination detected: {result['hallucination_detected']}")
    print(f"Unsupported claims: {result['unsupported_claims']}")
    print(f"Reasoning: {result['reasoning']}")
    print(f"Normalized (0-1): {result['normalized_score']}")