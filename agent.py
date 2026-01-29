import json
from openai import OpenAI
import os
import config
import tools
import validator

# Initialize OpenAI Client
client = OpenAI(
    api_key=config.API_KEY,      # Uses the Groq key from config
    base_url=config.BASE_URL     # <--- TELLS IT TO USE GROQ SERVERS
)

class Agent:
    def __init__(self):
        self.messages = [
            {
                "role": "system", 
                "content": (
                    "You are a Sequential Execution Agent.\n"
                    "CRITICAL PROTOCOL:\n"
                    "1. SINGLE ACTION PRINCIPLE: Trigger a tool, then STOP and WAIT.\n"
                    "2. NO RETRIES ON ERROR: If a tool returns 'Error: ...', do NOT try the same tool again. Accept the failure and tell the user.\n"
                    "3. CHAIN OF THOUGHT EXECUTION:\n"
                    "   - Plan -> Execute -> Wait -> Observe.\n"
                    "4. FILE HANDLING: Pass 'filename' to the calculator. Do not read manually."
                )
            }
        ]

    def run(self, user_query):
        print(f"\n🚀 STARTING TASK: {user_query}")
        self.messages.append({"role": "user", "content": user_query})
        
        past_tool_calls = []
        
        step = 0
        while step < config.MAX_STEPS:
            step += 1
            print(f"\n🔄 Step {step}: Thinking...")

            response = client.chat.completions.create(
                model=config.MODEL_NAME,
                messages=self.messages,
                tools=tools.TOOL_DEFINITIONS,
                tool_choice="auto", # Let the model decide
                temperature=config.TEMPERATURE
            )
            
            msg = response.choices[0].message
            self.messages.append(msg)

            if msg.tool_calls:
                # --- PROCESS TOOLS ---
                for tool_call in msg.tool_calls:
                    func_name = tool_call.function.name
                    args = json.loads(tool_call.function.arguments)
                    
                    # 🛑 SOFT LANDING LOOP CHECK 🛑
                    current_call = f"{func_name}:{args}"
                    if current_call in past_tool_calls:
                        print(f"⚠️ Loop Detected on {func_name}. Stopping tool use to force Final Answer.")
                        
                        # Trick: We inject a system message telling it to stop and answer
                        self.messages.append({
                            "role": "system", 
                            "content": "You are repeating yourself. STOP using tools. Output the FINAL ANSWER based on what you already know."
                        })
                        
                        # Skip execution and force the next loop to just talk
                        break 
                    
                    past_tool_calls.append(current_call)
                    
                    print(f"🛠  Executing: {func_name} with {args}")
                    
                    try:
                        func = tools.AVAILABLE_TOOLS[func_name]
                        raw_output = func(**args)
                        clean_output = validator.validate_tool_output(func_name, raw_output)
                        
                        print(f"   -> Result: {clean_output}")
                        
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": func_name,
                            "content": clean_output
                        })
                    except Exception as e:
                        print(f"   -> Error: {e}")
                        self.messages.append({
                            "role": "tool",
                            "tool_call_id": tool_call.id,
                            "name": func_name,
                            "content": f"Error: {str(e)}"
                        })
            else:
                # No tools used? That means we have the answer!
                print(f"\n✅ FINAL ANSWER: {msg.content}")
                return

        print("❌ Failed: Max steps reached.")
if __name__ == "__main__":
    # Initialize the agent
    agent = Agent()
    
    # Run the agent with user input
    agent.run(input("enter your query: "))