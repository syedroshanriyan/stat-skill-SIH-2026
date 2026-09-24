# STAT-SKILL AI

<p align="center">
  <strong>National Statistical Competency Intelligence Platform</strong>
</p>

<p align="center">
  AI-powered competency assessment, skill-gap intelligence, personalized learning, and evidence-based workforce development for Government, Industry, and Academia.
</p>

<p align="center">

![SIH 2026](https://img.shields.io/badge/Smart%20India%20Hackathon-2026-blue?style=for-the-badge)
![Next.js](https://img.shields.io/badge/Next.js-14-black?style=for-the-badge\&logo=next.js)
![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge\&logo=fastapi)
![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge\&logo=typescript)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-pgvector-4169E1?style=for-the-badge\&logo=postgresql)
![Docker](https://img.shields.io/badge/Docker-Ready-2496ED?style=for-the-badge\&logo=docker)

</p>

<p align="center">
  <a href="#-overview">Overview</a> •
  <a href="#-problem">Problem</a> •
  <a href="#-solution">Solution</a> •
  <a href="#-core-capabilities">Capabilities</a> •
  <a href="#-architecture">Architecture</a> •
  <a href="#-getting-started">Getting Started</a> •
  <a href="#-deployment">Deployment</a>
</p>

---

## 1. Overview

**STAT-SKILL AI** is a competency intelligence platform designed to identify what a learner or professional knows, determine where competency gaps exist, and convert those gaps into structured learning actions.

The platform is built around a **shared AI Competency Intelligence Engine** and supports three connected tracks:

| Track              | Primary Purpose                          | Example Focus                                                                 |
| ------------------ | ---------------------------------------- | ----------------------------------------------------------------------------- |
| 🏛️ **Government** | Statistical workforce capacity building  | Official Statistics, survey methodology, sampling, national accounts, indices |
| 🏢 **Industry**    | Data and analytics workforce development | Analytics, econometrics, SQL, BI, applied projects                            |
| 🎓 **Academia**    | Curriculum and learner development       | Statistics curriculum, competency mapping, internship readiness               |

The **Government Track** is the primary SIH-oriented workflow, while Industry and Academia extend the same competency intelligence architecture into adjacent ecosystems.

---

# 2. The Problem

Traditional learning platforms primarily answer:

> **"What courses are available?"**

STAT-SKILL AI addresses a different question:

> **"What does this person actually need to learn next, and why?"**

The platform addresses several interconnected problems:

* Skill levels are often inferred from qualifications rather than demonstrated competency.
* Learners may not know their precise competency gaps.
* Training recommendations are frequently generic rather than gap-driven.
* Government employees require domain-specific capacity building.
* Official learning resources can be difficult to connect directly to individual competency needs.
* Uploaded institutional learning material is often disconnected from assessment.
* Institutions lack a unified view of competency development.
* AI-generated recommendations can become unreliable when they are not grounded in structured competency data.

STAT-SKILL AI therefore combines:

**Profile → Assessment → Competency Model → Gap Analysis → Recommendation → Learning → Reassessment**

---

# 3. Solution

```text
                    ┌───────────────────────────┐
                    │        USER PROFILE       │
                    │ Education • Role • Goal   │
                    │ Experience • Track        │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │   COMPETENCY ASSESSMENT   │
                    │ Diagnostic Questions /     │
                    │ Document-grounded Quizzes  │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │ COMPETENCY INTELLIGENCE   │
                    │ Score • Level • Confidence │
                    │ Evidence • History         │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │       SKILL GAP ENGINE     │
                    │ Current vs Required Level  │
                    │ Gap • Priority • Status    │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │ RECOMMENDATION ENGINE     │
                    │ Gap Relevance              │
                    │ Track Preference           │
                    │ Resource Mapping           │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │ PERSONALIZED LEARNING     │
                    │ Courses • Paths • Quizzes │
                    │ Documents • Assistant     │
                    └─────────────┬─────────────┘
                                  │
                                  ▼
                    ┌───────────────────────────┐
                    │       REASSESSMENT        │
                    │ Progress • Competency     │
                    │ History • Gap Reduction   │
                    └───────────────────────────┘
```

---

# 4. Core Capabilities

## 4.1 AI Competency Intelligence

The platform maintains competency information beyond a simple percentage score.

A competency record can represent:

* Current score
* Proficiency level
* Confidence
* Assessment source
* Assessment timestamp
* Competency history
* Score delta
* Required proficiency

This allows the platform to track **how competency changes over time**.

---

## 4.2 Diagnostic Assessments

STAT-SKILL AI provides structured assessments designed around competency domains.

Assessment results contribute to the learner's competency state and can subsequently affect:

* Skill-gap calculations
* Learning recommendations
* Learning paths
* Progress analytics

The backend contains dedicated assessment routing and service layers rather than embedding assessment logic directly into the UI.

---

## 4.3 Deterministic Skill-Gap Analysis

The platform separates competency measurement from recommendation generation.

Conceptually:

```text
Required Competency
        │
        │
        ▼
┌─────────────────┐
│ Required Level  │
└────────┬────────┘
         │
         │ comparison
         ▼
┌─────────────────┐
│ Current Ability │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│   Skill Gap     │
│ Value + Priority│
└─────────────────┘
```

Each identified gap can have:

* Current score
* Required score
* Gap value
* Priority
* Status
* Updated timestamp

This provides an explicit basis for subsequent recommendations.

---

# 5. Three-Track Intelligence Model

## 🏛️ Government Track

The primary track for the SIH problem context.

The Government workflow focuses on competency development within the **Official Statistical System**, including areas such as:

* Survey methodology
* Sampling
* National accounts
* Price indices
* Statistical data production
* Statistical analysis
* Official statistical workflows

The architecture also provides catalogue/provider concepts for government-oriented learning resources such as:

* iGOT Karmayogi
* NSSTA
* Government-oriented training resources

### Government Flow

```text
Government Employee
        │
        ▼
Profile + Role Analysis
        │
        ▼
Statistical Competency Assessment
        │
        ▼
Competency Profile
        │
        ▼
Skill-Gap Analysis
        │
        ▼
iGOT / NSSTA / Relevant Resources
        │
        ▼
Personalized Learning Path
        │
        ▼
Reassessment
```

---

## 🏢 Industry Track

The same competency engine can be applied to industry-oriented analytics roles.

Example competency areas include:

* SQL
* Data analytics
* Business intelligence
* Econometrics
* Statistical modelling
* Data interpretation
* Applied analytical projects

Industry recommendations can prioritize resources mapped to industry-oriented competency requirements.

---

## 🎓 Academia Track

The Academia Track applies competency intelligence to learners and institutions.

Potential use cases include:

* Statistics curriculum mapping
* Course Outcome alignment
* Competency assessment
* Student skill-gap identification
* Internship readiness
* Learning recommendations

This allows the same underlying intelligence engine to operate across the education-to-employment pipeline.

---

# 6. Document → Knowledge → Assessment

One of the important capabilities of STAT-SKILL AI is converting uploaded learning material into assessment content.

Supported document processing includes formats such as:

* PDF
* DOCX
* PPTX

The processing pipeline is conceptually:

```text
       Uploaded Document
              │
              ▼
       Document Extraction
              │
              ▼
        Text / Pages
              │
              ▼
      Document Chunking
              │
              ▼
       Knowledge / RAG
              │
              ▼
       AI Question Generation
              │
              ▼
        Grounded MCQs
              │
              ▼
       Source References
              │
              ▼
        Quiz Assessment
```

Generated questions are associated with source references so that assessment content can remain connected to the underlying learning material.

---

# 7. AI-Assisted Quiz Generation

STAT-SKILL AI can generate multiple-choice assessments from indexed learning material.

The quiz generation pipeline supports:

* Competency selection
* Difficulty selection
* Configurable question count
* Four-option MCQs
* Correct answer identification
* Explanations
* Source references
* Competency assessment mode

When the Gemini API is configured, the system can use Gemini for question generation.

The backend also contains deterministic fallback behavior for environments where the AI service is unavailable, allowing the application to continue functioning during local development and testing.

---

# 8. Recommendation Intelligence

Recommendations are not treated as arbitrary AI output.

The backend contains a hybrid recommendation mechanism that considers factors including:

```text
Skill Gap
   +
Resource Relevance
   +
Track / Provider Preference
   +
Gap Priority
   =
Recommendation Score
```

For the Government track, the recommendation layer can prioritize government-oriented providers such as:

* iGOT
* NSSTA

Industry and Academia tracks use corresponding provider/resource categories.

This creates a more explainable recommendation flow than simply asking an LLM:

> "What should this user learn?"

---

# 9. RAG / Embedding Layer

The backend contains an embedding layer designed to support semantic document processing.

When a Gemini API key is available, the system can attempt to generate embeddings through the configured Google model.

For offline/test environments, the repository includes a deterministic fallback embedding mechanism.

```text
                 Document
                    │
                    ▼
             Text Extraction
                    │
                    ▼
               Chunking
                    │
                    ▼
               Embeddings
              /           \
             /             \
      Gemini API       Deterministic
       Enabled          Fallback
             \             /
              \           /
               ▼         ▼
              Vector Representation
                       │
                       ▼
                 Retrieval Layer
```

The production-oriented database configuration also supports PostgreSQL with `pgvector`.

---

# 10. Competency State Lifecycle

A key design principle is that assessments can update the user's competency state.

For competency assessments:

```text
Quiz Attempt
     │
     ▼
Calculate Score
     │
     ▼
Compare with Previous State
     │
     ├───────────────┐
     ▼               ▼
Score Update    Confidence Update
     │               │
     └───────┬───────┘
             ▼
      Competency History
             │
             ▼
        Skill Gap Update
             │
             ▼
     Recommendation Refresh
```

This creates a feedback loop rather than treating each quiz as an isolated activity.

---

# 11. Evidence & Progress

The platform also contains dedicated modules for evidence and analytics.

The broader competency model is designed to support:

* Competency history
* Assessment evidence
* Progress tracking
* Learning outcomes
* Portfolio-oriented evidence
* Institutional analytics

The goal is to move beyond:

> **Course completed**

toward:

> **Competency demonstrated and progress evidenced**

---

# 12. Platform Architecture

STAT-SKILL AI uses a monorepo architecture.

```text
STAT-SKILL AI
│
├── apps/
│   │
│   ├── web/
│   │   └── Next.js + TypeScript
│   │
│   └── api/
│       └── FastAPI + Python
│
├── packages/
│   │
│   └── shared-types/
│       └── Shared Type Definitions
│
├── scripts/
│   └── Development / Startup Utilities
│
├── docker-compose.yml
├── render.yaml
├── railway.json
├── Procfile
└── package.json
```

---

# 13. Frontend Architecture

The frontend is implemented using:

* Next.js 14
* React 18
* TypeScript
* Tailwind CSS
* Recharts
* Lucide React

The application uses the Next.js App Router.

Major application areas include:

```text
apps/web/src/app/

├── (dashboard)
├── academia
├── government
├── industry
├── features
├── how-it-works
├── faq
├── legal-intelligence
├── login
├── register
└── page.tsx
```

The interface includes separate experiences for the major platform tracks rather than forcing every user into the same dashboard.

---

# 14. Backend Architecture

The backend is implemented with:

* Python
* FastAPI
* SQLAlchemy
* Pydantic
* Uvicorn
* PostgreSQL / SQLite
* pgvector
* JWT authentication
* Google Gemini integration

The backend follows a modular domain-oriented structure.

```text
apps/api/app/

├── admin/
├── analytics/
├── assessments/
├── assistant/
├── auth/
├── catalogues/
├── competencies/
├── core/
├── documents/
├── evidence/
├── frameworks/
├── gaps/
├── health/
├── learning_paths/
├── legal/
├── models/
├── quizzes/
├── rag/
├── recommendations/
├── schemas/
├── scraper/
├── users/
└── main.py
```

This separation keeps domain logic away from the presentation layer and makes individual capabilities easier to test and evolve.

---

# 15. API Layer

The FastAPI application exposes versioned routes under:

```text
/api/v1
```

The backend currently organizes API functionality around domains including:

| Module            | Responsibility                      |
| ----------------- | ----------------------------------- |
| `auth`            | Authentication and identity         |
| `users`           | User profiles                       |
| `frameworks`      | Competency frameworks               |
| `competencies`    | Competency definitions and states   |
| `assessments`     | Diagnostic assessments              |
| `gaps`            | Skill-gap analysis                  |
| `recommendations` | Learning recommendations            |
| `catalogues`      | Learning-resource catalogues        |
| `learning_paths`  | Personalized learning pathways      |
| `documents`       | Document ingestion                  |
| `quizzes`         | AI/document-grounded assessments    |
| `assistant`       | AI assistant functionality          |
| `evidence`        | Evidence and competency artifacts   |
| `analytics`       | Progress and analytics              |
| `admin`           | Administrative functionality        |
| `health`          | Service health                      |
| `legal`           | Legal/privacy-related functionality |

Interactive API documentation is available through FastAPI's Swagger interface.

---

# 16. Technology Stack

## Frontend

| Technology   | Purpose                   |
| ------------ | ------------------------- |
| Next.js 14   | Web application framework |
| React 18     | UI                        |
| TypeScript   | Type safety               |
| Tailwind CSS | Styling                   |
| Recharts     | Data visualization        |
| Lucide React | Interface icons           |

## Backend

| Technology       | Purpose           |
| ---------------- | ----------------- |
| Python           | Backend language  |
| FastAPI          | REST API          |
| Uvicorn          | ASGI server       |
| SQLAlchemy       | ORM               |
| Pydantic         | Data validation   |
| JWT              | Authentication    |
| bcrypt / Passlib | Password security |
| pytest           | Testing           |

## AI / Data

| Technology    | Purpose                        |
| ------------- | ------------------------------ |
| Google Gemini | AI generation / embeddings     |
| RAG pipeline  | Grounded document intelligence |
| PostgreSQL    | Production relational database |
| pgvector      | Vector similarity support      |
| SQLite        | Lightweight local development  |

## Infrastructure

| Technology     | Purpose                         |
| -------------- | ------------------------------- |
| Docker         | Containerized deployment        |
| Docker Compose | Multi-service local environment |
| Vercel         | Frontend deployment             |
| Render         | Backend deployment              |
| Railway        | Alternative backend deployment  |

---

# 17. Local Development

## Prerequisites

Install:

* Node.js 18+
* npm
* Python 3.11+
* Git

For the containerized setup:

* Docker
* Docker Compose

---

## Option A — Standard Local Setup

### 1. Clone the repository

```bash
git clone https://github.com/syedroshanriyan/stat-skill-SIH-2026.git
cd stat-skill-SIH-2026
```

### 2. Install frontend dependencies

```bash
npm install
```

### 3. Install backend dependencies

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

Then:

```bash
pip install -r apps/api/requirements.txt
```

---

## 4. Configure Environment Variables

Create the required environment configuration for the backend.

Example:

```env
DATABASE_URL=sqlite:///./statskill.db
JWT_SECRET=replace-with-a-secure-secret
CORS_ORIGINS=http://localhost:3000
GEMINI_API_KEY=your-gemini-api-key
```

> Never commit real API keys, JWT secrets, database passwords, or production credentials to Git.

---

# 18. Run the Platform

The repository includes a root startup script.

### Windows

```bash
.\start.bat
```

### Or

```bash
npm start
```

The application is designed to provide the primary web experience through:

```text
http://localhost:3000
```

Useful development endpoints:

| Service         | URL                              |
| --------------- | -------------------------------- |
| Web Application | `http://localhost:3000`          |
| Login           | `http://localhost:3000/login`    |
| Registration    | `http://localhost:3000/register` |
| API             | `http://localhost:3000/api/v1`   |
| Swagger         | `http://localhost:3000/docs`     |
| ReDoc           | `http://localhost:3000/redoc`    |

---

# 19. Docker Deployment

The repository includes a complete Docker Compose configuration.

The containerized architecture is:

```text
┌───────────────────────────────────────┐
│              Browser                  │
└───────────────────┬───────────────────┘
                    │
                    ▼
             ┌─────────────┐
             │   Web       │
             │  Next.js    │
             │   :3000     │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │    API      │
             │  FastAPI    │
             │   :8000     │
             └──────┬──────┘
                    │
                    ▼
             ┌─────────────┐
             │ PostgreSQL  │
             │  + pgvector │
             │   :5432     │
             └─────────────┘
```

Start the complete stack with:

```bash
docker compose up --build
```

Stop it with:

```bash
docker compose down
```

---

# 20. Deployment

## Frontend — Vercel

The frontend application is located at:

```text
apps/web
```

Set the Vercel root directory to:

```text
apps/web
```

Typical environment configuration:

```env
BACKEND_URL=https://your-backend-url
NEXT_PUBLIC_API_URL=/api/v1
```

---

## Backend — Render

The repository includes a `render.yaml` deployment blueprint.

The backend can be started with:

```bash
uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir apps/api
```

---

## Backend — Railway

A `Procfile` and Railway configuration are included for alternative backend deployment.

Example:

```text
web: uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000} --app-dir apps/api
```

---

# 21. Testing

Backend tests can be executed using:

```bash
python -m pytest apps/api/tests -v
```

For frontend validation:

```bash
npm run lint:web
```

For a production frontend build:

```bash
npm run build:web
```

---

# 22. Security Principles

STAT-SKILL AI is designed around several security principles:

* JWT-based authentication
* Password hashing
* Configurable CORS
* Environment-based secrets
* Request identifiers
* Audit events
* User-scoped document access
* User-scoped assessment data
* Separation between competency data and presentation
* No hard-coded production secrets

### Important

This repository should **not** be treated as automatically compliant with any statutory privacy framework merely because privacy-related modules exist.

Production deployment should independently validate:

* Data retention
* Consent
* User rights
* Access control
* Encryption
* Audit requirements
* Data residency
* Incident response
* DPDP Act obligations
* Third-party AI data handling

---

# 23. System Design Philosophy

STAT-SKILL AI follows five major principles.

### 1. Evidence over assumptions

Competency should be supported by assessment results and evidence rather than profile claims alone.

### 2. Gap before recommendation

The platform should identify the competency deficit before selecting learning resources.

### 3. Grounded AI

AI-generated content should remain connected to the underlying source material wherever applicable.

### 4. Explainable recommendations

Recommendations should provide a reason instead of appearing as unexplained AI output.

### 5. Continuous competency improvement

Assessment should feed back into the competency model, which can then update gaps and recommendations.

---

# 24. End-to-End User Journey

```text
┌────────────────────┐
│      Register      │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Build User Profile │
│ Education / Role   │
│ Experience / Goal  │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Select Track       │
│ Government         │
│ Industry           │
│ Academia           │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Diagnostic         │
│ Assessment         │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Competency Profile │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Skill Gap Analysis │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Recommendations    │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Learning Path      │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Learn / Practice   │
│ / AI Quiz          │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Reassessment       │
└─────────┬──────────┘
          ▼
┌────────────────────┐
│ Updated Competency │
│ + Reduced Gap      │
└────────────────────┘
```

---

# 25. SIH 2026 Alignment

STAT-SKILL AI is designed around the SIH 2026 problem context involving an AI-enabled learning platform for identifying competency gaps, recommending personalized training, integrating with relevant government learning ecosystems, and generating assessments from uploaded learning material.

### Requirement → Platform Mapping

| Requirement                   | STAT-SKILL AI Capability            |
| ----------------------------- | ----------------------------------- |
| Identify competency gaps      | Competency + Skill Gap Engine       |
| Personalized training         | Hybrid Recommendation Engine        |
| Government capacity building  | Government Track                    |
| iGOT-oriented recommendations | Government catalogue/provider model |
| NSSTA-oriented resources      | Government catalogue/provider model |
| AI assessment                 | Diagnostic Assessment Engine        |
| Generate MCQs                 | Document-to-Quiz Pipeline           |
| Uploaded learning material    | Document Processing + RAG           |
| Personalized learning         | Learning Path Engine                |
| Progress tracking             | Competency History + Analytics      |
| Evidence-based development    | Evidence module                     |
| Multi-sector extension        | Government + Industry + Academia    |

---

# 26. Why the Architecture Is Extensible

The platform is intentionally designed around a shared intelligence layer rather than three independent applications.

```text
                     ┌──────────────────────┐
                     │ Competency Intelligence│
                     │       Engine          │
                     └──────────┬───────────┘
                                │
             ┌──────────────────┼──────────────────┐
             │                  │                  │
             ▼                  ▼                  ▼
       ┌───────────┐      ┌───────────┐      ┌───────────┐
       │ Government│      │ Industry  │      │ Academia  │
       └───────────┘      └───────────┘      └───────────┘
             │                  │                  │
             ▼                  ▼                  ▼
       Government         Industry Skills    Academic Skills
       Competencies       & Roles            & Curriculum
             │                  │                  │
             └──────────────────┼──────────────────┘
                                ▼
                       Shared Learning Engine
```

Adding a new sector therefore does not require rebuilding the complete platform.

A new track can primarily introduce:

* Competency frameworks
* Role definitions
* Required proficiency levels
* Resource providers
* Assessment content
* Recommendation mappings

while reusing the same underlying intelligence engine.

---

# 27. Repository Structure

```text
stat-skill-SIH-2026/
│
├── apps/
│   ├── api/
│   │   ├── app/
│   │   │   ├── admin/
│   │   │   ├── analytics/
│   │   │   ├── assessments/
│   │   │   ├── assistant/
│   │   │   ├── auth/
│   │   │   ├── catalogues/
│   │   │   ├── competencies/
│   │   │   ├── core/
│   │   │   ├── documents/
│   │   │   ├── evidence/
│   │   │   ├── frameworks/
│   │   │   ├── gaps/
│   │   │   ├── health/
│   │   │   ├── learning_paths/
│   │   │   ├── legal/
│   │   │   ├── models/
│   │   │   ├── quizzes/
│   │   │   ├── rag/
│   │   │   ├── recommendations/
│   │   │   ├── schemas/
│   │   │   ├── scraper/
│   │   │   ├── users/
│   │   │   └── main.py
│   │   │
│   │   ├── tests/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   └── web/
│       ├── src/
│       │   ├── app/
│       │   └── components/
│       ├── Dockerfile
│       ├── package.json
│       └── next.config.js
│
├── packages/
│   └── shared-types/
│
├── scripts/
│
├── docker-compose.yml
├── railway.json
├── render.yaml
├── Procfile
├── package.json
└── README.md
```

---

# 28. API Documentation

Once the backend is running, interactive API documentation is available through:

```text
/docs
```

and:

```text
/redoc
```

The API follows a versioned structure:

```text
/api/v1
```

This makes the backend easier to evolve without breaking existing clients.

---

# 29. Project Status

### Current implementation areas

* [x] Next.js frontend
* [x] FastAPI backend
* [x] Authentication structure
* [x] User profiles
* [x] Competency framework
* [x] Diagnostic assessments
* [x] Skill-gap analysis
* [x] Learning recommendations
* [x] Learning-resource catalogues
* [x] Learning-path architecture
* [x] Document ingestion
* [x] AI-assisted quiz generation
* [x] RAG / embedding layer
* [x] Competency history
* [x] Evidence module
* [x] Analytics module
* [x] Government / Industry / Academia track structure
* [x] Docker Compose configuration
* [x] Render deployment configuration
* [x] Railway deployment configuration
* [x] Vercel frontend configuration

### Planned / deployment-dependent capabilities

* [ ] Production-grade external catalogue synchronization
* [ ] Production government ecosystem integrations
* [ ] Production-scale vector infrastructure
* [ ] Production observability
* [ ] Formal privacy/security audit
* [ ] Expanded institutional analytics
* [ ] Expanded competency frameworks

---

# 30. Important Deployment Note

The repository contains both SQLite-oriented local/deployment configuration and PostgreSQL + pgvector configuration.

For development:

```text
SQLite
```

is convenient and portable.

For a production deployment requiring semantic/vector search at scale:

```text
PostgreSQL + pgvector
```

is the intended architecture.

Do not expose development database credentials or JWT secrets in a public deployment.

---

# 31. Contributing

Contributions should preserve the platform's modular architecture.

Recommended workflow:

```text
1. Create a feature branch
2. Implement the feature in its domain module
3. Add/update backend tests
4. Validate frontend build
5. Run linting
6. Verify API behaviour
7. Submit a pull request
```

Keep business logic inside the appropriate backend domain instead of placing it directly inside route handlers or frontend components.

---

# 32. Team / Hackathon Context

**STAT-SKILL AI** is developed as a Smart India Hackathon 2026 solution focused on competency intelligence, personalized learning, and capacity building.

The project combines:

```text
Artificial Intelligence
        +
Competency Modeling
        +
Skill-Gap Analytics
        +
RAG / Document Intelligence
        +
Personalized Learning
        +
Government Training Ecosystem
```

into one unified platform.

---

# 33. License

This project is developed as a Smart India Hackathon 2026 solution.

Unless otherwise specified by the project maintainers, all rights to the source code and project materials are reserved.

---

# 34. Project Links

**Repository**

https://github.com/syedroshanriyan/stat-skill-SIH-2026

**Local Application**

```text
http://localhost:3000
```

**API Documentation**

```text
http://localhost:3000/docs
```

---

<p align="center">

### STAT-SKILL AI

**From competency measurement to measurable capability development.**

</p>

<p align="center">
Built for <strong>Smart India Hackathon 2026</strong>
</p>
