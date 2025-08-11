import json
import os
from datetime import datetime
from typing import Dict, Any
from pathlib import Path

def save_json_output(data: Dict[str, Any], filename: str, output_dir: str = None) -> str:
    """Sauvegarde un fichier JSON"""
    if output_dir is None:
        output_dir = "./outputs"
    
    try:
        os.makedirs(output_dir, exist_ok=True)
        filepath = Path(output_dir) / filename
        
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False, default=str)
        
        print(f"📁 JSON sauvegardé : {filepath}")
        return str(filepath)
        
    except Exception as e:
        print(f"⚠️ Erreur sauvegarde {filename}: {e}")
        return None

def load_json_file(filepath: str) -> Dict[str, Any]:
    """Charge un fichier JSON"""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"❌ Erreur chargement {filepath}: {e}")
        return {}

def get_session_directory(session_id: str, base_dir: str = "./outputs") -> str:
    """Crée et retourne le répertoire de session"""
    session_dir = Path(base_dir) / "sessions" / f"session_{session_id[:8]}"
    session_dir.mkdir(parents=True, exist_ok=True)
    return str(session_dir)