def evaluate(relevance, accuracy, hallucination, completeness):
    """
    Verdict Agent

    Computes the final quality score by combining
    the outputs of all evaluation agents.

    Evaluation Parameters:
        - Relevance
        - Accuracy
        - Hallucination
        - Completeness

    Returns:
        float: Overall quality score between 0 and 1
    """

    scores = [
        relevance,
        accuracy,
        hallucination,
        completeness
    ]

    # Ensure all scores remain within the valid range
    scores = [max(0.0, min(score, 1.0)) for score in scores]

    overall_score = sum(scores) / len(scores)

    return round(overall_score, 2)