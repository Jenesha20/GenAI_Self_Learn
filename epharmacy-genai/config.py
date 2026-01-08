# config.py
import os
from dotenv import load_dotenv

load_dotenv()

# Database configuration
DB_CONFIG = {
    'host': os.getenv('DB_HOST', 'localhost'),
    'port': os.getenv('DB_PORT', '5432'),
    'database': os.getenv('DB_NAME', 'epharmacy'),
    'user': os.getenv('DB_USER', 'postgres'),
    'password': os.getenv('DB_PASSWORD', 'password')
}

# LLM configuration (if using Groq/OpenAI)
LLM_CONFIG = {
    'api_key': os.getenv('GROQ_API_KEY', ''),
    'model': os.getenv('LLM_MODEL', 'llama3-70b-8192'),
    'temperature': 0.7
}

# App configuration
APP_CONFIG = {
    'title': 'E-Pharmacy AI Assistant',
    'debug': os.getenv('DEBUG', 'False').lower() == 'true'
}