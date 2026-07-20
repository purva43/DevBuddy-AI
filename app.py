from llm_client import ask

history = []
reply, history = ask("What is 847 multiplied by 392? Also, briefly, why can't LLMs normally do exact math reliably?")
print(reply)