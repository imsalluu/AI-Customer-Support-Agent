# SupportIQ AI — Production Deployment & Hardening Guide

## 1. Quickstart with Docker Compose

To launch all services (FastAPI Backend, Next.js Frontend, PostgreSQL with pgvector, and Redis):

```bash
# Clone repository
git clone https://github.com/imsalluu/SupportIQ-AI-Customer-Support-Agent.git
cd SupportIQ-AI-Customer-Support-Agent

# Configure environment
cp backend/.env.example backend/.env

# Build and start services
docker-compose up -d --build
```

Access:
- Frontend Dashboard & Landing: `http://localhost:3000`
- FastAPI REST Backend & Swagger Docs: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

---

## 2. Local Development Setup

### Backend
```bash
cd backend
python -m venv venv
# Windows:
.\venv\Scripts\activate
# Linux/macOS:
source venv/bin/activate

pip install -r requirements.txt
python seed_data.py
uvicorn app.main:app --reload --port 8000
```

### Running Backend Tests
```bash
cd backend
python -m pytest tests/ -v
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

---

## 3. Production Security Checklist

1. Change `SECRET_KEY` in production `.env` to a 64-character cryptographically random string.
2. Ensure PostgreSQL connections enforce SSL mode (`sslmode=require`).
3. Set `DEBUG=False` in FastAPI configuration.
4. Restrict `BACKEND_CORS_ORIGINS` strictly to your production domain (e.g. `https://app.supportiq.ai`).
