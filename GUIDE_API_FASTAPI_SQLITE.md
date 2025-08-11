# 🌐 Guide de l'API FastAPI avec SQLite

## 🎯 **Objectif**

Exposer le contenu de la base SQLite via une API REST FastAPI, permettant au frontend de récupérer le contenu e-learning au format JSON exact sans modification.

## 🚀 **Démarrage Rapide**

### **1. Installer les Dépendances**
```bash
pip install fastapi uvicorn requests
```

### **2. Démarrer l'API**
```bash
python start_fastapi_server.py
```

### **3. Accéder à la Documentation**
- **API Base** : http://localhost:8000
- **Documentation Swagger** : http://localhost:8000/docs
- **Health Check** : http://localhost:8000/health

## 📊 **Endpoints Disponibles**

### **Endpoints Principaux**

| Méthode | Endpoint | Description |
|---------|----------|-------------|
| `GET` | `/` | Informations de l'API |
| `GET` | `/health` | Vérification de santé |
| `GET` | `/api/sessions` | Liste des sessions |
| `GET` | `/api/sessions/{id}` | Session spécifique |
| `GET` | `/api/sessions/{id}/content` | Contenu complet |
| `GET` | `/api/sessions/{id}/content/simple` | Contenu simple (frontend) |
| `GET` | `/api/statistics` | Statistiques globales |

## 🔗 **Utilisation des Endpoints**

### **1. Récupérer les Sessions**
```bash
curl "http://localhost:8000/api/sessions?limit=10"
```

**Réponse :**
```json
[
  {
    "session_id": "4d761e3f-c2af-4a0c-8bcd-564c069e9013",
    "title": "Session ERP Systems",
    "status": "completed",
    "start_time": "2024-01-15T10:30:00",
    "end_time": "2024-01-15T11:45:00",
    "duration_seconds": 4500,
    "user_input": {
      "course_subject": "ERP systems",
      "target_audience": "formation pour client bas niveau"
    }
  }
]
```

### **2. Récupérer le Contenu d'une Session**
```bash
curl "http://localhost:8000/api/sessions/4d761e3f-c2af-4a0c-8bcd-564c069e9013/content/simple"
```

**Réponse (Format JSON Exact) :**
```json
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
```

### **3. Récupérer les Statistiques**
```bash
curl "http://localhost:8000/api/statistics"
```

**Réponse :**
```json
{
  "sessions": {
    "total": 15,
    "completed": 12,
    "failed": 3,
    "avg_duration_seconds": 4200.5
  },
  "activities": {
    "total": 75,
    "sessions_with_activities": 15
  },
  "distributions": {
    "activity_types": {
      "text": 45,
      "quiz": 20,
      "video": 10
    }
  }
}
```

## 💻 **Intégration Frontend**

### **JavaScript (Fetch API)**
```javascript
const API_BASE_URL = 'http://localhost:8000';

// Récupérer les sessions
async function getSessions(limit = 10) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/sessions?limit=${limit}`);
    if (!response.ok) throw new Error('Erreur réseau');
    return await response.json();
  } catch (error) {
    console.error('Erreur récupération sessions:', error);
    return [];
  }
}

// Récupérer le contenu d'une session (format exact)
async function getSessionContent(sessionId) {
  try {
    const response = await fetch(`${API_BASE_URL}/api/sessions/${sessionId}/content/simple`);
    if (!response.ok) throw new Error('Erreur réseau');
    return await response.json();
  } catch (error) {
    console.error('Erreur récupération contenu:', error);
    return {};
  }
}

// Utilisation
async function loadElearningContent() {
  // Récupérer les sessions
  const sessions = await getSessions(5);
  console.log('Sessions disponibles:', sessions);
  
  if (sessions.length > 0) {
    // Récupérer le contenu de la première session
    const content = await getSessionContent(sessions[0].session_id);
    console.log('Contenu e-learning:', content);
    
    // Le contenu est au format exact attendu par le frontend
    // {activity_id: {activite: {...}, script: '...'}}
    loadContentInApp(content);
  }
}
```

### **JavaScript (Axios)**
```javascript
import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

// Configuration Axios
const api = axios.create({
  baseURL: API_BASE_URL,
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
});

// Récupérer les sessions
const getSessions = async (limit = 10) => {
  try {
    const response = await api.get(`/api/sessions?limit=${limit}`);
    return response.data;
  } catch (error) {
    console.error('Erreur récupération sessions:', error);
    return [];
  }
};

// Récupérer le contenu d'une session
const getSessionContent = async (sessionId) => {
  try {
    const response = await api.get(`/api/sessions/${sessionId}/content/simple`);
    return response.data;
  } catch (error) {
    console.error('Erreur récupération contenu:', error);
    return {};
  }
};
```

### **React Hook Personnalisé**
```javascript
import { useState, useEffect } from 'react';

const useElearningAPI = () => {
  const [sessions, setSessions] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);

  const fetchSessions = async (limit = 10) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await fetch(`http://localhost:8000/api/sessions?limit=${limit}`);
      if (!response.ok) throw new Error('Erreur réseau');
      
      const data = await response.json();
      setSessions(data);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchSessionContent = async (sessionId) => {
    try {
      const response = await fetch(`http://localhost:8000/api/sessions/${sessionId}/content/simple`);
      if (!response.ok) throw new Error('Erreur réseau');
      
      return await response.json();
    } catch (err) {
      setError(err.message);
      return {};
    }
  };

  useEffect(() => {
    fetchSessions();
  }, []);

  return {
    sessions,
    loading,
    error,
    fetchSessions,
    fetchSessionContent
  };
};

// Utilisation dans un composant
function ElearningApp() {
  const { sessions, loading, error, fetchSessionContent } = useElearningAPI();
  const [selectedContent, setSelectedContent] = useState(null);

  const handleSessionSelect = async (sessionId) => {
    const content = await fetchSessionContent(sessionId);
    setSelectedContent(content);
  };

  if (loading) return <div>Chargement...</div>;
  if (error) return <div>Erreur: {error}</div>;

  return (
    <div>
      <h1>E-Learning Content</h1>
      
      {/* Liste des sessions */}
      <div>
        <h2>Sessions disponibles</h2>
        {sessions.map(session => (
          <button 
            key={session.session_id}
            onClick={() => handleSessionSelect(session.session_id)}
          >
            {session.title}
          </button>
        ))}
      </div>

      {/* Contenu de la session sélectionnée */}
      {selectedContent && (
        <div>
          <h2>Contenu de la session</h2>
          {Object.entries(selectedContent).map(([activityId, activity]) => (
            <div key={activityId}>
              <h3>{activity.activite.titre_ecran}</h3>
              <p>{activity.activite.resume_contenu}</p>
              <div>{activity.script}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
```

## 🧪 **Tests de l'API**

### **Test Automatique**
```bash
python test_fastapi_sqlite.py
```

### **Test Manuel avec cURL**
```bash
# Health check
curl http://localhost:8000/health

# Sessions
curl http://localhost:8000/api/sessions?limit=5

# Contenu d'une session
curl http://localhost:8000/api/sessions/SESSION_ID/content/simple

# Statistiques
curl http://localhost:8000/api/statistics
```

### **Test avec l'Interface Swagger**
1. Ouvrir http://localhost:8000/docs
2. Cliquer sur un endpoint
3. Cliquer sur "Try it out"
4. Exécuter la requête
5. Vérifier la réponse

## 🔧 **Configuration CORS**

L'API est configurée pour accepter les requêtes depuis :
- `http://localhost:5173` (Vite)
- `http://localhost:3000` (Create React App)
- `http://127.0.0.1:*` (Variantes localhost)
- `http://10.110.3.155:5176` (IP réseau spécifique)
- `*` (Toutes les origines - temporaire pour les tests)

## 📊 **Structure de la Base de Données**

L'API interroge les tables SQLite suivantes :
- **`workflow_sessions`** : Sessions de workflow
- **`sequencer_activities`** : Activités du séquenceur
- **`generated_scripts`** : Scripts générés

## 🎯 **Avantages de cette Approche**

### **✅ Compatibilité Frontend**
- **Format JSON exact** - Aucune modification du frontend nécessaire
- **Structure identique** à celle attendue
- **CORS configuré** pour tous les frontends

### **✅ Performance**
- **Base SQLite locale** - Accès rapide aux données
- **Requêtes optimisées** - Jointures SQL efficaces
- **Cache automatique** - Pas de requêtes répétées

### **✅ Maintenance**
- **API REST standard** - Endpoints prévisibles
- **Documentation automatique** - Swagger/OpenAPI
- **Tests automatisés** - Validation des fonctionnalités

### **✅ Flexibilité**
- **Endpoints multiples** - Contenu complet ou simple
- **Filtres et limites** - Pagination des résultats
- **Statistiques** - Monitoring des données

## 🚀 **Prochaines Étapes**

### **1. Tester l'API**
```bash
python start_fastapi_server.py
python test_fastapi_sqlite.py
```

### **2. Intégrer dans le Frontend**
- Utiliser les endpoints pour récupérer le contenu
- Afficher le contenu e-learning
- Gérer les erreurs et le chargement

### **3. Personnaliser selon les Besoins**
- Ajouter des filtres par type d'activité
- Implémenter la pagination
- Ajouter l'authentification si nécessaire

---

## 🎉 **Conclusion**

**L'API FastAPI avec SQLite est maintenant prête !**

**✅ Format JSON exact exposé via API REST**
**✅ Base SQLite accessible via endpoints standard**
**✅ Documentation automatique avec Swagger**
**✅ CORS configuré pour tous les frontends**
**✅ Tests automatisés et validation**

**Votre frontend peut maintenant récupérer le contenu e-learning au format exact sans aucune modification !** 🚀 