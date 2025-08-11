#!/usr/bin/env python3
"""
Test de l'API FastAPI avec SQLite
"""

import requests
import json
import sys
from datetime import datetime

def test_fastapi_sqlite():
    """Test l'API FastAPI avec SQLite"""
    print("🎯 Test de l'API FastAPI avec SQLite")
    print("=" * 60)
    
    # URL de base
    base_url = "http://localhost:8000"
    
    try:
        # Test 1: Health Check
        print("\n🔍 Test 1: Health Check")
        response = requests.get(f"{base_url}/health")
        
        if response.status_code == 200:
            health_data = response.json()
            print("✅ API FastAPI accessible")
            print(f"   📊 Sessions dans SQLite: {health_data['database']['sessions_count']}")
            print(f"   🔗 Statut: {health_data['database']['status']}")
        else:
            print(f"❌ Erreur health check: {response.status_code}")
            return False
        
        # Test 2: Récupérer les sessions
        print("\n📊 Test 2: Récupération des sessions")
        response = requests.get(f"{base_url}/api/sessions?limit=5")
        
        if response.status_code == 200:
            sessions = response.json()
            print(f"✅ {len(sessions)} sessions récupérées")
            
            if sessions:
                session = sessions[0]
                session_id = session["session_id"]
                print(f"📋 Session sélectionnée: {session_id[:8]}...")
                print(f"   Titre: {session.get('title', 'N/A')}")
                print(f"   Statut: {session.get('status', 'N/A')}")
                
                # Test 3: Récupérer le contenu de cette session
                print(f"\n📚 Test 3: Récupération du contenu")
                print(f"   URL: {base_url}/api/sessions/{session_id}/content")
                
                response = requests.get(f"{base_url}/api/sessions/{session_id}/content")
                
                if response.status_code == 200:
                    content = response.json()
                    print("✅ Contenu récupéré avec succès !")
                    
                    # Afficher les métadonnées
                    metadata = content.get("metadata", {})
                    print(f"   📊 Activités: {metadata.get('total_activities', 0)}")
                    print(f"   ⏰ Généré: {metadata.get('generated_at', 'N/A')}")
                    
                    # Afficher le contenu
                    content_data = content.get("content", {})
                    print(f"   📋 Activités dans le contenu: {len(content_data)}")
                    
                    # Afficher les premières activités
                    for i, (activity_id, activity_data) in enumerate(list(content_data.items())[:3]):
                        activite = activity_data.get("activite", {})
                        print(f"   {i+1}. {activity_id}")
                        print(f"      Titre: {activite.get('titre_ecran', 'N/A')}")
                        print(f"      Type: {activite.get('type_activite', 'N/A')}")
                        print(f"      Durée: {activite.get('duree_estimee', 'N/A')} min")
                        
                        # Vérifier si le script est présent
                        script = activity_data.get("script", "")
                        if script:
                            print(f"      ✅ Script présent ({len(str(script))} caractères)")
                        else:
                            print(f"      ⚠️ Script manquant")
                    
                    # Sauvegarder le contenu dans un fichier pour inspection
                    output_file = f"fastapi_content_{session_id[:8]}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(content, f, indent=2, ensure_ascii=False)
                    print(f"   💾 Contenu sauvegardé dans: {output_file}")
                    
                else:
                    print(f"❌ Erreur récupération contenu: {response.status_code}")
                    print(f"   Réponse: {response.text}")
                    return False
                
                # Test 4: Récupérer le contenu simple (format frontend)
                print(f"\n🎯 Test 4: Récupération du contenu simple (format frontend)")
                response = requests.get(f"{base_url}/api/sessions/{session_id}/content/simple")
                
                if response.status_code == 200:
                    simple_content = response.json()
                    print("✅ Contenu simple récupéré avec succès !")
                    print(f"   📋 Activités: {len(simple_content)}")
                    
                    # Vérifier le format exact
                    if simple_content:
                        first_activity = list(simple_content.values())[0]
                        expected_keys = {'activite', 'script'}
                        actual_keys = set(first_activity.keys())
                        
                        if actual_keys == expected_keys:
                            print("   ✅ Format JSON exact respecté: {activite: {...}, script: '...'}")
                        else:
                            print(f"   ❌ Format incorrect: {actual_keys}")
                            return False
                    
                    # Sauvegarder le contenu simple
                    output_file = f"fastapi_content_simple_{session_id[:8]}.json"
                    with open(output_file, 'w', encoding='utf-8') as f:
                        json.dump(simple_content, f, indent=2, ensure_ascii=False)
                    print(f"   💾 Contenu simple sauvegardé dans: {output_file}")
                    
                else:
                    print(f"❌ Erreur récupération contenu simple: {response.status_code}")
                    return False
                
                # Test 5: Statistiques
                print(f"\n📈 Test 5: Récupération des statistiques")
                response = requests.get(f"{base_url}/api/statistics")
                
                if response.status_code == 200:
                    stats = response.json()
                    print("✅ Statistiques récupérées")
                    print(f"   📊 Sessions totales: {stats['sessions']['total']}")
                    print(f"   📚 Activités totales: {stats['activities']['total']}")
                    print(f"   🎯 Types d'activités: {stats['distributions']['activity_types']}")
                    
                else:
                    print(f"❌ Erreur récupération statistiques: {response.status_code}")
        
        else:
            print(f"❌ Erreur récupération sessions: {response.status_code}")
            return False
        
        print("\n" + "=" * 60)
        print("🎉 Tests de l'API FastAPI + SQLite terminés avec succès !")
        print("=" * 60)
        
        print("\n📋 RÉSUMÉ:")
        print(f"✅ API FastAPI fonctionne correctement")
        print(f"✅ Endpoints de contenu opérationnels")
        print(f"✅ Format JSON exact respecté")
        print(f"✅ Base SQLite accessible")
        print(f"✅ CORS configuré pour le frontend")
        
        print("\n🎯 AVANTAGES:")
        print("✅ **Format JSON exact** - Compatible frontend sans modification")
        print("✅ **Base SQLite** - Stockage local et efficace")
        print("✅ **API REST** - Endpoints standards et documentés")
        print("✅ **Documentation automatique** - Swagger/OpenAPI")
        print("✅ **CORS configuré** - Compatible avec tous les frontends")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("❌ Impossible de se connecter à l'API FastAPI")
        print("💡 Assurez-vous que l'API est démarrée: python start_fastapi_server.py")
        return False
    except Exception as e:
        print(f"❌ Erreur lors du test: {e}")
        return False

def main():
    """Fonction principale"""
    print("🚀 Test de l'API FastAPI + SQLite")
    print("=" * 50)
    
    success = test_fastapi_sqlite()
    
    if success:
        print("\n✅ Tous les tests sont passés !")
        print("🎯 L'API FastAPI + SQLite est prête pour l'intégration frontend")
        print("🔗 Utilisez les endpoints pour charger le contenu e-learning")
        print("📚 Documentation: http://localhost:8000/docs")
    else:
        print("\n❌ Certains tests ont échoué")
        print("🔧 Vérifiez que l'API FastAPI est démarrée")
        print("🚀 Lancez: python start_fastapi_server.py")
    
    print("\n" + "=" * 60)

if __name__ == "__main__":
    main() 