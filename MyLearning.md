# My Learning: Building an AI Agent from Scratch (DevBuddy AI)

This document is my personal notes from building **DevBuddy AI**, a small AI agent project, over my first two weeks as a fresher learning how AI agents actually work — not by using a framework, but by building one piece by piece.

If you're reading this and don't know anything about AI agents yet, that's fine. I'll explain everything simply, the way I learned it.

---

## Week 1 — How LLMs Actually Work

### Day 1: An LLM has no memory, no tools, nothing extra

**The concept:** Before writing any code, I learned the most important fact about AI models: an LLM (Large Language Model) only predicts the next word in a sequence of text. That's it. It has no memory of past conversations, no internet access, no calculator, no ability to run code — unless a developer specifically adds those things.

**Why this matters:** Every "smart" thing an AI assistant seems to do (remembering your name, searching the web, doing math) is *not* something the model does natively. It's something a developer built *around* the model. Understanding this early stopped me from thinking of AI as "magic" and helped me see it as a system I could actually build and debug.

**What I built:** A simple script that sends one line of text to an AI model (Gemini) and prints the reply.

---

### Day 2: System Prompts — telling the AI *who to be*

**The concept:** There are different "roles" you can send to an AI model:
- **System prompt** — sets the AI's identity, tone, and rules (set once, applies to everything)
- **User prompt** — the actual question being asked

**Why this matters:** The exact same model, given the exact same question, will answer completely differently depending on its system prompt. I tested this by giving it a "friendly mentor" personality vs a "sarcastic pirate" personality — same brain, totally different behavior. This taught me that **prompt engineering isn't about making the AI smarter — it's about steering the same underlying model.**

---

### Day 3: Chat History — how "memory" is faked

**The concept:** Since the AI has no real memory (Day 1), how do apps like ChatGPT remember your conversation? The trick: **the entire conversation is resent to the model every single time you send a new message.** The app keeps a growing list of every message (yours and the AI's), and sends that whole list along with your newest question.

**Why this matters:** This explained something that used to confuse me — why AI chat apps sometimes "forget" things from very early in a long conversation. It's not really forgetting — it's that the message list got too long to fully resend (see Day 4).

**What I built:** A `history` list that stores every message, and gets sent in full on every new request.

---

### Day 4: Tokens and the Context Window

**The concept:** A **token** is roughly ¾ of a word — the unit AI models actually "think" in and get billed for. The **context window** is the maximum number of tokens a model can read in one request.

**Why this matters:** Since Day 3 taught me the whole conversation gets resent every time, I realized: **the longer a conversation gets, the more tokens (and money) every single new message costs** — even if your new question is just one sentence. Eventually, a long enough conversation can hit the model's hard context window limit and fail outright.

**What I saw in practice:** I printed the real token counts from Gemini's response and watched the `prompt_token_count` grow from 27 → 317 between two turns, just from resending history. Seeing the real numbers made this concept click in a way reading about it never did.

---

### Day 5: Streaming — showing text as it's generated

**The concept:** Normally, a script waits for the model's *entire* response to finish generating before showing anything. **Streaming** shows the reply chunk by chunk, as it's being generated — which is why ChatGPT-style apps feel like they're "typing."

**Why this matters:** For short answers it barely matters. But imagine asking for a 2,000-word essay — without streaming, you stare at a blank screen for 15+ seconds. With streaming, you see the first sentence almost instantly. It's a UX (user experience) improvement, not a capability upgrade.

---

### Day 6: Error Handling & Retries

**The concept:** Real APIs fail sometimes — servers get overloaded, networks hiccup. A script that crashes on the first failure is fragile. I built a retry system using **exponential backoff**: if a request fails, wait a *little* before retrying, and wait *longer* each subsequent failure (e.g. 2s → 4s → 8s) instead of retrying instantly.

**Why this matters (the real reason, not just "it's good practice"):** If a server is already overloaded and every failed client retries instantly at the same moment, it creates a **thundering herd** — everyone hammering the struggling server at once, making the overload worse. Waiting progressively longer gives the server room to recover. Every serious AI API client does this internally.

**A real lesson I learned the hard way:** Not all errors are the same. A `503` error means "server is busy, try again shortly." A `429` quota error means "you're out of your daily allowance — retrying faster won't help, you have to wait for the reset." I had to update my retry code to read Google's actual error messages and treat these two cases differently, instead of retrying the same way for both.

---

### Day 7: Refactoring into Clean Code Structure

**The concept:** Instead of keeping everything in one messy file, I split my project into:
- `llm_client.py` — all the "how do I talk to the AI" logic (retries, history, API calls)
- `app.py` — the actual program that *uses* that logic

**Why this matters:** This is called **modularization** — separating "how something works" from "what the app does with it." It means `app.py` doesn't need to know or care about retry logic, token limits, or which AI provider I'm using underneath. This pattern is how real, larger codebases stay manageable as they grow — I saw this firsthand in Week 2 when adding new tools became easy because the structure was already clean.

---

## Week 2 — Giving the AI Tools (This Is Where It Becomes an "Agent")

### The Core Idea Behind Every Tool I Built

An LLM by itself can't do exact math, can't know today's news, can't read your files. **Tool calling** is the fix: you describe a Python function to the model (its name, what it does, what arguments it needs), and the model can decide *"I should call this function"* instead of guessing an answer. Your code actually runs the function, and the real result gets fed back to the model to use in its answer.

```
User asks something
     ↓
Model decides: "I need a tool for this"
     ↓
Your code runs the real function
     ↓
Real result goes back to the model
     ↓
Model writes the final answer using that real data
```

This single pattern — describe a function, let the model decide when to use it — is the foundation of every tool I built this week.

---

### Day 8: Calculator Tool

**Why it was needed:** LLMs predict text, they don't calculate. Ask one "what's 847 × 392?" without a tool, and it's genuinely guessing based on patterns from training data — it can get big multiplications wrong. A calculator tool means the *real* Python `*` operator does the math, not the model's guesswork.

---

### Day 9: Web Search Tool

**Why it was needed:** The model's knowledge has a training cutoff date — it doesn't know about anything that happened after that, including current events, today's date, or the latest software versions. A search tool lets it look up real, current information instead of confidently guessing outdated answers.

**A mistake I actually made and learned from:** The first time I tested this, the model answered a "what's the latest news" question using old training data *without even using the search tool* — and it sounded just as confident as if it had searched. This taught me an important lesson: **giving a model access to a tool does not guarantee it uses the tool.** I had to make my system prompt more explicit ("you MUST use web_search for anything time-sensitive") before it reliably searched instead of guessed.

---

### Day 10: File Reader Tool

**Why it was needed:** This lets DevBuddy read and summarize local text files — the first step toward real use cases like "review my code" or "check my notes."

**A safety concept I learned:** I added a `max_chars` limit that truncates very long files before sending them to the model. Why? Because of Day 4's lesson — every character read from a file becomes tokens sent to the model. Without a limit, someone could ask it to read a massive file and either blow past the context window or rack up a huge, unexpected cost. This is a **guard rail** — a deliberate limitation that trades a little completeness for safety and predictability.

---

### Day 11: Multiple Tools — How the Model Chooses

**The concept:** Once I had 3+ tools registered at once, I learned that the model doesn't run all of them — it reads each tool's name and description (the docstring) and picks the single best match for the question, or decides no tool is needed at all.

**Why this matters:** This means **how you describe a tool matters a lot.** The model is essentially choosing based on a short "job description" per tool — vague or unclear descriptions lead to it picking the wrong tool, or not using one when it should.

**A real problem I found (and it's an important one):** Even with multiple tools registered, I tested asking about real-world news and found two separate failure modes:
1. The tool didn't fire at all, and the model answered confidently from stale memory instead.
2. The tool *did* fire and pulled real information, but the model's final summary still contained one inaccurate detail mixed in.

**The big lesson:** Having a tool doesn't guarantee correctness in two separate ways — you have to check *whether* the tool was actually used, **and** independently verify what it reported back. Both checks matter. This is one of the most important things I learned in the whole two weeks.

---

### Day 12: Python Code Execution Tool (and Security Thinking)

**Why it was needed:** For anything more complex than basic arithmetic (loops, lists, custom logic), I gave DevBuddy the ability to write and actually run small Python snippets.

**Why this is dangerous if done carelessly:** If an AI can run *any* code with no restrictions, a bad prompt (accidental or malicious) could delete files, read secret API keys, or worse. So I built a **sandbox** — a restricted environment where code can only do safe things.

**How my sandbox worked, in simple terms:**
1. **A blocklist** — before running any code, I scan the text for dangerous keywords (`import`, `os.`, `exec(`, etc.) and refuse to run it if found.
2. **A limited toolbox** — even code that passes the blocklist only gets access to a small set of safe built-in functions (`print`, `range`, `sum`, etc.) — not full Python.

**The honest limitation I learned:** A keyword blocklist is not a real, bulletproof security boundary. A determined person could hide dangerous code using tricks like string concatenation (building the word "import" without ever typing it directly) or encoding tricks. Real production systems don't try to *read* code and guess if it's dangerous — they make dangerous actions **physically impossible** using isolated containers with no real file/network access at all. My version is correct for learning the *concept* of sandboxing, but I now understand it's not something I'd deploy publicly as-is.

---

### Day 13: PDF Reading Tool

**Why it was needed:** A natural next step from the file reader — but PDFs need special handling because they're not plain text; they're a binary format with fonts and layout baked in.

**An important distinction I learned:** A **typed PDF** stores actual text data internally, so a library can extract the real characters. A **scanned PDF** is just a photograph of a page saved inside a PDF container — there's no text data at all, only pixels that *look like* letters. My tool correctly detects this and returns a clear error instead of failing silently or making something up. Reading actual text from a scanned document requires **OCR (Optical Character Recognition)** — a separate, more advanced technique I haven't built yet.

---

### Day 14: Bringing It All Together

By the end of Week 2, DevBuddy could:
- Remember an ongoing conversation (Week 1)
- Do exact math (Day 8)
- Search the web for current info (Day 9)
- Read local text files (Day 10)
- Run real Python code safely (Day 12)
- Read and summarize PDFs (Day 13)
- Automatically decide which of these to use for a given question (Day 11)

I also turned the project from "a script I edit and rerun for every question" into a real interactive chat loop — a genuine, usable program instead of a one-off test script.

---

## Week 3 — Memory & Knowledge (Making the Agent Actually Remember and Know Things)

### Day 15: Persistent Memory with SQLite

**The concept:** Up until this point, DevBuddy's memory (the `history` list from Day 3) only lived in the computer's RAM while the script was running. Close the terminal, and it's gone forever. **Persistent memory** means saving conversations to an actual file on disk — a database — so the AI remembers you *tomorrow*, not just within one run.

**Why SQLite specifically:** It's a real, proper database (tables, rows, structured queries — the same ideas used in big production systems), but it's just a single file on your computer. No server to install. It's already built into Python (`sqlite3` module), which made it a perfect way to learn real database concepts without extra setup pain.

**A security habit I learned here:** always insert data using placeholders (`?`) instead of directly pasting values into a SQL string. This prevents a real, serious vulnerability called **SQL injection**, where a malicious input could be crafted to run destructive commands (like deleting an entire table) if you build queries by simple text concatenation.

**Proof it actually worked:** I ran a test script twice in a row. The second run showed 4 saved messages instead of 2 — meaning the first run's data was still there on disk, waiting, even after the program had fully closed.

---

### Day 16: Wiring Real Memory into the Chat Loop

**The concept:** Day 15's database worked in isolation. Today I connected it to the actual chat loop — every real message now gets saved automatically, and every time the program starts, it loads all past messages back into `history` *before* you even type anything.

**Why this matters — the real test:** I told DevBuddy my name, quit the program completely, restarted it fresh, and asked "what's my name?" without reminding it. It answered correctly. That's the real milestone: the difference between an AI that "remembers" only during one conversation (Day 3) and one that remembers **across separate sessions entirely** — genuine persistence.

---

### Day 17: Embeddings — What "Search by Meaning" Actually Means

**The concept:** Imagine DevBuddy eventually had access to hundreds of documents. You can't stuff all of them into one prompt (Day 4's token/context-window lesson, at a much bigger scale). The fix: only pull in the *relevant* pieces first. But finding "relevant" by exact keyword matching misses a lot — so instead, AI systems use **embeddings**.

**What an embedding actually is, in simple words:** every piece of text gets converted into a long list of numbers (a "coordinate" in a huge mathematical space). Texts with **similar meaning** end up as **nearby coordinates**, even if they don't share any of the same actual words.

**Proof, with real numbers:** I compared the similarity of "I love my dog" vs "My puppy is great" (scored **0.70**) against "I love my dog" vs "The stock market crashed" (scored **0.48**). The dog/puppy pair scored meaningfully closer, even though they share zero identical words. That's "search by meaning" as a real, measurable thing — not just a buzzword.

---

### Day 18: Vector Storage with ChromaDB

**The concept:** Manually comparing embeddings by hand (like I did on Day 17) doesn't scale to thousands of documents. **ChromaDB** is a **vector database** — a specialized storage system built specifically to hold embeddings and instantly find the closest "meaning" matches out of a large collection, without me writing any comparison math myself.

**What I noticed:** I never had to call an embedding function or write similarity math directly — ChromaDB handled converting text into embeddings and finding the closest matches internally. I tested it by storing 4 unrelated sentences and searching "Tell me about my pet" — it correctly returned only the dog/puppy sentences, ignoring the stock market and interest rate ones, even though the query shared no exact words with either match.

---

### Day 19: Building RAG (Retrieval-Augmented Generation)

**The concept, explained simply:** RAG means the AI works like a student taking an **open-book exam**, instead of answering purely from memory.
- **Without RAG:** the AI can only answer using what it learned during training — it has no idea about facts specific to my project.
- **With RAG:** before answering, the AI first searches my own stored notes for the relevant piece, then answers using that real information.

**The 4-step flow:**
1. Search stored documents by meaning (using Day 17-18's embeddings/ChromaDB)
2. Pull out only the most relevant pieces
3. Secretly add those pieces into the prompt, before my actual question
4. The AI answers using that real, specific information — not a guess

**A real mistake I hit (and this was the most important lesson of the whole week):** the first time I tested this, DevBuddy answered a project-specific question completely wrong — it described "Gemini" in generic terms instead of correctly naming my actual model choice. The **tool simply didn't fire** — same failure pattern as Day 11's web search issue. The fix was the same too: make the system prompt explicitly say *when* the AI must use this tool, instead of leaving it to guess between "answer from general knowledge" or "check my notes." After that fix, it correctly retrieved my real notes and answered accurately.

---

### Day 20: Combining Memory + RAG + Tools Together

**The concept:** This wasn't new code — it was a stress test. By now DevBuddy had persistent memory, 6 tools, and a system prompt steering tool choice, all running at once. I ran one continuous conversation covering all of it: a memory fact, a math question, a project-specific question (testing RAG), a current-events question (testing web search), then a full restart to check memory survived.

**A subtle but important failure I found:** when I asked a project question with typos in it, DevBuddy again failed to trigger the knowledge base tool and gave a confidently wrong answer (a made-up model name that isn't even real). When I asked the exact same question with clean spelling, it worked correctly.

**The real lesson here — worth remembering more than almost anything else this week:** a typo shouldn't be able to make an AI silently give a wrong, confident-sounding answer. The dangerous failure mode in agent design isn't "the AI clearly doesn't know" — it's "the AI answers wrong, but it *sounds* just as confident as when it's right." You can't tell the difference just by reading the response; you have to actually know the correct answer yourself, or test deliberately, to catch it.

---

### Day 21: Week 3 Review + Cleanup

**The concept:** Same idea as Day 14 — pause and tidy up instead of endlessly stacking new features. I reviewed my growing system prompt (which had accumulated several specific tool-usage rules over the week) and made sure generated files — my SQLite database and ChromaDB folder — were properly excluded from git using `.gitignore`, since those are generated data, not source code, and shouldn't be committed (especially since they could contain real conversation history).

---

## Week 4 — Real Agent Behavior (Making It Production-Aware)

### Day 22: The Agent Loop — Made Visible

**The concept:** Everything before this point was "ask one question, get one answer" — even with tools, it felt like a single request-response cycle. Today's idea: a true **agent** works in a repeating loop — **Think → Act → Observe → Think again (if needed) → ...** — using the result of one step to decide the next, instead of stopping after one action.

**What I actually learned, beyond the diagram:** this loop had been running invisibly the whole time, because I was using "automatic function calling" — the SDK quietly handles the full think-act-observe cycle internally and only hands back the final answer. Making it explicit (printing each step) revealed this: my loop only ever showed "Step 1," even for questions needing multiple tool calls, because the SDK bundles multiple internal rounds into what looks like one call from the outside.

**A real bug I found here:** I asked a combined question (math + a "latest version" question). It got the math right instantly but answered the version question with an *outdated* number, because it skipped calling web search for that half and just guessed from training memory instead. The fix was making the system prompt explicitly say: *"even in multi-part questions, use the correct tool for every part — never skip one."* This was actually the third time I'd hit this same root bug in a different disguise (first with news, then with a project fact, now with a version number), and each time the fix was the same category of thing: **vague instructions get followed inconsistently; explicit, repeated instructions get followed reliably.**

---

### Day 23: Real Multi-Step Reasoning

**The concept:** A genuine test of chained reasoning — asking the agent to search for something, then use *that specific result* to do a calculation, where step 2 genuinely depends on step 1's real output (not two independent tasks bundled together).

**What worked well:** I asked it to find who won the most recent Nobel Prize in Physics and calculate how many years ago that was. It correctly searched, got the real names and year, and calculated the right answer. I independently verified the facts were accurate.

**The insight worth remembering:** this worked more reliably than Day 22's combined question, and the likely reason is structural — one flowing, dependent task ("search, then use that to calculate") seems to guide the model into the right tool sequence more naturally than two separate questions stapled together in one prompt. How you *phrase* a multi-part request seems to genuinely affect how reliably tools get used.

---

### Day 24: Planning — Does "Think First" Actually Help?

**The concept:** A common technique for hard tasks is asking the AI to write out a numbered plan *before* executing it, on the theory that this improves reliability.

**A genuinely surprising result:** I compared two versions of the same question — one plain, one asked to "plan first." The plain version actually gave the *more accurate* answer; the "plan first" version cited an older, less current data source despite dutifully following its own stated plan.

**The real, nuanced lesson:** planning makes the AI's reasoning more *visible* and easier to debug — but visible reasoning is not the same as *correct* reasoning. Telling an AI to plan doesn't automatically make it pull more current or accurate data; you still have to independently verify the actual facts it retrieves, regardless of how organized its explanation looks. Confident, well-structured reasoning can still be built on a wrong or outdated fact.

---

### Day 25: Async Programming Basics

**The concept:** Everything I'd built so far runs **synchronously** — one operation fully finishes before the next one starts. **Async** programming lets independent slow operations (like network calls) run *at the same time* instead of waiting for each one in turn.

**The analogy that made it click:** ordering at 3 restaurant counters. Synchronous = go to counter 1, wait, get food, *then* go to counter 2, wait, get food, *then* counter 3 — total time is the sum of all three waits. Async = place orders at all 3 counters first, then collect each one as it's ready — total time is roughly just the *longest single wait*, not the sum.

**Proof, with real numbers:** I ran 3 fake "slow tasks" (2 seconds each) synchronously and asynchronously. Sync took 6.0 seconds (2+2+2, added up). Async took 2.0 seconds (all three running at once). That gap is the entire value of async — and it matters more the more independent slow operations you have (e.g., 10 tasks would be 20s sync vs. still roughly 2s async).

---

### Day 26: A Real Web UI (Streamlit)

**The concept:** Moving DevBuddy from a terminal-only tool to an actual browser-based chat interface, using Streamlit — a Python library that turns a script into a web app without needing to write HTML/CSS/JS.

**The real test I ran:** I asked a genuinely current-events question with real stakes (about a real public figure), got an answer, then refreshed the browser page entirely. My past messages were still there — proof the UI was correctly reading from my persistent SQLite database, not just Streamlit's temporary in-browser memory.

**A good habit I practiced here:** the AI's answer involved a serious, specific claim (someone's death, with a date). Rather than just accepting a confident-sounding answer, I verified it against real sources before trusting it — which turned out to be accurate, but the habit of checking mattered more than the specific result.

---

### Day 27: Streaming in the UI

**The concept:** Bringing back Day 5's word-by-word streaming effect, but rendered inside the browser instead of a terminal, using Streamlit's `st.write_stream()`.

**A debugging lesson worth remembering:** I initially thought streaming was broken because a screenshot showed a blank response bubble. Adding temporary debug `print()` statements inside the streaming loop revealed the real content was generating correctly the whole time (14 real chunks, full message) — the screenshot had just been taken one frame too early, before the browser finished rendering. This taught me a genuinely useful debugging technique: when something looks broken, add visibility (print statements, logs) into the actual data flow before assuming the logic is wrong — the bug might be somewhere else entirely, like the display layer.

---

### Day 28: Logging & Config Cleanup

**The concept:** Two small but important production habits:
1. **Logging** — replacing scattered `print()` statements (which disappear when a terminal closes) with `logging.warning(...)`, which writes permanently to a file (`devbuddy.log`) I can review later.
2. **Centralized config** — moving hardcoded values like the model name into one `config.py` file, so a future change (like Google deprecating a model, which genuinely happened to me during this project) means editing one line instead of hunting through multiple files.

**An unexpected discovery from the log file:** looking at real log entries revealed that my web search tool was quietly querying 7+ different search engines behind the scenes for a single search (not just one, as I'd assumed), and that one of them (Startpage) was actually returning a CAPTCHA-blocked page instead of real results. This was a genuinely useful, real-world lesson about the hidden fragility of scraping-based search tools — something I never would have known without actually reading the logs.

---

### Day 29: README & Architecture Documentation

**The concept:** A different kind of writing than my own learning notes — a README is written *for someone else* (a recruiter, another developer) who needs to understand what the project is and how to run it, quickly. Good structure: what it is, what it does, how the pieces fit together (architecture), how to run it, and an honest note on limitations.

**Why I included an honest "limitations" section:** rather than only listing what works, I specifically wrote out the real weak points I'd found (the code sandbox isn't production-grade security, the search tool can get CAPTCHA-blocked, tool-triggering is sensitive to phrasing). This is a deliberate choice — showing you understand a system's edges, not just its happy path, is a stronger signal of real understanding than only listing features.

---

### Day 30: Final Review — Explaining It Out Loud

**The concept:** No new code — practicing explaining the whole project clearly, the way I'd need to in a real interview. This is a genuinely different skill from building something; being able to talk through *what* I built, *why*, and *how*, under real questioning, matters just as much as the code itself.

**Questions I practiced answering:**
- "Tell me about a project" — a short, structured summary (what, why, how it evolved, proof it works)
- "What was the hardest part?" — a specific, honest story (multi-part questions causing silent tool-skipping), not a vague answer
- "Explain the technical mechanism" — walking through exactly what happens when a tool gets called, step by step
- "Explain RAG simply" — using the open-book-exam analogy before any jargon
- "What would you improve?" — naming real, tested limitations (sandbox security, search reliability, tool-triggering) with concrete next steps, not generic answers

**The biggest realization from this final day:** the most impressive things I learned this month weren't really about any single tool or piece of code — they were about **verifying AI output instead of trusting it by default**, and about **being honest about a system's real limitations** instead of only presenting its best side. Those two habits are worth more than any specific technical skill from this bootcamp.

---

## Debugging Lessons That Weren't Tied to a Single Day

Some of the most valuable things I learned came from things going wrong, not from following instructions perfectly. I think these are worth writing down separately because they're the kind of thing you only really learn by hitting them yourself.

**Free-tier APIs are unstable and change often.** Over just a few days, I hit model deprecation errors (a model I used got blocked for new accounts), quota exhaustion errors (used up my daily free requests), and confusing 429 errors that actually meant two different things depending on the exact numbers inside them. The fix wasn't to keep guessing model names from blog posts — it was to query the API directly (`client.models.list()`) to see exactly what my own account could access, and to check the official pricing page instead of trusting outdated articles.

**Read errors from the bottom up.** Python tracebacks look scary and long, but the actual cause is almost always the last line. Learning to skip straight to `SomeError: actual message here` instead of panicking at the whole wall of text saved me a lot of time.

**"It looks right" isn't the same as "it is right."** More than once, an AI response *sounded* completely confident and well-formatted while actually being wrong or outdated underneath. This taught me to treat confident-sounding AI output as something to verify, not something to trust automatically — especially for anything time-sensitive or high-stakes.

---

## The One-Sentence Summary

An AI agent isn't one clever trick — it's a plain language model with **no memory and no abilities of its own**, wrapped in code that gives it memory (chat history, persistent across sessions via SQLite), knowledge (tools like search, file reading, and a real RAG pipeline for answering from its own notes), and judgment (deciding which tool to use, in what order, and safety limits on what it's allowed to do). Every "smart" behavior is something a developer deliberately built, not something the model does on its own — and even with all of that built, the AI can still fail silently and confidently, which is why testing, verifying, and being honest about a system's real limitations matters as much as building the features themselves.

This project took 30 days, went from a single line of code that just talked to an LLM, to a full agent with persistent memory, six tools, retrieval-augmented generation, a web interface, and real production habits like logging and centralized config. But the most valuable thing I built wasn't any single feature — it was the habit of not trusting confident-sounding AI output by default, and the ability to explain clearly, honestly, and in plain language exactly how and why each piece works.
