import os
import json
import uuid
import gradio as gr
from datetime import datetime
from dotenv import load_dotenv
from crewai import Agent, Task, Crew, Process
from langchain_community.utilities import ArxivAPIWrapper
from crewai.tools import tool 


load_dotenv()
os.environ["OPENAI_API_KEY"] = "dummy_key_to_bypass_checks"

HISTORY_FILE = "chat_history.json"

def load_all_history():
    if not os.path.exists(HISTORY_FILE):
        return {}
    with open(HISTORY_FILE, "r") as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return {}

def save_session(session_id, history_data, title):
    data = load_all_history()
    data[session_id] = {
        "title": title,
        "history": history_data,
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(HISTORY_FILE, "w") as f:
        json.dump(data, f, indent=4)

def get_history_dropdown_choices():
    data = load_all_history()
    return [f"{info['title'][:30]}... ({info['timestamp']}) | {session_id}" 
            for session_id, info in reversed(data.items())]

arxiv_wrapper = ArxivAPIWrapper(top_k_results=3, doc_content_chars_max=2000)

@tool("ArXiv Search Tool")
def arxiv_search_tool(query: str) -> str:
    """Search academic papers on ArXiv."""
    return arxiv_wrapper.run(query)

researcher = Agent(
    role='Senior Academic Researcher',
    goal='Uncover groundbreaking academic papers, extract methodologies, and meticulously record citation metadata for {topic}.',
    backstory="You are an expert academic researcher. You extract core arguments from dense scientific papers and record their exact Authors, Titles, Years, and URLs.",
    verbose=True,
    allow_delegation=False,
    tools=[arxiv_search_tool],
    llm="groq/llama-3.3-70b-versatile" 
)

writer = Agent(
    role='Academic Synthesis Writer',
    goal='Synthesize complex research findings into a structured literature review with strict IEEE in-text citations.',
    backstory="You are a skilled technical writer specializing in academic literature reviews. You strictly adhere to IEEE citation standards.",
    verbose=True,
    allow_delegation=False,
    llm="groq/llama-3.3-70b-versatile" 
)

def run_scholarflow(topic):
    research_task = Task(
        description=f"Search ArXiv for recent papers on: {topic}. Extract methodologies, findings, and full citation details: Authors, Year, Title, ArXiv ID.",
        expected_output="A detailed bulleted list of 3 papers with complete citation metadata.",
        agent=researcher
    )

    synthesis_task = Task(
        description="Write a cohesive, academic-style literature review (approx. 400 words) synthesizing these papers. \n\nCRITICAL INSTRUCTIONS:\n1. Use strict IEEE format for in-text citations.\n2. Do NOT hallucinate citations.\n3. Include a numbered 'References' section at the end.",
        expected_output="A structured literature review with Introduction, Findings, and an IEEE References section.",
        agent=writer
    )

    crew = Crew(
        agents=[researcher, writer],
        tasks=[research_task, synthesis_task],
        process=Process.sequential,
        verbose=True
    )

    return str(crew.kickoff(inputs={'topic': topic}))

with gr.Blocks() as interface:
    
    current_session_id = gr.State(str(uuid.uuid4()))
    current_history = gr.State([])

    gr.Markdown("# ScholarFlow: Research Assistant")
    
    with gr.Row():
        with gr.Column(scale=1, min_width=250):
            gr.Markdown("### Chat History")
            history_dropdown = gr.Dropdown(
                choices=get_history_dropdown_choices(),
                label="Previous Sessions",
                interactive=True
            )
            load_btn = gr.Button("Load Selected Chat")
            new_chat_btn = gr.Button("Start New Chat", variant="secondary")

        with gr.Column(scale=4):
            chatbot = gr.Chatbot(height=600)
            
            with gr.Row():
                msg = gr.Textbox(
                    show_label=False,
                    placeholder="Enter a research topic (e.g., Back-Translation Data Augmentation for NLP)",
                    container=False,
                    scale=8
                )
                submit_btn = gr.Button("Submit", scale=1)

    # --- EVENT LOGIC ---
    
    def process_message(user_message, history, session_id):
        new_history = history + [{"role": "user", "content": user_message}]
        return "", new_history, session_id

    def generate_response(history, session_id):
        user_message = history[-1]["content"]
        
        bot_reply = run_scholarflow(user_message)
        
        history.append({"role": "assistant", "content": bot_reply})
        
        title = history[0]["content"] if history else "Empty Session"
        save_session(session_id, history, title=title)
        
        updated_choices = get_history_dropdown_choices()
        return history, history, gr.update(choices=updated_choices)

    msg.submit(process_message, [msg, current_history, current_session_id], [msg, chatbot, current_session_id], queue=False).then(
        generate_response, [chatbot, current_session_id], [current_history, chatbot, history_dropdown]
    )
    submit_btn.click(process_message, [msg, current_history, current_session_id], [msg, chatbot, current_session_id], queue=False).then(
        generate_response, [chatbot, current_session_id], [current_history, chatbot, history_dropdown]
    )

    def start_new_chat():
        new_id = str(uuid.uuid4())
        return [], [], new_id

    new_chat_btn.click(start_new_chat, None, [chatbot, current_history, current_session_id], queue=False)

    def load_past_chat(dropdown_value):
        if not dropdown_value:
            return gr.update(), gr.update(), gr.update()
        
        session_id = dropdown_value.split(" | ")[-1]
        data = load_all_history()
        
        if session_id in data:
            past_history = data[session_id]["history"]
            return past_history, past_history, session_id
        return gr.update(), gr.update(), gr.update()

    load_btn.click(load_past_chat, inputs=[history_dropdown], outputs=[chatbot, current_history, current_session_id])

if __name__ == "__main__":
    custom_css = """
        button[aria-label="Settings"],
        button[title="Settings"] { display: none !important; }
    """
    interface.launch(theme=gr.themes.Soft(), css=custom_css)