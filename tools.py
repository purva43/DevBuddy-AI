from ddgs import DDGS


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