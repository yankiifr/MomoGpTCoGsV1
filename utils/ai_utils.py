import random
from cryptography.fernet import Fernet
from config import AVAILABLE_MODELS

ENCRYPTION_KEY = Fernet.generate_key()
fernet = Fernet(ENCRYPTION_KEY)

def encrypt_api_key(api_key):
    return fernet.encrypt(api_key.encode()).decode()

def decrypt_api_key(encrypted_key):
    return fernet.decrypt(encrypted_key.encode()).decode()

async def generate_ai_message(prompt, use_free_model=False):
    if use_free_model:
        free_models = AVAILABLE_MODELS["Gratuit"]["Mistral"] + AVAILABLE_MODELS["Gratuit"]["Llama2"]
        model = random.choice(free_models)
    else:
        model = "gpt-3.5-turbo"  # ou un autre modèle par défaut

    try:
        # Simulons une réponse pour l'exemple
        # Dans une implémentation réelle, vous devriez appeler l'API appropriée ici
        response = f"{prompt[:100]}..."  # Simuler une réponse basée sur le prompt
        return response
    except Exception as e:
        print(f"Erreur lors de la génération du message : {e}")
        return "Désolé, je n'ai pas pu générer de message."

async def ping_model(model):
    # Implémentez ici la logique pour pinger un modèle
    return True
