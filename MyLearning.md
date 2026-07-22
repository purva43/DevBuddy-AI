day 9:web search tool
free no_API key search option -duckduckgo-search



day 10
max_guard is safeguard for AI agent
What is max_chars?

max_chars is a limit on how many characters the AI reads from a file.

Why do we use it?
Prevents context window overflow.
Reduces token usage.
Saves API cost and quota.
Makes responses faster.
Prevents crashes when reading large files.

day 11
sandbox
The problem it solves:
You want your AI to be able to run code — like doing real calculations, not just guessing at math. But "let the AI run any code it wants" is scary, because code can do anything on your computer: delete files, steal your passwords, mess with your system.
The idea of a "sandbox":
A sandbox is a safe, boxed-in space where code can run, but it can't reach anything outside that box. Like literally a kid's sandbox — they can play, dig, build inside it, but the walls stop them from wandering into traffic.
In your project specifically, your sandbox is two simple walls:
Wall 1 — a blocklist. Before running any code, you check the text for scary words first:
pythonblocked = ["import", "open(", "os.", "exec("]
if any(word in code for word in blocked):
    return "Error: blocked"
If the AI tries to write code containing these words, you refuse to run it at all.
Wall 2 — a limited toolbox. Even if code passes Wall 1, when you actually run it, you only give it a few safe tools to work with:
pythonexec(code, {"__builtins__": {"print": print, "range": range, "sum": sum, ...}})
Normally, Python code has access to everything — reading files, deleting things, talking to the internet. Here, you hand it a tiny toolbox with only print, range, sum, and a few other harmless tools. It literally cannot reach anything else, because you never gave it access.
Put together, in one sentence:
A sandboxed code execution tool lets an AI run code to do useful things (like math or logic), while physically boxing it in so it can't touch your files, your computer, or anything dangerous — even if it tried to.

Day 13
The real-world fix for scanned PDFs is called OCR (Optical Character Recognition) — software that looks at the pixel shapes and guesses what letters they represent 


Persistent memory means saving conversations to an actual file on disk (a database)



Never guess why your program is failing.
Print the values and observe what is actually happening.

(This is a debugging technique: when you can't see what's happening inside a black box, you add print statements to expose it.)
print(f"CHUNK {chunk_count}: text={chunk.text!r}")
...
print(f"TOTAL CHUNKS: {chunk_count}, FULL TEXT LENGTH: {len(full_text)}")


pip freeze > requirements.txt 
This automatically writes out every package currently installed in your environment for creating requirements.txt
