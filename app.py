from llm_client import ask

history = []
reply, history = ask(
    "Run this code: import os; print(os.getcwd())"
)
print(reply)