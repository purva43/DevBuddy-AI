
from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

SYSTEM_PROMPT = "You are DevBuddy, a friendly programming mentor."

def ask(prompt, history=None, max_retries=3):
    """
    Send a prompt to Gemini, with optional conversation history and retry logic.
    Returns (reply_text, updated_history).
    """
    if history is None:
        history = []

    history.append(types.Content(role="user", parts=[types.Part(text=prompt)]))

    for attempt in range(1, max_retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
                contents=history
            )
            history.append(types.Content(role="model", parts=[types.Part(text=response.text)]))
            return response.text, history

        except Exception as e:
            print(f"Attempt {attempt} failed: {e}")
            if attempt == max_retries:
                return "Sorry, I couldn't reach the AI service right now.", history
            time.sleep(2 ** attempt)


def ask_streaming(prompt):
    """Stream a single response chunk by chunk (no history)."""
    return client.models.generate_content_stream(
        model="gemini-flash-latest",
        config=types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT),
        contents=prompt
    )