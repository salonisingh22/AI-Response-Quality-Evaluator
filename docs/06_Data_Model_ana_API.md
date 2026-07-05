# AI Response Quality Evaluator

# 6. Data Model and API

## Introduction

The project requires structured data so that every evaluation can be processed correctly. The data model defines how information moves inside the system.

---

# 1. User Input

The user provides the following information:

• Question

• AI-generated Response

• Optional Reference Answer

• Optional Source Document

---

# 2. Evaluation Record

Each evaluation stores the following information:

Question

AI Response

Reference Answer

Relevance Score

Accuracy Score

Hallucination Score

Completeness Score

Final Verdict

Timestamp

---

# 3. Knowledge Base

The knowledge base contains trusted reference documents collected from public datasets. These documents are converted into embeddings and stored inside ChromaDB.

---

# 4. API Flow

The Evaluation Input Module sends the user input to the Evaluation Orchestrator.

The orchestrator retrieves reference information from the RAG pipeline.

The response is then sent to all evaluation agents.

Each agent generates its own score.

The Verdict Agent combines all scores.

The dashboard displays the final evaluation report.

---

# 5. Data Storage

The project stores embeddings inside ChromaDB.

Evaluation reports can be stored for future analysis and comparison.

---

# Conclusion

A structured data model helps different project modules communicate properly. It also makes the system more organized and easier to improve in future versions.