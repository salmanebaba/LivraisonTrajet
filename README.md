# 🚚 Optimisation de Tournées de Livraison

**Système de calcul d'itinéraires optimisés** utilisant :
- **OSRM** pour le moteur de routage
- **FastAPI** (backend API)
- **Leaflet.js** (carte interactive)
- **Docker** pour le déploiement

## 📋 Prérequis

- Docker 🐳 + Docker Compose
- Python 3.11+ (pour développement local)

## 🛠 Installation

```bash
# 1. Cloner le dépôt
git clone https://github.com/babasalmane/LivraisonTrajet.git
cd LivraisonTrajet

# 2. Créer le dossier des cartes (obligatoire)
mkdir -p maps && touch maps/.gitkeep

# 3. Lancer les services
docker-compose up --build