# ShopStack — Docker Run Guide

This document contains only the commands required to build and run the ShopStack frontend and backend Docker images.

## 1. Go to the Project Root

```bash
cd ~/argo/shopstack-fullstack
```

Verify the project:

```bash
ls
```

Expected:

```text
backend/
frontend/
docker-compose.yml
```

---

# 2. Build the Backend Image

Go into the backend directory:

```bash
cd backend
```

Build the backend Docker image:

```bash
docker build -t shopstack-backend:latest .
```

Verify the image:

```bash
docker images | grep shopstack-backend
```

Expected:

```text
shopstack-backend    latest
```

---

# 3. Build the Frontend Image

Go back to the project root:

```bash
cd ..
```

Go into the frontend directory:

```bash
cd frontend
```

Build the frontend Docker image:

```bash
docker build -t shopstack-frontend:latest .
```

Verify the image:

```bash
docker images | grep shopstack-frontend
```

Expected:

```text
shopstack-frontend    latest
```

---

# 4. Verify Both Images

Go back to the project root:

```bash
cd ..
```

Run:

```bash
docker images | grep shopstack
```

You should have:

```text
shopstack-backend     latest
shopstack-frontend    latest
```

---

# 5. Run Backend Container Manually

Run the backend container:

```bash
docker run -d \
  --name shopstack-backend \
  -p 8000:8000 \
  shopstack-backend:latest
```

The port mapping is:

```text
Host                Container
8000        →       8000
```

The backend is available at:

```text
http://localhost:8000
```

FastAPI Swagger:

```text
http://localhost:8000/docs
```

---

# 6. Check Backend Container

```bash
docker ps
```

You should see:

```text
shopstack-backend
```

Check backend logs:

```bash
docker logs shopstack-backend
```

Follow the logs:

```bash
docker logs -f shopstack-backend
```

---

# 7. Run Frontend Container Manually

Run:

```bash
docker run -d \
  --name shopstack-frontend \
  -p 3000:3000 \
  shopstack-frontend:latest
```

The port mapping is:

```text
Host                Container
3000        →       3000
```

The frontend is available at:

```text
http://localhost:3000
```

---

# 8. Check Frontend Container

```bash
docker ps
```

You should see:

```text
shopstack-frontend
shopstack-backend
```

Check frontend logs:

```bash
docker logs shopstack-frontend
```

Follow the logs:

```bash
docker logs -f shopstack-frontend
```

---

# 9. Check Both Containers

Run:

```bash
docker ps
```

Expected port forwarding:

```text
shopstack-frontend
0.0.0.0:3000 -> 3000

shopstack-backend
0.0.0.0:8000 -> 8000
```

---

# 10. Test Backend

Open:

```text
http://localhost:8000
```

Swagger:

```text
http://localhost:8000/docs
```

Or test from the terminal:

```bash
curl http://localhost:8000
```

---

# 11. Test Frontend

Open:

```text
http://localhost:3000
```

The React application should load.

---

# 12. Stop Backend

```bash
docker stop shopstack-backend
```

Remove the container:

```bash
docker rm shopstack-backend
```

---

# 13. Stop Frontend

```bash
docker stop shopstack-frontend
```

Remove the container:

```bash
docker rm shopstack-frontend
```

---

# 14. Start Existing Containers Again

If you stopped the containers but did not remove them:

```bash
docker start shopstack-backend
docker start shopstack-frontend
```

Check:

```bash
docker ps
```

---

# 15. Rebuild After Code Changes

If backend code changes:

```bash
cd backend
docker build -t shopstack-backend:latest .
```

If frontend code changes:

```bash
cd ../frontend
docker build -t shopstack-frontend:latest .
```

Then recreate the containers:

```bash
docker rm -f shopstack-backend shopstack-frontend
```

Run backend:

```bash
docker run -d \
  --name shopstack-backend \
  -p 8000:8000 \
  shopstack-backend:latest
```

Run frontend:

```bash
docker run -d \
  --name shopstack-frontend \
  -p 3000:3000 \
  shopstack-frontend:latest
```

---

# 16. Docker Compose Run

If `docker-compose.yml` is already configured for both images/services, the preferred way to run the complete application is:

```bash
cd ~/argo/shopstack-fullstack
```

Build everything:

```bash
docker compose build
```

Start everything:

```bash
docker compose up -d
```

Or build and start together:

```bash
docker compose up --build -d
```

Check:

```bash
docker compose ps
```

---

# 17. View Compose Logs

All services:

```bash
docker compose logs -f
```

Backend:

```bash
docker compose logs -f backend
```

Frontend:

```bash
docker compose logs -f frontend
```

---

# 18. Stop Docker Compose

```bash
docker compose down
```

---

# 19. Final Application Ports

| Service  | Host Port | Container Port | URL                        |
| -------- | --------: | -------------: | -------------------------- |
| Frontend |    `3000` |         `3000` | http://localhost:3000      |
| Backend  |    `8000` |         `8000` | http://localhost:8000      |
| Swagger  |    `8000` |         `8000` | http://localhost:8000/docs |
| MySQL    |    `3306` |         `3306` | Internal database          |

## Final Commands

For normal development, from the project root:

```bash
docker compose up --build -d
```

Check:

```bash
docker compose ps
```

Open:

```text
Frontend:
http://localhost:3000

Backend:
http://localhost:8000

Swagger:
http://localhost:8000/docs
```

Stop:

```bash
docker compose down
```
