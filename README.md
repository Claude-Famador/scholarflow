# 🧠 ScholarFlow: Autonomous Multi-Agent Research Assistant

## Overview
ScholarFlow is an agentic AI system designed to automate the academic literature review process. Utilizing the CrewAI framework, the system orchestrates multiple specialized AI agents to search for academic papers, extract key methodologies, and synthesize the findings into a cohesive report.

## System Architecture
The system operates using a sequential multi-agent architecture:
1. **User Input:** Received via a Gradio web interface.
2. **Senior Researcher Agent:** Equipped with the ArXiv API tool, this agent queries academic databases, reads paper abstracts, and extracts pertinent data.
3. **CrewAI Memory:** Internal context flow ensures data is retained between agent tasks.
4. **Synthesis Writer Agent:** Receives the raw extraction from the Researcher and structures it into an academic literature review.

```mermaid
graph TD;
    A[User UI] -->|Topic| B(CrewAI Orchestrator)
    B --> C[Researcher Agent]
    C <-->|Search| D[(ArXiv API)]
    C -->|Extracted Data| E[Memory/Context]
    E --> F[Synthesis Writer Agent]
    F -->|Formatted Review| A