import json
import asyncio
import uuid
import os
from typing import Dict, Any, List, Optional
from dataclasses import dataclass
from enum import Enum
from datetime import datetime
import sys
from pathlib import Path
try:
    from database.database_manager import DatabaseManager
except ImportError:
    # Fallback si le module database n'est pas disponible
    class DatabaseManager:
        def __init__(self, db_path: str = "educational_platform.db"):
            print(f"⚠️ DatabaseManager non disponible, mode local uniquement")
        
        def create_workflow_session(self, session_id: str, user_input: dict) -> bool:
            return True
        
        def save_agent_analysis(self, session_id: str, analysis_data: dict) -> bool:
            return True
        
        def save_sequencer_data(self, session_id: str, sequencer_activities: list) -> bool:
            return True
        
        def save_scripts_data(self, session_id: str, scripts_data: dict) -> bool:
            return True
        
        def update_workflow_session(self, session_id: str, **kwargs) -> bool:
            return True

# Ajouter les chemins pour importer les composants
sys.path.append(str(Path(__file__).parent.parent / "agent"))
sys.path.append(str(Path(__file__).parent.parent / "automations"))
sys.path.append(str(Path(__file__).parent.parent))  # Ajouter le répertoire racine

class WorkflowStatus(Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"

@dataclass
class SimpleWorkflowState:
    """État du workflow simplifié"""
    user_input: Dict[str, Any]
    session_id: str
    agent_analysis: Optional[Dict[str, Any]] = None
    sequencer_data: Optional[List[Dict[str, Any]]] = None
    scripts_data: Optional[Dict[str, Any]] = None
    current_step: int = 0
    status: WorkflowStatus = WorkflowStatus.PENDING
    error_message: Optional[str] = None
    execution_log: List[str] = None
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    
    def __post_init__(self):
        if self.execution_log is None:
            self.execution_log = []
        if self.start_time is None:
            self.start_time = datetime.now()

class SimpleEducationalOrchestrator:
    """Orchestrateur simplifié pour l'IA éducative"""
    
    def __init__(self, openai_api_key: str, output_directory: str = "./outputs", db_path: str = "educational_platform.db"):
        self.openai_api_key = openai_api_key
        self.output_directory = output_directory
        os.makedirs(output_directory, exist_ok=True)
        
        # 🗄️ INITIALISER LA BASE DE DONNÉES
        self.db_manager = DatabaseManager(db_path)
        
        # Composants
        self.agent = None
        self.sequencer = None
        self.script_generator = None
        
        print("🚀 Orchestrateur avec base de données initialisé")
    
    async def initialize_components(self, state: SimpleWorkflowState) -> SimpleWorkflowState:
        """Initialise les composants"""
        try:
            state.execution_log.append("🔧 Initialisation des composants...")
            state.current_step = 1
            
            # Initialiser l'agent
            from enhanced_agent import EnhancedLearningObjectiveAgent
            self.agent = EnhancedLearningObjectiveAgent(
                api_key=self.openai_api_key,
                model="gpt-4o-mini",
                temperature=0.2,
                verbose=True
            )
            
            # Initialiser le séquenceur
            from sequencer.pedagogical_sequencer_v2 import PedagogicalSequencerV2
            self.sequencer = PedagogicalSequencerV2(api_key=self.openai_api_key)
            
            # Initialiser le générateur de scripts
            from scripts.script_generator import ScriptGenerator
            self.script_generator = ScriptGenerator(api_key=self.openai_api_key)
            
            state.execution_log.append("✅ Tous les composants initialisés")
            
        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error_message = f"Erreur d'initialisation : {str(e)}"
            state.execution_log.append(f"❌ Erreur : {e}")
        
        return state
    
    async def run_agent_analysis(self, state: SimpleWorkflowState) -> SimpleWorkflowState:
        """Exécute l'analyse avec l'agent"""
        try:
            state.execution_log.append("🤖 Analyse des objectifs...")
            state.current_step = 2
            
            # Préparation du contenu
            content_parts = ["# INFORMATIONS SUR LE COURS\n"]
            content_parts.append(f"## Sujet Principal\n{state.user_input['course_subject']}\n")
            
            if state.user_input.get("target_audience"):
                content_parts.append(f"## Public Cible\n{state.user_input['target_audience']}\n")
            
            if state.user_input.get("learning_objectives"):
                content_parts.append(f"## Objectifs Existants\n{state.user_input['learning_objectives']}\n")
            
            if state.user_input.get("source_text"):
                content_parts.append(f"## Contenu Supplémentaire\n{state.user_input['source_text']}\n")
            
            content = "\n".join(content_parts)
            
            # Exécution de l'analyse
            analysis_results = self.agent.process_content_with_documents(content)
            state.agent_analysis = analysis_results
            
            # Sauvegarde
            await self.save_json_output(
                analysis_results, 
                f"agent_analysis_{state.session_id[:8]}.json"
            )
            
            state.execution_log.append("✅ Analyse terminée")
            
        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error_message = f"Erreur d'analyse : {str(e)}"
            state.execution_log.append(f"❌ Erreur : {e}")
        
        return state
    
    async def generate_sequencer(self, state: SimpleWorkflowState) -> SimpleWorkflowState:
        """Génère le séquenceur"""
        try:
            state.execution_log.append("📚 Génération du séquenceur...")
            state.current_step = 3
            
            if not state.agent_analysis:
                raise ValueError("Résultats d'analyse manquants")
            
            sequencer_data = self.sequencer.generate_sequencer(state.agent_analysis)
            
            if not sequencer_data:
                raise ValueError("Échec de la génération du séquenceur")
            
            state.sequencer_data = sequencer_data
            
            await self.save_json_output(
                sequencer_data,
                f"sequencer_{state.session_id[:8]}.json"
            )
            
            state.execution_log.append(f"✅ Séquenceur généré ({len(sequencer_data)} activités)")
            
        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error_message = f"Erreur séquenceur : {str(e)}"
            state.execution_log.append(f"❌ Erreur : {e}")
        
        return state
    

    
    async def generate_scripts(self, state: SimpleWorkflowState) -> SimpleWorkflowState:
        """Génère les scripts"""
        try:
            state.execution_log.append("📝 Génération des scripts...")
            state.current_step = 4
            
            if not state.sequencer_data:
                raise ValueError("Données séquenceur manquantes")
            
            scripts = {}
            
            for i, activity in enumerate(state.sequencer_data):
                try:
                    activity_type = activity.get('type_activite', 'text')
                    script_content = self.script_generator.generate_script(activity, activity_type)
                    
                    # Formater l'ID selon la structure demandée
                    num_ecran = activity.get('num_ecran', f"{i+1:02d}")
                    sequence = activity.get('sequence', f"Seq{i+1}")
                    script_id = f"{num_ecran}-{sequence}_{activity_type}"
                    
                    # Formater l'activité selon la structure demandée
                    formatted_activity = {
                        "sequence": activity.get('sequence', f"Séquence {i+1}"),
                        "num_ecran": activity.get('num_ecran', f"{i+1:02d}-{sequence}"),
                        "titre_ecran": activity.get('titre_ecran', f"Écran {i+1}"),
                        "sous_titre": activity.get('sous_titre', ""),
                        "resume_contenu": activity.get('resume_contenu', ""),
                        "type_activite": activity_type,
                        "niveau_bloom": activity.get('niveau_bloom', 'Comprendre'),
                        "difficulte": activity.get('difficulte', 'facile'),
                        "duree_estimee": activity.get('duree_estimee', 10),
                        "objectif_lie": activity.get('objectif_lie', ""),
                        "commentaire": activity.get('commentaire', "")
                    }
                    
                    scripts[script_id] = {
                        'activite': formatted_activity,
                        'script': script_content,
                        'generated_at': datetime.now().isoformat()
                    }
                    
                except Exception as script_error:
                    state.execution_log.append(f"⚠️ Erreur script {i+1}: {script_error}")
                    continue
            
            state.scripts_data = scripts
            
            # Sauvegarder localement
            await self.save_json_output(
                scripts,
                f"scripts_{state.session_id[:8]}.json"
            )
            
            state.execution_log.append(f"✅ {len(scripts)} scripts générés")
            
        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error_message = f"Erreur scripts : {str(e)}"
            state.execution_log.append(f"❌ Erreur : {e}")
        
        return state
    
    async def finalize_workflow(self, state: SimpleWorkflowState) -> SimpleWorkflowState:
        """Finalise le workflow"""
        try:
            state.execution_log.append("🎉 Finalisation...")
            state.current_step = 5
            state.end_time = datetime.now()
            
            final_results = {
                "workflow_metadata": {
                    "session_id": state.session_id,
                    "start_time": state.start_time.isoformat(),
                    "end_time": state.end_time.isoformat(),
                    "duration_seconds": (state.end_time - state.start_time).total_seconds(),
                    "total_steps": state.current_step,
                    "status": "completed"
                },
                "user_input": state.user_input,
                "agent_analysis": state.agent_analysis,
                "sequencer_data": state.sequencer_data,
                "scripts_data": state.scripts_data,
                "execution_log": state.execution_log,
                "statistics": {
                    "objectives_analyzed": len(state.agent_analysis.get("objectives", [])) if state.agent_analysis else 0,
                    "activities_generated": len(state.sequencer_data) if state.sequencer_data else 0,
                    "scripts_generated": len(state.scripts_data) if state.scripts_data else 0
                }
            }
            
            await self.save_json_output(
                final_results,
                f"final_results_{state.session_id[:8]}.json"
            )
            
            state.status = WorkflowStatus.COMPLETED
            state.execution_log.append("🎯 Workflow terminé!")
            
        except Exception as e:
            state.status = WorkflowStatus.FAILED
            state.error_message = f"Erreur finalisation : {str(e)}"
            state.execution_log.append(f"❌ Erreur : {e}")
        
        return state
    
    async def save_json_output(self, data: Dict[str, Any], filename: str):
        """Sauvegarde JSON"""
        try:
            filepath = os.path.join(self.output_directory, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=2, ensure_ascii=False, default=str)
            print(f"📁 Sauvegardé : {filepath}")
        except Exception as e:
            print(f"⚠️ Erreur sauvegarde {filename}: {e}")
    
    async def run_complete_workflow(self, user_input: Dict[str, Any], session_id: str = None) -> SimpleWorkflowState:
        """Exécute le workflow complet avec sauvegarde en base"""
        if not session_id:
            session_id = str(uuid.uuid4())
        
        print(f"🚀 Workflow avec DB - Session: {session_id[:8]}")
        
        # 🗄️ CRÉER LA SESSION EN BASE
        self.db_manager.create_workflow_session(session_id, user_input)
        
        state = SimpleWorkflowState(
            user_input=user_input,
            session_id=session_id
        )
        
        try:
            # Exécution séquentielle
            if state.status != WorkflowStatus.FAILED:
                state = await self.initialize_components(state)
            
            if state.status != WorkflowStatus.FAILED:
                state = await self.run_agent_analysis(state)
                # 🗄️ SAUVEGARDER L'ANALYSE EN BASE
                if state.agent_analysis:
                    self.db_manager.save_agent_analysis(session_id, state.agent_analysis)
            
            if state.status != WorkflowStatus.FAILED:
                state = await self.generate_sequencer(state)
                # 🗄️ SAUVEGARDER LE SÉQUENCEUR EN BASE
                if state.sequencer_data:
                    self.db_manager.save_sequencer_data(session_id, state.sequencer_data)
            
            if state.status != WorkflowStatus.FAILED:
                state = await self.generate_scripts(state)
                # 🗄️ SAUVEGARDER LES SCRIPTS EN BASE
                if state.scripts_data:
                    self.db_manager.save_scripts_data(session_id, state.scripts_data)
            
            if state.status != WorkflowStatus.FAILED:
                state = await self.finalize_workflow(state)
            
            # 🗄️ METTRE À JOUR LE STATUT EN BASE
            if state.status == WorkflowStatus.COMPLETED:
                self.db_manager.update_workflow_session(
                    session_id,
                    status='completed',
                    end_time=state.end_time,
                    duration_seconds=(state.end_time - state.start_time).total_seconds(),
                    execution_log=state.execution_log
                )
                print(f"🎉 Workflow terminé et sauvegardé!")
                print(f"📊 Durée: {(state.end_time - state.start_time).total_seconds():.1f}s")
            else:
                self.db_manager.update_workflow_session(
                    session_id,
                    status='failed',
                    end_time=datetime.now(),
                    error_message=state.error_message,
                    execution_log=state.execution_log
                )
                print(f"❌ Workflow échoué et sauvegardé")
            
            return state
            
        except Exception as e:
            print(f"💥 Erreur critique: {e}")
            # 🗄️ SAUVEGARDER L'ERREUR EN BASE
            self.db_manager.update_workflow_session(
                session_id,
                status='failed',
                end_time=datetime.now(),
                error_message=f"Erreur critique: {str(e)}"
            )
            
            state.status = WorkflowStatus.FAILED
            state.error_message = f"Erreur critique: {str(e)}"
            state.end_time = datetime.now()
            return state

# Fonctions utilitaires compatibles
def create_educational_orchestrator(openai_api_key: str, output_directory: str = "./outputs", db_path: str = "educational_platform.db") -> SimpleEducationalOrchestrator:
    """Crée l'orchestrateur avec base de données"""
    return SimpleEducationalOrchestrator(
        openai_api_key=openai_api_key,
        output_directory=output_directory,
        db_path=db_path
    )

async def run_educational_pipeline(
    orchestrator: SimpleEducationalOrchestrator,
    course_data: Dict[str, Any],
    uploaded_files: List = None,
    session_id: str = None
) -> SimpleWorkflowState:
    """Lance le pipeline simple"""
    
    user_input = course_data.copy()
    if uploaded_files:
        user_input["uploaded_files"] = uploaded_files
    
    return await orchestrator.run_complete_workflow(user_input, session_id)