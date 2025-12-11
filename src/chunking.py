"""
Module de chunking pour parser le règlement technique en chunks structurés.
Basé sur la méthode du notebook Локальные_модели_для_формирования_эмбеддингов_и_векторные_БД.
"""

import re
import gdown
from typing import List, Dict


def download_regulation(file_id: str, output_filename: str = 'regulation.txt') -> None:
    """
    Télécharge un fichier depuis Google Drive.
    
    Args:
        file_id: ID du fichier Google Drive
        output_filename: Nom du fichier de sortie
    """
    url = f"https://drive.google.com/uc?id={file_id}"
    gdown.download(url, output_filename, quiet=False)
    print(f"Fichier téléchargé: {output_filename}")


def parse_regulation_to_chunks(text: str) -> List[Dict]:
    """
    Parse le règlement en chunks par articles et points.
    Retourne une liste de dictionnaires avec métadonnées.
    
    Args:
        text: Texte complet du règlement
        
    Returns:
        Liste de chunks avec métadonnées (id, article_num, article_title, point_num, text)
    """
    chunks = []
    article_pattern = r"Статья (\d+)\. (.+?)(?=\n|$)"
    article_matches = list(re.finditer(article_pattern, text))

    for i, match in enumerate(article_matches):
        article_num = match.group(1)
        article_title = match.group(2).strip()

        start = match.end()
        end = article_matches[i + 1].start() if i + 1 < len(article_matches) else len(text)
        article_text = text[start:end].strip()

        point_pattern = r"^(\d+)\.\s+(.+?)(?=^\d+\.\s+|\Z)"
        points = re.findall(point_pattern, article_text, re.MULTILINE | re.DOTALL)

        for pt, point_text in points:
            chunks.append({
                'id': f"{article_num}.{pt}",
                'article_num': article_num,
                'article_title': article_title,
                'point_num': pt,
                'text': point_text.strip()
            })

    return chunks


def save_chunks_to_txt(chunks: List[Dict], filename: str = 'chunks.txt') -> None:
    """
    Sauvegarde les chunks dans un fichier texte formaté.
    
    Args:
        chunks: Liste des chunks
        filename: Nom du fichier de sortie
    """
    with open(filename, 'w', encoding='utf-8') as f:
        for chunk in chunks:
            f.write(f"ID: {chunk['id']}\n")
            f.write(f"номер статьи: {chunk['article_num']}\t{chunk['article_title']}\n")
            f.write(f"номер пункта внутри статьи: {chunk['point_num']}\n")
            f.write(f"Text: {chunk['text']}\n")
            f.write("-" * 80 + "\n\n")
    print(f"Chunks sauvegardés dans {filename}")


def load_chunks_from_txt(filename: str = 'chunks.txt') -> List[Dict]:
    """
    Charge les chunks depuis un fichier texte.
    
    Args:
        filename: Nom du fichier à charger
        
    Returns:
        Liste de chunks
    """
    chunks = []
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()

    chunk_blocks = content.split('-' * 80)

    for block in chunk_blocks:
        block = block.strip()
        if not block:
            continue

        lines = block.split('\n')
        chunk_data = {}

        for i, line in enumerate(lines):
            if line.startswith('ID:'):
                chunk_data['id'] = line.replace('ID:', '').strip()
            elif line.startswith('номер статьи:'):
                parts = line.replace('номер статьи:', '').strip().split('\t')
                chunk_data['article_num'] = parts[0].strip()
                chunk_data['article_title'] = parts[1].strip() if len(parts) > 1 else ''
            elif line.startswith('номер пункта внутри статьи:'):
                chunk_data['point_num'] = line.replace('номер пункта внутри статьи:', '').strip()
            elif line.startswith('Text:'):
                chunk_data['text'] = '\n'.join(lines[i:]).replace('Text:', '', 1).strip()
                break

        if 'id' in chunk_data and 'text' in chunk_data:
            chunks.append(chunk_data)

    print(f"{len(chunks)} chunks chargés depuis {filename}")
    return chunks
