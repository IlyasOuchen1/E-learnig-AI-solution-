import streamlit as st
import asyncio
import uuid
import sys
from pathlib import Path

# Ajouter les chemins
sys.path.append(str(Path(__file__).parent.parent))

from orchestrator.simple_orchestrator import create_educational_orchestrator, run_educational_pipeline
from shared.config.settings import settings

# Configuration de la page
st.set_page_config(
    page_title="🎓 Educational AI Platform",
    page_icon="🎓",
    layout="wide"
)

# CSS pour le style
st.markdown("""
<style>
    .main .block-container {
        padding-top: 2rem;
    }
    
    .stButton > button {
        background-color: #4CAF50;
        color: white;
        border: none;
        border-radius: 4px;
        padding: 0.5rem 1rem;
    }
    
    .success-box {
        background-color: #d4edda;
        border: 1px solid #c3e6cb;
        color: #155724;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
    
    .error-box {
        background-color: #f8d7da;
        border: 1px solid #f5c6cb;
        color: #721c24;
        padding: 1rem;
        border-radius: 4px;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation de la session
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = None
if 'session_id' not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if 'workflow_results' not in st.session_state:
    st.session_state.workflow_results = None

def main():
    """Interface principale"""
    
    st.title("🎓 Educational AI Platform")
    st.markdown("**Création automatisée de contenu éducatif avec IA**")
    
    # Sidebar pour la configuration
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # Clé API
        api_key = st.text_input(
            "Clé API OpenAI",
            type="password",
            value=settings.OPENAI_API_KEY or "",
            help="Votre clé API OpenAI"
        )
        
        # Validation de la clé
        if api_key and api_key.startswith('sk-'):
            st.success("✅ Clé API valide")
            
            # Initialiser l'orchestrateur
            if not st.session_state.orchestrator:
                try:
                    st.session_state.orchestrator = create_educational_orchestrator(
                        api_key, 
                        str(settings.OUTPUTS_DIR)
                    )
                    st.success("🚀 Orchestrateur initialisé")
                except Exception as e:
                    st.error(f"❌ Erreur: {e}")
        else:
            st.warning("⚠️ Clé API OpenAI requise")
        
        st.divider()
        
        # Informations de session
        st.header("📊 Session")
        st.info(f"**ID:** {st.session_state.session_id[:8]}...")
        
        if st.button("🔄 Nouvelle Session"):
            st.session_state.session_id = str(uuid.uuid4())
            st.session_state.workflow_results = None
            st.rerun()
    
    # Interface principale
    if not st.session_state.orchestrator:
        st.warning("⚠️ Veuillez configurer votre clé API OpenAI dans la sidebar")
        return
    
    # Formulaire de saisie
    st.header("📝 Informations du Cours")
    
    with st.form("course_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            course_subject = st.text_area(
                "Sujet du cours *",
                height=120,
                placeholder="Ex: Introduction à l'intelligence artificielle...",
                help="Décrivez le sujet principal de votre cours"
            )
            
            learning_objectives = st.text_area(
                "Objectifs d'apprentissage",
                height=100,
                placeholder="Ex: - Comprendre les concepts IA\n- Implémenter des algorithmes",
                help="Listez vos objectifs existants (optionnel)"
            )
        
        with col2:
            target_audience = st.text_area(
                "Public cible",
                height=120,
                placeholder="Ex: Étudiants licence informatique avec bases Python...",
                help="Décrivez votre audience (optionnel)"
            )
            
            source_text = st.text_area(
                "Contenu supplémentaire",
                height=100,
                placeholder="Collez ici du contenu additionnel...",
                help="Plan de cours, ressources, etc. (optionnel)"
            )
        
        # Upload de fichiers
        st.subheader("📁 Documents Pédagogiques")
        uploaded_files = st.file_uploader(
            "Choisissez vos fichiers (PDF, TXT, DOCX)",
            type=['pdf', 'txt', 'docx'],
            accept_multiple_files=True,
            help="L'IA extraira automatiquement les objectifs de vos documents"
        )
        
        # Bouton de soumission
        submitted = st.form_submit_button("🚀 Lancer l'Analyse Complète", type="primary")
    
    # Traitement du formulaire
    if submitted:
        if not course_subject.strip():
            st.error("❌ Le sujet du cours est obligatoire")
            return
        
        # Préparer les données
        course_data = {
            "course_subject": course_subject,
            "target_audience": target_audience,
            "learning_objectives": learning_objectives,
            "source_text": source_text
        }
        
        # Lancer le workflow
        with st.spinner("🔄 Exécution du workflow complet..."):
            try:
                # Utiliser asyncio pour exécuter le workflow
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                
                final_state = loop.run_until_complete(
                    run_educational_pipeline(
                        st.session_state.orchestrator,
                        course_data,
                        uploaded_files,
                        st.session_state.session_id
                    )
                )
                
                loop.close()
                
                # Sauvegarder les résultats
                st.session_state.workflow_results = final_state
                
                # Afficher le résultat
                if final_state.status.value == "completed":
                    st.success("🎉 Workflow terminé avec succès!")
                    st.balloons()
                else:
                    st.error(f"❌ Workflow échoué: {final_state.error_message}")
                
            except Exception as e:
                st.error(f"💥 Erreur critique: {str(e)}")
    
    # Affichage des résultats
    if st.session_state.workflow_results:
        display_results(st.session_state.workflow_results)

def display_results(workflow_state):
    """Affiche les résultats du workflow"""
    
    st.header("📊 Résultats du Workflow")
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        objectives_count = 0
        if workflow_state.agent_analysis and "objectives" in workflow_state.agent_analysis:
            objectives_count = len(workflow_state.agent_analysis["objectives"])
        st.metric("🎯 Objectifs", objectives_count)
    
    with col2:
        activities_count = 0
        if workflow_state.sequencer_data:
            activities_count = len(workflow_state.sequencer_data)
        st.metric("📚 Activités", activities_count)
    
    with col3:
        scripts_count = 0
        if workflow_state.scripts_data:
            scripts_count = len(workflow_state.scripts_data)
        st.metric("📝 Scripts", scripts_count)
    
    with col4:
        duration = 0
        if workflow_state.start_time and workflow_state.end_time:
            duration = (workflow_state.end_time - workflow_state.start_time).total_seconds()
        st.metric("⏱️ Durée", f"{duration:.1f}s")
    
    # Onglets des résultats
    tab1, tab2, tab3, tab4 = st.tabs(["🤖 Agent", "📚 Séquenceur", "📝 Scripts", "📋 Logs"])
    
    with tab1:
        st.subheader("Analyse des Objectifs")
        if workflow_state.agent_analysis:
            st.json(workflow_state.agent_analysis)
        else:
            st.info("Aucune analyse disponible")
    
    with tab2:
        st.subheader("Séquenceur Pédagogique")
        if workflow_state.sequencer_data:
            st.json(workflow_state.sequencer_data)
        else:
            st.info("Aucun séquenceur généré")
    
    with tab3:
        st.subheader("Scripts Générés")
        if workflow_state.scripts_data:
            for script_id, script_info in workflow_state.scripts_data.items():
                with st.expander(f"📄 {script_id}"):
                    st.code(script_info.get('script', 'Pas de contenu'))
        else:
            st.info("Aucun script généré")
    
    with tab4:
        st.subheader("Journal d'Exécution")
        if workflow_state.execution_log:
            for log_entry in workflow_state.execution_log:
                st.text(log_entry)
        else:
            st.info("Aucun log disponible")

if __name__ == "__main__":
    main()