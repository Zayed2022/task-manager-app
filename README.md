# <div align="center"> 🗂️ **DevOps Task Manager with CI/CD** </div>

A fully containerized **Task Manager Application** built with:

* **FastAPI** (Backend)
* **MongoDB** (Database)
* **HTML/CSS/JS + Nginx** (Frontend)
* **Docker & Docker Compose**
* **Azure VM (Ubuntu 22.04)**
* **GitHub Actions CI/CD**
* **Docker Hub Image Registry**

This project demonstrates **end-to-end DevOps**, including containerization, cloud deployment, reverse proxying, networking, and automated delivery pipelines.

---

# 🏗️ **Architecture Diagram**

✔ Supports **frontend → backend → MongoDB**
✔ Includes **Nginx, Docker, Azure VM**
✔ CI/CD through **GitHub Actions + Docker Hub**

---

### 📌 **ASCII Diagram (also included in README):**

```
                    ┌──────────────────────────────┐
                    │          GitHub Repo          │
                    │   (Source Code + Workflow)    │
                    └──────────────┬───────────────┘
                                   │ Push
                                   ▼
                      ┌────────────────────────┐
                      │   GitHub Actions CI/CD │
                      │ Builds Docker Images   │
                      │ Pushes to Docker Hub   │
                      │ Deploys via SSH to VM  │
                      └─────────────┬──────────┘
                                    │ pull latest
                                    ▼
                     ┌─────────────────────────────────┐
                     │        Azure Ubuntu VM           │
                     │  ─────────────────────────────   │
                     │   Docker Engine + Compose        │
                     │   ┌────────────┬──────────────┐ │
                     │   │ Frontend   │   Backend     │ │
                     │   │  Nginx     │   FastAPI     │ │
                     │   └──────┬─────┴──────────┬───┘ │
                     │          │ reverse proxy   │     │
                     │          ▼                 ▼     │
                     │        Browser         MongoDB   │
                     └──────────────────────────────────┘
```

---

<img width="1536" height="1024" alt="ChatGPT Image Nov 28, 2025, 04_50_29 PM" src="https://github.com/user-attachments/assets/8456eb5c-4726-4d2e-9257-9f6e8b7ff269" />


---

# 🚀 **Features**

### 🟢 **Frontend**

* Simple Task UI
* Add, delete, complete tasks
* Calls backend through `/api` → Nginx → FastAPI

### 🔵 **Backend (FastAPI)**

* Full CRUD for tasks
* MongoDB integration
* CORS enabled
* JSON API responses

### 🟣 **Database**

* MongoDB container
* Volume for persistent storage

### 🟠 **Nginx Reverse Proxy**

* Port 80 → Frontend
* `/api` → Backend
* Clean URLs (`http://server/`)

### 🔥 **DevOps**

* Dockerized frontend, backend, DB
* Docker Compose for orchestration
* Azure VM deployment
* GitHub Actions for automated CI/CD
* Docker Hub as registry
* Automatic re-deploy on every push

---

# 🐳 **Docker Compose Setup**

```yaml
version: "3.8"

services:
  mongo:
    image: mongo
    container_name: mongo
    restart: always
    ports:
      - "27017:27017"
    volumes:
      - mongo_data:/data/db

  backend:
    image: zayed2022/taskmanager-backend:latest
    container_name: backend
    restart: always
    depends_on:
      - mongo
    ports:
      - "8000:8000"

  frontend:
    image: zayed2022/taskmanager-frontend:latest
    container_name: frontend
    restart: always
    depends_on:
      - backend
    ports:
      - "8080:80"

volumes:
  mongo_data:
```

---

# 🔁 **CI/CD Workflow (GitHub Actions)**

Builds → Pushes → Deploys:

```yaml
name: CI/CD Pipeline

on:
  push:
    branches:
      - main

jobs:
  deploy:
    runs-on: ubuntu-latest

    steps:
      - name: Checkout Code
        uses: actions/checkout@v3

      - name: Log in to Docker Hub
        uses: docker/login-action@v2
        with:
          username: ${{ secrets.DOCKER_USERNAME }}
          password: ${{ secrets.DOCKER_PASSWORD }}

      - name: Build Backend Image
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/taskmanager-backend:latest ./backend

      - name: Build Frontend Image
        run: |
          docker build -t ${{ secrets.DOCKER_USERNAME }}/taskmanager-frontend:latest ./frontend

      - name: Push Images to Docker Hub
        run: |
          docker push ${{ secrets.DOCKER_USERNAME }}/taskmanager-backend:latest
          docker push ${{ secrets.DOCKER_USERNAME }}/taskmanager-frontend:latest

      - name: Deploy on Azure VM
        uses: appleboy/ssh-action@v1.0.3
        with:
          host: ${{ secrets.SSH_HOST }}
          username: ${{ secrets.SSH_USER }}
          key: ${{ secrets.SSH_KEY }}
          script: |
            cd task-manager-app
            git pull
            docker compose down
            docker pull ${{ secrets.DOCKER_USERNAME }}/taskmanager-backend:latest
            docker pull ${{ secrets.DOCKER_USERNAME }}/taskmanager-frontend:latest
            docker compose up -d
```

---

# 🔧 **Nginx Config**

```nginx
server {
    listen 80;
    server_name _;

    location / {
        proxy_pass http://localhost:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }

    location /api/ {
        rewrite ^/api/?(.*)$ /$1 break;
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

# 🖥️ **How to Deploy on Azure VM**

```bash
git pull
docker compose down
docker compose up -d
```

---

# 👨‍💻 **Author**

**Mohammed Zayed**
Cloud | DevOps | Backend | AWS | Azure | Python

---


