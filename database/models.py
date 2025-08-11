from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, Float, Boolean
from sqlalchemy.orm import declarative_base
from sqlalchemy.sql import func
from datetime import datetime

Base = declarative_base()

class WorkflowSession(Base):
    """Table pour les sessions de workflow"""
    __tablename__ = 'workflow_sessions'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), unique=True, nullable=False, index=True)
    user_input = Column(JSON, nullable=False)
    status = Column(String(50), default='pending')  # pending, in_progress, completed, failed
    start_time = Column(DateTime, default=func.now())
    end_time = Column(DateTime)
    duration_seconds = Column(Float)
    execution_log = Column(JSON, default=list)
    error_message = Column(Text)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())

class AgentAnalysis(Base):
    """Table pour les analyses de l'agent"""
    __tablename__ = 'agent_analyses'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False, index=True)
    objectives = Column(JSON, default=list)
    content_analysis = Column(JSON, default=dict)
    classification = Column(JSON, default=dict)
    formatted_objectives = Column(JSON, default=dict)
    difficulty_evaluation = Column(JSON, default=dict)
    recommendations = Column(JSON, default=dict)
    feedback = Column(JSON, default=dict)
    statistics = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())

class SequencerData(Base):
    """Table pour les données du séquenceur"""
    __tablename__ = 'sequencer_activities'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False, index=True)
    sequence_name = Column(String(255))
    num_ecran = Column(String(50))
    titre_ecran = Column(String(255))
    sous_titre = Column(String(255))
    resume_contenu = Column(Text)
    type_activite = Column(String(100))
    niveau_bloom = Column(String(100))
    difficulte = Column(String(50))
    duree_estimee = Column(Integer, default=0)
    objectif_lie = Column(String(255))
    commentaire = Column(Text)
    created_at = Column(DateTime, default=func.now())

class ScriptData(Base):
    """Table pour les scripts générés"""
    __tablename__ = 'generated_scripts'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False, index=True)
    script_id = Column(String(255), nullable=False)
    activity_data = Column(JSON, default=dict)
    script_content = Column(JSON, default=dict)
    script_type = Column(String(100))
    created_at = Column(DateTime, default=func.now())

class WorkflowStats(Base):
    """Table pour les statistiques de workflow"""
    __tablename__ = 'workflow_statistics'
    
    id = Column(Integer, primary_key=True)
    session_id = Column(String(255), nullable=False, index=True)
    total_objectives = Column(Integer, default=0)
    total_activities = Column(Integer, default=0)
    total_scripts = Column(Integer, default=0)
    total_documents_processed = Column(Integer, default=0)
    bloom_distribution = Column(JSON, default=dict)
    difficulty_distribution = Column(JSON, default=dict)
    activity_types_distribution = Column(JSON, default=dict)
    created_at = Column(DateTime, default=func.now())