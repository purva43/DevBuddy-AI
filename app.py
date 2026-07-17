from google import genai
from google.genai import types
from dotenv import load_dotenv
import os
import time

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

response_stream = client.models.generate_content_stream(
    model="gemini-flash-latest",
    config=types.GenerateContentConfig(
        system_instruction="You are DevBuddy, a friendly programming mentor."
    ),
    contents="Explain what streaming means in 3 sentences."
)

chunk_count = 0
for chunk in response_stream:
    chunk_count += 1
    print(chunk.text, end="", flush=True)
    time.sleep(0.3)

print(f"\n\n--- Received {chunk_count} separate chunks ---")