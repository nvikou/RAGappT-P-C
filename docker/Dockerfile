FROM python:3.10-slim

# Définir le répertoire de travail
WORKDIR /app

# Copier les fichiers de requirements depuis la racine du projet
COPY ../requirements.txt .

# Installer les dépendances Python
RUN pip install --no-cache-dir -r requirements.txt

# Copier le code source Python
COPY ../src /app/src

# Créer les répertoires nécessaires
RUN mkdir -p data models

# Exposer le port Gradio
EXPOSE 7860

# Variables d'environnement
ENV PYTHONUNBUFFERED=1
ENV GRADIO_SERVER_NAME=0.0.0.0
ENV GRADIO_SERVER_PORT=7860
ENV PYTHONPATH=/app

# Commande de démarrage
CMD ["python", "src/app.py", "--host", "0.0.0.0", "--port", "7860"]
