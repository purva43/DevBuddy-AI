from llm_client import ask_with_loop

# Version A: no explicit planning instruction
reply_a, _ = ask_with_loop(
    "Find the current population of Japan, then calculate what 10% of that number is."
)
print("VERSION A:", reply_a)

# Version B: explicitly asked to plan first
reply_b, _ = ask_with_loop(
    "Before answering, first write out your plan as numbered steps. "
    "Then execute it: find the current population of Japan, then calculate what 10% of that number is."
)
print("\nVERSION B:", reply_b)