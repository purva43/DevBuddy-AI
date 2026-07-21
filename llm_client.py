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
    "who built it, etc.), you MUST use the search_knowledge_base tool first — "
    "do not answer from general knowledge, since this project's specific details "
    "are not something you'd know natively. "
    "Use calculator for math, web_search for current events, read_file/read_pdf for local files."
)
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