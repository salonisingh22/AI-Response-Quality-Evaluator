from src.agents.relevance_judge import evaluate as relevance_judge
from src.agents.accuracy_judge import evaluate as accuracy_judge
from src.agents.hallucination_judge import evaluate as hallucination_judge
from src.agents.completeness_agent import evaluate as completeness_agent
from src.agents.verdict_agent import evaluate as verdict_agent


def evaluate_response(question, ai_response, reference_answer):

    try:

        relevance_result = relevance_judge(
            question,
            ai_response
        )

        accuracy_result = accuracy_judge(
            ai_response,
            reference_answer
        )

        hallucination_result = hallucination_judge(
            ai_response,
            reference_answer
        )

        # Completeness stays on the existing (non-LLM) logic for now --
        # this is Milestone 3 in the mentor's roadmap
        completeness = completeness_agent(
            reference_answer,
            ai_response
        )

        overall = verdict_agent(
            relevance_result["normalized_score"],
            accuracy_result["normalized_score"],
            hallucination_result["normalized_score"],
            completeness
        )

        return {
            "relevance": relevance_result["normalized_score"],
            "accuracy": accuracy_result["normalized_score"],
            "hallucination": hallucination_result["normalized_score"],
            "completeness": completeness,
            "overall": overall,

            # Structured judge output (Milestone 2 requirement) --
            # scores, reasoning, and evidence from each LLM judge
            "judge_details": {
                "relevance": relevance_result,
                "accuracy": accuracy_result,
                "hallucination": hallucination_result,
            }
        }

    except Exception as e:

        return {
            "relevance": 0,
            "accuracy": 0,
            "hallucination": 0,
            "completeness": 0,
            "overall": 0,
            "error": str(e)
        }