# Projet : Infrastructure TODO App avec Docker Compose, Traefik, Prometheus et Grafana

Ce projet met en place une architecture Docker composée de plusieurs services pour faire tourner une application web de gestion de tâches (TODO app) monitorée via Prometheus et Grafana, et routée dynamiquement par Traefik.

##  Objectifs du TP

* Conteneuriser une application Flask connectée à PostgreSQL
* Exposer l'application via un reverse proxy (Traefik)
* Mettre en place la supervision avec Prometheus et Grafana
* Créer une stack complète et fonctionnelle via Docker Compose

---

##  Architecture

* **app** : Application Flask exposant une API REST (/api/tasks)
* **db** : Base de données PostgreSQL 15 contenant les tâches
* **prometheus** : Collecte les métriques de l'application
* **grafana** : Visualise les métriques Prometheus
* **traefik** : Reverse proxy dynamique ([http://localhost](http://localhost))



---

##  Lancement du projet

1. Cloner le repo :

```bash
git clone https://github.com/alexiiiiiiiiiiiiiiiii/todo-docker-infra.git
cd todo-docker-infra
```

2. Créer un fichier `.env` à la racine :

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=todo
API_PORT=5000
```

3. Lancer les services :

```bash
docker compose up --build
```

---

##  Accès aux services

| Service    | URL                                                      | Infos                    |
| ---------- | -------------------------------------------------------- | ------------------------ |
| API Flask  | [http://localhost/api/tasks](http://localhost/api/tasks) | Retourne les tâches      |
| Prometheus | [http://localhost:9090](http://localhost:9090)           | Monitoring des métriques |
| Grafana    | [http://localhost:3000](http://localhost:3000)           | admin / admin            |
| Traefik    | [http://localhost:8080](http://localhost:8080)           | Dashboard reverse proxy  |

---


##  Fonctions techniques

* Monitoring automatique avec `prometheus_flask_exporter`
* Endpoint `/metrics` exposé automatiquement par Flask
* Configuration Prometheus à `scrape_interval: 5s`
* Dashboards Grafana personnalisables
* Reverse proxy défini par labels Docker avec Traefik

---

##  Structure du projet

```
todo-docker-infra/
├── app/                  # Code Flask
├── client/               # (optionnel frontend)
├── db/                   # Données PostgreSQL (volume)
├── grafana/
│   ├── dashboards/
│   └── provisioning/
├── prometheus/
│   └── prometheus.yml
├── scripts/
│   └── init-db.sql
├── traefik/              # (optionnel)
├── .env
├── docker-compose.yml
└── README.md
```

              +------------------+
              |     Traefik      |
              +--------+---------+
                       |
        +--------------+--------------+
        |                             |
        v                             v
+------------------+        +---------------------+
|     API (Flask)  |<------>|    Prometheus       |
+--------+---------+        +----------+----------+
         |                             |
         v                             v
+------------------+        +---------------------+
|    PostgreSQL     |        |   Node Exporter     |
+--------+---------+        +---------------------+
         |
         v
+------------------+
|     Grafana      |
+------------------+

```

