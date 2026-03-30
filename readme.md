# projet-flask-docker

Application web Flask avec base de données PostgreSQL, containerisée avec Docker et déployée automatiquement sur VPS OVH via GitHub Actions.

Accessible sur : [https://flask.theo-massenya.fr](https://flask.theo-massenya.fr)

## Stack 

- **Backend** — Python / Flask
- **Serveur WSGI** — Gunicorn (3 workers)
- **Base de données** — PostgreSQL 16
- **Containerisation** — Docker / Docker Compose
- **Registry** — GitHub Container Registry (ghcr.io)
- **CI/CD** — GitHub Actions
- **Reverse proxy** — Traefik v3 + HTTPS Let's Encrypt
- **Hébergement** — VPS OVH (Ubuntu)

## Pipeline CI/CD

À chaque push sur la branche `main` :

1. GitHub Actions lance une machine Ubuntu
2. Build de l'image Docker Flask
3. Push de l'image sur `ghcr.io`
4. Connexion SSH au VPS 
5. Pull de la nouvelle image et redémarrage automatique

```
git push → build → push ghcr.io → deploy VPS → en prod ✅
```

## Sécurité

- **Secrets** — aucun mot de passe hardcodé, tout passe par GitHub Secrets et un fichier `.env` non versionné
- **Clé SSH dédiée** — paire de clés SSH spécifique à GitHub Actions
- **Réseaux isolés** — PostgreSQL accessible uniquement par Flask via le réseau `internal`, pas depuis internet
- **`.gitignore`** — le fichier `.env` n'est jamais pushé sur GitHub

## Lancer en local

### Prérequis

- Docker Desktop installé

### Variables d'environnement

Crée un fichier `.env` à la racine :

```env
POSTGRES_USER=user
POSTGRES_PASSWORD=password
POSTGRES_DB=madb
DATABASE_URL=postgresql://user:password@db:5432/madb
```

### Démarrage

```bash
# Cloner le repo
git clone https://github.com/Theo1335/projet-flask-docker.git
cd projet-flask-docker

# Lancer la stack complète
docker compose up --build

# Accessible sur http://localhost:5000
```

### Arrêt

```bash
docker compose down
```

## Structure du projet

```
projet-flask-docker/
├── app.py                        # Application Flask + connection pool PostgreSQL
├── requirements.txt              # Dépendances Python (flask, psycopg2, gunicorn)
├── Dockerfile                    # Image Docker Flask avec Gunicorn
├── docker-compose.yml            # Stack complète (Flask + PostgreSQL + Traefik)
├── .env                          # Variables d'environnement (non versionné)
├── .gitignore
├── templates/
│   └── index.html                # Template HTML
├── static/
│   └── style.css                 # Styles CSS
└── .github/
    └── workflows/
        └── deploy.yml            # Pipeline CI/CD
```