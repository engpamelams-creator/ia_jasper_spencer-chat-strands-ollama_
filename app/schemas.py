from pydantic import BaseModel


class ChatRequest(BaseModel):
    """
    Esquema para a requisição do endpoint /chat.
    """
    message: str


class ChatResponse(BaseModel):
    """
    Esquema para a resposta do endpoint /chat.
    """
    response: str
