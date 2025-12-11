#!/bin/bash

# Script de démarrage rapide pour l'application RAG

# Se déplacer à la racine du projet
cd "$(dirname "$0")/.."

echo "🚀 Démarrage de l'application RAG..."
echo "=================================="

# Vérifier si Docker est installé
if ! command -v docker &> /dev/null; then
    echo "❌ Docker n'est pas installé. Veuillez installer Docker Desktop."
    exit 1
fi

# Vérifier si Docker Compose est installé
if ! command -v docker-compose &> /dev/null; then
    echo "❌ Docker Compose n'est pas installé."
    exit 1
fi

# Vérifier si le fichier du règlement existe
if [ ! -f "data/regulation.txt" ]; then
    echo "⚠️  Le fichier du règlement n'existe pas."
    echo "📥 Téléchargement du règlement..."
    mkdir -p data
    python src/init_database.py
fi

# Démarrer l'application depuis le dossier docker
echo "🐳 Démarrage des conteneurs Docker..."
cd docker
docker-compose up --build

echo "✅ Application démarrée!"
echo "🌐 Accédez à l'application sur: http://localhost:7860"
