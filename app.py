from llm_client import ask

history = []
reply, history = ask(
    "Read the file read.pdf and give me a 3-sentence summary.")
print(reply)