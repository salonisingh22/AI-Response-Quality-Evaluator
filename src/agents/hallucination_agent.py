import re


def preprocess_text(text):
    """
    Converts text to lowercase, removes punctuation,
    and returns a set of unique words.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return set(text.split())


def evaluate(ai_response, reference_answer):
    """
    Hallucination Agent

    Detects unsupported information in the AI response
    by comparing it with the reference answer.

    A higher score indicates fewer hallucinations.

    Returns:
        float: Hallucination score between 0 and 1
    """

    ai_words = preprocess_text(ai_response)
    reference_words = preprocess_text(reference_answer)

    if len(ai_words) == 0:
        return 1.0

    unsupported_words = ai_words - reference_words

    score = 1 - (len(unsupported_words) / len(ai_words))

    score = max(0.0, min(score, 1.0))

    return round(score, 2)