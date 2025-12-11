# 🤖 RAG_app_TехническийPегламентТC

Application de Question-Réponse intelligente basée sur RAG (Retrieval-Augmented Generation) pour interroger le règlement technique.

## 📁 Structure du Projet

```
RAG_app_TехническийPегламентТC/
│
├── 📂 src/                    # Code source Python
│   ├── app.py                 # Application Gradio principale
│   ├── rag_system.py          # Système RAG complet
│   ├── chunking.py            # Parsing du règlement
│   ├── config.py              # Configuration
│   ├── init_database.py       # Initialisation base de données
│   ├── check_setup.py         # Vérification environnement
│   ├── examples.py            # Exemples d'utilisation
│   └── test_rag.py            # Tests unitaires
│
├── 🐳 docker/                 # Configuration Docker
│   ├── Dockerfile             # Image Docker
│   └── docker-compose.yml     # Orchestration multi-conteneurs
│
├── 📚 docs/                   # Documentation
│   ├── README.md              # Documentation complète
│   ├── QUICKSTART.md          # Guide démarrage rapide
│   ├── ARCHITECTURE.md        # Architecture détaillée
│   ├── PROJECT_SUMMARY.md     # Récapitulatif
│   ├── WORKFLOWS.md           # Workflows visuels
│   ├── OVERVIEW.txt           # Vue d'ensemble
│   └── CHECKLIST.md           # Checklist de vérification
│
├── 🚀 scripts/                # Scripts utilitaires
│   ├── start.bat              # Démarrage Windows
│   └── start.sh               # Démarrage Linux/Mac
│
├── 📂 data/                   # Données (règlement, chunks, ChromaDB)
├── 📂 models/                 # Modèles téléchargés
├── requirements.txt           # Dépendances Python
└── .gitignore                # Fichiers à ignorer
```

## 🚀 Démarrage Rapide

### Avec Docker (Recommandé)

```bash
# Windows
scripts\start.bat

# Linux/Mac
./scripts/start.sh

# Ou depuis le dossier docker
cd docker
docker-compose up --build
```

### Sans Docker

```bash
# 1. Installer les dépendances
pip install -r requirements.txt

# 2. Installer et configurer Ollama
# Télécharger depuis https://ollama.ai
ollama pull llama3.2:latest

# 3. Initialiser la base de données
python src/init_database.py

# 4. Lancer l'application
python src/app.py
```

### Accès

Ouvrez votre navigateur : **http://localhost:7860**

## ✨ Fonctionnalités

- ✅ **Chunking structuré** : Parsing par articles et points
- ✅ **Recherche sémantique** : SentenceTransformers + ChromaDB
- ✅ **LLM local** : Llama 3.2 via Ollama
- ✅ **Interface Gradio** : Interface web moderne
- ✅ **Streaming** : Réponses en temps réel
- ✅ **Citations sources** : Références précises aux articles
- ✅ **Support multilingue** : Français et Russe

## 📖 Documentation

Consultez le dossier [docs/](docs/) pour la documentation complète :

- [README complet](docs/README.md) - Guide complet d'utilisation
- [Guide rapide](docs/QUICKSTART.md) - Démarrage en 5 minutes
- [Architecture](docs/ARCHITECTURE.md) - Architecture détaillée
- [Workflows](docs/WORKFLOWS.md) - Diagrammes visuels

## 🛠️ Développement

### Tests

```bash
python src/test_rag.py
```

### Vérification

```bash
python src/check_setup.py
```

### Exemples

```bash
python src/examples.py
```

## 🐳 Docker

Tous les fichiers Docker sont dans le dossier `docker/` :

```bash
cd docker
docker-compose up          # Démarrer
docker-compose down        # Arrêter
docker-compose logs -f     # Voir les logs
```

## 📝 Configuration

Configuration dans [src/config.py](src/config.py) :

- Modèles d'embeddings
- Paramètres ChromaDB
- Configuration LLM
- Chemins des données

## 🤝 Support

Pour toute question :
1. Consulter [docs/README.md](docs/README.md)
2. Exécuter `python src/check_setup.py`
3. Vérifier les logs Docker

---

**Développé avec ❤️ en utilisant les méthodes des notebooks RAG**
