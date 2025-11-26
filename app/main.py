# app/main.py

from fastapi import FastAPI, HTTPException, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

import threading
import webbrowser
import time
import os

from app.agent import run_agent

# imports novos
from io import BytesIO
from PyPDF2 import PdfReader
from docx import Document


# =====================================
# Abre navegador automaticamente
# =====================================
def abrir_navegador_automaticamente():
    time.sleep(1)
    webbrowser.open("http://127.0.0.1:8001")


# =====================================
# Inicialização FastAPI
# =====================================
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =====================================
# Arquivos estáticos (interface)
# =====================================
app.mount("/static", StaticFiles(directory="app/static"), name="static")


@app.get("/")
async def index():
    return FileResponse("app/static/index.html")


# =====================================
# Modelo da requisição
# Agora com session_id
# =====================================
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"  # sessão padrão se não vier no request


# =====================================
# Endpoint principal do Jasper
# =====================================
@app.post("/chat")
async def chat(req: ChatRequest):
    try:
        resposta = run_agent(
            user_message=req.message,
            session_id=req.session_id
        )
        return {"response": resposta}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# novo endpoint de upload de arquivos (PDF / DOCX)
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        content = await file.read()
        text = ""

        if file.filename.lower().endswith(".pdf"):
            reader = PdfReader(BytesIO(content))
            for page in reader.pages:
                text += page.extract_text() or ""

        elif file.filename.lower().endswith((".docx", ".doc")):
            doc = Document(BytesIO(content))
            for para in doc.paragraphs:
                text += para.text + "\n"
        else:
            raise HTTPException(status_code=400, detail="Formato de arquivo não suportado.")

        # Envia para o agente com um prompt (limita o conteúdo para evitar sobrecarga)
        resumo = run_agent(f"Resuma o seguinte conteúdo de forma clara e objetiva:\n\n{text[:4000]}", session_id="docs-session")

        return {"summary": resumo}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# =====================================
# Evento on startup
# =====================================
@app.on_event("startup")
def startup_event():
    threading.Thread(
        target=abrir_navegador_automaticamente,
        daemon=True
    ).start()
