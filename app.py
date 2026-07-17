from llm_client import ask

history = []

reply, history = ask("My name is Purva and I'm learning to build AI agents.", history)
print(reply)

reply, history = ask("What's my name, and what am I learning?", history)
print(reply)