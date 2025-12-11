# 🚀 Guide de Démarrage Rapide

## Installation Express (5 minutes)

### 🐳 Avec Docker (Recommandé)

1. **Démarrer l'application**
   ```bash
   # Windows
   start.bat
   
   # Linux/Mac
   ./start.sh
   ```

2. **Accéder à l'interface**
   - Ouvrez : http://localhost:7860
   - Attendez 2-3 minutes pour le téléchargement du modèle

### 🐍 Sans Docker

1. **Installer Ollama**
   ```bash
   # Télécharger depuis https://ollama.ai
   ollama pull llama3.2:latest
   ```

2. **Installer les dépendances**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialiser la base de données**
   ```bash
   python init_database.py
   ```

4. **Lancer l'application**
   ```bash
   python app.py
   ```

## 🎯 Premiers Pas

### Test Rapide

1. Dans l'interface web, essayez :
   ```
   Что говорится в статье 5 о требованиях безопасности?
   ```

2. Vous devriez obtenir :
   - ✅ Une réponse claire et précise
   - ✅ Des citations d'articles et points
   - ✅ Les sources référencées

### Exemples de Questions

**🇷🇺 En Russe :**
- "Какие документы необходимы для подтверждения соответствия?"
- "Как осуществляется маркировка продукции?"
- "Что такое декларация о соответствии?"

**🇫🇷 En Français :**
- "Quelles sont les exigences de sécurité?"
- "Comment obtenir la certification?"
- "Quelle est la durée de validité des documents?"

## 🔧 Configuration Personnalisée

### Changer le Modèle LLM

Dans [config.py](config.py) :
```python
LLM_MODEL = "llama3.2:latest"  # Ou "llama2", "mistral", etc.
```

### Modifier le Nombre de Résultats

```python
RAG_N_RESULTS = 5  # Augmenter pour plus de contexte
```

## ❓ Problèmes Courants

### Port 7860 déjà utilisé

```bash
# Changer le port dans docker-compose.yml
ports:
  - "8080:7860"  # Utiliser le port 8080 à la place
```

### Ollama ne répond pas

```bash
# Redémarrer le conteneur
docker-compose restart ollama

# Vérifier les logs
docker-compose logs ollama
```

### Base de données vide

```bash
# Réinitialiser
python init_database.py
```

## 📚 Documentation Complète

Voir [README.md](README.md) pour plus de détails.

---

**Besoin d'aide ?** Ouvrez une issue sur GitHub.
