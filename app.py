from llm_client import ask

history = []
reply, history = ask("What is the latest stable version of Python? Search if you're not sure.")
print(reply)