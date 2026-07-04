# AI Response Quality Evaluator

## 1. Project Overview

The AI Response Quality Evaluator is a multi-agent system designed to measure the quality and reliability of AI-generated responses. The main objective of this project is to automatically evaluate whether an AI answer is relevant to the user's query, factually correct, complete, and free from hallucinated information.

The system follows an agent-based approach where each evaluation agent focuses on a specific quality parameter. To improve the accuracy of the evaluation, the system refers to a Retrieval-Augmented Generation (RAG) knowledge base that provides trusted reference information whenever required. The outputs of all evaluation agents are collected and processed by an orchestration module, which generates a final quality report containing individual scores, an overall assessment, and useful feedback. This report is then presented to the user through a dashboard for easy analysis.

The project aims to provide a structured and scalable framework for evaluating AI responses, making it useful for applications where the reliability and quality of AI-generated content are important.


## 2. Problem Statement

Nowadays, AI is being used in many fields to answer different types of questions. Although it gives quick responses, every answer is not always correct. Sometimes the response contains incorrect facts, misses important information, or includes details that are not supported by any trusted source. Because of this, it becomes difficult for users to decide whether they should trust the AI response or not.

This project is being developed to solve this problem by checking the quality of an AI-generated response from different aspects. Instead of using a single evaluation, different agents work together to check relevance, accuracy, hallucination, and completeness. Based on the result from each agent, the system generates a final evaluation report that helps the user understand how reliable the response is.



## 3. Design Objectives

The purpose of this project is to create a system that can check the quality of AI-generated responses in a structured way. Instead of giving a single overall judgement, the system evaluates different aspects such as relevance, accuracy, completeness, and hallucination separately, making the final result more meaningful.

Another important goal is to keep the design simple and modular. Since each agent has its own responsibility, the system can be maintained easily and new features can be added in the future without affecting the existing workflow. The use of a RAG knowledge base also helps the system compare AI responses with trusted information whenever verification is required.


## 4. Tech Stack

The following technologies will be used to develop this project:

| Technology | Why it is used |
|------------|----------------|
| Python | Python is the main programming language used to build the project. |
| Streamlit | It is used to create a simple interface where users can enter the question, AI response, and reference answer. |
| LangChain | It is used to build the RAG pipeline and connect different modules of the project. |
| ChromaDB | It is used as the vector database to store embeddings and retrieve relevant information from the knowledge base. |
| Hugging Face Datasets | It is used to access public datasets like TruthfulQA and SQuAD for building the reference knowledge base. |
| Sentence Transformers | It is used to convert text into embeddings so that similar information can be searched efficiently. |
| Large Language Model (LLM) | An LLM will be used to generate and evaluate AI responses. The specific model may be finalized during the implementation phase. |
| Git & GitHub | They are used for version control and managing the project repository. |
| Visual Studio Code (VS Code) | It is used for writing the code and preparing the documentation. |
| Markdown | It is used to write and organize the design documentation. |


## 5. Literature Review 

Before starting the project, I studied some topics that are important for AI response evaluation. This helped me understand how AI responses are checked and what things should be considered while evaluating them. The concepts I studied are explained below.

### 5.1 LLM Evaluation Techniques

While studying LLM evaluation, I understood that checking whether an AI response is good is not just about seeing if the answer is correct. A good response should answer the user's question properly, the information should be correct, all the important points should be covered, and the response should not contain any unnecessary or misleading information. These are the same things that I have considered while designing this project.

### 5.2 Hallucination Detection

I also learned about hallucination in AI. Sometimes AI gives information that looks correct but is actually wrong or is not supported by any trusted source. This can confuse users because the response sounds very confident. To solve this problem, I have included a Hallucination Detection Agent in my project that checks whether the response contains any unsupported information.

### 5.3 RAG (Retrieval-Augmented Generation)

I studied RAG because it is one of the main parts of this project. I understood that instead of depending only on the AI response, RAG first retrieves relevant information from a trusted knowledge base. Then that information is used during the evaluation process. This makes the evaluation more accurate and helps in checking facts more reliably.

### 5.4 RAGAS

During my research, I also came across RAGAS. It is an evaluation framework specially designed for RAG-based applications. I learned that it checks different aspects like answer relevance and faithfulness. Studying RAGAS helped me understand how RAG systems are evaluated and how different evaluation parameters are used.

### 5.5 TruLens

I also read about TruLens, which is another framework used for evaluating LLM applications. It helps in analyzing AI responses and gives useful feedback about the quality of the response. This gave me a better understanding of how different evaluation methods can be used to improve the overall performance of an AI system.

Overall, studying all these concepts helped me understand how the project should work and how different modules and evaluation agents can be designed to make the evaluation process more reliable.


## 6. Project Modules

To make the project simple and well organized, I have divided it into different modules. Every module has its own work to do, and together all the modules complete the whole evaluation process. This also makes the project easier to understand and manage.

The main modules used in this project are:

1. Evaluation Input Module
2. Reference Knowledge Base and RAG Pipeline Module
3. Multi-Agent Judging Pipeline
4. Per-Dimension Scoring and Reasoning Display Module
5. Batch Evaluation Processing and Results Management Module
6. Evaluation Scoring Dashboard and Quality Analytics Module


## 7. Project Modules Description

### 7.1 Evaluation Input Module

This is the first module of the project. Here, the user enters the question and the AI-generated response. If the user has a reference answer or any source document, that can also be added. After the input is submitted, it is sent to the evaluation system so that the response can be checked by different agents.

### 7.2 Reference Knowledge Base and RAG Pipeline Module

This module is used to build the knowledge base of the project. Public datasets like TruthfulQA and SQuAD are used because they contain trusted information. The data is processed, divided into smaller chunks, converted into embeddings, and stored in ChromaDB. Whenever the system needs to verify any information, it retrieves the most relevant data from the knowledge base using the RAG pipeline. This helps in making the evaluation more reliable.

### 7.3 Multi-Agent Judging Pipeline

This is the main module of the project because the actual evaluation happens here. Instead of using only one agent, different agents work together. Every agent has its own responsibility. One checks relevance, another checks accuracy, another detects hallucinations, and another checks completeness. Finally, the Verdict Agent collects all the results and prepares the final evaluation.

### 7.4 Per-Dimension Scoring and Reasoning Display Module

After the evaluation is completed, this module shows separate scores for each evaluation parameter. Along with the score, it also gives a short reason so that the user can understand why that score was given. This makes the evaluation easier to understand.

### 7.5 Batch Evaluation Processing and Results Management Module

This module is useful when multiple AI responses need to be evaluated together. Instead of checking every response one by one, the system can evaluate them in batches. It also stores the evaluation results so that they can be viewed later whenever required.

### 7.6 Evaluation Scoring Dashboard and Quality Analytics Module

This is the final module of the project. It displays the complete evaluation report in a simple and easy-to-understand format. The dashboard shows the scores given by different agents, the overall score, and the final verdict so that users can easily understand the quality of the AI-generated response.



## 8. Agent Responsibilities

Since one person cannot do every job equally well, this project also divides the evaluation into different parts. Each agent is given a separate responsibility, so instead of checking everything together, every agent focuses on only one aspect of the AI response. This makes the evaluation process more systematic and also makes it easier to identify where the response is actually good or where it needs improvement.
     | Agent | Responsibility |
|--------|----------------|
| Relevance Agent | This agent checks whether the AI has actually answered the user's question. Sometimes an AI gives a long answer, but it doesn't really answer what was asked. The Relevance Agent makes sure the response stays on the topic. |
| Accuracy Agent | This agent checks whether the information given by the AI is correct. If there are facts, dates, names or other important details, it compares them with the reference available in the knowledge base to make sure the answer is reliable. || Hallucination Agent | Sometimes AI gives information that sounds correct but is actually wrong or has no proof. The Hallucination Agent checks for such information and verifies it with the reference data. If the information is not supported, it is marked as a hallucination. |
| Completeness Agent | This agent checks whether the AI has answered the question completely. Even if the answer is correct, it may miss some important points. The Completeness Agent helps find those missing parts. |
| Verdict Agent | This is the final agent in the system. It collects the results from all the other agents and prepares the final evaluation report. The report gives an overall idea of how good and reliable the AI response is. |


## 9. Scoring Dimensions

The AI-generated response is evaluated on the basis of different quality parameters. Each parameter checks a different aspect of the response so that the final evaluation is more accurate and reliable.

### Relevance

This checks whether the AI response is actually related to the user's question and answers what was asked.

### Accuracy

This checks whether the information given in the response is factually correct and reliable.

### Hallucination

This checks whether the AI has added any information that is incorrect, unsupported, or not present in the reference knowledge base.

### Completeness

This checks whether the response covers all the important points that are expected in the answer.

### Overall Verdict

The final verdict is prepared after combining the results from all the evaluation agents. It gives the overall quality of the AI-generated response.


## 10. Data Model

The evaluation process starts when the user enters the question, the AI-generated response, and an optional reference answer or source document. This information is then sent to the evaluation system. Different agents analyze the response based on their own responsibilities and generate their individual results. Finally, the Verdict Agent collects all these results and prepares the final evaluation report, which is displayed on the dashboard.

## 11. Agent Orchestration Flow

In this project, all the agents work together to evaluate the AI-generated response. The process starts when the user enters a question along with the AI response. After receiving the input, the Evaluation Orchestrator manages the complete workflow and sends the response to different evaluation agents.

Each agent has its own role in the evaluation. The Relevance Agent checks if the response answers the user's question, the Accuracy Agent verifies whether the information is correct, the Hallucination Agent checks for any unsupported or incorrect claims, and the Completeness Agent makes sure that no important point has been missed.

If the system needs to verify any information, it retrieves the required reference from the RAG knowledge base. After all the agents finish their work, their results are collected by the Verdict Agent. The Verdict Agent combines all the findings and prepares the final evaluation report, which is then displayed on the dashboard. In this way, all the agents work together to provide a complete and reliable evaluation of the AI-generated response.

   ### Agent Orchestration Flow Diagram

User
   │
   ▼
Input Module
   │
   ▼
Evaluation Orchestrator
   │
   ├── Relevance Agent
   ├── Accuracy Agent
   ├── Hallucination Agent
   ├── Completeness Agent
   │
   ▼
Verdict Agent
   │
   ▼
Dashboard


## 12. System Architecture

The system is designed in a way that every part has its own job. When the user gives a question and an AI-generated response, the evaluation process starts. If the system needs to check whether any information is correct, it first gets the required reference from the RAG knowledge base.

After that, the Evaluation Orchestrator takes over and sends the response to different evaluation agents. Instead of checking everything together, each agent checks only one thing. The Relevance Agent checks whether the response actually answers the question. The Accuracy Agent checks if the information is correct. The Hallucination Agent looks for any information that is not supported by the reference, and the Completeness Agent checks whether any important point has been left out.

When all the agents finish their work, the Verdict Agent collects their results and prepares the final evaluation report. This report is then shown on the dashboard so that the user can easily understand how good and reliable the AI response is.

I chose this modular design because it keeps the system simple and organized. It also makes it easier to improve the project later by adding more evaluation agents without changing the whole system.!


### System Architecture Diagram
![System Architecture](images/system_architecture.jpeg)


## 15. Why RAG is Used

I have used RAG in this project because sometimes AI gives information that looks correct but is actually wrong. If we only depend on the AI response, it becomes difficult to know whether the information is really correct.

With the help of RAG, the system can retrieve relevant information from a trusted knowledge base and compare it with the AI response. This helps the evaluation agents check the response more accurately and makes the final evaluation more reliable.


## 13. Future Scope

There are many ways in which this project can be improved in the future. More evaluation agents can be added to check other factors like readability, bias, and tone of the AI response.

The knowledge base can also be expanded by adding more trusted datasets so that the evaluation becomes more accurate. In the future, this project can also be connected with different AI models so that responses from multiple models can be evaluated on the same platform.


## 14. Conclusion

This project is developed to evaluate AI-generated responses in a better and more organized way. Instead of checking only one thing, different agents evaluate different aspects like relevance, accuracy, hallucination, and completeness.

Using RAG also makes the evaluation more reliable because the AI response can be compared with trusted information. Overall, this project helps users understand the quality of an AI response in a simple and structured way.


## 15. Conclusion

This project is developed to evaluate AI-generated responses in a better and more organized way. Instead of checking only one thing, different agents evaluate different aspects like relevance, accuracy, hallucination, and completeness.

Using RAG also makes the evaluation more reliable because the AI response can be compared with trusted information. Overall, this project helps users understand the quality of an AI response in a simple and structured way.


## 16. Approach Followed

Before starting the project, I first learned about AI response evaluation, hallucination detection, RAG architecture, RAGAS, and TruLens. This helped me understand how the project should work.

After that, I planned the system architecture, decided the work of each agent, and divided the project into different modules. Then I selected the technologies that will be used and prepared the design documentation.

Once everything was planned properly, I created the GitHub repository and started building the project step by step. Planning everything before starting the implementation made the project more organized and easier to develop.


## 17. References

1. LangChain Documentation
2. ChromaDB Documentation
3. Hugging Face Documentation
4. RAGAS Documentation
5. TruLens Documentation
6. Python Documentation
7. GitHub Documentation