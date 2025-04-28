from fastapi import APIRouter
from ..services.ai import get_ai_response
from fastapi.responses import StreamingResponse
router = APIRouter()

@router.post("")
async def ai(prompt: str):
    try:
        stream = get_ai_response(prompt)
        return StreamingResponse(stream, media_type="text/event-stream")
    except Exception as e:
        return {"error": str(e)}

