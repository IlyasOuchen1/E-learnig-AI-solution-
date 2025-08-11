#!/usr/bin/env python3
"""
API Server FastAPI avec SQLite pour l'Intégration Frontend
Expose le contenu de la base SQLite avec le format JSON exact
"""

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from typing import List, Dict, Any, Optional
import sqlite3
import json
from datetime import datetime
from pathlib import Path
import os

# Initialisation FastAPI
app = FastAPI(
    title="Educational AI API - SQLite",
    description="API pour l'intégration frontend avec base de données SQLite et format JSON exact",
    version="1.0.0"
)

# Configuration CORS pour frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174", 
        "http://localhost:5175",
        "http://localhost:5176",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:5174",
        "http://127.0.0.1:5175", 
        "http://127.0.0.1:5176",
        "http://10.110.3.155:5176",
        "*"  # Temporaire pour les tests
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configuration de la base de données
DB_PATH = "educational_platform.db"

def get_db_connection():
    """Crée une connexion à la base SQLite"""
    try:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = sqlite3.Row
        return conn
    except Exception as e:
        print(f"❌ Erreur connexion base de données: {e}")
        return None

def check_database():
    """Vérifie que la base de données existe et est accessible"""
    if not os.path.exists(DB_PATH):
        return False, f"Base de données non trouvée: {DB_PATH}"
    
    conn = get_db_connection()
    if not conn:
        return False, "Impossible de se connecter à la base de données"
    
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        conn.close()
        
        if not tables:
            return False, "Aucune table trouvée dans la base de données"
        
        return True, f"Base de données accessible avec {len(tables)} tables"
        
    except Exception as e:
        conn.close()
        return False, f"Erreur vérification base: {e}"

# ===========================================
# ENDPOINTS PRINCIPAUX
# ===========================================

@app.get("/")
async def root():
    """Endpoint racine avec informations API"""
    db_status, db_message = check_database()
    
    return {
        "message": "Educational AI API avec SQLite",
        "version": "1.0.0",
        "database": "SQLite",
        "database_status": "✅" if db_status else "❌",
        "database_message": db_message,
        "endpoints": {
            "sessions": "/api/sessions",
            "content": "/api/sessions/{session_id}/content",
            "content_simple": "/api/sessions/{session_id}/content/simple",
            "statistics": "/api/statistics",
            "health": "/health"
        }
    }

@app.get("/health")
async def health_check():
    """Vérification de santé de l'API et SQLite"""
    db_status, db_message = check_database()
    
    if db_status:
        # Compter les sessions
        conn = get_db_connection()
        if conn:
            try:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM workflow_sessions")
                session_count = cursor.fetchone()[0]
                conn.close()
                
                return {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "database": {
                        "type": "SQLite",
                        "path": DB_PATH,
                        "status": "accessible",
                        "sessions_count": session_count
                    }
                }
            except Exception as e:
                conn.close()
                return {
                    "status": "healthy",
                    "timestamp": datetime.now().isoformat(),
                    "database": {
                        "type": "SQLite",
                        "path": DB_PATH,
                        "status": "accessible",
                        "error": str(e)
                    }
                }
    
    return {
        "status": "unhealthy",
        "timestamp": datetime.now().isoformat(),
        "database": {
            "type": "SQLite",
            "path": DB_PATH,
            "status": "inaccessible",
            "error": db_message
        }
    }

# ===========================================
# ENDPOINTS SESSIONS
# ===========================================

@app.get("/api/sessions")
async def get_sessions(limit: int = Query(10, ge=1, le=100)):
    """Récupère les sessions de workflow (sans le contenu pour optimiser)"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erreur connexion base de données")
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT session_id, user_input, status, start_time, end_time, duration_seconds
            FROM workflow_sessions 
            ORDER BY start_time DESC 
            LIMIT ?
        """, (limit,))
        
        sessions = []
        for row in cursor.fetchall():
            session = dict(row)
            # Parser le JSON user_input
            if session['user_input']:
                try:
                    session['user_input'] = json.loads(session['user_input'])
                except:
                    session['user_input'] = {}
            
            # Ajouter un titre basé sur user_input
            if session['user_input'] and 'course_subject' in session['user_input']:
                session['title'] = f"Session {session['user_input']['course_subject']}"
            else:
                session['title'] = f"Session {session['session_id'][:8]}..."
            
            sessions.append(session)
        
        conn.close()
        return sessions
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erreur récupération sessions: {str(e)}")

@app.get("/api/sessions/{session_id}")
async def get_session(session_id: str):
    """Récupère une session spécifique (sans le contenu)"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erreur connexion base de données")
    
    try:
        cursor = conn.cursor()
        cursor.execute("""
            SELECT session_id, user_input, status, start_time, end_time, duration_seconds
            FROM workflow_sessions 
            WHERE session_id = ?
        """, (session_id,))
        
        row = cursor.fetchone()
        if not row:
            conn.close()
            raise HTTPException(status_code=404, detail="Session non trouvée")
        
        session = dict(row)
        # Parser le JSON user_input
        if session['user_input']:
            try:
                session['user_input'] = json.loads(session['user_input'])
            except:
                session['user_input'] = {}
        
        # Ajouter un titre
        if session['user_input'] and 'course_subject' in session['user_input']:
            session['title'] = f"Session {session['user_input']['course_subject']}"
        else:
            session['title'] = f"Session {session['session_id'][:8]}..."
        
        conn.close()
        return session
        
    except HTTPException:
        raise
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erreur récupération session: {str(e)}")

# ===========================================
# ENDPOINTS DE CONTENU E-LEARNING
# ===========================================

@app.get("/api/sessions/{session_id}/content")
async def get_session_content(session_id: str):
    """
    Récupère le contenu JSON complet d'une session spécifique
    Format: {activity_id: {"activite": {...}, "script": {...}}}
    """
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erreur connexion base de données")
    
    try:
        cursor = conn.cursor()
        
        # Vérifier que la session existe
        cursor.execute("SELECT status FROM workflow_sessions WHERE session_id = ?", (session_id,))
        session_row = cursor.fetchone()
        if not session_row:
            conn.close()
            raise HTTPException(status_code=404, detail="Session non trouvée")
        
        # Récupérer les activités du séquenceur
        cursor.execute("""
            SELECT sequence_name, num_ecran, titre_ecran, sous_titre, resume_contenu,
                   type_activite, niveau_bloom, difficulte, duree_estimee, objectif_lie
            FROM sequencer_activities 
            WHERE session_id = ? 
            ORDER BY num_ecran
        """, (session_id,))
        
        activities = cursor.fetchall()
        if not activities:
            conn.close()
            raise HTTPException(status_code=404, detail="Aucune activité trouvée pour cette session")
        
        # Récupérer les scripts générés
        cursor.execute("""
            SELECT script_type, activity_data, script_content
            FROM generated_scripts 
            WHERE session_id = ?
        """, (session_id,))
        
        scripts = cursor.fetchall()
        conn.close()
        
        # Construire le contenu au format JSON exact
        content = {}
        for activity in activities:
            # Créer l'ID de l'activité
            activity_id = f"{activity['num_ecran']}-{activity['titre_ecran'].replace(' ', '-')}_{activity['type_activite']}"
            
            # Construire l'objet activité
            activite = {
                "sequence": activity['sequence_name'],
                "num_ecran": activity['num_ecran'],
                "titre_ecran": activity['titre_ecran'],
                "sous_titre": activity['sous_titre'] or "",
                "resume_contenu": activity['resume_contenu'] or "",
                "type_activite": activity['type_activite'],
                "niveau_bloom": activity['niveau_bloom'],
                "difficulte": activity['difficulte'],
                "duree_estimee": activity['duree_estimee'],
                "objectif_lie": activity['objectif_lie'] or ""
            }
            
            # Trouver le script correspondant
            script_content = ""
            for script in scripts:
                if script['script_type'] == activity['type_activite']:
                    try:
                        script_data = json.loads(script['script_content'])
                        script_content = script_data
                        break
                    except:
                        script_content = script['script_content']
                        break
            
            # Construire l'entrée finale au format exact
            content[activity_id] = {
                "activite": activite,
                "script": script_content
            }
        
        return {
            "session_id": session_id,
            "session_status": session_row['status'],
            "content": content,
            "metadata": {
                "total_activities": len(content),
                "generated_at": datetime.now().isoformat()
            }
        }
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération contenu: {str(e)}")

@app.get("/api/sessions/{session_id}/content/simple")
async def get_session_content_simple(session_id: str):
    """
    Récupère le contenu JSON simple d'une session (format frontend)
    Retourne directement le contenu au format exact
    """
    try:
        full_content = await get_session_content(session_id)
        # Retourner seulement la partie content pour le frontend
        return full_content["content"]
        
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erreur récupération contenu simple: {str(e)}")

# ===========================================
# ENDPOINTS DE STATISTIQUES
# ===========================================

@app.get("/api/statistics")
async def get_statistics():
    """Récupère les statistiques globales"""
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Erreur connexion base de données")
    
    try:
        cursor = conn.cursor()
        
        # Statistiques des sessions
        cursor.execute("SELECT COUNT(*) FROM workflow_sessions")
        total_sessions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM workflow_sessions WHERE status = 'completed'")
        completed_sessions = cursor.fetchone()[0]
        
        cursor.execute("SELECT COUNT(*) FROM workflow_sessions WHERE status = 'failed'")
        failed_sessions = cursor.fetchone()[0]
        
        # Calculer la durée moyenne
        cursor.execute("""
            SELECT AVG(duration_seconds) 
            FROM workflow_sessions 
            WHERE duration_seconds IS NOT NULL
        """)
        avg_duration_result = cursor.fetchone()
        avg_duration = avg_duration_result[0] if avg_duration_result[0] else 0
        
        # Compter les activités par type
        cursor.execute("""
            SELECT type_activite, COUNT(*) 
            FROM sequencer_activities 
            GROUP BY type_activite
        """)
        activity_types_result = cursor.fetchall()
        activity_types = {row[0]: row[1] for row in activity_types_result}
        
        # Compter le total des activités
        cursor.execute("SELECT COUNT(*) FROM sequencer_activities")
        total_activities = cursor.fetchone()[0]
        
        conn.close()
        
        return {
            "sessions": {
                "total": total_sessions,
                "completed": completed_sessions,
                "failed": failed_sessions,
                "avg_duration_seconds": avg_duration
            },
            "activities": {
                "total": total_activities,
                "sessions_with_activities": total_sessions
            },
            "distributions": {
                "activity_types": activity_types
            }
        }
        
    except Exception as e:
        conn.close()
        raise HTTPException(status_code=500, detail=f"Erreur récupération statistiques: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    print("🚀 Démarrage de l'API FastAPI avec SQLite...")
    print(f"🗄️ Base de données: SQLite ({DB_PATH})")
    print(f"🌐 URL: http://localhost:8000")
    print(f"📚 Documentation: http://localhost:8000/docs")
    print(f"🔍 Health Check: http://localhost:8000/health")
    
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True) 