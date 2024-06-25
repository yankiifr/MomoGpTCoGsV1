import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
PERPLEXITY_API_KEY = os.getenv('PERPLEXITY_API_KEY')
CODESTRAL_API_KEY = os.getenv('CODESTRAL_API_KEY')

QUOTA_CHECK_INTERVAL = int(os.getenv('QUOTA_CHECK_INTERVAL', 300))
INACTIVITY_THRESHOLD = int(os.getenv('INACTIVITY_THRESHOLD', 60))

AVAILABLE_MODELS = {
    "Gratuit": {
        "Mistral": ["mistral-7b-instruct-v0.1", "mistral-7b-instruct-v0.2"],
        "Llama2": ["llama-2-7b-chat", "llama-2-13b-chat", "llama-2-70b-chat"]
    },
    "Payant": {
        "OpenAI": ["gpt-3.5-turbo", "gpt-4"],
        "Perplexity": ["pplx-7b-online", "pplx-70b-online"],
        "Mistral": ["mistral-small-latest", "mistral-medium-latest", "mistral-large-latest"],
        "Codestral": ["codestral-latest"]
    }
}

DEBUG = os.getenv('DEBUG', 'False').lower() in ('true', '1', 't')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

USER_API_KEYS = {}
