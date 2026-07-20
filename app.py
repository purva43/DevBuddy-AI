from llm_client import ask

print("DevBuddy AI — type 'quit' to exit\n")
history = []

while True:
    user_input = input("You: ")
    if user_input.lower() == "quit":
        break
    reply, history = ask(user_input, history)
    print(f"DevBuddy: {reply}\n")