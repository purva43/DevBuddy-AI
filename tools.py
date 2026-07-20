import io
import contextlib
from ddgs import DDGS
from pypdf import PdfReader


def calculator(a: float, b: float, operation: str) -> float:
    """Perform a basic arithmetic operation between two numbers.

    Args:
        a: first number
        b: second number
        operation: one of 'add', 'subtract', 'multiply', 'divide'
    """
    if operation == "add":
        return a + b
    elif operation == "subtract":
        return a - b
    elif operation == "multiply":
        return a * b
    elif operation == "divide":
        return a / b if b != 0 else "Error: division by zero"
    else:
        return "Unknown operation"


def web_search(query: str) -> str:
    """Search the web for current, real-time information.

    Args:
        query: the search query
    """
    try:
        results = DDGS().text(query, max_results=3)
        if not results:
            return "No results found."

        formatted = []
        for r in results:
            formatted.append(f"Title: {r['title']}\nSnippet: {r['body']}\nURL: {r['href']}")
        return "\n\n".join(formatted)
    except Exception as e:
        return f"Search failed: {e}"
    
def read_file(filepath: str) -> str:
    """Read and return the contents of a local text file.

    Args:
        filepath: path to the file, e.g. 'notes.txt' or 'C:/Users/Purva/resume.txt'
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        # Guard against dumping a massive file straight into the model
        max_chars = 5000
        if len(content) > max_chars:
            return content[:max_chars] + "\n\n[...file truncated, too long to read fully...]"
        return content
    except FileNotFoundError:
        return f"Error: file not found at '{filepath}'"
    except Exception as e:
        return f"Error reading file: {e}"
    
def run_python_code(code: str) -> str:
    """Execute a small Python snippet for calculations or data processing,
    and return whatever it prints. Use this for anything more complex than
    basic arithmetic (loops, lists, string processing, etc).
    Does NOT have access to files, network, or imports — sandboxed for safety.

    Args:
        code: valid Python code as a string. Must use print() to show results.
    """
    # Very basic safety net: block obviously dangerous keywords.
    # (Not bulletproof — just a beginner-friendly guardrail for this project.)
    blocked = ["import", "open(", "exec(", "eval(", "__", "os.", "sys.", "subprocess"]
    if any(word in code for word in blocked):
        return "Error: this code contains a blocked operation for safety reasons."

    output_buffer = io.StringIO()
    try:
        with contextlib.redirect_stdout(output_buffer):
            exec(code, {"__builtins__": {"print": print, "range": range, "len": len,
                                          "sum": sum, "min": min, "max": max,
                                          "sorted": sorted, "abs": abs, "round": round}})
        result = output_buffer.getvalue()
        return result if result else "Code ran with no printed output."
    except Exception as e:
        return f"Error running code: {e}"
    

def read_pdf(filepath: str) -> str:
    """Extract and return text content from a local PDF file.

    Args:
        filepath: path to the PDF file, e.g. 'resume.pdf'
    """
    try:
        reader = PdfReader(filepath)
        text = ""
        for page in reader.pages:
            text += page.extract_text() + "\n"

        if not text.strip():
            return "Error: could not extract any text (this PDF might be a scanned image, not real text)."

        max_chars = 6000
        if len(text) > max_chars:
            return text[:max_chars] + "\n\n[...PDF truncated, too long to read fully...]"
        return text

    except FileNotFoundError:
        return f"Error: file not found at '{filepath}'"
    except Exception as e:
        return f"Error reading PDF: {e}"