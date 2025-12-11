"""
Script de vérification de l'installation et de l'environnement.
"""

import sys
import os
from pathlib import Path


def check_python_version():
    """Vérifie la version de Python."""
    print("🐍 Vérification de Python...")
    version = sys.version_info
    if version >= (3, 10):
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro} (requis: 3.10+)")
        return False


def check_dependencies():
    """Vérifie les dépendances Python."""
    print("\n📦 Vérification des dépendances...")
    
    dependencies = [
        'sentence_transformers',
        'chromadb',
        'langchain',
        'langchain_ollama',
        'gradio',
        'gdown',
    ]
    
    missing = []
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"   ✅ {dep}")
        except ImportError:
            print(f"   ❌ {dep}")
            missing.append(dep)
    
    if missing:
        print(f"\n⚠️  Dépendances manquantes: {', '.join(missing)}")
        print("   Installez avec: pip install -r requirements.txt")
        return False
    
    return True


def check_files():
    """Vérifie la présence des fichiers nécessaires."""
    print("\n📁 Vérification des fichiers...")
    
    files = [
        'app.py',
        'rag_system.py',
        'chunking.py',
        'config.py',
        'init_database.py',
        'requirements.txt',
        'Dockerfile',
        'docker-compose.yml',
        'README.md',
    ]
    
    all_present = True
    for file in files:
        if Path(file).exists():
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file}")
            all_present = False
    
    return all_present


def check_directories():
    """Vérifie la présence des répertoires nécessaires."""
    print("\n📂 Vérification des répertoires...")
    
    dirs = ['data', 'models']
    
    all_present = True
    for dir_name in dirs:
        dir_path = Path(dir_name)
        if dir_path.exists():
            print(f"   ✅ {dir_name}/")
        else:
            print(f"   ⚠️  {dir_name}/ (sera créé automatiquement)")
            dir_path.mkdir(exist_ok=True)
    
    return True


def check_docker():
    """Vérifie Docker."""
    print("\n🐳 Vérification de Docker...")
    
    try:
        import subprocess
        result = subprocess.run(['docker', '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.strip()
            print(f"   ✅ {version}")
            
            # Vérifier docker-compose
            result = subprocess.run(['docker-compose', '--version'],
                                  capture_output=True,
                                  text=True,
                                  timeout=5)
            if result.returncode == 0:
                version = result.stdout.strip()
                print(f"   ✅ {version}")
                return True
            else:
                print("   ⚠️  docker-compose non trouvé")
                return False
        else:
            print("   ❌ Docker non accessible")
            return False
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("   ⚠️  Docker non installé ou non démarré")
        print("      Installation optionnelle pour le déploiement")
        return False


def check_ollama():
    """Vérifie Ollama."""
    print("\n🦙 Vérification d'Ollama...")
    
    try:
        import requests
        response = requests.get('http://localhost:11434/', timeout=2)
        if response.status_code == 200:
            print("   ✅ Ollama en cours d'exécution")
            
            # Vérifier le modèle
            try:
                response = requests.get('http://localhost:11434/api/tags', timeout=2)
                if response.status_code == 200:
                    models = response.json().get('models', [])
                    llama_models = [m for m in models if 'llama3.2' in m.get('name', '')]
                    if llama_models:
                        print(f"   ✅ Modèle llama3.2 disponible")
                        return True
                    else:
                        print("   ⚠️  Modèle llama3.2 non trouvé")
                        print("      Téléchargez avec: ollama pull llama3.2:latest")
                        return False
            except:
                return True
        else:
            print("   ⚠️  Ollama répond mais état inconnu")
            return False
    except:
        print("   ⚠️  Ollama non accessible (http://localhost:11434)")
        print("      Installation: https://ollama.ai")
        print("      Ou utilisez Docker avec docker-compose")
        return False


def check_regulation():
    """Vérifie la présence du règlement."""
    print("\n📄 Vérification du règlement...")
    
    regulation_file = Path('data/regulation.txt')
    if regulation_file.exists():
        size = regulation_file.stat().st_size
        print(f"   ✅ regulation.txt ({size:,} octets)")
        return True
    else:
        print("   ⚠️  regulation.txt non trouvé")
        print("      Exécutez: python init_database.py")
        return False


def check_database():
    """Vérifie la base de données ChromaDB."""
    print("\n💾 Vérification de la base de données...")
    
    db_path = Path('data/chroma_db')
    if db_path.exists():
        print(f"   ✅ ChromaDB existe")
        
        # Compter les fichiers
        files = list(db_path.rglob('*'))
        print(f"      {len(files)} fichiers dans la base")
        return True
    else:
        print("   ⚠️  ChromaDB non initialisée")
        print("      Exécutez: python init_database.py")
        return False


def print_summary(checks):
    """Affiche le résumé des vérifications."""
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ")
    print("=" * 60)
    
    total = len(checks)
    passed = sum(checks.values())
    
    for name, status in checks.items():
        icon = "✅" if status else "❌"
        print(f"{icon} {name}")
    
    print("=" * 60)
    print(f"Score: {passed}/{total} vérifications réussies")
    
    if passed == total:
        print("\n🎉 Tout est prêt ! Vous pouvez lancer l'application.")
        print("\n   Avec Docker: docker-compose up")
        print("   Sans Docker: python app.py")
    else:
        print("\n⚠️  Certains composants manquent. Consultez les messages ci-dessus.")


def main():
    """Fonction principale."""
    print("\n" + "=" * 60)
    print("🔍 VÉRIFICATION DE L'ENVIRONNEMENT RAG")
    print("=" * 60)
    
    checks = {
        'Python 3.10+': check_python_version(),
        'Dépendances Python': check_dependencies(),
        'Fichiers du projet': check_files(),
        'Répertoires': check_directories(),
        'Docker': check_docker(),
        'Ollama': check_ollama(),
        'Règlement': check_regulation(),
        'Base de données': check_database(),
    }
    
    print_summary(checks)
    
    print("\n" + "=" * 60)
    print("💡 PROCHAINES ÉTAPES")
    print("=" * 60)
    
    if not checks['Règlement'] or not checks['Base de données']:
        print("\n1️⃣  Initialiser la base de données:")
        print("    python init_database.py")
    
    if not checks['Docker'] and not checks['Ollama']:
        print("\n2️⃣  Installer Ollama OU Docker:")
        print("    • Ollama: https://ollama.ai")
        print("    • Docker: https://docker.com")
    
    if checks['Python 3.10+'] and checks['Dépendances Python']:
        print("\n3️⃣  Lancer l'application:")
        if checks['Docker']:
            print("    docker-compose up")
        else:
            print("    python app.py")
    
    print("\n📚 Documentation:")
    print("    • Guide rapide: QUICKSTART.md")
    print("    • Documentation complète: README.md")
    print("    • Architecture: ARCHITECTURE.md")
    print("    • Exemples: examples.py")
    print()


if __name__ == "__main__":
    main()
