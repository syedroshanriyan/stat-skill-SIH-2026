from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from app.core.config import settings
from app.models.recommendation import LearningResource, ResourceCompetency
from app.models.competency import Competency


class BaseCatalogueProvider(ABC):
    @abstractmethod
    def search_resources(self, db: Session, query: Optional[str] = None, competency_id: Optional[str] = None) -> List[LearningResource]:
        pass

    @abstractmethod
    def get_resource(self, db: Session, external_id: str) -> Optional[LearningResource]:
        pass

    @abstractmethod
    def get_provider_status(self) -> Dict[str, Any]:
        pass


class IGOTProvider(BaseCatalogueProvider):
    def __init__(self):
        self.api_key = settings.IGOT_API_KEY
        self.has_live_credentials = bool(self.api_key and len(self.api_key) > 5)

    def get_provider_status(self) -> Dict[str, Any]:
        return {
            "provider": "iGOT Karmayogi",
            "type": "igot",
            "is_live": self.has_live_credentials,
            "mode": "LIVE_API" if self.has_live_credentials else "DEMO_CATALOGUE",
            "description": "Integrated Government Online Training platform for civil servants capacity building."
        }

    def search_resources(self, db: Session, query: Optional[str] = None, competency_id: Optional[str] = None) -> List[LearningResource]:
        q = db.query(LearningResource).filter(LearningResource.provider_type == "igot")
        if query:
            q = q.filter(LearningResource.title.ilike(f"%{query}%") | LearningResource.description.ilike(f"%{query}%"))
        if competency_id:
            q = q.join(ResourceCompetency).filter(ResourceCompetency.competency_id == competency_id)
        return q.all()

    def get_resource(self, db: Session, external_id: str) -> Optional[LearningResource]:
        return db.query(LearningResource).filter(
            LearningResource.provider_type == "igot",
            LearningResource.provider_external_id == external_id
        ).first()


class NSSTAProvider(BaseCatalogueProvider):
    def __init__(self):
        self.api_key = settings.NSSTA_API_KEY
        self.has_live_credentials = bool(self.api_key and len(self.api_key) > 5)

    def get_provider_status(self) -> Dict[str, Any]:
        return {
            "provider": "NSSTA TPAC",
            "type": "nssta",
            "is_live": self.has_live_credentials,
            "mode": "LIVE_API" if self.has_live_credentials else "DEMO_CATALOGUE",
            "description": "National Statistical Systems Training Academy Training Programmes for Official Statisticians."
        }

    def search_resources(self, db: Session, query: Optional[str] = None, competency_id: Optional[str] = None) -> List[LearningResource]:
        q = db.query(LearningResource).filter(LearningResource.provider_type == "nssta")
        if query:
            q = q.filter(LearningResource.title.ilike(f"%{query}%") | LearningResource.description.ilike(f"%{query}%"))
        if competency_id:
            q = q.join(ResourceCompetency).filter(ResourceCompetency.competency_id == competency_id)
        return q.all()

    def get_resource(self, db: Session, external_id: str) -> Optional[LearningResource]:
        return db.query(LearningResource).filter(
            LearningResource.provider_type == "nssta",
            LearningResource.provider_external_id == external_id
        ).first()


class IndustryCatalogueProvider(BaseCatalogueProvider):
    def get_provider_status(self) -> Dict[str, Any]:
        return {
            "provider": "Industry Learning Network",
            "type": "industry",
            "is_live": True,
            "mode": "VERIFIED_CATALOGUE",
            "description": "Professional upskilling, certifications, and real-world project specifications."
        }

    def search_resources(self, db: Session, query: Optional[str] = None, competency_id: Optional[str] = None) -> List[LearningResource]:
        q = db.query(LearningResource).filter(LearningResource.provider_type == "industry")
        if query:
            q = q.filter(LearningResource.title.ilike(f"%{query}%") | LearningResource.description.ilike(f"%{query}%"))
        if competency_id:
            q = q.join(ResourceCompetency).filter(ResourceCompetency.competency_id == competency_id)
        return q.all()

    def get_resource(self, db: Session, external_id: str) -> Optional[LearningResource]:
        return db.query(LearningResource).filter(
            LearningResource.provider_type == "industry",
            LearningResource.provider_external_id == external_id
        ).first()


class AcademiaCatalogueProvider(BaseCatalogueProvider):
    def get_provider_status(self) -> Dict[str, Any]:
        return {
            "provider": "Academic Curriculum & Labs",
            "type": "academia",
            "is_live": True,
            "mode": "VERIFIED_CATALOGUE",
            "description": "Higher education courses, university labs, and coursework outcome mapping."
        }

    def search_resources(self, db: Session, query: Optional[str] = None, competency_id: Optional[str] = None) -> List[LearningResource]:
        q = db.query(LearningResource).filter(LearningResource.provider_type == "academia")
        if query:
            q = q.filter(LearningResource.title.ilike(f"%{query}%") | LearningResource.description.ilike(f"%{query}%"))
        if competency_id:
            q = q.join(ResourceCompetency).filter(ResourceCompetency.competency_id == competency_id)
        return q.all()

    def get_resource(self, db: Session, external_id: str) -> Optional[LearningResource]:
        return db.query(LearningResource).filter(
            LearningResource.provider_type == "academia",
            LearningResource.provider_external_id == external_id
        ).first()


PROVIDERS = {
    "igot": IGOTProvider(),
    "nssta": NSSTAProvider(),
    "industry": IndustryCatalogueProvider(),
    "academia": AcademiaCatalogueProvider()
}
