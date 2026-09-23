import time
import uuid
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from app.core.config import settings
from app.core.logging import logger

# Import routers
from app.auth.router import router as auth_router
from app.users.router import router as users_router
from app.frameworks.router import router as frameworks_router
from app.competencies.router import router as competencies_router
from app.assessments.router import router as assessments_router
from app.gaps.router import router as gaps_router
from app.recommendations.router import router as recommendations_router
from app.catalogues.router import router as catalogues_router
from app.learning_paths.router import router as learning_paths_router
from app.documents.router import router as documents_router
from app.quizzes.router import router as quizzes_router
from app.assistant.router import router as assistant_router
from app.evidence.router import router as evidence_router
from app.analytics.router import router as analytics_router
from app.admin.router import router as admin_router
from app.health.router import router as health_router
from app.legal.router import router as legal_router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    description="Canonical API for STAT-SKILL AI — AI-Powered Competency Intelligence Platform",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=r"https?://.*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Request ID and Latency Middleware
@app.middleware("http")
async def request_logging_middleware(request: Request, call_next):
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id
    start_time = time.time()

    response = await call_next(request)

    latency_ms = round((time.time() - start_time) * 1000, 2)
    response.headers["X-Request-ID"] = request_id
    response.headers["X-Response-Time-Ms"] = str(latency_ms)

    logger.info(
        f"{request.method} {request.url.path} - Status: {response.status_code} - Latency: {latency_ms}ms"
    )
    return response


# Include Routers under /api/v1
v1_str = settings.API_V1_STR

app.include_router(health_router, prefix=v1_str)
app.include_router(auth_router, prefix=v1_str)
app.include_router(users_router, prefix=v1_str)
app.include_router(frameworks_router, prefix=v1_str)
app.include_router(competencies_router, prefix=v1_str)
app.include_router(assessments_router, prefix=v1_str)
app.include_router(gaps_router, prefix=v1_str)
app.include_router(recommendations_router, prefix=v1_str)
app.include_router(catalogues_router, prefix=v1_str)
app.include_router(learning_paths_router, prefix=v1_str)
app.include_router(documents_router, prefix=v1_str)
app.include_router(quizzes_router, prefix=v1_str)
app.include_router(assistant_router, prefix=v1_str)
app.include_router(evidence_router, prefix=v1_str)
app.include_router(analytics_router, prefix=v1_str)
app.include_router(admin_router, prefix=v1_str)
app.include_router(legal_router, prefix=v1_str)


# Global Root
@app.get("/")
def root():
    return {
        "product": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "architecture": "Three-Track Competency Intelligence Engine (Government, Industry, Academia)",
        "documentation": "/docs",
        "api_v1": v1_str
    }
