"""
Configuration centralisée pour l'application RAG.
"""

import os
from pathlib import Path

# Chemins - Ajusté pour la nouvelle structure
BASE_DIR = Path(__file__).parent.parent  # Remonte au dossier rag-app
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
CHROMA_DB_PATH = DATA_DIR / "chroma_db"

# Fichiers
REGULATION_FILE = DATA_DIR / "regulation.txt"
CHUNKS_FILE = DATA_DIR / "chunks.txt"

# Google Drive
REGULATION_GOOGLE_DRIVE_ID = "1DhT50DonrOVzt5bX_JgCScvM03L9GOIK"

# Modèles
EMBEDDING_MODEL = "multi-qa-mpnet-base-dot-v1"
LLM_MODEL = "llama3.2:latest"

# Ollama
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://localhost:11434")

# Gradio
GRADIO_SERVER_NAME = os.getenv("GRADIO_SERVER_NAME", "0.0.0.0")
GRADIO_SERVER_PORT = int(os.getenv("GRADIO_SERVER_PORT", "7860"))
GRADIO_SHARE = os.getenv("GRADIO_SHARE", "false").lower() == "true"

# RAG
RAG_N_RESULTS = 5  # Nombre de chunks à récupérer
RAG_CONTEXT_MAX_LENGTH = 4000  # Longueur maximale du contexte

# Créer les répertoires si nécessaire
DATA_DIR.mkdir(exist_ok=True)
MODELS_DIR.mkdir(exist_ok=True)
