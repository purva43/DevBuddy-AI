from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time
from tools import calculator,web_search  # import your tool

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = "You are DevBuddy, a friendly programming mentor. Use tools when they help you give an exact, correct answer."

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
                    tools=[calculator ,web_search]# <-- give the model access to th
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