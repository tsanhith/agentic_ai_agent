import os

def read_file_content(filename):
    """Helper to read file content safely."""
    try:
        filepath = os.path.join("sample_data", filename)
        if not os.path.exists(filepath):
            return None
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None

def calculator(operation, a=0, b=0, numbers=None, filename=None):
    """
    Smart Calculator.
    - Can do basic math (a + b).
    - Can do list math (mean, sum) from a provided list.
    - [NEW] Can do list math directly from a FILENAME.
    """
    try:
        # 1. If a filename is provided, load numbers from the file automatically
        if filename:
            content = read_file_content(filename)
            if not content:
                return f"Error: File '{filename}' not found."
            
            # Smart extraction: converts text to a list of numbers
            # Handles commas, newlines, and mixed text
            numbers = []
            for word in content.replace(',', ' ').split():
                try:
                    numbers.append(float(word))
                except ValueError:
                    continue # Skip non-numbers
        
        # 2. Handle List Operations (Mean, Sum, Max, Min)
        if numbers and isinstance(numbers, list):
            if not numbers:
                return "Error: No valid numbers found."
                
            if operation == "mean":
                return sum(numbers) / len(numbers)
            if operation == "sum":
                return sum(numbers)
            if operation == "max":
                return max(numbers)
            if operation == "min":
                return min(numbers)

        # 3. Handle Basic Math (a, b)
        a, b = float(a), float(b)
        if operation == "add": return a + b
        if operation == "subtract": return a - b
        if operation == "multiply": return a * b
        if operation == "divide": return a / b if b != 0 else "Error: Division by zero"
        
        return "Error: Invalid operation."
    except Exception as e:
        return f"Error: {str(e)}"

def write_file(content, filename):
    try:
        os.makedirs("sample_data", exist_ok=True)
        filepath = os.path.join("sample_data", filename)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        return f"Successfully wrote to {filename}."
    except Exception as e:
        return f"Error writing file: {str(e)}"

def read_file(filename):
    """Reads content from a file."""
    content = read_file_content(filename)
    if content is None:
        return "Error: File not found."
    return content

AVAILABLE_TOOLS = {
    "calculator": calculator,
    "write_file": write_file,
    "read_file": read_file
}

TOOL_DEFINITIONS = [
    {
        "type": "function",
        "function": {
            "name": "calculator",
            "description": "Perform math. Use 'filename' to calculate stats from a file automatically.",
            "parameters": {
                "type": "object",
                "properties": {
                    "operation": {"type": "string", "enum": ["add", "subtract", "multiply", "divide", "mean", "sum", "max", "min"]},
                    "a": {"type": "string"},
                    "b": {"type": "string"},
                    "numbers": {"type": "array", "items": {"type": "number"}},
                    "filename": {"type": "string", "description": "Name of the file to read numbers from (e.g., 'scores.txt')"}
                },
                "required": ["operation"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "write_file",
            "description": "Write text to a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "content": {"type": "string"},
                    "filename": {"type": "string"}
                },
                "required": ["content", "filename"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "read_file",
            "description": "Read text from a file.",
            "parameters": {
                "type": "object",
                "properties": {
                    "filename": {"type": "string"}
                },
                "required": ["filename"]
            }
        }
    }
]