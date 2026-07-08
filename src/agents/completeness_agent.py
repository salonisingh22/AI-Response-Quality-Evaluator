import re


def preprocess_text(text):
    """
    Converts text to lowercase, removes punctuation,
    and returns a set of unique words.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return set(text.split())


def evaluate(reference_answer, ai_response):
    """
    Completeness Agent

    Checks whether the important information
    from the reference answer is covered
    in the AI-generated response.

    Returns:
        float: Completeness score between 0 and 1
    """

    if not reference_answer.strip():
        return 0.0

    reference_words = preprocess_text(reference_answer)
    ai_words = preprocess_text(ai_response)

    if len(reference_words) == 0:
        return 0.0

    matched_words = reference_words.intersection(ai_words)

    score = len(matched_words) / len(reference_words)

    score = max(0.0, min(score, 1.0))

    return round(score, 2)