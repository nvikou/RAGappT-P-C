# 📐 Architecture de l'Application RAG

## Vue d'Ensemble

L'application RAG (Retrieval-Augmented Generation) combine plusieurs technologies pour créer un système de question-réponse intelligent sur le règlement technique.

```
┌─────────────────────────────────────────────────────────────┐
│                    Interface Utilisateur                     │
│                      (Gradio Web UI)                        │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                   Application RAG (app.py)                   │
│  - Gestion des requêtes utilisateur                         │
│  - Streaming des réponses                                    │
│  - Formatage des résultats                                   │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                 Système RAG (rag_system.py)                  │
│  ┌─────────────────────────────────────────────────────┐   │
│  │  1. Génération Embeddings (SentenceTransformers)    │   │
│  │     • multi-qa-mpnet-base-dot-v1                    │   │
│  │     • 768 dimensions                                 │   │
│  └─────────────────────────────────────────────────────┘   │
│                            │                                 │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │  2. Base Vectorielle (ChromaDB)                      │ │
│  │     • Stockage persistant                            │ │
│  │     • Recherche par similarité cosinus               │ │
│  │     • Métadonnées structurées                        │ │
│  └─────────────────────────────────────────────────────┘ │
│                            │                                 │
│  ┌─────────────────────────▼─────────────────────────────┐ │
│  │  3. Génération Réponses (Ollama + LangChain)        │ │
│  │     • Llama 3.2                                      │ │
│  │     • Température: 0.1                               │ │
│  │     • Streaming support                              │ │
│  └─────────────────────────────────────────────────────┘ │
└───────────────────────────┬─────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│              Module Chunking (chunking.py)                   │
│  - Parsing du règlement par articles/points                 │
│  - Métadonnées: article_num, title, point_num               │
│  - Format structuré avec IDs uniques                        │
└─────────────────────────────────────────────────────────────┘
```

## 🔄 Workflow de Traitement d'une Question

```
1. Question Utilisateur
   │
   ▼
2. Génération Embedding Question
   │  (SentenceTransformers)
   ▼
3. Recherche Vectorielle
   │  (ChromaDB - Similarité Cosinus)
   ▼
4. Récupération Top-K Chunks
   │  (Par défaut: 5 chunks)
   ▼
5. Construction du Contexte
   │  (Concaténation des chunks)
   ▼
6. Génération Réponse
   │  (LLM avec prompt template)
   ▼
7. Formatage + Sources
   │  (Réponse + Citations)
   ▼
8. Affichage Streaming
   │  (Gradio Interface)
   ▼
9. Résultat Final
```

## 📦 Composants Principaux

### 1. chunking.py
**Responsabilités :**
- Téléchargement du règlement depuis Google Drive
- Parsing structuré par articles et points
- Extraction de métadonnées
- Sauvegarde/chargement des chunks

**Méthode de Chunking :**
```python
Règlement
  ├── Статья X. Titre
  │   ├── Point 1 → Chunk X.1
  │   ├── Point 2 → Chunk X.2
  │   └── Point N → Chunk X.N
  └── ...
```

**Exemple de Chunk :**
```python
{
    'id': '5.3',
    'article_num': '5',
    'article_title': 'Требования безопасности',
    'point_num': '3',
    'text': 'Документация должна быть...'
}
```

### 2. rag_system.py
**Responsabilités :**
- Initialisation des modèles (embeddings + LLM)
- Gestion de ChromaDB
- Indexation des chunks
- Recherche sémantique
- Génération de réponses

**Classes principales :**
```python
class RAGSystem:
    - __init__(): Initialisation
    - load_regulation(): Chargement du règlement
    - index_chunks(): Indexation ChromaDB
    - retrieve_context(): Recherche vectorielle
    - get_llm_answer(): Génération réponse
    - query(): Requête complète
    - query_streaming(): Streaming
```

### 3. app.py
**Responsabilités :**
- Interface Gradio
- Gestion des sessions utilisateur
- Streaming des réponses
- Configuration serveur

**Classes principales :**
```python
class RAGGradioApp:
    - __init__(): Initialisation RAG
    - rag_interface(): Interface de requête
    - create_interface(): Construction UI
    - launch(): Démarrage serveur
```

### 4. init_database.py
**Responsabilités :**
- Téléchargement initial du règlement
- Parsing et sauvegarde des chunks
- Indexation complète dans ChromaDB

### 5. config.py
**Responsabilités :**
- Configuration centralisée
- Variables d'environnement
- Paramètres par défaut

## 🐳 Architecture Docker

```
┌─────────────────────────────────────────────────────────────┐
│                     docker-compose.yml                       │
└─────────────────────────────────────────────────────────────┘
                            │
            ┌───────────────┴───────────────┐
            ▼                               ▼
┌─────────────────────┐         ┌─────────────────────┐
│  Container: ollama  │         │ Container: rag-app  │
│                     │         │                     │
│  • Ollama server    │◄────────┤  • Python app       │
│  • Port: 11434      │         │  • Gradio UI        │
│  • Llama 3.2        │         │  • Port: 7860       │
│  • GPU support      │         │                     │
└─────────┬───────────┘         └──────────┬──────────┘
          │                                │
          ▼                                ▼
┌─────────────────────┐         ┌─────────────────────┐
│ Volume: ollama_data │         │   Volume: ./data    │
│  • Modèles LLM      │         │  • regulation.txt   │
│  • Cache            │         │  • chunks.txt       │
│                     │         │  • chroma_db/       │
└─────────────────────┘         └─────────────────────┘
```

### Réseau Docker

```
rag-network (bridge)
├── ollama (http://ollama:11434)
└── rag-app
    └── Accès à ollama via hostname
```

## 📊 Flux de Données

### Initialisation

```
1. Téléchargement Règlement
   │  (Google Drive → data/regulation.txt)
   ▼
2. Parsing
   │  (regulation.txt → chunks structurés)
   ▼
3. Génération Embeddings
   │  (chunks → vecteurs 768D)
   ▼
4. Indexation ChromaDB
   │  (vecteurs + métadonnées → base vectorielle)
   ▼
5. Système Prêt
```

### Requête Utilisateur

```
1. Input Question
   │  (Interface Gradio)
   ▼
2. Embedding Question
   │  (Question → vecteur 768D)
   ▼
3. Recherche Similarité
   │  (Vecteur question vs ChromaDB)
   │  • Calcul cosinus similarity
   │  • Top-K résultats (default: 5)
   ▼
4. Construction Prompt
   │  • Template + Contexte + Question
   │  • Limite: 4000 tokens
   ▼
5. Génération LLM
   │  (Ollama/Llama 3.2)
   │  • Streaming token par token
   ▼
6. Formatage Réponse
   │  • Réponse générée
   │  • Sources (3 premières)
   │  • Métadonnées (articles/points)
   ▼
7. Display
   │  (Gradio Markdown)
```

## 🔐 Sécurité et Isolation

- ✅ **Docker Network Isolation** : Les conteneurs communiquent via réseau privé
- ✅ **Volume Persistence** : Données persistantes en dehors des conteneurs
- ✅ **Port Mapping** : Seuls les ports nécessaires exposés
- ✅ **LLM Local** : Aucune donnée envoyée à des APIs externes

## 📈 Scalabilité

### Points d'Extension

1. **Modèles d'Embeddings**
   - Changer dans config.py
   - Supports : sentence-transformers, OpenAI, etc.

2. **Base Vectorielle**
   - ChromaDB (actuel)
   - Alternatives : Pinecone, Weaviate, FAISS

3. **LLM**
   - Ollama (actuel)
   - Alternatives : OpenAI API, HuggingFace, etc.

4. **Interface**
   - Gradio (actuel)
   - Alternatives : Streamlit, FastAPI, etc.

### Performance

- **Embeddings** : ~100ms par requête
- **Recherche ChromaDB** : ~50ms pour 1000+ chunks
- **LLM Génération** : 2-5s selon la longueur
- **Total** : ~3-6s par requête complète

## 🧪 Tests

Voir [test_rag.py](test_rag.py) :
- Tests unitaires pour chunking
- Tests d'embeddings
- Tests d'intégration

## 📝 Logs et Monitoring

```
docker-compose logs -f
├── ollama : Logs du serveur Ollama
└── rag-app : Logs de l'application
    ├── Requêtes utilisateur
    ├── Temps de réponse
    └── Erreurs
```

## 🔧 Maintenance

### Mise à jour du Règlement

```bash
# 1. Nouveau fichier
cp nouveau_reglement.txt data/regulation.txt

# 2. Réindexation
python init_database.py
```

### Mise à jour du Modèle LLM

```bash
docker-compose exec ollama ollama pull llama3.2:latest
docker-compose restart rag-app
```

---

**Architecture conçue pour la performance, la maintenabilité et l'extensibilité.**
