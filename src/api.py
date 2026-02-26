from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
import uuid, logging
from src.chatbot import CustomerSupportChatbot
app  = FastAPI(title = "Digimind Support API",version = "1.0")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
sessions: dict[str, CustomerSupportChatbot] = {}

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = None
    
class ChatResponse(BaseModel):
    answer:str
    session_id:str
    sources: list[str]
    success: bool
    
@app.get("/")
async def health():
    return {
        "status":"online",
        "service": "Digimind Support Chatbot"
    }

@app.post('/chat', response_model=ChatResponse)
async def chat(req: ChatRequest):

    if not req.message.strip():
        raise HTTPException(400, detail="Message cannot be empty")

    sid = req.session_id or str(uuid.uuid4())

    if sid not in sessions:
        sessions[sid] = CustomerSupportChatbot()

    bot = sessions[sid]
    result = bot.chat(req.message)

    return ChatResponse(
        answer=result["answer"],
        session_id=sid,
        sources=result["sources"],
        success=result["success"]
    )
        
@app.delete('/session/{sid}')
async def clear_session(sid:str):
    if sid in sessions:del sessions[sid]
    return {"cleared": sid}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host = "0.0.0.0", port=8000, reload = True)
        