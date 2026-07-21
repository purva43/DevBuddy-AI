from llm_client import ask
from memory_db import init_db, save_message, load_all_messages
from google.genai import types

init_db()

# Rebuild history from the database on startup
saved_messages = load_all_messages()
history = []
for role, content in saved_messages:
    history.append(types.Content(role=role, parts=[types.Part(text=content)]))

print(f"DevBuddy AI — loaded {len(saved_messages)} past messages. Type 'quit' to exit.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break

    save_message("user", user_input)
    reply, history = ask(user_input, history)
    save_message("model", reply)

    print(f"DevBuddy: {reply}\n")