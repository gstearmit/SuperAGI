from fastapi_sqlalchemy import db
from fastapi import HTTPException, Depends, Query, status
from fastapi import APIRouter
from chatdevagi.config.config import get_config
from chatdevagi.helper.auth import check_auth
from chatdevagi.models.knowledge_configs import KnowledgeConfigs
from fastapi_jwt_auth import AuthJWT

router = APIRouter()

@router.get("/marketplace/details/{knowledge_id}")
def get_marketplace_knowledge_configs(knowledge_id: int):
    knowledge_configs = db.session.query(KnowledgeConfigs).filter(KnowledgeConfigs.knowledge_id == knowledge_id).all()
    return knowledge_configs

