from fastapi import FastAPI
from core.config import settings  
from api.api import api_router

app = FastAPI(
  title= settings.PROJECT_NAME,
  version= settings.PROJECT_VERSION,
  description= "This is a Social Media API"
)

app.include_router(api_router)