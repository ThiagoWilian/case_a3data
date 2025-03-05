from app.schemas.schemas import queryChat
from fastapi import APIRouter

router = APIRouter()


@router.post("/chat")
async def chat_with_bot(query: queryChat):
    resposta = "AGENTE SQL EM BREVE. VOCÊ PODERÁ FAZER PERGUNTAS SOBRE INFORMAÇÕES DO BANCO DE DADOS."
    return {"response": resposta}
