"""
Application Gradio pour l'interface utilisateur du système RAG.
"""

import gradio as gr
import os
from pathlib import Path
from rag_system import RAGSystem


class RAGGradioApp:
    """Application Gradio pour le système RAG."""
    
    def __init__(self, regulation_file: str = None):
        """
        Initialise l'application Gradio.
        
        Args:
            regulation_file: Chemin vers le fichier du règlement
        """
        print("🚀 Démarrage de l'application RAG...")
        
        # Initialiser le système RAG
        self.rag = RAGSystem(
            embedding_model='multi-qa-mpnet-base-dot-v1',
            llm_model='llama3.2:latest',
            chroma_db_path='./data/chroma_db'
        )
        
        # Charger et indexer le règlement si fourni
        if regulation_file and os.path.exists(regulation_file):
            print(f"📖 Chargement du règlement: {regulation_file}")
            chunks = self.rag.load_regulation(regulation_file)
            self.rag.index_chunks(chunks)
        else:
            print("⚠️  Aucun fichier de règlement fourni. Utilisation de la collection existante.")
    
    def rag_interface(self, question: str):
        """
        Interface Gradio avec streaming.
        
        Args:
            question: Question de l'utilisateur
            
        Yields:
            Réponses progressives
        """
        if not question.strip():
            yield "Veuillez entrer une question."
            return
        
        # Utiliser le streaming pour une meilleure UX
        for response in self.rag.query_streaming(question, n_results=5):
            yield response
    
    def create_interface(self):
        """
        Crée l'interface Gradio.
        
        Returns:
            Interface Gradio
        """
        demo = gr.Interface(
            fn=self.rag_interface,
            inputs=gr.Textbox(
                label="Posez une question sur le règlement technique",
                placeholder="Что говорится о безопасности продукции?",
                lines=3,
            ),
            outputs=gr.Markdown(label="Réponse"),
            title="🤖 Système RAG - Règlement Technique",
            description="""
            Posez vos questions sur le règlement technique et obtenez des réponses précises avec citations des sources.
            
            **Fonctionnalités:**
            - ✅ Recherche sémantique intelligente
            - ✅ Réponses basées sur le règlement officiel
            - ✅ Citations des articles et points pertinents
            - ✅ Support multilingue (Français/Russe)
            """,
            examples=[
                "Что говорится в статье 5 о требованиях безопасности?",
                "Какие документы необходимы для подтверждения соответствия?",
                "Quelles sont les exigences de sécurité pour les produits?",
                "Как осуществляется маркировка продукции?",
            ],
            allow_flagging="never",
            theme=gr.themes.Soft(),
        )
        
        return demo
    
    def launch(self, share: bool = False, server_name: str = "0.0.0.0", server_port: int = 7860):
        """
        Lance l'application Gradio.
        
        Args:
            share: Si True, crée un lien public
            server_name: Nom du serveur
            server_port: Port du serveur
        """
        demo = self.create_interface()
        
        print(f"\n🌐 Lancement de l'application sur http://{server_name}:{server_port}")
        
        demo.queue().launch(
            share=share,
            server_name=server_name,
            server_port=server_port
        )


def main():
    """Point d'entrée principal."""
    import argparse
    
    parser = argparse.ArgumentParser(description="Application RAG pour le règlement technique")
    parser.add_argument(
        "--regulation-file",
        type=str,
        default="./data/regulation.txt",
        help="Chemin vers le fichier du règlement"
    )
    parser.add_argument(
        "--share",
        action="store_true",
        help="Créer un lien public Gradio"
    )
    parser.add_argument(
        "--host",
        type=str,
        default="0.0.0.0",
        help="Adresse du serveur"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=7860,
        help="Port du serveur"
    )
    
    args = parser.parse_args()
    
    # Créer et lancer l'application
    app = RAGGradioApp(regulation_file=args.regulation_file)
    app.launch(
        share=args.share,
        server_name=args.host,
        server_port=args.port
    )


if __name__ == "__main__":
    main()
