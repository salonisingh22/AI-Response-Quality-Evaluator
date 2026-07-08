import re


def preprocess_text(text):
    """
    Converts text to lowercase, removes punctuation,
    and returns a set of unique words.
    """
    text = text.lower()
    text = re.sub(r"[^\w\s]", "", text)
    return set(text.split())


def evaluate(question, ai_response):
    """
    Relevance Agent

    Evaluates how well the AI response
    answers the user's question based on
    keyword overlap.

    Returns:
        float: Relevance score between 0 and 1
    """

    if not question.strip():
        return 0.0

    question_words = preprocess_text(question)
    response_words = preprocess_text(ai_response)

    if len(question_words) == 0:
        return 0.0

    matched_words = question_words.intersection(response_words)

    score = len(matched_words) / len(question_words)

    score = max(0.0, min(score, 1.0))

    return round(score, 2)