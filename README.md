# STAT-SKILL AI

### AI-Powered Competency Intelligence Platform

**Assess → Diagnose → Learn → Reassess**

A unified competency intelligence platform for **Government, Industry,
and Academia**, built to turn profile data and measurable assessments
into explainable skill-gap insights, grounded learning pathways,
document-based quizzes, and continuous competency development.

[![Live
Demo](https://img.shields.io/badge/Live%20Demo-STAT--SKILL%20AI-143326?style=for-the-badge&logo=vercel&logoColor=white)](https://stat-skill-ai-psi.vercel.app)
[![SIH
2026](https://img.shields.io/badge/Smart%20India%20Hackathon-2026-0F766E?style=for-the-badge)](https://www.sih.gov.in/)
[![Next.js](https://img.shields.io/badge/Next.js-14-111827?style=for-the-badge&logo=next.js&logoColor=white)](https://nextjs.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Python-009688?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5.x-3178C6?style=for-the-badge&logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Ready-336791?style=for-the-badge&logo=postgresql&logoColor=white)](https://www.postgresql.org/)

**[Launch the Live Platform →](https://stat-skill-ai-psi.vercel.app)**

------------------------------------------------------------------------

## Table of Contents

-   [Overview](#-overview)
-   [The Problem](#-the-problem)
-   [The STAT-SKILL Approach](#-the-stat-skill-approach)
-   [Core Intelligence Engine](#-core-intelligence-engine)
-   [Three Specialized Tracks](#-three-specialized-tracks)
-   [Key Capabilities](#-key-capabilities)
-   [How It Works](#-how-it-works)
-   [Document-to-Quiz Intelligence](#-document-to-quiz-intelligence)
-   [Skill-Gap Intelligence](#-skill-gap-intelligence)
-   [Platform Architecture](#-platform-architecture)
-   [Technology Stack](#-technology-stack)
-   [Repository Structure](#-repository-structure)
-   [Application Routes](#-application-routes)
-   [Getting Started](#-getting-started)
-   [Environment Variables](#-environment-variables)
-   [Docker](#-docker)
-   [Testing & Build](#-testing--build)
-   [Deployment](#-deployment)
-   [Security & Data Handling](#-security--data-handling)
-   [Design Principles](#-design-principles)
-   [Project Status](#-project-status)
-   [Contributing](#-contributing)
-   [License](#-license)

------------------------------------------------------------------------

## ✨ Overview

**STAT-SKILL AI** is a competency intelligence platform designed around
a simple principle:

> **Do not recommend learning before understanding the competency gap.**

Instead of behaving like a conventional course catalogue, STAT-SKILL AI
creates a closed-loop competency workflow:

``` text
Profile
   ↓
Diagnostic Assessment
   ↓
Competency Profile
   ↓
Skill-Gap Analysis
   ↓
Grounded Recommendations
   ↓
Personalized Learning Path
   ↓
Practice / Evidence
   ↓
Reassessment
   ↓
Updated Competency State
```

The platform uses one shared intelligence architecture while supporting
three distinct ecosystems:

  -----------------------------------------------------------------------
  Track                   Primary Purpose         Example Competencies
  ----------------------- ----------------------- -----------------------
  🏛️ **Government**       Statistical workforce   Survey methodology,
                          capacity building       sampling, national
                                                  accounts, price
                                                  indices, official
                                                  statistics

  🏢 **Industry**         Analytics &             SQL, BI, data
                          professional            analytics,
                          development             econometrics,
                                                  statistical modelling

  🎓 **Academia**         Curriculum &            Course outcomes,
                          employability alignment competency mapping,
                                                  internship readiness
  -----------------------------------------------------------------------

The **Government track is the primary SIH-oriented implementation**,
while Industry and Academia extend the same competency engine to
adjacent use cases.

------------------------------------------------------------------------

## 🎯 The Problem

Traditional learning systems usually start with:

> **"Here are the courses available."**

STAT-SKILL AI starts with:

> **"What competency does this person currently demonstrate, what level
> is required, and what is the measurable gap?"**

### Problems addressed

-   Competency is often inferred from qualifications rather than
    demonstrated ability.
-   Learners may not know which specific skills are below the required
    level.
-   Generic course recommendations are not necessarily tied to
    measurable deficiencies.
-   Government statistical capacity building requires domain-specific
    competency pathways.
-   Learning material and assessment frequently exist as disconnected
    workflows.
-   Free-form AI recommendations can become unreliable when they are not
    grounded in structured competency data.
-   Institutions need a continuous view of competency development rather
    than isolated test scores.

------------------------------------------------------------------------

## 🧠 The STAT-SKILL Approach

The platform separates **measurement**, **diagnosis**, and
**recommendation**.

``` mermaid
flowchart LR
    A["User Profile"] --> B["Diagnostic Assessment"]
    B --> C["Competency State"]
    C --> D["Skill-Gap Engine"]
    D --> E["Recommendation Engine"]
    E --> F["Learning Path"]
    F --> G["Practice / Evidence"]
    G --> H["Reassessment"]
    H --> C

    I["Learning Documents"] --> J["Document Intelligence"]
    J --> K["Retrieval / Embeddings"]
    K --> L["Grounded Quiz Generation"]
    L --> B
```

### Why this architecture matters

-   **Assessment is deterministic** rather than delegated entirely to an
    LLM.
-   **Skill gaps are explicitly calculated** against defined targets.
-   **Recommendations have a reason**: competency, role, track,
    priority, and resource relevance.
-   **AI is grounded** where the workflow requires source-based
    generation.
-   **Competency state persists** so improvement can be measured over
    time.
-   The same engine can support different competency frameworks without
    rebuilding the entire platform.

------------------------------------------------------------------------

## 🧩 Core Intelligence Engine

At the centre of STAT-SKILL AI is a shared **AI Competency Intelligence
Engine**.

``` mermaid
flowchart TD
    P["Profile + Role"] --> A["Diagnostic Assessment"]
    A --> C["Competency Intelligence"]
    C --> G["Gap Analysis"]
    G --> R["Recommendation Engine"]
    R --> L["Personalized Learning"]
    L --> E["Evidence / Practice"]
    E --> RA["Reassessment"]
    RA --> C

    D["PDF / DOCX / PPTX"] --> DI["Document Intelligence"]
    DI --> CH["Chunking"]
    CH --> EMB["Embeddings / Retrieval"]
    EMB --> Q["Grounded Quiz Generation"]
    Q --> A
```

### Core separation of concerns

  -----------------------------------------------------------------------
  Layer                               Responsibility
  ----------------------------------- -----------------------------------
  **Assessment Engine**               Establishes measurable competency
                                      baselines

  **Competency Engine**               Maintains proficiency state and
                                      history

  **Gap Engine**                      Calculates shortfalls against
                                      required levels

  **Recommendation Engine**           Maps gaps to relevant learning
                                      resources

  **Learning Path Engine**            Converts gaps into sequenced
                                      development plans

  **Document Intelligence**           Extracts knowledge from uploaded
                                      material

  **RAG / Retrieval Layer**           Retrieves relevant source context

  **Quiz Engine**                     Produces structured,
                                      source-grounded assessments

  **Analytics**                       Aggregates competency and learning
                                      progress

  **Evidence Layer**                  Stores competency-related evidence
                                      and submissions
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 🏛️ Three Specialized Tracks

## 1. Government --- Official Statistics

The Government track is the primary SIH-oriented workflow.

It is designed around statistical workforce capacity building and
includes competency areas such as:

-   Survey methodology
-   Sampling methodology
-   Statistical analysis
-   National accounts
-   CPI / WPI and price indices
-   Official statistical data production
-   Statistical workflows
-   Role-specific statistical competencies

### Government workflow

``` mermaid
flowchart LR
    A["Officer Profile"] --> B["Role & Cadre Mapping"]
    B --> C["Diagnostic Assessment"]
    C --> D["Competency Profile"]
    D --> E["Skill-Gap Analysis"]
    E --> F["iGOT / NSSTA Resources"]
    F --> G["Personalized Learning Path"]
    G --> H["Practice + Assessment"]
    H --> I["Reassessment"]
    I --> D
```

The catalogue architecture supports government-oriented learning sources
such as:

-   **iGOT Karmayogi**
-   **NSSTA**
-   Other configured government training resources

------------------------------------------------------------------------

## 2. Industry --- Analytics & Professional Development

The Industry track reuses the same competency intelligence engine for
professional analytics roles.

Example competency areas:

-   SQL
-   Data analytics
-   Business intelligence
-   Econometrics
-   Statistical modelling
-   Data interpretation
-   Applied analytical projects
-   Role-oriented skill development

``` text
Target Role
    ↓
Role Requirements
    ↓
Current Competency
    ↓
Skill Gap
    ↓
Learning + Projects
    ↓
Evidence
    ↓
Reassessment
```

------------------------------------------------------------------------

## 3. Academia --- Curriculum & Employability

The Academia track connects academic learning with demonstrated
competency.

Potential workflows include:

-   Curriculum mapping
-   Course Outcome alignment
-   Student competency assessment
-   Skill-gap identification
-   Internship readiness
-   Personalized learning
-   Evidence portfolio development

``` text
Coursework
    ↓
Course Outcomes
    ↓
Competency Mapping
    ↓
Student Assessment
    ↓
Skill Gaps
    ↓
Targeted Development
    ↓
Internship / Career Readiness
```

------------------------------------------------------------------------

# 🚀 Key Capabilities

  -----------------------------------------------------------------------
  Capability                          What it does
  ----------------------------------- -----------------------------------
  🧪 **Diagnostic Assessment**        Establishes a measurable competency
                                      baseline

  🧠 **Competency Intelligence**      Maintains proficiency state,
                                      history, and evidence

  📉 **Skill-Gap Analysis**           Compares current proficiency with
                                      required benchmarks

  🎯 **Grounded Recommendations**     Maps gaps to relevant resources

  🗺️ **Learning Paths**               Converts identified gaps into
                                      structured development journeys

  📄 **Document Intelligence**        Extracts content from PDF, DOCX,
                                      and PPTX files

  🤖 **AI Quiz Generation**           Generates structured MCQs from
                                      relevant source material

  🔎 **RAG / Embeddings**             Enables semantic retrieval over
                                      indexed content

  📈 **Progress Analytics**           Tracks competency development and
                                      learning activity

  🗂️ **Evidence Layer**               Supports evidence-oriented
                                      competency development

  🔐 **Track / Tenant Isolation**     Enforces server-side data access
                                      boundaries

  🏛️ **Government Catalogue           Supports iGOT Karmayogi /
  Adapters**                          NSSTA-oriented resource mapping
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# ⚙️ How It Works

STAT-SKILL AI follows a nine-stage competency lifecycle.

``` mermaid
flowchart TD
    S1["01 · Onboarding & Role Mapping"]
    S2["02 · Diagnostic Baseline"]
    S3["03 · Competency Spectrum"]
    S4["04 · Skill-Gap Identification"]
    S5["05 · Learning Roadmap"]
    S6["06 · Grounded Capacity Building"]
    S7["07 · AI Grounded Quizzes"]
    S8["08 · Competency History"]
    S9["09 · Evidence & Oversight"]

    S1 --> S2 --> S3 --> S4 --> S5 --> S6 --> S7 --> S8 --> S9
    S8 --> S3
```

### Stage-by-stage

**01 --- Onboarding & Role Mapping**

The learner selects a sector and role. The platform establishes the
competency framework and target requirements.

**02 --- Diagnostic Baseline**

A structured assessment establishes the learner's starting competency
state.

**03 --- Competency Spectrum**

Scores are mapped into defined proficiency tiers and visualized through
the competency dashboard.

**04 --- Skill-Gap Identification**

Current proficiency is compared with target requirements and shortfalls
are prioritized.

**05 --- Learning Roadmap**

The recommendation layer converts priority gaps into an ordered learning
pathway.

**06 --- Grounded Capacity Building**

Relevant resources are mapped from configured catalogues, including
government-oriented iGOT / NSSTA pathways.

**07 --- AI Grounded Quizzes**

Uploaded manuals, circulars, textbooks, or learning material can be
transformed into source-grounded assessment content.

**08 --- Competency History**

Assessment events update persisted competency state and maintain
historical changes.

**09 --- Evidence & Oversight**

Learners can build competency evidence while institutional views can
aggregate workforce-level insights within authorized scopes.

------------------------------------------------------------------------

# 📄 Document-to-Quiz Intelligence

One of the platform's key workflows is converting learning material into
assessment content.

### Supported source formats

-   PDF
-   DOCX
-   PPTX

### Pipeline

``` mermaid
flowchart LR
    A["Upload Document"] --> B["Text Extraction"]
    B --> C["Chunking"]
    C --> D["Embedding / Knowledge Layer"]
    D --> E["Relevant Context"]
    E --> F["AI Generation"]
    F --> G["Validation / Normalization"]
    G --> H["Grounded MCQs"]
    H --> I["Assessment"]
```

Generated assessment content can contain:

-   Question
-   Multiple options
-   Correct answer
-   Explanation
-   Difficulty
-   Competency mapping
-   Source / page reference where available

The objective is to keep generated assessment content connected to the
source material used to generate it.

------------------------------------------------------------------------

# 🤖 AI + Grounded Generation

The backend supports Google Gemini-based generation when the required
API configuration is available.

Conceptually:

``` text
Source Material
      ↓
Relevant Context
      ↓
AI Generation
      ↓
Structured MCQ
      ↓
Validation / Normalization
      ↓
Assessment
```

The repository also includes deterministic fallback behavior for
development and testing scenarios where an external AI service is
unavailable.

This makes AI-assisted workflows less dependent on a single provider
being available at every moment.

------------------------------------------------------------------------

# 📉 Skill-Gap Intelligence

STAT-SKILL AI deliberately separates **measurement** from
**recommendation**.

``` text
Required Proficiency
        │
        ▼
┌─────────────────────┐
│ Required Level      │
└──────────┬──────────┘
           │
           │ comparison
           ▼
┌─────────────────────┐
│ Current Ability     │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────┐
│ Skill Gap           │
│ + Priority          │
└─────────────────────┘
```

A competency record can incorporate values such as:

-   Current score
-   Required score / level
-   Gap
-   Priority
-   Status
-   Assessment attempt
-   Confidence / history metadata
-   Last update

This provides a structured basis for recommendations instead of relying
only on free-form AI output.

------------------------------------------------------------------------

# 🏗️ Platform Architecture

``` mermaid
flowchart TB
    U["Browser / User"]

    U --> W["Next.js Web Application"]
    W --> P["Next.js API Proxy"]
    P --> A["FastAPI Backend"]

    A --> AUTH["Authentication"]
    A --> COMP["Competency Engine"]
    A --> ASS["Assessment Engine"]
    A --> GAP["Skill-Gap Engine"]
    A --> REC["Recommendation Engine"]
    A --> LP["Learning Paths"]
    A --> DOC["Document Intelligence"]
    A --> QUIZ["Quiz Engine"]
    A --> RAG["RAG / Embeddings"]
    A --> ANA["Analytics"]
    A --> EVI["Evidence"]

    A --> DB[("SQLite / PostgreSQL")]
    RAG --> VDB[("PostgreSQL + pgvector")]

    DOC --> AI["Google Gemini"]
    QUIZ --> AI
```

### Architectural characteristics

-   **Frontend / backend separation**
-   **Next.js reverse proxy for API access**
-   **Domain-oriented FastAPI modules**
-   **SQLAlchemy-based persistence**
-   **SQLite for lightweight development**
-   **PostgreSQL + pgvector for production-oriented retrieval**
-   **Provider-aware AI generation**
-   **Server-side authorization and data isolation**
-   **Modular competency frameworks**
-   **Reusable engine across Government, Industry, and Academia**

------------------------------------------------------------------------

# 🛠️ Technology Stack

## Frontend

  Technology           Purpose
  -------------------- ----------------------------------
  **Next.js 14**       Application framework
  **React 18**         UI layer
  **TypeScript 5.x**   Type-safe development
  **Tailwind CSS**     Design system and styling
  **Recharts**         Analytics and data visualization
  **Lucide React**     Interface icons

## Backend

  Technology             Purpose
  ---------------------- ------------------------
  **Python 3.12**        Backend runtime
  **FastAPI**            REST API
  **Uvicorn**            ASGI server
  **SQLAlchemy 2**       ORM / persistence
  **Pydantic 2**         Validation and schemas
  **JWT**                Authentication
  **bcrypt / Passlib**   Password hashing
  **pytest**             Backend testing

## AI & Data

  Technology          Purpose
  ------------------- --------------------------------------------
  **Google Gemini**   AI generation / embeddings when configured
  **RAG**             Grounded document intelligence
  **PostgreSQL**      Production-oriented relational database
  **pgvector**        Vector similarity search
  **SQLite**          Lightweight local database

## Deployment

  Platform             Role
  -------------------- ----------------------------------------------
  **Vercel**           Live frontend deployment
  **Render**           Backend deployment
  **Docker Compose**   Local multi-service environment
  **Railway**          Alternative backend deployment configuration

------------------------------------------------------------------------

# 📁 Repository Structure

``` text
stat-skill-SIH-2026/
│
├── apps/
│   ├── web/                         # Next.js frontend
│   │   ├── src/
│   │   │   ├── app/                 # Pages and application routes
│   │   │   └── components/          # Shared UI components
│   │   ├── Dockerfile
│   │   ├── package.json
│   │   └── vercel.json
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
│   └── shared-types/                # Shared TypeScript types
│
├── scripts/                         # Startup, seed and test utilities
├── infra/                           # Infrastructure placeholders/config
├── uploads/                         # Upload storage directory
├── docker-compose.yml
├── render.yaml
├── railway.json
├── Procfile
├── package.json
└── README.md
```

------------------------------------------------------------------------

# 🧭 Application Routes

The public web application currently exposes dedicated experiences for
the major platform areas.

  Route                   Purpose
  ----------------------- ----------------------------------------
  `/`                     Platform landing page
  `/login`                Authentication
  `/register`             Learner registration
  `/government`           Government / Official Statistics track
  `/industry`             Industry / analytics track
  `/academia`             Academia / curriculum track
  `/features`             Platform capabilities
  `/how-it-works`         Competency lifecycle
  `/legal-intelligence`   Statutory / legal intelligence area
  `/faq`                  Frequently asked questions

The authenticated application contains dashboard areas for competency,
assessments, gaps, recommendations, learning paths, documents, quizzes,
evidence, analytics, and related workflows.

------------------------------------------------------------------------

# ⚡ Getting Started

## Prerequisites

Install:

-   **Node.js 18+**
-   **npm**
-   **Python 3.11+**
-   **Git**

Optional:

-   Docker
-   Docker Compose

------------------------------------------------------------------------

## 1. Clone the Repository

``` bash
git clone https://github.com/syedroshanriyan/stat-skill-SIH-2026.git
cd stat-skill-SIH-2026
```

------------------------------------------------------------------------

## 2. Install Frontend Dependencies

``` bash
npm install
```

------------------------------------------------------------------------

## 3. Create a Python Virtual Environment

### Windows

``` bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

``` bash
python3 -m venv .venv
source .venv/bin/activate
```

------------------------------------------------------------------------

## 4. Install Backend Dependencies

``` bash
pip install -r apps/api/requirements.txt
```

------------------------------------------------------------------------

## 5. Configure Environment Variables

Create the required environment configuration for the backend.

Example:

``` env
DATABASE_URL=sqlite:///./statskill.db
JWT_SECRET=replace-with-a-secure-secret
CORS_ORIGINS=http://localhost:3000
GEMINI_API_KEY=your-gemini-api-key
```

> **Never commit real API keys, database credentials, JWT secrets, or
> production environment values.**

------------------------------------------------------------------------

## 6. Start the Platform

### Recommended

``` bash
npm start
```

The repository's startup script launches the web and API services for
local development.

### Frontend only

``` bash
npm run dev:web
```

Then open:

``` text
http://localhost:3000
```

------------------------------------------------------------------------

# 🔌 Local API Access

When running through the local proxy, the main application endpoints
include:

  Endpoint      Purpose
  ------------- -------------------------------
  `/`           Landing page
  `/login`      Authentication
  `/register`   Registration
  `/api/v1`     Versioned API
  `/docs`       FastAPI Swagger documentation
  `/redoc`      FastAPI ReDoc documentation

------------------------------------------------------------------------

# 🐳 Docker

The repository includes Docker Compose configuration for a multi-service
environment.

``` mermaid
flowchart LR
    B["Browser"] --> W["Next.js :3000"]
    W --> A["FastAPI :8000"]
    A --> D[("PostgreSQL + pgvector")]
```

Start the environment:

``` bash
docker compose up --build
```

Stop it:

``` bash
docker compose down
```

The Docker configuration is intended to support:

-   Next.js
-   FastAPI
-   PostgreSQL
-   pgvector
-   Persistent database storage
-   Local upload storage

------------------------------------------------------------------------

# 🧪 Testing & Build

## Backend tests

``` bash
python -m pytest apps/api/tests -v
```

## Frontend production build

``` bash
npm run build:web
```

## Frontend linting

``` bash
npm run lint:web
```

------------------------------------------------------------------------

# ☁️ Deployment

## Live Application

The public application is deployed on Vercel:

### **https://stat-skill-ai-psi.vercel.app**

[![Open Live
Application](https://img.shields.io/badge/OPEN%20LIVE%20APPLICATION-143326?style=for-the-badge&logo=vercel&logoColor=white)](https://stat-skill-ai-psi.vercel.app)

### Frontend deployment

The frontend lives in:

``` text
apps/web
```

For Vercel:

``` text
Root Directory: apps/web
```

The application uses the frontend API/proxy layer so the public README
does not need to expose the backend service URL.

### Backend deployment

The repository is configured for a separate Render backend deployment
through:

``` text
render.yaml
```

The backend deployment is intentionally kept behind the application's
API/proxy configuration rather than presented as a public-facing project
URL.

Alternative backend deployment configuration is also included through:

``` text
Procfile
railway.json
```

------------------------------------------------------------------------

# 🔐 Security & Data Handling

STAT-SKILL AI includes security-oriented architecture such as:

-   JWT-based authentication
-   Password hashing
-   Configurable CORS
-   Environment-based secret management
-   User-scoped data access
-   Server-side authorization
-   Track / tenant isolation
-   Audit-oriented infrastructure
-   Separation between presentation, API, and domain logic
-   Permission-aware document and retrieval workflows

### Important

Security features in the codebase should **not automatically be
interpreted as a legal or regulatory compliance certification**.

A production deployment should independently validate:

-   Consent and lawful processing
-   Data retention
-   Access control
-   Encryption
-   Audit requirements
-   Data residency
-   Incident response
-   Applicable DPDP Act obligations
-   Third-party AI provider data handling

------------------------------------------------------------------------

# 🧭 Design Principles

### 1. Evidence before assumptions

Competency should be supported by assessment results and evidence rather
than profile claims alone.

### 2. Gap before recommendation

The system should identify what is missing before deciding what the
learner should study.

### 3. Grounded AI

When source-grounded generation is required, AI output should remain
connected to the relevant source material.

### 4. Explainable recommendations

A recommendation should have an identifiable relationship to competency
needs, role, track, priority, or learning resources.

### 5. Continuous improvement

Assessment results feed back into competency state and future
recommendations.

### 6. Modular extensibility

Government, Industry, and Academia reuse the same intelligence engine
while maintaining their own competency frameworks and resource mappings.

------------------------------------------------------------------------

# 🔁 Closed-Loop Competency Lifecycle

``` mermaid
stateDiagram-v2
    [*] --> Profile
    Profile --> Assessment
    Assessment --> CompetencyState
    CompetencyState --> GapAnalysis
    GapAnalysis --> Recommendations
    Recommendations --> Learning
    Learning --> Evidence
    Evidence --> Reassessment
    Reassessment --> CompetencyState
```

### The core loop

**Assess → Diagnose → Learn → Practice → Reassess → Update**

This makes competency development a continuous process instead of a
one-time quiz score.

------------------------------------------------------------------------

# 📊 Platform at a Glance

``` text
┌─────────────────────────────────────────────────────────────┐
│                      STAT-SKILL AI                          │
│        National Statistical Competency Intelligence         │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  GOVERNMENT        INDUSTRY          ACADEMIA               │
│  Official Stats    Analytics         Curriculum             │
│       │                │                 │                  │
│       └────────────────┼─────────────────┘                  │
│                        ▼                                    │
│             SHARED COMPETENCY ENGINE                        │
│                        │                                    │
│       ┌────────────────┼────────────────┐                   │
│       ▼                ▼                ▼                   │
│   Assessment       Skill Gaps      Recommendations          │
│       │                │                │                   │
│       └────────────────┼────────────────┘                   │
│                        ▼                                    │
│                Learning Pathways                            │
│                        │                                    │
│                        ▼                                    │
│              Practice / Evidence                            │
│                        │                                    │
│                        ▼                                    │
│                   Reassessment                              │
│                        │                                    │
│                        └──────────────► Updated State       │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

------------------------------------------------------------------------

# 📌 Project Status

  Area                               Status
  ---------------------------------- ----------------
  Next.js frontend                   ✅ Implemented
  FastAPI backend                    ✅ Implemented
  Authentication                     ✅ Implemented
  Government track                   ✅ Implemented
  Industry track                     ✅ Implemented
  Academia track                     ✅ Implemented
  Diagnostic assessments             ✅ Implemented
  Competency / skill-gap workflows   ✅ Implemented
  Recommendations                    ✅ Implemented
  Learning paths                     ✅ Implemented
  Document processing                ✅ Implemented
  AI-assisted quiz generation        ✅ Implemented
  RAG / embedding architecture       ✅ Implemented
  Analytics                          ✅ Implemented
  Evidence workflows                 ✅ Implemented
  Docker configuration               ✅ Included
  Vercel deployment                  ✅ Live
  Render backend configuration       ✅ Included

------------------------------------------------------------------------

# 🌐 Useful Links

  ----------------------------------------------------------------------------------------------------------------------------------------------
  Resource                            Link
  ----------------------------------- ----------------------------------------------------------------------------------------------------------
  🚀 **Live Application**             [stat-skill-ai-psi.vercel.app](https://stat-skill-ai-psi.vercel.app)

  💻 **GitHub Repository**            [github.com/syedroshanriyan/stat-skill-SIH-2026](https://github.com/syedroshanriyan/stat-skill-SIH-2026)

  🏛️ **Smart India Hackathon**        [sih.gov.in](https://www.sih.gov.in/)
  ----------------------------------------------------------------------------------------------------------------------------------------------

------------------------------------------------------------------------

# 🤝 Contributing

Contributions are welcome.

For substantial changes:

1.  Fork the repository.
2.  Create a feature branch.
3.  Make focused changes.
4.  Add or update tests where appropriate.
5.  Verify the frontend build and backend tests.
6.  Open a pull request with a clear description of the change.

Example:

``` bash
git checkout -b feature/your-feature
git add .
git commit -m "feat: add your feature"
git push origin feature/your-feature
```

------------------------------------------------------------------------

# 📄 License

This project is developed for **Smart India Hackathon 2026** and
institutional competency-development use.

See the repository for the applicable licensing terms and project
ownership information.

------------------------------------------------------------------------

## STAT-SKILL AI

**Measure competency. Identify the gap. Build the pathway. Verify the
growth.**

**[🚀 Launch STAT-SKILL AI](https://stat-skill-ai-psi.vercel.app)**

Built for a measurable, evidence-oriented approach to **statistical
capacity building and workforce intelligence**.
