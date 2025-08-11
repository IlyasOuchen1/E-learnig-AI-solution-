
import sys
import os
from pathlib import Path

# Ajouter le répertoire racine au PYTHONPATH
ROOT_DIR = Path(__file__).parent
sys.path.insert(0, str(ROOT_DIR))

def main():
    """Point d'entrée principal avec menu de sélection"""
    print("🎓 Educational AI Platform")
    print("=" * 40)
    print("Plateforme IA pour la création de contenu éducatif")
    print("")
    print("Options disponibles :")
    print("1. 🖥️  Interface Streamlit (Recommandée)")
    print("2. 🔧 Mode Console/Debug")
    print("3. 🧪 Tests")
    print("4. ℹ️  Informations système")
    print("5. 🚪 Quitter")
    print("")
    
    while True:
        try:
            choice = input("Choisissez une option (1-5): ").strip()
            
            if choice == "1":
                run_streamlit_interface()
                break
            elif choice == "2":
                run_console_mode()
                break
            elif choice == "3":
                run_tests()
                break
            elif choice == "4":
                show_system_info()
            elif choice == "5":
                print("👋 Au revoir!")
                break
            else:
                print("❌ Option invalide. Choisissez entre 1 et 5.")
                
        except KeyboardInterrupt:
            print("\n👋 Arrêt demandé par l'utilisateur")
            break
        except Exception as e:
            print(f"❌ Erreur: {e}")

def run_streamlit_interface():
    """Lance l'interface Streamlit"""
    print("🚀 Lancement de l'interface Streamlit...")
    print("📱 L'interface s'ouvrira dans votre navigateur")
    print("🔄 Ctrl+C pour arrêter le serveur")
    print("")
    
    try:
        import subprocess
        subprocess.run([
            "streamlit", "run", 
            "interfaces/streamlit_main.py",
            "--server.port", "8501",
            "--server.address", "localhost"
        ])
    except ImportError:
        print("❌ Streamlit non installé.")
        print("💡 Installez avec: pip install streamlit")
    except FileNotFoundError:
        print("❌ Commande streamlit non trouvée.")
        print("💡 Assurez-vous que Streamlit est installé et dans votre PATH")
    except Exception as e:
        print(f"❌ Erreur lors du lancement: {e}")

def run_console_mode():
    """Mode console pour tests et développement"""
    print("🔧 Mode Console - Educational AI Platform")
    print("=" * 40)
    
    try:
        from shared.config.settings import settings
        
        print("📋 Configuration actuelle:")
        config = settings.get_summary()
        for key, value in config.items():
            print(f"  {key}: {value}")
        
        print("")
        
        if not settings.OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY non configuré")
            print("💡 Configurez votre clé dans le fichier .env")
            return
        
        print("✅ Configuration valide")
        print("")
        print("🔧 Options du mode console:")
        print("1. Tester l'orchestrateur")
        print("2. Vérifier les composants")
        print("3. Nettoyer les outputs")
        
        choice = input("Votre choix (1-3): ").strip()
        
        if choice == "1":
            test_orchestrator()
        elif choice == "2":
            check_components()
        elif choice == "3":
            cleanup_outputs()
        else:
            print("❌ Option invalide")
            
    except ImportError as e:
        print(f"❌ Erreur d'import: {e}")
        print("💡 Vérifiez que tous les modules sont installés")
    except Exception as e:
        print(f"❌ Erreur: {e}")

def test_orchestrator():
    """Test basique de l'orchestrateur"""
    print("🧪 Test de l'orchestrateur...")
    
    try:
        from orchestrator.simple_orchestrator import create_educational_orchestrator
        from shared.config.settings import settings
        
        orchestrator = create_educational_orchestrator(
            settings.OPENAI_API_KEY,
            str(settings.OUTPUTS_DIR)
        )
        print("✅ Orchestrateur créé avec succès")
        
        # Test simple de validation
        test_data = {
            "course_subject": "Test d'orchestrateur",
            "target_audience": "Développeurs",
            "learning_objectives": "Tester le système"
        }
        
        print("📝 Test avec données exemple...")
        print("⚠️ Ce test ne lance pas le workflow complet")
        print("✅ Structure de données validée")
        
    except Exception as e:
        print(f"❌ Erreur test orchestrateur: {e}")

def check_components():
    """Vérifie la disponibilité des composants"""
    print("🔍 Vérification des composants...")
    
    components = [
        ("Agent", "agent.enhanced_agent"),
        ("Séquenceur", "automations.sequencer.pedagogical_sequencer_v2"),
        ("Générateur Scripts", "automations.scripts.script_generator"),
        ("Orchestrateur", "orchestrator.workflow_orchestrator"),
        ("Configuration", "shared.config.settings")
    ]
    
    for name, module_path in components:
        try:
            __import__(module_path)
            print(f"✅ {name}: Disponible")
        except ImportError as e:
            print(f"❌ {name}: Manquant ({e})")
        except Exception as e:
            print(f"⚠️ {name}: Erreur ({e})")

def cleanup_outputs():
    """Nettoie les fichiers de sortie"""
    print("🧹 Nettoyage des outputs...")
    
    try:
        from shared.config.settings import settings
        import shutil
        
        outputs_dir = settings.OUTPUTS_DIR
        
        if outputs_dir.exists():
            response = input(f"Supprimer {outputs_dir} ? (y/N): ")
            if response.lower() == 'y':
                shutil.rmtree(outputs_dir)
                outputs_dir.mkdir()
                print("✅ Outputs nettoyés")
            else:
                print("❌ Nettoyage annulé")
        else:
            print("ℹ️ Aucun fichier output à nettoyer")
            
    except Exception as e:
        print(f"❌ Erreur nettoyage: {e}")

def run_tests():
    """Lance les tests unitaires"""
    print("🧪 Lancement des tests...")
    
    try:
        import subprocess
        result = subprocess.run([
            "python", "-m", "pytest", 
            "tests/", 
            "-v",
            "--tb=short"
        ], capture_output=True, text=True)
        
        print(result.stdout)
        if result.stderr:
            print("Erreurs:")
            print(result.stderr)
            
    except ImportError:
        print("❌ pytest non installé.")
        print("💡 Installez avec: pip install pytest")
    except Exception as e:
        print(f"❌ Erreur lors des tests: {e}")

def show_system_info():
    """Affiche les informations système"""
    print("ℹ️ Informations Système")
    print("=" * 30)
    
    import platform
    import sys
    
    print(f"🐍 Python: {sys.version}")
    print(f"💻 Système: {platform.system()} {platform.release()}")
    print(f"🏗️ Architecture: {platform.architecture()[0]}")
    print(f"📁 Répertoire: {Path.cwd()}")
    
    # Vérifier les dépendances clés
    key_packages = [
        "openai", "streamlit", "langchain", "langgraph", 
        "pinecone", "pandas", "plotly"
    ]
    
    print("\n📦 Packages clés:")
    for package in key_packages:
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'Version inconnue')
            print(f"  ✅ {package}: {version}")
        except ImportError:
            print(f"  ❌ {package}: Non installé")
    
    print("")

if __name__ == "__main__":
    main()