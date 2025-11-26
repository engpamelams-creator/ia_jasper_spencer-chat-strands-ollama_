# app/agent.py

import os
import requests
from dotenv import load_dotenv
from typing import List, Dict

from app.memory.database import init_db, save_message, load_memory

# Carregar .env
load_dotenv()

# Configurações do modelo
AGENT_MODEL = os.getenv("AGENT_MODEL", "llama3.1")
AGENT_TEMPERATURE = float(os.getenv("AGENT_TEMPERATURE", "0.2"))
AGENT_SYSTEM_PROMPT = os.getenv("AGENT_SYSTEM_PROMPT", "").strip()

# Inicializar banco
init_db()

# Limites de segurança
MAX_MEMORY_MESSAGES = 6           # memória curta eficiente
MAX_TOTAL_CHARS = 2500            # evita travamento do Ollama
OLLAMA_URL = "http://localhost:11434/api/chat"


# -----------------------------------------
# 🔧 1. Compactação Inteligente
# -----------------------------------------
def compress_messages(messages: List[Dict[str, str]]) -> List[Dict[str, str]]:
    total = sum(len(m["content"]) for m in messages)

    while total > MAX_TOTAL_CHARS and len(messages) > 2:
        messages.pop(1)  # remove mensagem antiga (depois do system)
        total = sum(len(m["content"]) for m in messages)

    return messages


# -----------------------------------------
# 🔧 2. Construção de mensagens + memória
# -----------------------------------------
def build_messages(session_id: str, user_message: str):
    history = load_memory(session_id, limit=MAX_MEMORY_MESSAGES)

    messages = [{"role": "system", "content": AGENT_SYSTEM_PROMPT}]
    messages.extend(history)
    messages.append({"role": "user", "content": user_message})

    # salvar usuário
    save_message(session_id, "user", user_message)

    # compactar se necessário
    return compress_messages(messages)


# -----------------------------------------
# 🔧 3. Sanitização profissional
# -----------------------------------------
def sanitize(text: str) -> str:
    t = text.strip()
    
    # remover respostas erradas, tools, json, etc
    blacklist = ["```", "<json>", "</json>", "tool:", "<tool>", "</tool>", "{", "}", "[]"]
    for b in blacklist:
        t = t.replace(b, "")
    
    return t.strip()


# -----------------------------------------
# 🤖 4. Função principal do agente
# -----------------------------------------
def run_agent(user_message: str, session_id: str = "default") -> str:

    messages = build_messages(session_id, user_message)

    payload = {
        "model": AGENT_MODEL,
        "stream": False,
        "options": {
            "temperature": AGENT_TEMPERATURE
        },
        "messages": messages
    }

    try:
        response = requests.post(
            OLLAMA_URL,
            json=payload,
            headers={"Connection": "keep-alive"},
            timeout=180   # ← AQUI ESTÁ O TIMEOUT AUMENTADO
        )

        response.raise_for_status()
        data = response.json()

        bot_text = data.get("message", {}).get("content", "").strip()
        if not bot_text:
            bot_text = "Não consegui gerar resposta agora."

        bot_text = sanitize(bot_text)

        # salvar memória da IA
        save_message(session_id, "assistant", bot_text)

        return bot_text

    except requests.exceptions.Timeout:
        return "O modelo demorou mais do que o esperado para responder."

    except Exception as e:
        return f"Erro ao conectar com o modelo: {e}"
