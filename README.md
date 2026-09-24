STAT-SKILL AI

<p align="center">
<img src="https://img.shields.io/badge/Smart%20India%20Hackathon-2026-0F766E?style=for-the-badge" alt="SIH 2026">
<img src="https://img.shields.io/badge/AI-Competency%20Intelligence-7C3AED?style=for-the-badge" alt="AI Competency Intelligence">
<img src="https://img.shields.io/badge/Next.js-14-111827?style=for-the-badge&logo=next.js&logoColor=white" alt="Next.js 14">
<img src="https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI">
<img src="https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white" alt="TypeScript">
</p>
<p align="center">
<strong>National Statistical Competency Intelligence Platform</strong>
</p>
<p align="center">
A unified AI-powered platform for competency assessment, skill-gap
intelligence, personalized learning, document-grounded quizzes, and
workforce capability development.
</p>
<p align="center">
<a href="https://stat-skill-ai-psi.vercel.app"><strong>🚀 Live
Demo</strong></a>  • 
<a href="https://github.com/syedroshanriyan/stat-skill-SIH-2026"><strong>💻
Repository</strong></a>
</p>

✨ What is STAT-SKILL AI?

STAT-SKILL AI is a competency intelligence platform built around one
core idea:

Don’t recommend learning first. Understand the competency gap
first.

The platform combines user profiling, diagnostic assessment, competency
modeling, deterministic skill-gap analysis, grounded recommendations,
document-to-quiz generation, learning paths, and progress tracking into
one workflow.

It is designed around three connected tracks:

Track

Purpose

Example Focus

🏛️ Government

Statistical workforce capacity building

Official Statistics, survey methodology, sampling, national accounts, indices

🏢 Industry

Analytics and data workforce development

SQL, BI, analytics, econometrics, applied projects

🎓 Academia

Student and curriculum development

Statistics curriculum, competency mapping, internship readiness

The Government track is the primary SIH 2026 problem-context
implementation, while Industry and Academia extend the same competency
intelligence engine to adjacent ecosystems.

🚀 Live Application

Open STAT-SKILL AI →

The deployed frontend is hosted on Vercel.

The backend API is deployed separately and connected to the frontend
through the application’s API/proxy configuration, so the public README
does not need to expose the backend service URL.

🎯 Problem

Most learning platforms answer:

“What courses are available?”

STAT-SKILL AI asks:

“What does this person need to learn next, and what evidence shows
that?”

The platform addresses

Competency being inferred from qualifications instead of demonstrated
ability.

Learners not knowing their exact skill gaps.

Generic recommendations that are not tied to measurable deficiencies.

Difficulty connecting government employees with domain-specific
capacity-building resources.

Learning material being disconnected from assessment.

AI recommendations becoming unreliable when they are not grounded in
structured competency data.

Institutions lacking a continuous view of competency development.

The intended transformation

Profile
   ↓
Diagnostic Assessment
   ↓
Competency Profile
   ↓
Skill-Gap Analysis
   ↓
Grounded Recommendation
   ↓
Personalized Learning
   ↓
Reassessment
   ↓
Updated Competency State

🧠 Core Intelligence Model

STAT-SKILL AI is built around a shared AI Competency Intelligence
Engine.

flowchart LR
    A[User Profile] --> B[Diagnostic Assessment]
    B --> C[Competency Intelligence]
    C --> D[Skill-Gap Engine]
    D --> E[Recommendation Engine]
    E --> F[Personalized Learning]
    F --> G[Reassessment]
    G --> C

    H[Learning Documents] --> I[Document Intelligence]
    I --> J[RAG / Embeddings]
    J --> K[Grounded Quiz Generation]
    K --> B

The important architectural decision is that assessment, competency
state, gap analysis, and recommendations are separate concerns.

This makes the system easier to explain, test, extend, and adapt to new
sectors.

🏛️ Government Track

The Government track is the primary SIH-oriented workflow.

It focuses on competency development within the Official Statistical
System, including areas such as:

Survey methodology

Sampling methodology

Statistical analysis

National accounts

Price indices

Official statistical data production

Statistical workflows

Role-specific statistical competencies

The platform’s catalogue/provider architecture also supports
government-oriented learning sources such as:

iGOT Karmayogi

NSSTA

Other configured government training resources

Government workflow

flowchart TD
    A[Government Officer] --> B[Profile + Role]
    B --> C[Diagnostic Assessment]
    C --> D[Competency Profile]
    D --> E[Skill-Gap Analysis]
    E --> F[iGOT / NSSTA / Relevant Resources]
    F --> G[Personalized Learning Path]
    G --> H[Practice + Assessment]
    H --> I[Reassessment]
    I --> D

🏢 Industry Track

The same competency engine can support analytics-oriented professional
development.

Example competency areas include:

SQL

Data analytics

Business intelligence

Econometrics

Statistical modeling

Data interpretation

Applied analytical projects

The architecture allows industry roles and competency frameworks to be
added without rebuilding the core assessment and recommendation
infrastructure.

🎓 Academia Track

The Academia track extends the platform toward education and
employability.

Potential use cases include:

Statistics curriculum mapping

Course Outcome alignment

Student competency assessment

Skill-gap identification

Internship readiness

Personalized learning recommendations

Progress monitoring

This creates a bridge from academic learning → demonstrated competency
→ industry/government readiness.

📊 Key Capabilities

Capability

What it does

🧪 Diagnostic Assessment

Establishes a measurable competency baseline

🧠 Competency Intelligence

Maintains competency state, level, evidence, and history

📉 Skill-Gap Analysis

Compares current competency against required proficiency

🎯 Recommendations

Maps identified gaps to relevant learning resources

🗺️ Learning Paths

Converts gaps into structured learning journeys

📄 Document Intelligence

Extracts knowledge from uploaded learning material

🤖 AI Quiz Generation

Generates MCQs grounded in source material

🔎 RAG / Embeddings

Supports semantic retrieval over indexed content

📈 Progress Analytics

Tracks competency development over time

🗂️ Evidence

Supports evidence-oriented competency development

🏛️ Multi-Track Architecture

Government, Industry, and Academia on one engine

📄 Document → Knowledge → Quiz

One of the platform’s important workflows is turning learning material
into assessment content.

Supported document processing includes:

PDF

DOCX

PPTX

flowchart LR
    A[Upload Document] --> B[Text Extraction]
    B --> C[Chunking]
    C --> D[Embeddings / Knowledge Layer]
    D --> E[Relevant Context]
    E --> F[AI Quiz Generation]
    F --> G[Grounded MCQs]
    G --> H[Assessment]

Generated questions can contain:

Question

Multiple options

Correct answer

Explanation

Difficulty

Competency mapping

Source/page reference where available

The objective is to keep generated assessment content connected to the
material from which it was produced.

🤖 AI-Assisted Quiz Generation

The backend supports Google Gemini-based generation when an API key is
configured.

The quiz pipeline can use:

Source Material
      ↓
Relevant Content
      ↓
AI Generation
      ↓
Structured MCQ
      ↓
Validation / Normalization
      ↓
Assessment

The system also contains deterministic fallback behavior for
development/testing environments where the external AI service is
unavailable.

This prevents the complete application from becoming unusable simply
because an AI provider is temporarily unavailable.

🎯 Skill-Gap Intelligence

STAT-SKILL AI separates measurement from recommendation.

Conceptually:

Required Proficiency
        │
        ▼
┌──────────────────┐
│ Required Level   │
└────────┬─────────┘
         │
         │ comparison
         ▼
┌──────────────────┐
│ Current Ability  │
└────────┬─────────┘
         │
         ▼
┌──────────────────┐
│ Skill Gap        │
│ + Priority       │
└──────────────────┘

A competency gap can be represented through values such as:

Current score

Required score

Gap value

Priority

Status

Last updated time

This provides an explicit basis for recommendations rather than relying
only on free-form AI output.

🧩 Recommendation Engine

The recommendation layer is designed as a hybrid system.

Current Competency
        +
Required Competency
        +
Gap Priority
        +
Track
        +
Resource Relevance
        +
Provider / Catalogue
        ↓
Recommendation

For example, a Government-track competency gap can be mapped toward
configured government-oriented resources instead of returning arbitrary
internet content.

This makes recommendations more traceable and domain-aware.

🔎 RAG & Embedding Architecture

The backend contains an embedding and retrieval layer for
document-grounded intelligence.

flowchart TD
    A[Document] --> B[Extraction]
    B --> C[Chunks]
    C --> D[Embedding]
    D --> E[(Vector Store)]
    F[User Query / Quiz Request] --> G[Query Embedding]
    G --> E
    E --> H[Relevant Context]
    H --> I[AI Generation]
    I --> J[Grounded Output]

The architecture supports:

Google model-based embeddings when configured.

Deterministic fallback embeddings for offline/testing scenarios.

PostgreSQL with pgvector for vector-search-oriented deployments.

SQLite for lightweight local development.

🔄 Continuous Competency Lifecycle

Assessment is not intended to be an isolated event.

stateDiagram-v2
    [*] --> Profile
    Profile --> Assessment
    Assessment --> CompetencyState
    CompetencyState --> GapAnalysis
    GapAnalysis --> Recommendations
    Recommendations --> Learning
    Learning --> Reassessment
    Reassessment --> CompetencyState

The resulting feedback loop is:

Assess → Diagnose → Learn → Reassess → Update

This allows competency development to be treated as a continuous process
instead of a one-time quiz score.

🏗️ System Architecture

flowchart TB
    U[Browser / User] --> W[Next.js Web Application]

    W --> P[Next.js API Proxy]
    P --> A[FastAPI Backend]

    A --> AUTH[Authentication]
    A --> COMP[Competency Engine]
    A --> ASSESS[Assessment Engine]
    A --> GAP[Skill-Gap Engine]
    A --> REC[Recommendation Engine]
    A --> DOC[Document Intelligence]
    A --> QUIZ[Quiz Engine]
    A --> RAG[RAG / Embedding Layer]
    A --> ANALYTICS[Analytics]
    A --> EVIDENCE[Evidence]

    A --> DB[(SQLite / PostgreSQL)]
    RAG --> VDB[(PostgreSQL + pgvector)]
    DOC --> AI[Google Gemini]
    QUIZ --> AI

🧱 Repository Architecture

stat-skill-SIH-2026/
│
├── apps/
│   ├── web/                         # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/
│   │   │   └── components/
│   │   ├── Dockerfile
│   │   └── package.json
│   │
│   └── api/                         # FastAPI backend
│       ├── app/
│       │   ├── admin/
│       │   ├── analytics/
│       │   ├── assessments/
│       │   ├── assistant/
│       │   ├── auth/
│       │   ├── catalogues/
│       │   ├── competencies/
│       │   ├── core/
│       │   ├── documents/
│       │   ├── evidence/
│       │   ├── frameworks/
│       │   ├── gaps/
│       │   ├── health/
│       │   ├── learning_paths/
│       │   ├── legal/
│       │   ├── models/
│       │   ├── quizzes/
│       │   ├── rag/
│       │   ├── recommendations/
│       │   ├── schemas/
│       │   ├── scraper/
│       │   ├── users/
│       │   └── main.py
│       ├── tests/
│       └── requirements.txt
│
├── packages/
│   └── shared-types/                # Shared type definitions
│
├── scripts/                         # Startup / development scripts
├── uploads/                         # Upload-related project resources
├── docker-compose.yml
├── render.yaml
├── railway.json
├── Procfile
├── package.json
└── README.md

🛠️ Technology Stack

Frontend

Technology

Role

Next.js 14

Application framework

React 18

UI layer

TypeScript

Type-safe development

Tailwind CSS

Styling

Recharts

Analytics and visualizations

Lucide React

UI icons

Backend

Technology

Role

Python 3.12

Backend runtime

FastAPI

REST API

Uvicorn

ASGI server

SQLAlchemy 2

ORM

Pydantic 2

Validation and schemas

JWT

Authentication

bcrypt / Passlib

Password hashing

pytest

Testing

AI & Data

Technology

Role

Google Gemini

AI generation / embeddings

RAG

Grounded document intelligence

PostgreSQL

Production-oriented relational database

pgvector

Vector similarity search

SQLite

Lightweight local/deployment option

Deployment

Platform

Role

Vercel

Live frontend deployment

Render

Backend deployment

Docker Compose

Local multi-service environment

Railway

Alternative backend deployment

📁 Backend Domain Modules

The FastAPI backend is organized by domain rather than putting all
business logic into a single application file.

Module

Responsibility

auth

Authentication and identity

users

User profiles

frameworks

Competency frameworks

competencies

Competency definitions and states

assessments

Diagnostic assessments

gaps

Skill-gap calculations

recommendations

Learning recommendations

catalogues

Resource/catalogue management

learning_paths

Personalized learning paths

documents

File/document processing

quizzes

Quiz generation and assessment

rag

Retrieval and embeddings

assistant

AI assistant functionality

evidence

Competency evidence

analytics

Progress and analytics

admin

Administrative operations

health

Health checks

legal

Legal/privacy-related functionality

⚡ Getting Started

Prerequisites

Install:

Node.js 18+

npm

Python 3.11+

Git

Optional:

Docker

Docker Compose

1. Clone the repository

git clone https://github.com/syedroshanriyan/stat-skill-SIH-2026.git
cd stat-skill-SIH-2026

2. Install frontend dependencies

npm install

3. Create a Python environment

Windows

python -m venv .venv
.venv\Scripts\activate

Linux / macOS

python3 -m venv .venv
source .venv/bin/activate

4. Install backend dependencies

pip install -r apps/api/requirements.txt

5. Configure environment variables

Create the required backend environment configuration.

Example:

DATABASE_URL=sqlite:///./statskill.db
JWT_SECRET=replace-with-a-secure-secret
CORS_ORIGINS=http://localhost:3000
GEMINI_API_KEY=your-gemini-api-key

Never commit real API keys, database passwords, JWT secrets, or
production credentials.

6. Start the platform

Recommended

npm start

The repository’s startup script launches the web and API services for
local development.

Frontend only

npm run dev:web

Then open:

http://localhost:3000

🔌 Local API Endpoints

When running through the local proxy, the main application endpoints
include:

Endpoint

Purpose

/

Landing page

/login

Authentication

/register

User registration

/api/v1

Versioned API

/docs

Swagger API documentation

/redoc

ReDoc API documentation

🐳 Docker Setup

The repository includes Docker Compose configuration for a multi-service
environment.

flowchart LR
    B[Browser] --> W[Next.js :3000]
    W --> A[FastAPI :8000]
    A --> D[(PostgreSQL + pgvector :5432)]

Start:

docker compose up --build

Stop:

docker compose down

The Docker configuration provides:

PostgreSQL

pgvector

FastAPI

Next.js

Persistent database volume

Local upload storage

☁️ Deployment

Frontend

The live frontend is deployed on Vercel.

Live URL

https://stat-skill-ai-psi.vercel.app

The frontend is located in:

apps/web

For Vercel deployment, use:

Root Directory: apps/web

Typical environment configuration:

BACKEND_URL=<your-render-backend-url>
NEXT_PUBLIC_API_URL=/api/v1

The public application uses the frontend API/proxy layer, so users do
not need to interact directly with the backend deployment URL.

Backend

The backend is configured for Render using:

render.yaml

The deployment command is:

uvicorn app.main:app --host 0.0.0.0 --port $PORT --app-dir apps/api

The repository also contains:

Procfile

railway.json

for alternative backend deployment.

🧪 Testing

Run backend tests:

python -m pytest apps/api/tests -v

Build the frontend:

npm run build:web

Run frontend linting:

npm run lint:web

🔐 Security & Data Handling

The project includes security-oriented mechanisms such as:

JWT authentication

Password hashing

Configurable CORS

Environment-based secrets

User-scoped data handling

Request/audit-oriented infrastructure

Separation of API, domain, and presentation layers

Production note

The presence of security/privacy modules does not by itself establish
legal or regulatory compliance.

A production deployment should independently validate:

Consent and lawful processing

Data retention

Access control

Encryption

Audit requirements

Data residency

Incident response

DPDP Act obligations

Third-party AI provider data handling

🧭 Design Principles

1. Evidence before assumptions

Competency should be supported by assessment results and evidence rather
than profile claims alone.

2. Gap before recommendation

The system should identify what is missing before deciding what the user
should learn.

3. Grounded AI

AI-generated content should remain connected to source material wherever
the workflow requires grounding.

4. Explainable recommendations

A recommendation should have a reason tied to competency needs, role,
track, or learning resources.

5. Continuous improvement

Assessment results should feed back into competency state and future
recommendations.

6. Modular extensibility

Government, Industry, and Academia should reuse the same intelligence
engine while maintaining separate competency frameworks and resource
mappings.

🔁 End-to-End User Journey

┌──────────────────────┐
│       Register       │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Build Profile        │
│ Education / Role     │
│ Experience / Goal    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Select Track         │
│ Government           │
│ Industry             │
│ Academia             │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Diagnostic           │
│ Assessment           │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Competency Profile   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Skill-Gap Analysis   │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Recommendations      │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Personalized Path    │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Learn + Practice     │
│ + AI-Generated Quiz  │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Reassessment         │
└──────────┬───────────┘
           ↓
┌──────────────────────┐
│ Updated Competency   │
│ + Gap Reduction      │
└──────────────────────┘

🎯 SIH 2026 Requirement Mapping

SIH-oriented requirement

STAT-SKILL AI implementation

Identify competency gaps

Competency + Skill-Gap Engine

Personalized training

Recommendation + Learning Path Engine

Government capacity building

Government Track

iGOT-oriented learning

Government catalogue/provider model

NSSTA-oriented learning

Government catalogue/provider model

AI-enabled assessment

Diagnostic Assessment Engine

Generate MCQs

Document-to-Quiz Pipeline

Uploaded learning material

Document Intelligence + RAG

Personalized learning

Learning Path Engine

Track competency development

Competency History + Analytics

Evidence-based progress

Evidence module

Extend beyond Government

Industry + Academia tracks

📈 Project Status

Implemented

Next.js frontend

FastAPI backend

Authentication architecture

User profiles

Competency frameworks

Diagnostic assessments

Skill-gap analysis

Learning recommendations

Learning-resource catalogues

Learning-path architecture

Document ingestion

AI-assisted quiz generation

RAG / embedding layer

Competency history

Evidence module

Analytics module

Government / Industry / Academia tracks

Docker Compose setup

Render deployment configuration

Vercel frontend deployment configuration

Future / production expansion

Production-grade external catalogue synchronization

Deeper government ecosystem integrations

Larger-scale vector infrastructure

Production observability and monitoring

Formal security/privacy audit

Expanded institutional analytics

Expanded competency frameworks

Additional evidence and credential integrations

🔭 Extensibility

The platform is intentionally designed around a shared competency
engine.

flowchart TB
    C[Shared AI Competency Intelligence Engine]

    C --> G[Government]
    C --> I[Industry]
    C --> A[Academia]

    G --> GF[Official Statistics Frameworks]
    G --> GR[iGOT / NSSTA Resources]

    I --> IF[Industry Skill Frameworks]
    I --> IR[Industry Learning Resources]

    A --> AF[Academic Competency Frameworks]
    A --> AR[Curriculum / Internship Resources]

A new sector can reuse the same core infrastructure while adding:

Competency frameworks

Role definitions

Required proficiency levels

Assessment content

Resource providers

Recommendation mappings

📚 Project Documentation & API

For local development, FastAPI automatically exposes:

Swagger: http://localhost:3000/docs
ReDoc:   http://localhost:3000/redoc

The versioned API is organized under:

/api/v1

This structure allows the backend to evolve without unnecessarily
breaking existing clients.

🤝 Contributing

If extending the project:

Create a feature branch.

Keep business logic inside the appropriate domain module.

Add or update backend tests.

Validate frontend linting.

Validate the production build.

Test API behaviour.

Submit a pull request with a clear description.

Avoid placing domain logic directly inside UI components or oversized
route handlers.

🏆 Smart India Hackathon 2026

STAT-SKILL AI is developed as a Smart India Hackathon 2026 solution
focused on competency intelligence, personalized learning, and capacity
building.

The platform combines:

Artificial Intelligence
        +
Competency Modeling
        +
Skill-Gap Analytics
        +
Document Intelligence
        +
RAG / Embeddings
        +
Personalized Learning
        +
Government Training Ecosystem

into a unified platform.

🔗 Links

Resource

Link

🚀 Live Application

https://stat-skill-ai-psi.vercel.app

💻 GitHub Repository

https://github.com/syedroshanriyan/stat-skill-SIH-2026

STAT-SKILL AI

<p align="center">
<strong>From competency measurement to measurable capability
development.</strong>
</p>
<p align="center">
Built for <strong>Smart India Hackathon 2026</strong>
</p>
