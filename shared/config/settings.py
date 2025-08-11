import os
from pathlib import Path
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class Settings:
    """Configuration centralisée pour la plateforme"""
    
    # Environnement
    APP_ENV = os.getenv('APP_ENV', 'development')
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    VERBOSE_MODE = os.getenv('VERBOSE_MODE', 'true').lower() == 'true'
    
    # Chemins de base
    BASE_DIR = Path(__file__).parent.parent.parent
    OUTPUTS_DIR = Path(os.getenv('OUTPUT_DIRECTORY', './outputs'))
    LOGS_DIR = Path(os.getenv('LOGS_DIRECTORY', './logs'))
    
    # API Keys
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    PINECONE_API_KEY = os.getenv('PINECONE_API_KEY')
    
    # Modèles LLM
    LLM_MODEL = os.getenv('LLM_MODEL', 'gpt-4o-mini')
    AGENT_TEMPERATURE = float(os.getenv('AGENT_TEMPERATURE', 0.2))
    SEQUENCER_TEMPERATURE = float(os.getenv('SEQUENCER_TEMPERATURE', 0.7))
    
    # Interface
    STREAMLIT_PORT = int(os.getenv('STREAMLIT_PORT', 8501))
    
    @classmethod
    def validate(cls) -> bool:
        """Valide la configuration"""
        if not cls.OPENAI_API_KEY:
            print("❌ OPENAI_API_KEY manquant")
            return False
        return True
    
    @classmethod
    def get_summary(cls) -> dict:
        """Résumé de configuration"""
        return {
            "environment": cls.APP_ENV,
            "debug": cls.DEBUG,
            "model": cls.LLM_MODEL,
            "api_configured": bool(cls.OPENAI_API_KEY),
            "outputs_dir": str(cls.OUTPUTS_DIR)
        }

# Instance globale
settings = Settings()

# Validation au chargement
if not settings.validate():
    print("⚠️ Configuration incomplète")