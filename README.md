<p align="center">
  <img src="app/static/avatar.png" alt="Jasper Spencer - Avatar" width="140" />
</p>

<h1 align="center">Jasper Spencer – Assistente IA Local</h1>

<p align="center">
  Assistente IA Local • FastAPI + Ollama • UI estilo ChatGPT
</p>

<p align="center">
  <em>Conversas em português, IA rodando na sua máquina, com memória, upload de arquivos e interface moderna.</em>
</p>

---

## ✨ Visão Geral

O **Jasper Spencer** é um assistente de IA local, pensado como um case técnico completo:

- Backend em **FastAPI**
- Modelo de linguagem rodando via **Ollama** na sua máquina
- **Interface web** estilo ChatGPT/Gemini (HTML + CSS + JS)
- **Memória conversacional** persistente em SQLite
- Upload de **PDF/DOCX** com resumo automático
- Modo **voz** (fala e ouve) usando APIs do navegador

Tudo isso rodando 100% **local** – ideal para estudos, demonstrações técnicas e uso offline.

---

## 🖼 Screenshot

> Exemplo da interface do Jasper em execução:

<p align="center">
  <img src="docs/jasper-screen.png" alt="Screenshot Jasper Spencer" width="850" />
</p>

> 💡 Dica: salve sua imagem em `docs/jasper-screen.png` (ou ajuste o caminho acima).

---

## 🚀 Principais Funcionalidades

- 💬 **Chat em linguagem natural** em português
- 🧠 **Memória conversacional** (SQLite) – o Jasper lembra do contexto recente
- 🧾 **Upload de arquivos PDF/DOC/DOCX** e geração de resumos
- 🔊 **Modo voz**:  
  - Fala → texto → Jasper → resposta  
  - Resposta → voz (text-to-speech)
- 🎨 **UI moderna**:
  - Tema dark com glassmorphism
  - Sidebar estilo ChatGPT
  - Avatar animado do Jasper
  - Sugestões iniciais de prompts
  - Animação de digitação (“Jasper está digitando...” com 3 bolinhas)
- 🗑 **Limpar chat** com um clique (reseta a conversa da interface)
- ⚙️ Configuração via `.env` (modelo do Ollama, temperatura, system prompt)

---

## 🧱 Stack Tecnológica

**Backend**

- [FastAPI](https://fastapi.tiangolo.com/)
- [Uvicorn](https://www.uvicorn.org/)
- [Ollama](https://ollama.com/) (LLM local – ex.: `llama3.1`)
- `requests`
- `python-dotenv`
- `sqlite3`
- `PyPDF2` (PDF)
- `python-docx` (DOC/DOCX)

**Frontend**

- HTML5
- CSS3 (tema dark/light, glassmorphism, animações)
- JavaScript (Axios, Web Speech API, animação de digitação)

---

## 🗂 Estrutura do Projeto

```bash
ia-chat-strands-ollama/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI: rotas /, /chat, /upload, static, CORS
│   ├── agent.py         # Lógica do agente Jasper (Ollama + memória)
│   ├── memory/
│   │   ├── __init__.py
│   │   └── database.py  # init_db, save_message, load_memory (SQLite)
│   └── static/
│       ├── index.html   # Interface do chat
│       ├── style.css    # Estilos (tema dark, sidebar, bolhas, etc.)
│       ├── app.js       # Lógica do front (chat, voz, upload, animações)
│       └── avatar.png   # Avatar do Jasper
├── docs/
│   └── jasper-screen.png   # Screenshot da interface
├── .env                    # Configurações do modelo e do agente (criado por você)
├── .env.example            # Exemplo de .env
├── requirements.txt        # Dependências Python
├── INSTALACAO.md           # (Opcional) Guia passo a passo
└── README.md               # Este arquivo
⚙️ Como Rodar o Projeto Localmente
1. Pré-requisitos
Python 3.10+

Ollama instalado
➜ https://ollama.com/

2. Clonar o repositório
bash
Copiar código
git clone https://github.com/SEU_USUARIO/ia-chat-strands-ollama.git
cd ia-chat-strands-ollama
3. Criar e ativar o ambiente virtual
Windows (PowerShell):

bash
Copiar código
python -m venv .venv
.\.venv\Scripts\Activate.ps1
Windows (cmd):

bash
Copiar código
python -m venv .venv
.\.venv\Scripts\activate
Linux / macOS:

bash
Copiar código
python3 -m venv .venv
source .venv/bin/activate
4. Instalar as dependências
bash
Copiar código
pip install -r requirements.txt
Se necessário, instale também:

bash
Copiar código
pip install PyPDF2 python-docx
5. Configurar o Ollama
Baixar o modelo (ex.: llama3.1):

bash
Copiar código
ollama pull llama3.1
Rodar o servidor do Ollama (em outro terminal):

bash
Copiar código
ollama serve
Deixe esse terminal aberto – é o “motor” da IA.

6. Configurar o .env
Crie um arquivo .env na raiz do projeto (ao lado do requirements.txt) com, por exemplo:

ini
Copiar código
AGENT_MODEL="llama3.1"
AGENT_TEMPERATURE="0.2"
AGENT_SYSTEM_PROMPT="Você é Jasper Spencer – Assistente IA Local. Responda SEMPRE de forma natural, clara e humana.

REGRAS IMPORTANTES E OBRIGATÓRIAS:
1. NUNCA mostre, mencione, descreva ou revele ferramentas internas.
2. NUNCA exiba JSON, tool_calls, código, estruturas internas ou metadados.
3. Sempre que houver números, contas ou expressões matemáticas, faça o cálculo internamente e responda apenas com o resultado final.
4. A resposta ao usuário deve ser SOMENTE o resultado final — humano, natural e direto.
5. Para cálculos, responda apenas: 'A resposta é X.' sem mostrar passos.
6. Para perguntas comuns, responda em 1–2 frases claras.
7. Se o modelo tentar responder em JSON ou formato técnico, ignore isso e devolva apenas texto natural em português."
7. Rodar o backend (FastAPI)
Com a venv ativada:

bash
Copiar código
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
Se tudo der certo, verá algo como:

text
Copiar código
Uvicorn running on http://127.0.0.1:8001
Application startup complete.
8. Abrir o Jasper no navegador
Acesse:

text
Copiar código
http://127.0.0.1:8001/
Pronto! 🎉
Você já pode conversar com o Jasper Spencer, enviar arquivos, usar o modo de voz e testar toda a interface.

🔌 Endpoints
Além da interface web, você pode consumir a API diretamente.

POST /chat
Request

json
Copiar código
{
  "message": "Me explique o que é FastAPI em poucas palavras."
}
Response

json
Copiar código
{
  "response": "FastAPI é um framework web em Python focado em alta performance e construção rápida de APIs."
}
POST /upload
Multipart (PDF/DOC/DOCX)

Retorna um JSON com o resumo do conteúdo do arquivo.

🧠 Memória Conversacional
O módulo app/memory/database.py usa SQLite para salvar:

session_id

role (user ou assistant)

content

created_at

O agent.py:

Carrega as últimas mensagens da sessão

Monta o contexto com:

system prompt

histórico

mensagem atual

Comprime o histórico se ficar muito grande

Envia tudo ao modelo do Ollama

Salva as mensagens novamente no banco

Assim o Jasper lembra do que foi dito recentemente e responde de forma mais coerente.

🗺 Roadmap / Ideias Futuras
Histórico real de conversas na sidebar (multi-sessão)

Autenticação simples para uso em rede local

Dockerfile para rodar tudo containerizado

Integração com outros modelos (OpenAI, Gemini) como fallback

Painel de configurações avançadas direto da interface

👩‍💻 Autoria
Projeto desenvolvido por [SEU NOME / Dev.Pamela MS], como case técnico de Assistente IA Local com Ollama + FastAPI, explorando:

Backend em Python

Integração com LLM local

Frontend moderno e interativo

Memória persistente e manipulação de arquivos

Se este projeto ajudou você de alguma forma, considere deixar uma ⭐ no repositório. 💜
