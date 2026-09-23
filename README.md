# STAT-SKILL AI

> **National Statistical Competency Intelligence Platform**  
> Unified capacity building, diagnostic assessment, automated skill gap detection, and grounded training recommendations for Government, Industry, and Academia.

---

## Overview

STAT-SKILL AI is a production-ready competency intelligence platform designed for statistical workforce development. It provides an integrated assessment and learning engine tailored for three specialized tracks:

1. **Government Track (MoSPI Alignment)**: National survey design, sampling methodology, national accounts compilation, CPI/WPI indices, and direct integration with iGOT Karmayogi and NSSTA training modules.
2. **Industry Track**: Enterprise analytics, econometric modeling, BI data marts, and practical project portfolios for data analysts.
3. **Academia Track**: Higher education statistics curricula, Course Outcome (CO) mapping, and graduate internship readiness.

---

## Key Features

- **Standardized Diagnostic Assessments**: Psychometrically calibrated baseline evaluations across core statistical and analytical competencies.
- **Deterministic Skill-Gap Math**: Automated calculation comparing individual proficiency scores against role benchmarks with zero hallucinated scoring.
- **Grounded Learning Pathways**: Targeted course recommendations mapped directly to national catalogues (iGOT Karmayogi & NSSTA).
- **AI Document-to-Quiz Ingestion**: Upload official manuals, circulars, or textbooks to extract validated evaluation quizzes with source citations.
- **Evidence Vault & Micro-Credentials**: Verifiable portfolio submissions and immutable competency progress records.
- **Statutory Data Governance**: Compliant with India's Digital Personal Data Protection (DPDP) Act 2023 with localized data sovereignty.

---

## Architecture & Technology Stack

- **Frontend (`apps/web`)**: Next.js 14 (App Router), TypeScript, Tailwind CSS, Lucide Icons.
- **Backend API (`apps/api`)**: Python 3.12, FastAPI, SQLAlchemy 2.0, Uvicorn, Pydantic v2.
- **Database**: SQLite (portable local default) / PostgreSQL with pgvector support.
- **Proxy Architecture**: Next.js reverse proxies all backend API calls (`/api/v1`) and documentation (`/docs`) on a single port (`3000`), eliminating cross-origin latency and multi-port friction.

---

## Local Development & Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.11+

### Running the Entire Platform on a Single Port (3000)

Start both the FastAPI backend and Next.js frontend with one command:

```bash
# Windows (PowerShell or Command Prompt)
.\start.bat

# Or via npm
npm start
```

Once started, access the complete platform on **Port 3000**:
- **Introduction & Landing Page**: [http://localhost:3000/](http://localhost:3000/)
- **Login Gateway**: [http://localhost:3000/login](http://localhost:3000/login)
- **Learner Registration**: [http://localhost:3000/register](http://localhost:3000/register)
- **Backend API**: [http://localhost:3000/api/v1](http://localhost:3000/api/v1)
- **Interactive Swagger Docs**: [http://localhost:3000/docs](http://localhost:3000/docs)

---

## Pre-Configured Demo Accounts

For reviewers and evaluators, the platform provides 4 ready-to-use demo accounts on the `/login` gateway with 1-click authentication:

| Sector / Track | Name | Email | Password | Context |
| :--- | :--- | :--- | :--- | :--- |
| **Government** | Ananya Rao | `ananya.rao@mospi.gov.in` | `Password123` | MoSPI Statistical Officer (Survey & Sampling) |
| **Industry** | Neha Sharma | `neha.sharma@datatech.io` | `Password123` | Senior Data Analyst (SQL & BI Modeling) |
| **Academia** | Arjun Mehta | `arjun.mehta@univ.edu.in` | `Password123` | Statistics Student (Curriculum & Internship) |
| **Governance** | System Admin | `admin@statskill.gov.in` | `Password123` | Platform Administrator & DPDP Audit |

---

## Cloud Deployment Guide

### 1. Backend Deployment (Render / Railway)

#### Deploy to Render
The repository includes a root `render.yaml` blueprint.
1. Connect your GitHub repository to [Render](https://render.com).
2. Choose **New > Blueprint** and select this repository.
3. Render automatically provisions the web service using `apps/api/requirements.txt` and starts Uvicorn:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir apps/api
   ```
4. Note your public backend URL (e.g., `https://statskill-api.onrender.com`).

#### Deploy to Railway
Railway automatically detects the included `Procfile` and `railway.json`:
```
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --app-dir apps/api
```

---

### 2. Frontend Deployment (Vercel)

1. Connect your GitHub repository to [Vercel](https://vercel.com).
2. Set the **Root Directory** to `apps/web`.
3. In **Environment Variables**, configure the link to your cloud backend:
   ```env
   BACKEND_URL=https://statskill-api.onrender.com
   NEXT_PUBLIC_API_URL=/api/v1
   ```
4. Click **Deploy**. Vercel compiles Next.js and rewrites all `/api/v1/*` requests directly to your Render backend.

---

## Automated Verification Tests

Run the backend test suite:

```bash
python -m pytest apps/api/tests -v
```

---

## License

This software is developed for official capacity building and institutional workforce intelligence. All rights reserved.
