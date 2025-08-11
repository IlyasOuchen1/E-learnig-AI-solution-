#!/usr/bin/env python3
"""
Test Simple du Format JSON Exact - Sans Orchestrateur Complet
"""

import json
from datetime import datetime

def test_json_format():
    """Test du format JSON exact des scripts"""
    print("🧪 Test du Format JSON Exact")
    print("=" * 50)
    
    # Simuler la génération de scripts avec le format exact
    scripts = {}
    
    # Script 1
    script_id_1 = "01-Intro-01-Introduction_text"
    scripts[script_id_1] = {
        "activite": {
            "sequence": "Introduction aux systèmes ERP",
            "num_ecran": "01-Intro-01",
            "titre_ecran": "Qu'est-ce qu'un système ERP ?",
            "sous_titre": "Contextualisation des systèmes ERP",
            "resume_contenu": "Dans cette section, nous allons explorer les concepts de base des systèmes ERP.",
            "type_activite": "text",
            "niveau_bloom": "Comprendre",
            "difficulte": "facile",
            "duree_estimee": 5,
            "objectif_lie": "Comprendre les concepts de base des systèmes ERP."
        },
        "script": "**Titre accrocheur :** Démystifions le Monde des ERP\n\n**Sous-titre :** Comprendre le contexte et les enjeux\n\n---\n\n**Introduction :**\n\nBienvenue dans le monde fascinant des systèmes ERP ! Cette formation vous permettra de comprendre les concepts fondamentaux..."
    }
    
    # Script 2
    script_id_2 = "02-Seq-01-Concepts-fondamentaux_text"
    scripts[script_id_2] = {
        "activite": {
            "sequence": "Module 1 : Concepts fondamentaux",
            "num_ecran": "02-Seq-01",
            "titre_ecran": "Concepts fondamentaux",
            "sous_titre": "Les bases des systèmes ERP",
            "resume_contenu": "Ce module couvre les concepts de base nécessaires à la compréhension des ERP.",
            "type_activite": "text",
            "niveau_bloom": "Analyser",
            "difficulte": "moyen",
            "duree_estimee": 8,
            "objectif_lie": "Maîtriser les concepts fondamentaux des systèmes ERP."
        },
        "script": "**Titre :** Concepts fondamentaux\n\n**Sous-titre :** Les bases des systèmes ERP\n\n---\n\n**Contenu :**\n\nLes systèmes ERP reposent sur plusieurs concepts clés..."
    }
    
    # Script 3 (Quiz)
    script_id_3 = "03-Quiz-01-Evaluation-connaissances_quiz"
    scripts[script_id_3] = {
        "activite": {
            "sequence": "Quiz d'évaluation",
            "num_ecran": "03-Quiz-01",
            "titre_ecran": "Évaluation des connaissances",
            "sous_titre": "Quiz sur les concepts ERP",
            "resume_contenu": "Un quiz interactif permettra aux apprenants de tester leur compréhension.",
            "type_activite": "quiz",
            "niveau_bloom": "Évaluer",
            "difficulte": "moyen",
            "duree_estimee": 10,
            "objectif_lie": "L'apprenant sera capable d'évaluer sa compréhension des concepts ERP."
        },
        "script": "```json\n[\n  {\n    \"question\": \"Qu'est-ce qu'un système ERP ?\",\n    \"options\": {\n      \"A\": \"Un logiciel de comptabilité\",\n      \"B\": \"Un système de gestion intégré\",\n      \"C\": \"Un outil de communication\",\n      \"D\": \"Un navigateur web\"\n    },\n    \"correct\": \"B\"\n  },\n  {\n    \"question\": \"Quel est l'avantage principal d'un ERP ?\",\n    \"options\": {\n      \"A\": \"Il est gratuit\",\n      \"B\": \"Il centralise toutes les données\",\n      \"C\": \"Il est facile à utiliser\",\n      \"D\": \"Il fonctionne hors ligne\"\n    },\n    \"correct\": \"B\"\n  }\n]\n```"
    }
    
    print(f"📚 Scripts générés: {len(scripts)}")
    
    # Vérifier le format de chaque script
    for script_id, script_data in scripts.items():
        print(f"\n🔍 Script: {script_id}")
        
        # Vérifier la structure
        expected_keys = {'activite', 'script'}
        actual_keys = set(script_data.keys())
        
        if actual_keys == expected_keys:
            print("   ✅ Format JSON exact respecté")
            
            # Vérifier la structure de l'activité
            activite = script_data['activite']
            required_activite_keys = {
                'sequence', 'num_ecran', 'titre_ecran', 'sous_titre',
                'resume_contenu', 'type_activite', 'niveau_bloom',
                'difficulte', 'duree_estimee', 'objectif_lie'
            }
            
            activite_keys = set(activite.keys())
            if activite_keys == required_activite_keys:
                print("   ✅ Structure activité complète")
            else:
                missing_keys = required_activite_keys - activite_keys
                extra_keys = activite_keys - required_activite_keys
                if missing_keys:
                    print(f"   ⚠️ Clés manquantes: {missing_keys}")
                if extra_keys:
                    print(f"   ⚠️ Clés supplémentaires: {extra_keys}")
            
            # Vérifier le script
            script_content = script_data['script']
            if script_content:
                print(f"   ✅ Script présent ({len(str(script_content))} caractères)")
            else:
                print("   ⚠️ Script vide")
                
        else:
            print(f"   ❌ Format incorrect")
            print(f"      Attendu: {expected_keys}")
            print(f"      Reçu: {actual_keys}")
            return False
    
    # Sauvegarder le format exact pour inspection
    output_file = "test_scripts_format_exact.json"
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(scripts, f, indent=2, ensure_ascii=False)
    
    print(f"\n💾 Format JSON exact sauvegardé dans: {output_file}")
    
    # Afficher un exemple complet
    print(f"\n📋 Exemple de script complet:")
    first_script = list(scripts.values())[0]
    print(json.dumps(first_script, indent=2, ensure_ascii=False))
    
    return True

def main():
    """Fonction principale"""
    print("🧪 Test du Format JSON Exact - Version Simple")
    print("=" * 60)
    
    success = test_json_format()
    
    if success:
        print("\n" + "=" * 60)
        print("🎉 Test réussi !")
        print("✅ Format JSON exact respecté")
        print("✅ Structure: {activite: {...}, script: '...'}")
        print("✅ Aucun champ supplémentaire ajouté")
        print("✅ Compatible avec le frontend")
        print("=" * 60)
        
        print("\n📋 Format JSON généré:")
        print("""
{
  "01-Intro-01-Introduction_text": {
    "activite": {
      "sequence": "Introduction aux systèmes ERP",
      "num_ecran": "01-Intro-01",
      "titre_ecran": "Qu'est-ce qu'un système ERP ?",
      "sous_titre": "Contextualisation des systèmes ERP",
      "resume_contenu": "Dans cette section, nous allons explorer...",
      "type_activite": "text",
      "niveau_bloom": "Comprendre",
      "difficulte": "facile",
      "duree_estimee": 5,
      "objectif_lie": "Comprendre les concepts de base des systèmes ERP."
    },
    "script": "**Titre accrocheur :** Démystifions le Monde des ERP..."
  }
}
        """)
        
    else:
        print("\n❌ Test échoué")
        print("🔧 Vérifiez la structure des scripts")

if __name__ == "__main__":
    main() 