"""
Exemples d'utilisation avancée du système RAG.
"""

# ==============================================================================
# EXEMPLE 1 : Utilisation Basique
# ==============================================================================

def example_basic_usage():
    """Exemple d'utilisation basique."""
    from rag_system import RAGSystem
    
    # Initialiser le système
    rag = RAGSystem()
    
    # Poser une question
    response = rag.query("Что говорится о безопасности продукции?")
    print(response)


# ==============================================================================
# EXEMPLE 2 : Utilisation avec Streaming
# ==============================================================================

def example_streaming():
    """Exemple d'utilisation avec streaming."""
    from rag_system import RAGSystem
    
    rag = RAGSystem()
    
    # Question avec réponse en streaming
    for chunk in rag.query_streaming("Какие документы необходимы?"):
        print(chunk, end='', flush=True)


# ==============================================================================
# EXEMPLE 3 : Indexation Personnalisée
# ==============================================================================

def example_custom_indexing():
    """Exemple d'indexation avec des paramètres personnalisés."""
    from rag_system import RAGSystem
    
    # Initialiser avec un modèle différent
    rag = RAGSystem(
        embedding_model='paraphrase-multilingual-mpnet-base-v2',
        llm_model='llama3.2:latest',
        chroma_db_path='./data/custom_db'
    )
    
    # Charger et indexer
    chunks = rag.load_regulation("data/regulation.txt")
    rag.index_chunks(chunks, force_reindex=True)
    
    print(f"✅ {len(chunks)} chunks indexés")


# ==============================================================================
# EXEMPLE 4 : Recherche Sans LLM (Recherche Pure)
# ==============================================================================

def example_search_only():
    """Recherche vectorielle sans génération de réponse."""
    from rag_system import RAGSystem
    
    rag = RAGSystem()
    
    # Récupérer uniquement le contexte
    context, documents, metadatas = rag.retrieve_context(
        "Что говорится о маркировке?",
        n_results=3
    )
    
    # Afficher les résultats
    for i, (doc, meta) in enumerate(zip(documents, metadatas), 1):
        print(f"\n📄 Résultat {i}:")
        print(f"   Article {meta['article_num']}, Point {meta['point_num']}")
        print(f"   Titre: {meta['article_title']}")
        print(f"   Texte: {doc[:200]}...")


# ==============================================================================
# EXEMPLE 5 : Traitement par Lots
# ==============================================================================

def example_batch_processing():
    """Traiter plusieurs questions en une fois."""
    from rag_system import RAGSystem
    
    rag = RAGSystem()
    
    questions = [
        "Что говорится о безопасности?",
        "Какие документы необходимы?",
        "Как осуществляется маркировка?"
    ]
    
    responses = []
    for question in questions:
        response = rag.query(question, n_results=3)
        responses.append({
            'question': question,
            'response': response
        })
    
    # Sauvegarder les résultats
    import json
    with open('batch_results.json', 'w', encoding='utf-8') as f:
        json.dump(responses, f, ensure_ascii=False, indent=2)
    
    print("✅ Résultats sauvegardés dans batch_results.json")


# ==============================================================================
# EXEMPLE 6 : Analyse de Similarité
# ==============================================================================

def example_similarity_analysis():
    """Analyser la similarité entre documents."""
    from sentence_transformers import SentenceTransformer, util
    import numpy as np
    
    model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
    
    # Documents à comparer
    texts = [
        "Продукция должна соответствовать требованиям безопасности",
        "Безопасность продукции обеспечивается производителем",
        "Маркировка должна содержать информацию о производителе"
    ]
    
    # Générer embeddings
    embeddings = model.encode(texts)
    
    # Calculer similarités
    similarities = util.cos_sim(embeddings, embeddings)
    
    # Afficher matrice de similarité
    print("\n📊 Matrice de Similarité:")
    print(np.round(similarities.numpy(), 3))


# ==============================================================================
# EXEMPLE 7 : Export des Chunks
# ==============================================================================

def example_export_chunks():
    """Exporter les chunks dans différents formats."""
    from chunking import load_chunks_from_txt
    import json
    import csv
    
    # Charger les chunks
    chunks = load_chunks_from_txt('data/chunks.txt')
    
    # Export JSON
    with open('chunks.json', 'w', encoding='utf-8') as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)
    
    # Export CSV
    with open('chunks.csv', 'w', encoding='utf-8', newline='') as f:
        if chunks:
            writer = csv.DictWriter(f, fieldnames=chunks[0].keys())
            writer.writeheader()
            writer.writerows(chunks)
    
    print("✅ Chunks exportés en JSON et CSV")


# ==============================================================================
# EXEMPLE 8 : Statistiques sur le Règlement
# ==============================================================================

def example_regulation_statistics():
    """Analyser les statistiques du règlement."""
    from chunking import load_chunks_from_txt
    from collections import Counter
    
    chunks = load_chunks_from_txt('data/chunks.txt')
    
    # Statistiques
    total_chunks = len(chunks)
    articles = set(chunk['article_num'] for chunk in chunks)
    total_articles = len(articles)
    
    # Points par article
    points_per_article = Counter(chunk['article_num'] for chunk in chunks)
    
    # Longueurs de texte
    text_lengths = [len(chunk['text']) for chunk in chunks]
    avg_length = sum(text_lengths) / len(text_lengths)
    min_length = min(text_lengths)
    max_length = max(text_lengths)
    
    # Affichage
    print("\n📊 STATISTIQUES DU RÈGLEMENT")
    print("=" * 60)
    print(f"Total d'articles: {total_articles}")
    print(f"Total de chunks: {total_chunks}")
    print(f"Moyenne chunks/article: {total_chunks/total_articles:.1f}")
    print(f"\nLongueur de texte:")
    print(f"  - Moyenne: {avg_length:.0f} caractères")
    print(f"  - Min: {min_length} caractères")
    print(f"  - Max: {max_length} caractères")
    print(f"\nTop 5 articles avec le plus de points:")
    for article, count in points_per_article.most_common(5):
        print(f"  Article {article}: {count} points")


# ==============================================================================
# EXEMPLE 9 : Interface CLI Interactive
# ==============================================================================

def example_interactive_cli():
    """Interface en ligne de commande interactive."""
    from rag_system import RAGSystem
    
    rag = RAGSystem()
    
    print("\n" + "=" * 60)
    print("🤖 SYSTÈME RAG INTERACTIF")
    print("=" * 60)
    print("Posez vos questions (tapez 'quit' pour quitter)\n")
    
    while True:
        question = input("❓ Votre question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("👋 Au revoir!")
            break
        
        if not question:
            continue
        
        print("\n🤔 Recherche en cours...\n")
        
        try:
            response = rag.query(question)
            print(response)
        except Exception as e:
            print(f"❌ Erreur: {e}")
        
        print("\n" + "-" * 60 + "\n")


# ==============================================================================
# EXEMPLE 10 : API REST Simple
# ==============================================================================

def example_rest_api():
    """Créer une API REST simple avec FastAPI."""
    try:
        from fastapi import FastAPI, HTTPException
        from pydantic import BaseModel
        from rag_system import RAGSystem
        
        app = FastAPI(title="RAG API")
        rag = RAGSystem()
        
        class Query(BaseModel):
            question: str
            n_results: int = 5
        
        class Response(BaseModel):
            question: str
            answer: str
        
        @app.post("/query", response_model=Response)
        async def query_endpoint(query: Query):
            """Endpoint pour poser une question."""
            try:
                response = rag.query(query.question, query.n_results)
                return Response(question=query.question, answer=response)
            except Exception as e:
                raise HTTPException(status_code=500, detail=str(e))
        
        @app.get("/health")
        async def health():
            """Endpoint de santé."""
            return {"status": "healthy"}
        
        # Pour lancer: uvicorn examples:app --reload
        print("✅ API REST créée. Lancez avec: uvicorn examples:app --reload")
        
    except ImportError:
        print("⚠️  FastAPI non installé. Installez avec: pip install fastapi uvicorn")


# ==============================================================================
# MENU PRINCIPAL
# ==============================================================================

def main():
    """Menu principal pour choisir un exemple."""
    examples = {
        '1': ('Utilisation Basique', example_basic_usage),
        '2': ('Streaming', example_streaming),
        '3': ('Indexation Personnalisée', example_custom_indexing),
        '4': ('Recherche Sans LLM', example_search_only),
        '5': ('Traitement par Lots', example_batch_processing),
        '6': ('Analyse de Similarité', example_similarity_analysis),
        '7': ('Export des Chunks', example_export_chunks),
        '8': ('Statistiques du Règlement', example_regulation_statistics),
        '9': ('Interface CLI Interactive', example_interactive_cli),
        '10': ('API REST', example_rest_api),
    }
    
    print("\n" + "=" * 60)
    print("📚 EXEMPLES D'UTILISATION DU SYSTÈME RAG")
    print("=" * 60)
    print("\nChoisissez un exemple:\n")
    
    for key, (name, _) in examples.items():
        print(f"  {key}. {name}")
    
    print("\n  0. Quitter")
    print("=" * 60)
    
    choice = input("\n👉 Votre choix: ").strip()
    
    if choice == '0':
        print("👋 Au revoir!")
        return
    
    if choice in examples:
        name, func = examples[choice]
        print(f"\n▶️  Exécution: {name}\n")
        try:
            func()
        except KeyboardInterrupt:
            print("\n\n⚠️  Interrompu par l'utilisateur")
        except Exception as e:
            print(f"\n❌ Erreur: {e}")
    else:
        print("❌ Choix invalide")


if __name__ == "__main__":
    main()
