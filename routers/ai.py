from fastapi import APIRouter, HTTPException
from ..services.ai import get_ai_response
from fastapi.responses import StreamingResponse
router = APIRouter()

@router.post("")
async def ai(prompt: str):
    try:
        stream = get_ai_response(prompt)
        return StreamingResponse(stream, media_type="text/event-stream")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

