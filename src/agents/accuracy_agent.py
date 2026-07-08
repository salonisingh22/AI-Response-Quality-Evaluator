import re


def preprocess_text(text):
    """
    Convert text to lowercase, remove punctuation,
    and split into unique words.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return set(text.split())


def evaluate(ai_response, reference_answer):
    """
    Accuracy Agent

    Compares the AI response with the reference answer
    using keyword overlap.

    Returns:
        float: Accuracy score between 0 and 1
    """

    if not reference_answer.strip():
        return 0.0

    ai_words = preprocess_text(ai_response)
    reference_words = preprocess_text(reference_answer)

    if len(reference_words) == 0:
        return 0.0

    matched_words = ai_words.intersection(reference_words)

    score = len(matched_words) / len(reference_words)

    score = max(0.0, min(score, 1.0))

    return round(score, 2)