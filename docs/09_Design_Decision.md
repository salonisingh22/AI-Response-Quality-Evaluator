# AI Response Quality Evaluator

# 9. Design Decisions

## Introduction

While designing this project, I had to make different decisions about the technologies and overall system design. The main goal was to keep the project simple, modular, and easy to improve in the future.

---

# Why Python?

I selected Python because it is simple to understand and provides many libraries for Artificial Intelligence and Machine Learning. It also works well with LangChain, ChromaDB, and Streamlit.

---

# Why Streamlit?

I selected Streamlit because it allows me to build a simple and interactive user interface without writing complex frontend code. It is suitable for displaying the evaluation results clearly.

---

# Why LangChain?

LangChain helps in managing multiple AI agents and connecting different parts of the project. Since my project uses multiple evaluation agents, LangChain makes the workflow more organized.

---

# Why ChromaDB?

The project needs a vector database to store embeddings and retrieve relevant information. ChromaDB is lightweight, open source, and easy to integrate with Python, so I selected it for this project.

---

# Why RAG?

I decided to use Retrieval Augmented Generation (RAG) because it allows the system to compare AI-generated responses with trusted reference information. This helps improve factual verification and reduces incorrect evaluations.

---

# Why Multi-Agent Architecture?

Instead of using one agent for all tasks, I divided the work among different agents. Each agent focuses on one quality parameter such as relevance, accuracy, hallucination, or completeness.

This makes the evaluation process more organized and easier to improve in future versions.

---

# Conclusion

These design decisions were taken after studying different evaluation techniques and understanding the project requirements. The selected technologies and architecture make the project flexible, modular, and scalable.