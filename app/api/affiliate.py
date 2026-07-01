from fastapi import APIRouter, HTTPException
from app.schemas.payload import ProductPayload, PostResponse, UrlPayload
from app.services.content_service import ContentService

router = APIRouter()
content_service = ContentService()

@router.post("/generate-post", response_model=PostResponse)
def generate_post(payload: ProductPayload):
    try:
        post_text = content_service.create_telegram_post(payload)
        return PostResponse(telegram_post=post_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-url", response_model=PostResponse)
def process_url(payload: UrlPayload):
    try:
        post_text = content_service.create_post_from_url(payload)

        return PostResponse(telegram_post=post_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))