# 📁 NOUVELLE STRUCTURE DU PROJET

Le projet **RAG_app_TехническийPегламентТC** a été réorganisé pour une meilleure clarté et maintenabilité.

## 🎯 Organisation

### 📂 Séparation par Type de Fichier

```
RAG_app_TехническийPегламентТC/
│
├── src/          → Tout le code Python
├── docker/       → Toute la configuration Docker
├── scripts/      → Scripts de démarrage
├── docs/         → Toute la documentation
├── data/         → Données (règlement, chunks, ChromaDB)
└── models/       → Modèles ML téléchargés
```

## 🐍 Dossier `src/` - Code Python

**Contenu :**
- `app.py` - Application Gradio principale
- `rag_system.py` - Système RAG complet
- `chunking.py` - Module de parsing
- `config.py` - Configuration centralisée
- `init_database.py` - Initialisation de la base
- `check_setup.py` - Vérification environnement
- `examples.py` - 10 exemples d'utilisation
- `test_rag.py` - Tests unitaires

**Utilisation :**
```bash
# Depuis la racine du projet
python src/app.py
python src/init_database.py
python src/check_setup.py
```

## 🐳 Dossier `docker/` - Configuration Docker

**Contenu :**
- `Dockerfile` - Image Docker de l'application
- `docker-compose.yml` - Orchestration (App + Ollama)

**Utilisation :**
```bash
cd docker
docker-compose up --build
docker-compose down
docker-compose logs -f
```

## 📚 Dossier `docs/` - Documentation

**Contenu :**
- `README.md` - Documentation complète
- `QUICKSTART.md` - Guide 5 minutes
- `ARCHITECTURE.md` - Architecture détaillée
- `PROJECT_SUMMARY.md` - Récapitulatif complet
- `WORKFLOWS.md` - Diagrammes visuels
- `OVERVIEW.txt` - Vue d'ensemble ASCII
- `CHECKLIST.md` - Liste de vérification

**Consultation :**
Tous les guides sont au format Markdown, lisibles directement dans VS Code ou sur GitHub.

## 🚀 Dossier `scripts/` - Scripts Utilitaires

**Contenu :**
- `start.bat` - Démarrage Windows
- `start.sh` - Démarrage Linux/Mac

**Utilisation :**
```bash
# Windows
scripts\start.bat

# Linux/Mac
chmod +x scripts/start.sh
./scripts/start.sh
```

Ces scripts :
1. Vérifient Docker
2. Téléchargent le règlement si nécessaire
3. Lancent docker-compose
4. Affichent l'URL d'accès

## 📦 Avantages de cette Structure

### ✅ Clarté
- Séparation claire entre code, config et documentation
- Facile de trouver ce qu'on cherche

### ✅ Maintenabilité
- Modification du code sans toucher Docker
- Modification Docker sans toucher le code
- Documentation séparée du code

### ✅ Scalabilité
- Facile d'ajouter de nouveaux modules Python dans `src/`
- Facile d'ajouter des services Docker dans `docker/`
- Structure extensible

### ✅ Professionnelle
- Organisation standard de projet
- Séparation des préoccupations
- Prête pour le versioning (Git)

## 🔄 Migration depuis l'Ancienne Structure

### Ancienne Structure
```
RAG_app_TехническийPегламентТC/
├── app.py
├── rag_system.py
├── Dockerfile
├── docker-compose.yml
├── README.md
└── ...
```

### Nouvelle Structure
```
RAG_app_TехническийPегламентТC/
├── src/
│   ├── app.py
│   └── rag_system.py
├── docker/
│   ├── Dockerfile
│   └── docker-compose.yml
├── docs/
│   └── README.md
└── ...
```

## 📝 Chemins Mis à Jour

### Dans le Code Python

**config.py :**
```python
# Avant
BASE_DIR = Path(__file__).parent

# Après
BASE_DIR = Path(__file__).parent.parent  # Remonte à rag-app/
```

### Dans Docker

**Dockerfile :**
```dockerfile
# Avant
COPY . .
CMD ["python", "app.py"]

# Après
COPY ../src /app/src
CMD ["python", "src/app.py"]
```

**docker-compose.yml :**
```yaml
# Avant
context: .
dockerfile: Dockerfile

# Après
context: ..
dockerfile: docker/Dockerfile
```

### Dans les Scripts

**start.bat / start.sh :**
```bash
# Avant
docker-compose up

# Après
cd docker
docker-compose up
```

## 🎓 Bonnes Pratiques

### Import de Modules

Depuis n'importe où dans `src/` :
```python
# Importer un module du même dossier
from chunking import parse_regulation_to_chunks
from config import DATA_DIR

# Pas besoin de chemins relatifs complexes !
```

### Lancement de l'Application

**Depuis la racine :**
```bash
python src/app.py
```

**Depuis src/ :**
```bash
cd src
python app.py
```

### Docker

**Toujours depuis le dossier docker/ :**
```bash
cd docker
docker-compose up
```

## 🔍 Localisation Rapide

**"Où trouver..."**

| Quoi | Où |
|------|-----|
| Code Python | `src/` |
| Docker | `docker/` |
| Documentation | `docs/` |
| Scripts de démarrage | `scripts/` |
| Données | `data/` |
| Modèles ML | `models/` |
| Config principale | `README.md` (racine) |

## ✅ Vérification de la Structure

Exécutez depuis la racine :
```bash
python src/check_setup.py
```

Ce script vérifie :
- ✅ Structure des dossiers
- ✅ Présence des fichiers
- ✅ Configuration Python
- ✅ Docker installé
- ✅ Dépendances

---

**Structure organisée pour une meilleure productivité ! 🚀**
