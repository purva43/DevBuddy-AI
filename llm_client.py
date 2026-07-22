from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
from tools import calculator,web_search,read_file,run_python_code,read_pdf,search_knowledge_base  # import your tool
 
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = (
    "You are DevBuddy, a friendly programming mentor and assistant for THIS specific project. "
    "For any question about this project itself (its tools, its model choice, its purpose, "
    "who built it, etc.), you MUST use the search_knowledge_base tool first. "
    "For ANY question involving current events, dates, versions, or anything that could have "
    "changed after your training — even if it's part of a multi-part question — you MUST use "
    "web_search for that part, answering each part with the right tool. Never answer time-sensitive "
    "questions from memory, even if you think you know the answer. "
    "Use calculator for math, read_file/read_pdf for local files."
)
def ask_with_loop(prompt, history=None, max_steps=5):
    """
    Runs the agent loop explicitly, printing each step so you can SEE
    the think -> act -> observe cycle happening.
    """
    if history is None:
        history = []

    history.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    for step in range(1, max_steps + 1):
        print(f"\n--- Step {step} ---")

        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            config=types.GenerateContentConfig(
                system_instruction=SYSTEM_PROMPT,
                tools=[calculator, web_search, read_file, run_python_code, read_pdf, search_knowledge_base]
            ),
            contents=history
        )

        # Check if the model wants to call a tool (this is the SDK handling "ACT")
        function_calls = getattr(response, "function_calls", None)

        if function_calls:
            print(f"THINK: Model wants to call a tool: {[fc.name for fc in function_calls]}")
        else:
            print("THINK: Model has enough info, giving final answer.")
            history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
            return response.text, history

        # If we get here, a tool was called automatically by the SDK already
        # (this happens internally) — this branch mostly won't trigger with
        # automatic function calling, but printing it teaches the concept.

    return "Reached max steps without a final answer.", history

def ask(prompt, history=None, max_retries=3):
    if history is None:
        history = []

    history.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT,
                    tools=[calculator ,web_search,read_file,run_python_code, read_pdf, search_knowledge_base]# <-- give the model access to the knowledge base search tool
                ),
                contents=history
            )
            history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
            return response.text, history

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                return "Sorry, I couldn't reach the AI service right now.", history
            time.sleep(2 ** attempt)