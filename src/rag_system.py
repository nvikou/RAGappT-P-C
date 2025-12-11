"""
Système RAG principal pour le règlement technique.
Combine chunking, embeddings, ChromaDB et LLM pour répondre aux questions.
"""

import os
from pathlib import Path
from typing import List, Dict, Tuple
from sentence_transformers import SentenceTransformer, util
import chromadb
from chromadb.config import Settings
from langchain_ollama import OllamaLLM
from langchain.prompts import PromptTemplate

from chunking import parse_regulation_to_chunks, load_chunks_from_txt, save_chunks_to_txt


class RAGSystem:
    """Système RAG pour le règlement technique."""
    
    def __init__(
        self, 
        embedding_model: str = 'multi-qa-mpnet-base-dot-v1',
        llm_model: str = 'llama3.2:latest',
        chroma_db_path: str = './data/chroma_db'
    ):
        """
        Initialise le système RAG.
        
        Args:
            embedding_model: Modèle SentenceTransformer pour les embeddings
            llm_model: Modèle Ollama pour la génération de réponses
            chroma_db_path: Chemin de la base de données ChromaDB
        """
        print("🔄 Initialisation du système RAG...")
        
        # Modèle d'embeddings
        print(f"📦 Chargement du modèle d'embeddings: {embedding_model}")
        self.embedding_model = SentenceTransformer(embedding_model)
        
        # ChromaDB
        print(f"💾 Initialisation de ChromaDB: {chroma_db_path}")
        self.chroma_client = chromadb.PersistentClient(
            path=chroma_db_path,
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Collection ChromaDB
        self.collection_name = "regulation_collection"
        try:
            self.collection = self.chroma_client.get_collection(name=self.collection_name)
            print(f"✅ Collection existante chargée: {self.collection_name}")
        except:
            self.collection = self.chroma_client.create_collection(
                name=self.collection_name,
                metadata={"hnsw:space": "cosine"}
            )
            print(f"✅ Nouvelle collection créée: {self.collection_name}")
        
        # LLM
        print(f"🤖 Initialisation du LLM: {llm_model}")
        self.llm = OllamaLLM(model=llm_model, temperature=0.1)
        
        # Prompt template
        self.prompt_template = PromptTemplate(
            input_variables=["context", "question"],
            template="""Vous êtes un expert en règlements techniques. Basé sur la documentation fournie, répondez à la question de manière claire et précise en français ou en russe selon la langue de la question.

Documentation:
{context}

Question: {question}

Réponse (soyez précis, citez les articles et points pertinents):"""
        )
        
        # Chaîne de traitement
        self.chain = self.prompt_template | self.llm
        
        print("✅ Système RAG initialisé avec succès!\n")
    
    def load_regulation(self, regulation_file: str) -> List[Dict]:
        """
        Charge et parse le règlement.
        
        Args:
            regulation_file: Chemin vers le fichier du règlement
            
        Returns:
            Liste de chunks
        """
        print(f"📖 Chargement du règlement: {regulation_file}")
        
        with open(regulation_file, 'r', encoding='utf-8') as f:
            text = f.read()
        
        print("🔍 Parsing du règlement en chunks...")
        chunks = parse_regulation_to_chunks(text)
        print(f"✅ {len(chunks)} chunks créés")
        
        return chunks
    
    def index_chunks(self, chunks: List[Dict], force_reindex: bool = False) -> None:
        """
        Indexe les chunks dans ChromaDB avec leurs embeddings.
        
        Args:
            chunks: Liste de chunks à indexer
            force_reindex: Si True, réindexe même si la collection n'est pas vide
        """
        # Vérifier si la collection est déjà remplie
        if self.collection.count() > 0 and not force_reindex:
            print(f"ℹ️  Collection déjà indexée avec {self.collection.count()} documents")
            return
        
        print(f"🔄 Indexation de {len(chunks)} chunks...")
        
        # Extraire les textes
        documents = [chunk['text'] for chunk in chunks]
        
        # Générer les embeddings
        print("🧮 Génération des embeddings...")
        embeddings = self.embedding_model.encode(documents, show_progress_bar=True)
        
        # Préparer les métadonnées
        metadatas = [
            {
                'id': chunk['id'],
                'article_num': chunk['article_num'],
                'article_title': chunk['article_title'],
                'point_num': chunk['point_num']
            }
            for chunk in chunks
        ]
        
        # IDs uniques
        ids = [f"chunk_{i}" for i in range(len(chunks))]
        
        # Ajouter à ChromaDB
        print("💾 Ajout à ChromaDB...")
        self.collection.add(
            embeddings=embeddings.tolist(),
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        
        print(f"✅ {len(chunks)} chunks indexés dans ChromaDB\n")
    
    def retrieve_context(self, question: str, n_results: int = 5) -> Tuple[str, List[str], List[Dict]]:
        """
        Récupère le contexte pertinent pour une question.
        
        Args:
            question: Question de l'utilisateur
            n_results: Nombre de résultats à retourner
            
        Returns:
            Tuple (context, documents, metadatas)
        """
        # Générer l'embedding de la question
        query_embedding = self.embedding_model.encode([question])
        
        # Rechercher dans ChromaDB
        results = self.collection.query(
            query_embeddings=query_embedding.tolist(),
            n_results=n_results,
            include=["documents", "metadatas", "distances"]
        )
        
        # Extraire les résultats
        documents = results["documents"][0]
        metadatas = results["metadatas"][0]
        
        # Créer le contexte
        context = "\n\n---SECTION---\n\n".join(documents)
        
        return context, documents, metadatas
    
    def get_llm_answer(self, question: str, context: str) -> str:
        """
        Génère une réponse en utilisant le LLM.
        
        Args:
            question: Question de l'utilisateur
            context: Contexte récupéré
            
        Returns:
            Réponse générée
        """
        answer = self.chain.invoke({
            "context": context[:4000],  # Limiter le contexte
            "question": question
        })
        return answer
    
    def stream_llm_answer(self, question: str, context: str):
        """
        Génère une réponse en streaming.
        
        Args:
            question: Question de l'utilisateur
            context: Contexte récupéré
            
        Yields:
            Tokens de la réponse
        """
        for token in self.llm.stream(
            self.prompt_template.format(context=context[:4000], question=question)
        ):
            yield token
    
    def format_response(
        self, 
        question: str, 
        answer: str, 
        source_chunks: List[str], 
        metadatas: List[Dict]
    ) -> str:
        """
        Formate la réponse finale avec les sources.
        
        Args:
            question: Question de l'utilisateur
            answer: Réponse générée
            source_chunks: Chunks sources
            metadatas: Métadonnées des chunks
            
        Returns:
            Réponse formatée
        """
        response = f"**Question:** {question}\n\n"
        response += f"**Réponse:** {answer}\n\n"
        response += "**Sources:**\n"
        
        for i, (chunk, metadata) in enumerate(zip(source_chunks[:3], metadatas[:3]), 1):
            article = metadata.get('article_num', 'N/A')
            point = metadata.get('point_num', 'N/A')
            title = metadata.get('article_title', 'N/A')
            preview = chunk[:150].replace("\n", " ") + "..."
            response += f"\n{i}. **Article {article}, Point {point}** ({title})\n"
            response += f"   {preview}\n"
        
        return response
    
    def query(self, question: str, n_results: int = 5) -> str:
        """
        Interroge le système RAG avec une question.
        
        Args:
            question: Question de l'utilisateur
            n_results: Nombre de chunks à récupérer
            
        Returns:
            Réponse formatée
        """
        # Récupérer le contexte
        context, documents, metadatas = self.retrieve_context(question, n_results)
        
        # Générer la réponse
        answer = self.get_llm_answer(question, context)
        
        # Formater la réponse
        return self.format_response(question, answer, documents, metadatas)
    
    def query_streaming(self, question: str, n_results: int = 5):
        """
        Interroge le système RAG avec streaming.
        
        Args:
            question: Question de l'utilisateur
            n_results: Nombre de chunks à récupérer
            
        Yields:
            Parties de la réponse
        """
        # Récupérer le contexte
        context, documents, metadatas = self.retrieve_context(question, n_results)
        
        # Générer la réponse en streaming
        response_start = f"**Question:** {question}\n\n**Réponse:** "
        answer = ""
        
        for token in self.stream_llm_answer(question, context):
            answer += token
            yield response_start + answer
        
        # Ajouter les sources
        yield self.format_response(question, answer, documents, metadatas)


if __name__ == "__main__":
    # Test du système
    rag = RAGSystem()
    
    # Charger le règlement (exemple)
    # chunks = rag.load_regulation("data/regulation.txt")
    # rag.index_chunks(chunks)
    
    # Test d'une question
    # response = rag.query("Что говорится о безопасности в статье 5?")
    # print(response)
