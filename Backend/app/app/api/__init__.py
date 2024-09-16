from fastapi import APIRouter

api_router = APIRouter()

@api_router.get("/health")
def read_health():
    return {"status": "ok"}