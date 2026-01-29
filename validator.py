def validate_tool_output(tool_name, output):
    """Ensures tool output is safe for the LLM to read."""
    
    # 1. Calculator Check
    if tool_name == "calculator":
        try:
            return str(float(output))
        except:
            return f"Error: Calculator returned invalid format: {output}"

    # 2. File Read Check
    elif tool_name == "read_file":
        if not output or len(str(output)) == 0:
            return "File was empty."
        return str(output)

    # 3. Write Check
    elif tool_name == "write_file":
        if "Successfully wrote" not in str(output):
            return "Error: File write failed."
        return str(output)

    # 4. Search Check
    elif tool_name == "web_search":
        if "No results" in str(output):
            return "Search found nothing. Try a different query."
        return str(output)

    return str(output)