from llm_client import ask

tests = [
    "What is 45 times 12?",
    "What's the latest news about SpaceX?",
    "Summarize the file notes.txt",
    "What's your favorite color?"  # trick question — no tool should fire
]

for question in tests:
    print(f"\nQ: {question}")
    reply, _ = ask(question)
    print(f"A: {reply}")