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