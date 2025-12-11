@echo off
REM Script de démarrage rapide pour Windows

echo 🚀 Démarrage de l'application RAG...
echo ==================================

cd /d "%~dp0.."

REM Vérifier si Docker est installé
docker --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker n'est pas installé. Veuillez installer Docker Desktop.
    pause
    exit /b 1
)

REM Vérifier si Docker Compose est installé
docker-compose --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Docker Compose n'est pas installé.
    pause
    exit /b 1
)

REM Vérifier si le fichier du règlement existe
if not exist "data\regulation.txt" (
    echo ⚠️  Le fichier du règlement n'existe pas.
    echo 📥 Téléchargement du règlement...
    if not exist "data" mkdir data
    python src\init_database.py
)

REM Démarrer l'application depuis le dossier docker
echo 🐳 Démarrage des conteneurs Docker...
cd docker
docker-compose up --build

echo ✅ Application démarrée!
echo 🌐 Accédez à l'application sur: http://localhost:7860
pause
