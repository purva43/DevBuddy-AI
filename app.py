from llm_client import ask

history = []
reply, history = ask("Read the file notes.txt and summarize what's in it.")
print(reply)