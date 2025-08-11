import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.exc import SQLAlchemyError
from typing import Dict, Any, List, Optional
import json
from datetime import datetime, timedelta
import os

try:
    from .models import Base, WorkflowSession, AgentAnalysis, SequencerData, ScriptData, WorkflowStats
except ImportError:
    from database.models import Base, WorkflowSession, AgentAnalysis, SequencerData, ScriptData, WorkflowStats

class DatabaseManager:
    """Gestionnaire principal pour les opérations SQLite"""
    
    def __init__(self, db_path: str = "educational_platform.db"):
        """
        Initialise le gestionnaire de base de données
        
        Args:
            db_path: Chemin vers le fichier SQLite
        """
        self.db_path = db_path
        self.engine = create_engine(f'sqlite:///{db_path}', echo=False)
        self.SessionLocal = scoped_session(sessionmaker(bind=self.engine))
        
        # Créer les tables si elles n'existent pas
        self.create_tables()
        
        print(f"🗄️ Base de données SQLite initialisée : {db_path}")
    
    def create_tables(self):
        """Crée toutes les tables dans la base"""
        try:
            Base.metadata.create_all(bind=self.engine)
            print("✅ Tables créées avec succès")
        except Exception as e:
            print(f"❌ Erreur création tables : {e}")
    
    def get_session(self):
        """Retourne une session de base de données"""
        return self.SessionLocal()
    
    def close_session(self, session):
        """Ferme une session"""
        try:
            session.close()
        except:
            pass
    
    # ===========================================
    # WORKFLOW SESSIONS
    # ===========================================
    
    def create_workflow_session(self, session_id: str, user_input: Dict[str, Any]) -> bool:
        """Crée une nouvelle session de workflow"""
        session = self.get_session()
        try:
            workflow_session = WorkflowSession(
                session_id=session_id,
                user_input=user_input,
                status='in_progress'
            )
            session.add(workflow_session)
            session.commit()
            print(f"✅ Session créée : {session_id[:8]}")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur création session : {e}")
            return False
        finally:
            self.close_session(session)
    
    def update_workflow_session(self, session_id: str, **kwargs) -> bool:
        """Met à jour une session de workflow"""
        session = self.get_session()
        try:
            workflow_session = session.query(WorkflowSession).filter_by(session_id=session_id).first()
            
            if workflow_session:
                for key, value in kwargs.items():
                    if hasattr(workflow_session, key):
                        setattr(workflow_session, key, value)
                
                session.commit()
                print(f"✅ Session mise à jour : {session_id[:8]}")
                return True
            else:
                print(f"⚠️ Session non trouvée : {session_id[:8]}")
                return False
                
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur mise à jour session : {e}")
            return False
        finally:
            self.close_session(session)
    
    # ===========================================
    # AGENT ANALYSIS
    # ===========================================
    
    def save_agent_analysis(self, session_id: str, analysis_data: Dict[str, Any]) -> bool:
        """Sauvegarde les résultats de l'agent"""
        session = self.get_session()
        try:
            agent_analysis = AgentAnalysis(
                session_id=session_id,
                objectives=analysis_data.get('objectives', []),
                content_analysis=analysis_data.get('content_analysis', {}),
                classification=analysis_data.get('classification', {}),
                formatted_objectives=analysis_data.get('formatted_objectives', {}),
                difficulty_evaluation=analysis_data.get('difficulty_evaluation', {}),
                recommendations=analysis_data.get('recommendations', {}),
                feedback=analysis_data.get('feedback', {}),
                statistics=analysis_data.get('stats', {})
            )
            session.add(agent_analysis)
            session.commit()
            print(f"✅ Analyse agent sauvegardée : {session_id[:8]}")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur sauvegarde agent : {e}")
            return False
        finally:
            self.close_session(session)
    
    # ===========================================
    # SEQUENCER DATA
    # ===========================================
    
    def save_sequencer_data(self, session_id: str, sequencer_activities: List[Dict[str, Any]]) -> bool:
        """Sauvegarde les activités du séquenceur"""
        session = self.get_session()
        try:
            for activity in sequencer_activities:
                sequencer_item = SequencerData(
                    session_id=session_id,
                    sequence_name=activity.get('sequence', ''),
                    num_ecran=activity.get('num_ecran', ''),
                    titre_ecran=activity.get('titre_ecran', ''),
                    sous_titre=activity.get('sous_titre', ''),
                    resume_contenu=activity.get('resume_contenu', ''),
                    type_activite=activity.get('type_activite', ''),
                    niveau_bloom=activity.get('niveau_bloom', ''),
                    difficulte=activity.get('difficulte', ''),
                    duree_estimee=activity.get('duree_estimee', 0),
                    objectif_lie=activity.get('objectif_lie', ''),
                    commentaire=activity.get('commentaire', '')
                )
                session.add(sequencer_item)
            
            session.commit()
            print(f"✅ Séquenceur sauvegardé : {len(sequencer_activities)} activités")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur sauvegarde séquenceur : {e}")
            return False
        finally:
            self.close_session(session)
    
    # ===========================================
    # SCRIPTS DATA
    # ===========================================
    
    def save_scripts_data(self, session_id: str, scripts_data: Dict[str, Any]) -> bool:
        """Sauvegarde les scripts générés"""
        session = self.get_session()
        try:
            for script_id, script_info in scripts_data.items():
                script_item = ScriptData(
                    session_id=session_id,
                    script_id=script_id,
                    activity_data=script_info.get('activite', {}),
                    script_content=script_info.get('script', ''),
                    script_type=script_info.get('activite', {}).get('type_activite', '')
                )
                session.add(script_item)
            
            session.commit()
            print(f"✅ Scripts sauvegardés : {len(scripts_data)} scripts")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur sauvegarde scripts : {e}")
            return False
        finally:
            self.close_session(session)
    
    # ===========================================
    # STATISTICS
    # ===========================================
    
    def save_workflow_statistics(self, session_id: str, stats: Dict[str, Any]) -> bool:
        """Sauvegarde les statistiques du workflow"""
        session = self.get_session()
        try:
            workflow_stats = WorkflowStats(
                session_id=session_id,
                total_objectives=stats.get('objectives_analyzed', 0),
                total_activities=stats.get('activities_generated', 0),
                total_scripts=stats.get('scripts_generated', 0),
                total_documents_processed=stats.get('processed_documents', 0),
                bloom_distribution=stats.get('bloom_distribution', {}),
                difficulty_distribution=stats.get('difficulty_distribution', {}),
                activity_types_distribution=stats.get('activity_types_distribution', {})
            )
            session.add(workflow_stats)
            session.commit()
            print(f"✅ Statistiques sauvegardées : {session_id[:8]}")
            return True
            
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur sauvegarde statistiques : {e}")
            return False
        finally:
            self.close_session(session)
    
    # ===========================================
    # QUERIES / RÉCUPÉRATION
    # ===========================================
    
    def get_workflow_session(self, session_id: str) -> Optional[Dict]:
        """Récupère une session complète"""
        session = self.get_session()
        try:
            workflow = session.query(WorkflowSession).filter_by(session_id=session_id).first()
            
            if workflow:
                return {
                    'session_id': workflow.session_id,
                    'user_input': workflow.user_input,
                    'status': workflow.status,
                    'start_time': workflow.start_time.isoformat() if workflow.start_time else None,
                    'end_time': workflow.end_time.isoformat() if workflow.end_time else None,
                    'duration_seconds': workflow.duration_seconds,
                    'execution_log': workflow.execution_log,
                    'error_message': workflow.error_message
                }
            return None
            
        except Exception as e:
            print(f"❌ Erreur récupération session : {e}")
            return None
        finally:
            self.close_session(session)
    
    def get_recent_sessions(self, limit: int = 10) -> List[Dict]:
        """Récupère les sessions récentes"""
        session = self.get_session()
        try:
            sessions = session.query(WorkflowSession)\
                           .order_by(WorkflowSession.created_at.desc())\
                           .limit(limit)\
                           .all()
            
            return [{
                'session_id': s.session_id,
                'status': s.status,
                'start_time': s.start_time.isoformat() if s.start_time else None,
                'created_at': s.created_at.isoformat() if s.created_at else None
            } for s in sessions]
            
        except Exception as e:
            print(f"❌ Erreur récupération sessions : {e}")
            return []
        finally:
            self.close_session(session)
    
    def get_workflow_statistics_summary(self) -> Dict:
        """Récupère un résumé des statistiques globales"""
        session = self.get_session()
        try:
            total_sessions = session.query(WorkflowSession).count()
            completed_sessions = session.query(WorkflowSession).filter_by(status='completed').count()
            failed_sessions = session.query(WorkflowSession).filter_by(status='failed').count()
            
            return {
                'total_sessions': total_sessions,
                'completed_sessions': completed_sessions,
                'failed_sessions': failed_sessions,
                'success_rate': (completed_sessions / total_sessions * 100) if total_sessions > 0 else 0
            }
            
        except Exception as e:
            print(f"❌ Erreur statistiques : {e}")
            return {}
        finally:
            self.close_session(session)
    
    # ===========================================
    # MAINTENANCE
    # ===========================================
    
    def cleanup_old_sessions(self, days: int = 30) -> int:
        """Supprime les sessions plus anciennes que X jours"""
        session = self.get_session()
        try:
            cutoff_date = datetime.now() - timedelta(days=days)
            
            old_sessions = session.query(WorkflowSession)\
                                .filter(WorkflowSession.created_at < cutoff_date)\
                                .all()
            
            count = len(old_sessions)
            
            for old_session in old_sessions:
                session.delete(old_session)
            
            session.commit()
            print(f"🧹 {count} anciennes sessions supprimées")
            return count
            
        except Exception as e:
            session.rollback()
            print(f"❌ Erreur nettoyage : {e}")
            return 0
        finally:
            self.close_session(session)
    
    def get_database_info(self) -> Dict:
        """Informations sur la base de données"""
        return {
            'database_path': self.db_path,
            'database_size': os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0,
            'tables': ['workflow_sessions', 'agent_analyses', 'sequencer_activities', 'generated_scripts', 'workflow_statistics']
        }