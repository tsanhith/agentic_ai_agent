import os
from dotenv import load_dotenv

load_dotenv()

# --- CONNECT TO GROQ ---
# Ensure your .env file has GROQ_API_KEY=gsk_...
API_KEY = os.getenv("GROQ_API_KEY")

# CRITICAL: This tells the code to talk to Groq, not OpenAI
BASE_URL = "https://api.groq.com/openai/v1" 

# Use a Groq-supported model (Llama 3)
MODEL_NAME = "llama-3.1-8b-instant"

# Standard settings
TEMPERATURE = 0.0
MAX_STEPS = 10
DATA_DIR = "sample_data"

if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)