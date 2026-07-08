from src.agents.relevance_agent import evaluate as relevance_agent
from src.agents.accuracy_agent import evaluate as accuracy_agent
from src.agents.hallucination_agent import evaluate as hallucination_agent
from src.agents.completeness_agent import evaluate as completeness_agent
from src.agents.verdict_agent import evaluate as verdict_agent



def evaluate_response(question, ai_response, reference_answer):

    try:

        relevance = relevance_agent(
            question,
            ai_response
        )


        accuracy = accuracy_agent(
            ai_response,
            reference_answer
        )


        hallucination = hallucination_agent(
            ai_response,
            reference_answer
        )


        completeness = completeness_agent(
            reference_answer,
            ai_response
        )


        overall = verdict_agent(
            relevance,
            accuracy,
            hallucination,
            completeness
        )


        return {

            "relevance": relevance,

            "accuracy": accuracy,

            "hallucination": hallucination,

            "completeness": completeness,

            "overall": overall

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