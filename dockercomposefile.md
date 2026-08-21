# ShopStack — Docker Compose Setup Guide

This guide explains how to run the ShopStack application using Docker Compose.

## Architecture

ShopStack contains three main services:

```text
┌──────────────────────────────────────────────┐
│                  Browser                     │
└───────────────────┬──────────────────────────┘
                    │
                    │ http://localhost:3000
                    ▼
┌──────────────────────────────────────────────┐
│                Frontend                      │
│              React + Vite                    │
│              Port: 3000                      │
└───────────────────┬──────────────────────────┘
                    │
                    │ API requests
                    │ http://localhost:8000
                    ▼
┌──────────────────────────────────────────────┐
│                 Backend                      │
│              FastAPI                         │
│              Port: 8000                      │
└───────────────────┬──────────────────────────┘
                    │
                    │ MySQL connection
                    ▼
┌──────────────────────────────────────────────┐
│                  MySQL                       │
│              Port: 3306                     │
│          Docker internal network             │
└──────────────────────────────────────────────┘
```

## Project Structure

The Docker Compose file should be located in the project root:

```text
shopstack-fullstack/
│
├── backend/
│   ├── app/
│   ├── requirements.txt
│   └── Dockerfile
│
├── frontend/
│   ├── src/
│   ├── package.json
│   └── Dockerfile
│
├── docker-compose.yml
├── DOCKER-COMPOSE.md
└── README.md
```

---

# 1. Install Docker

For Manjaro Linux, install Docker:

```bash
sudo pacman -S docker
```

Verify the installation:

```bash
docker --version
```

Example:

```text
Docker version 29.x.x
```

---

# 2. Start Docker Service

Enable Docker to start automatically:

```bash
sudo systemctl enable docker
```

Start Docker:

```bash
sudo systemctl start docker
```

Or use both commands together:

```bash
sudo systemctl enable --now docker
```

Check Docker status:

```bash
systemctl status docker
```

You should see:

```text
Active: active (running)
```

---

# 3. Test Docker

Run:

```bash
docker run hello-world
```

If Docker is working correctly, Docker will download the `hello-world` image and display a success message.

---

# 4. Install Docker Compose

Check whether Docker Compose is already available:

```bash
docker compose version
```

If you get a Compose version, Docker Compose is already installed.

If Compose is not available, install it on Manjaro:

```bash
sudo pacman -S docker-compose
```

Then check:

```bash
docker-compose --version
```

Depending on the Docker/Compose package available on your system, you may use either:

```bash
docker compose
```

or:

```bash
docker-compose
```

This guide uses:

```bash
docker compose
```

---

# 5. Allow Your User to Run Docker

By default, Docker may require `sudo`.

To allow your normal Linux user to run Docker:

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in.

Alternatively, restart your session.

Verify:

```bash
groups
```

You should see:

```text
docker
```

Test:

```bash
docker ps
```

You should no longer need `sudo`.

---

# 6. Clone the Project

Clone the ShopStack repository:

```bash
git clone <repository-url>
```

Enter the project:

```bash
cd shopstack-fullstack
```

Check the files:

```bash
ls
```

You should have:

```text
backend
frontend
docker-compose.yml
README.md
```

---

# 7. Check Docker Compose Configuration

From the project root:

```bash
docker compose config
```

This validates the Compose configuration.

If the configuration is valid, Docker Compose will print the resolved configuration.

If there is an error, fix the `docker-compose.yml` before continuing.

---

# 8. Build the Application

Build the frontend and backend images:

```bash
docker compose build
```

Or force a fresh build:

```bash
docker compose build --no-cache
```

Normally, use:

```bash
docker compose build
```

---

# 9. Start ShopStack

Start all services:

```bash
docker compose up
```

Or build and start in one command:

```bash
docker compose up --build
```

The services should start:

```text
frontend
backend
mysql
```

---

# 10. Run in Background

For normal development or testing, run:

```bash
docker compose up --build -d
```

The `-d` option means:

```text
detached mode
```

Docker Compose runs the containers in the background.

---

# 11. Check Running Containers

Run:

```bash
docker compose ps
```

Expected result:

```text
NAME                  STATUS
shopstack-frontend    Up
shopstack-backend     Up
shopstack-mysql       Up
```

The exact container names depend on the `docker-compose.yml`.

---

# 12. Check All Docker Containers

You can also use:

```bash
docker ps
```

Example:

```text
CONTAINER ID   IMAGE                 PORTS
xxxxxxxx       shopstack-frontend    0.0.0.0:3000->3000/tcp
xxxxxxxx       shopstack-backend     0.0.0.0:8000->8000/tcp
xxxxxxxx       mysql                 3306/tcp
```

---

# 13. Access the Frontend

Open your browser:

```text
http://localhost:3000
```

The React application should be available here.

---

# 14. Access the Backend

Open:

```text
http://localhost:8000
```

FastAPI should be running.

---

# 15. Access FastAPI Swagger

Open:

```text
http://localhost:8000/docs
```

This provides the interactive FastAPI API documentation.

You can test your API endpoints directly from Swagger UI.

---

# 16. Frontend Port

The frontend should expose:

```text
3000:3000
```

Meaning:

```text
Host                         Container
localhost:3000      →       frontend:3000
```

The browser accesses:

```text
http://localhost:3000
```

---

# 17. Backend Port

The backend should expose:

```text
8000:8000
```

Meaning:

```text
Host                         Container
localhost:8000      →       backend:8000
```

The API is available at:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

---

# 18. MySQL

MySQL runs as a separate Docker service.

The backend should connect to MySQL using the **Compose service name**, not `localhost`.

For example:

```text
mysql:3306
```

Do NOT use:

```text
localhost:3306
```

inside the backend container.

A typical database URL is:

```text
mysql+pymysql://root:mysql@mysql:3306/shopstack
```

Here:

```text
root       → MySQL username
mysql      → Docker Compose service name
3306       → MySQL port
shopstack  → database name
```

---

# 19. Check Backend Logs

View backend logs:

```bash
docker compose logs backend
```

Follow logs continuously:

```bash
docker compose logs -f backend
```

Press:

```text
Ctrl + C
```

to stop viewing the logs.

---

# 20. Check Frontend Logs

Run:

```bash
docker compose logs frontend
```

Follow live logs:

```bash
docker compose logs -f frontend
```

---

# 21. Check MySQL Logs

Run:

```bash
docker compose logs mysql
```

Follow live logs:

```bash
docker compose logs -f mysql
```

---

# 22. View All Logs

To see logs from every service:

```bash
docker compose logs
```

Follow all logs:

```bash
docker compose logs -f
```

---

# 23. Restart the Application

Restart all services:

```bash
docker compose restart
```

Restart only the backend:

```bash
docker compose restart backend
```

Restart only the frontend:

```bash
docker compose restart frontend
```

---

# 24. Stop the Application

Stop the application:

```bash
docker compose stop
```

This stops the containers but does not remove them.

---

# 25. Stop and Remove Containers

To stop and remove the Compose containers:

```bash
docker compose down
```

This removes:

```text
Containers
Networks
```

It does not normally remove named volumes.

---

# 26. Remove Containers and Volumes

To completely remove the Compose environment:

```bash
docker compose down -v
```

**Warning:** `-v` can remove the MySQL Docker volume and therefore delete your database data.

Only use this when you intentionally want to reset the database.

---

# 27. Rebuild After Code Changes

If you change the Dockerfile or dependencies:

```bash
docker compose down
docker compose build
docker compose up -d
```

Or simply:

```bash
docker compose up --build -d
```

---

# 28. Complete Start Command

For normal usage, you usually only need:

```bash
cd shopstack-fullstack
docker compose up --build -d
```

Then verify:

```bash
docker compose ps
```

Access:

```text
Frontend:
http://localhost:3000

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs
```

---

# 29. Complete Stop Command

When finished:

```bash
docker compose down
```

---

# 30. Troubleshooting

## Docker daemon is not running

If you see:

```text
Cannot connect to the Docker daemon
```

run:

```bash
sudo systemctl enable --now docker
```

Then:

```bash
docker ps
```

---

## Permission denied

If you see:

```text
permission denied while trying to connect to the Docker daemon
```

run:

```bash
sudo usermod -aG docker $USER
```

Then log out and log back in.

Test:

```bash
docker ps
```

---

## Compose command not found

Check:

```bash
docker compose version
```

If unavailable:

```bash
sudo pacman -S docker-compose
```

Then check:

```bash
docker-compose --version
```

If your system provides the standalone command, use:

```bash
docker-compose up --build
```

instead of:

```bash
docker compose up --build
```

---

# Quick Reference

| Task              | Command                              |
| ----------------- | ------------------------------------ |
| Start Docker      | `sudo systemctl enable --now docker` |
| Check Docker      | `docker --version`                   |
| Check Compose     | `docker compose version`             |
| Validate Compose  | `docker compose config`              |
| Build             | `docker compose build`               |
| Start             | `docker compose up`                  |
| Build + Start     | `docker compose up --build`          |
| Background        | `docker compose up --build -d`       |
| Check containers  | `docker compose ps`                  |
| View logs         | `docker compose logs`                |
| Follow logs       | `docker compose logs -f`             |
| Restart           | `docker compose restart`             |
| Stop              | `docker compose stop`                |
| Remove containers | `docker compose down`                |
| Remove volumes    | `docker compose down -v`             |

## Application URLs

```text
Frontend
http://localhost:3000

Backend
http://localhost:8000

FastAPI Swagger
http://localhost:8000/docs
```
