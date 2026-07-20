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