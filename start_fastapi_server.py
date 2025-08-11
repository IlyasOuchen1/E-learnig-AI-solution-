#!/usr/bin/env python3
"""
Script de Démarrage pour l'API FastAPI avec SQLite
"""

import os
import sys
import subprocess
import time
import webbrowser
from pathlib import Path

def check_dependencies():
    """Vérifie que les dépendances sont installées"""
    print("🔍 Vérification des dépendances...")
    
    required_packages = ['fastapi', 'uvicorn']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"   ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"   ❌ {package} - MANQUANT")
    
    if missing_packages:
        print(f"\n❌ Packages manquants: {', '.join(missing_packages)}")
        print("💡 Installez avec: pip install fastapi uvicorn")
        return False
    
    print("✅ Toutes les dépendances sont installées")
    return True

def check_database():
    """Vérifie que la base SQLite existe"""
    print("\n🗄️ Vérification de la base SQLite...")
    
    db_path = "educational_platform.db"
    if not os.path.exists(db_path):
        print(f"❌ Base de données non trouvée: {db_path}")
        print("💡 Assurez-vous que l'orchestrateur a généré des données")
        return False
    
    # Vérifier la taille de la base
    size_mb = os.path.getsize(db_path) / (1024 * 1024)
    print(f"✅ Base de données trouvée: {db_path}")
    print(f"   Taille: {size_mb:.1f} MB")
    
    # Vérifier qu'elle contient des données
    try:
        import sqlite3
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Compter les sessions
        cursor.execute("SELECT COUNT(*) FROM workflow_sessions")
        session_count = cursor.fetchone()[0]
        
        # Compter les activités
        cursor.execute("SELECT COUNT(*) FROM sequencer_activities")
        activity_count = cursor.fetchone()[0]
        
        # Compter les scripts
        cursor.execute("SELECT COUNT(*) FROM generated_scripts")
        script_count = cursor.fetchone()[0]
        
        conn.close()
        
        print(f"   Sessions: {session_count}")
        print(f"   Activités: {activity_count}")
        print(f"   Scripts: {script_count}")
        
        if session_count == 0:
            print("   ⚠️ Aucune session trouvée - l'orchestrateur n'a pas encore généré de données")
        
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur vérification base: {e}")
        return False

def start_fastapi_server():
    """Démarre le serveur FastAPI"""
    print("\n🚀 Démarrage du serveur FastAPI avec SQLite...")
    print("=" * 50)
    
    api_file = "api_server_sqlite.py"
    if not os.path.exists(api_file):
        print(f"❌ Fichier API non trouvé: {api_file}")
        return False
    
    print(f"📁 Fichier API: {api_file}")
    print("🌐 URL: http://localhost:8000")
    print("📚 Documentation: http://localhost:8000/docs")
    print("🔍 Health Check: http://localhost:8000/health")
    print("")
    print("🔄 Le serveur va démarrer...")
    print("   Appuyez sur Ctrl+C pour arrêter")
    print("=" * 50)
    
    try:
        # Attendre un peu puis ouvrir la documentation
        time.sleep(3)
        webbrowser.open("http://localhost:8000/docs")
        
        # Démarrer le serveur
        subprocess.run([
            sys.executable, "-m", "uvicorn", 
            "api_server_sqlite:app",
            "--host", "0.0.0.0",
            "--port", "8000",
            "--reload"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Arrêt demandé par l'utilisateur")
    except Exception as e:
        print(f"❌ Erreur lors du démarrage: {e}")
        return False
    
    return True

def show_api_info():
    """Affiche les informations de l'API"""
    print("\n" + "=" * 60)
    print("🌐 INFORMATIONS API FASTAPI + SQLITE")
    print("=" * 60)
    
    print("📋 URLs importantes:")
    print("   🌐 API Base: http://localhost:8000")
    print("   📚 Documentation: http://localhost:8000/docs")
    print("   🔍 Health Check: http://localhost:8000/health")
    
    print("\n📊 Endpoints disponibles:")
    print("   GET /api/sessions - Sessions de workflow")
    print("   GET /api/sessions/{id} - Session spécifique")
    print("   GET /api/sessions/{id}/content - Contenu complet")
    print("   GET /api/sessions/{id}/content/simple - Contenu simple (frontend)")
    print("   GET /api/statistics - Statistiques globales")
    
    print("\n💻 Exemple d'intégration JavaScript:")
    print("""
const API_BASE_URL = 'http://localhost:8000';

// Récupérer les sessions
fetch(`${API_BASE_URL}/api/sessions?limit=10`)
  .then(response => response.json())
  .then(sessions => console.log(sessions));

// Récupérer le contenu d'une session (format exact)
fetch(`${API_BASE_URL}/api/sessions/YOUR_SESSION_ID/content/simple`)
  .then(response => response.json())
  .then(content => {
    // content est exactement le format attendu par le frontend
    // {activity_id: {activite: {...}, script: '...'}}
    loadContentInApp(content);
  });
    """)
    
    print("\n🎯 Avantages de cette approche:")
    print("✅ **Format JSON exact** - Aucune modification du frontend")
    print("✅ **Base SQLite** - Stockage local et efficace")
    print("✅ **API REST** - Endpoints standards et documentés")
    print("✅ **CORS configuré** - Compatible avec tous les frontends")
    print("✅ **Documentation automatique** - Swagger/OpenAPI")
    
    print("\n🎯 Prochaines étapes:")
    print("1. ✅ API FastAPI démarrée sur http://localhost:8000")
    print("2. 📚 Consulter la documentation: http://localhost:8000/docs")
    print("3. 🧪 Tester les endpoints avec l'interface Swagger")
    print("4. 🔗 Intégrer dans votre frontend")
    print("=" * 60)

def main():
    """Fonction principale"""
    print("🚀 Démarrage API FastAPI + SQLite")
    print("=" * 50)
    
    # Vérifications préalables
    if not check_dependencies():
        return False
    
    if not check_database():
        return False
    
    # Afficher les informations de l'API
    show_api_info()
    
    # Démarrer le serveur
    return start_fastapi_server()

if __name__ == "__main__":
    main() 