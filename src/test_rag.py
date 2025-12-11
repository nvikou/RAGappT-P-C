"""
Tests unitaires pour le système RAG.
"""

import unittest
from pathlib import Path
from chunking import parse_regulation_to_chunks


class TestChunking(unittest.TestCase):
    """Tests pour le module de chunking."""
    
    def setUp(self):
        """Initialisation des tests."""
        self.sample_text = """
Статья 5. Требования безопасности

1. Продукция должна соответствовать требованиям безопасности.
2. Безопасность продукции обеспечивается производителем.
3. Документация должна быть на русском языке.

Статья 6. Маркировка продукции

1. Продукция должна быть промаркирована.
2. Маркировка должна содержать информацию о производителе.
"""
    
    def test_parse_regulation(self):
        """Teste le parsing du règlement."""
        chunks = parse_regulation_to_chunks(self.sample_text)
        
        # Vérifier le nombre de chunks
        self.assertGreater(len(chunks), 0)
        
        # Vérifier la structure des chunks
        for chunk in chunks:
            self.assertIn('id', chunk)
            self.assertIn('article_num', chunk)
            self.assertIn('article_title', chunk)
            self.assertIn('point_num', chunk)
            self.assertIn('text', chunk)
    
    def test_chunk_ids(self):
        """Teste les IDs des chunks."""
        chunks = parse_regulation_to_chunks(self.sample_text)
        
        # Vérifier que les IDs sont bien formés
        for chunk in chunks:
            self.assertRegex(chunk['id'], r'^\d+\.\d+$')
    
    def test_article_extraction(self):
        """Teste l'extraction des articles."""
        chunks = parse_regulation_to_chunks(self.sample_text)
        
        # Vérifier qu'on a bien les articles 5 et 6
        article_nums = [chunk['article_num'] for chunk in chunks]
        self.assertIn('5', article_nums)
        self.assertIn('6', article_nums)


class TestRAGSystem(unittest.TestCase):
    """Tests pour le système RAG."""
    
    def test_embedding_generation(self):
        """Teste la génération d'embeddings."""
        from sentence_transformers import SentenceTransformer
        
        model = SentenceTransformer('multi-qa-mpnet-base-dot-v1')
        text = "Test de génération d'embeddings"
        embedding = model.encode([text])
        
        # Vérifier la forme de l'embedding
        self.assertEqual(len(embedding.shape), 2)
        self.assertEqual(embedding.shape[0], 1)
        self.assertGreater(embedding.shape[1], 0)


def run_tests():
    """Exécute tous les tests."""
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    suite.addTests(loader.loadTestsFromTestCase(TestChunking))
    suite.addTests(loader.loadTestsFromTestCase(TestRAGSystem))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(suite)
    
    return result.wasSuccessful()


if __name__ == "__main__":
    success = run_tests()
    exit(0 if success else 1)
