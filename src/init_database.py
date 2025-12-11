"""
Script pour initialiser la base de données avec le règlement technique.
"""

import os
import sys
from chunking import download_regulation, parse_regulation_to_chunks, save_chunks_to_txt
from rag_system import RAGSystem


def main():
    """Initialise la base de données avec le règlement."""
    
    # ID du fichier Google Drive (extrait du lien fourni)
    file_id = "1DhT50DonrOVzt5bX_JgCScvM03L9GOIK"
    regulation_file = "./data/regulation.txt"
    chunks_file = "./data/chunks.txt"
    
    print("=" * 80)
    print("🚀 INITIALISATION DE LA BASE DE DONNÉES RAG")
    print("=" * 80)
    
    # Étape 1: Télécharger le règlement
    if not os.path.exists(regulation_file):
        print("\n📥 Étape 1/4: Téléchargement du règlement depuis Google Drive...")
        try:
            download_regulation(file_id, regulation_file)
        except Exception as e:
            print(f"❌ Erreur lors du téléchargement: {e}")
            print("⚠️  Veuillez placer manuellement le fichier 'regulation.txt' dans le dossier 'data/'")
            return
    else:
        print(f"\n✅ Étape 1/4: Règlement déjà téléchargé: {regulation_file}")
    
    # Étape 2: Parser le règlement en chunks
    print("\n🔍 Étape 2/4: Parsing du règlement en chunks...")
    with open(regulation_file, 'r', encoding='utf-8') as f:
        text = f.read()
    
    chunks = parse_regulation_to_chunks(text)
    print(f"✅ {len(chunks)} chunks créés")
    
    # Étape 3: Sauvegarder les chunks
    print("\n💾 Étape 3/4: Sauvegarde des chunks...")
    save_chunks_to_txt(chunks, chunks_file)
    
    # Étape 4: Indexer dans ChromaDB
    print("\n🔄 Étape 4/4: Indexation dans ChromaDB...")
    rag = RAGSystem()
    rag.index_chunks(chunks, force_reindex=True)
    
    print("\n" + "=" * 80)
    print("✅ INITIALISATION TERMINÉE AVEC SUCCÈS!")
    print("=" * 80)
    print(f"\n📊 Statistiques:")
    print(f"   - Chunks créés: {len(chunks)}")
    print(f"   - Fichier du règlement: {regulation_file}")
    print(f"   - Fichier des chunks: {chunks_file}")
    print(f"   - Base de données: ./data/chroma_db/")
    print("\n🎉 Vous pouvez maintenant lancer l'application avec: python app.py\n")


if __name__ == "__main__":
    main()
