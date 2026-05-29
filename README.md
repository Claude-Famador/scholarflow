# 🧠 ScholarFlow: Autonomous Multi-Agent Research Assistant on ArXiv Studies

## Overview
ScholarFlow is an agentic AI system designed to automate the academic literature review process. Utilizing the CrewAI framework, the system orchestrates multiple specialized AI agents to search for academic papers, extract key methodologies, and synthesize the findings into a cohesive report.

## System Architecture
The system operates using a sequential multi-agent architecture:
1. **User Input:** Received via a Gradio web interface.
2. **Senior Researcher Agent:** Equipped with the ArXiv API tool, this agent queries academic databases, reads paper abstracts, and extracts pertinent data.
3. **CrewAI Memory:** Internal context flow ensures data is retained between agent tasks.
4. **Synthesis Writer Agent:** Receives the raw extraction from the Researcher and structures it into an academic literature review.

<<<<<<< HEAD
## Tech Stack & Libraries
* **Framework:** [CrewAI](https://www.crewai.com/) for multi-agent orchestration.
* **LLM:** Llama-3.3-70b-versatile (via Groq API).
* **Tools:** LangChain Community ArXiv API Wrapper.
* **UI:** Gradio for the interactive web chatbot.

## Setup Instructions
1. Clone the repository:
   ```bash
   git clone [https://github.com/yourusername/scholarflow.git](https://github.com/yourusername/scholarflow.git)
   cd scholarflow

2. pip install -r requirements.txt

3. In the root folder of the project, create a new file named exactly .env (do not add a .txt extension).

   Open the file and add your API key like this:


   GROQ_API_KEY=your_actual_api_key_here

4. Run main.py
=======
```mermaid
graph TD;
    A[User UI] -->|Topic| B(CrewAI Orchestrator)
    B --> C[Researcher Agent]
    C <-->|Search| D[(ArXiv API)]
    C -->|Extracted Data| E[Memory/Context]
    E --> F[Synthesis Writer Agent]
    F -->|Formatted Review| A
>>>>>>> 3dbace4f09deb6cb4d4b468293c41de845995bba
