# 🤖 Jasper Spencer – Assistente IA Local (FastAPI + Ollama)

Este projeto é um **case técnico** que demonstra a criação de um **Assistente de IA local** chamado **“Jasper Spencer”**, com:

- **Backend em FastAPI** (API REST)
- **Modelo de linguagem local via Ollama**
- **Interface web moderna estilo ChatGPT/Gemini (HTML + CSS + JS)**
- **Memória conversacional persistente com SQLite**
- **Upload de PDF/DOCX com resumo automático**
- **Modo de voz (fala e ouve) via Web Speech API (frontend)**
- **Configuração via `.env` para modelo, temperatura e instruções do agente**

O objetivo central é expor um endpoint `/chat` que permita conversar com o agente de IA e, adicionalmente, oferecer recursos extras (memória, arquivos, voz, UI avançada), atendendo e indo além do case proposto pela empresa. :contentReference[oaicite:0]{index=0}  

---

## 🧾 Case original (resumo)

O case solicitado é:

> Desenvolver uma API de Chat simples que se conecta a um Agente de IA, configurado para utilizar uma **tool de cálculo matemático** para operações numéricas, rodando localmente com **Ollama** como LLM, e expor um endpoint `POST /chat` que recebe `message` e retorna `response`. :contentReference[oaicite:1]{index=1}  

Este projeto implementa:

- API FastAPI com `/chat` seguindo o contrato `{"message": "..."} -> {"response": "..."}`  
- Configuração via `.env` para LLM, sistema do agente e parâmetros de execução  
- Execução local com **Ollama** e modelo configurável  
- Lógica de agente dedicada (`app/agent.py`)  
- Ferramentas adicionais além do mínimo exigido:
  - Memória conversacional persistente
  - Interface web em HTML/CSS/JS
  - Upload e leitura de documentos (PDF/DOCX)
  - Voice-to-text e text-to-speech no front

---

## 🛠 Tecnologias Utilizadas

| Tecnologia        | Uso                                                                 |
|------------------|---------------------------------------------------------------------|
| **FastAPI**      | Framework web para a API (`/chat`, `/upload`, `/`)                 |
| **Uvicorn**      | ASGI server para rodar a aplicação FastAPI                         |
| **Ollama**       | Execução local do modelo de linguagem (LLM)                        |
| **Requests**     | Comunicação Python → Ollama (`/api/chat`)                          |
| **SQLite3**      | Banco local para memória conversacional persistente                |
| **python-dotenv**| Leitura das variáveis de ambiente do arquivo `.env`                |
| **PyPDF2**       | Leitura de conteúdo de arquivos PDF                               |
| **python-docx**  | Leitura de arquivos `.doc`/`.docx`                                  |
| **HTML + CSS + JS** | Interface web estilo ChatGPT (com animação de digitação, etc.) |
| **Web Speech API** | Reconhecimento de voz (STT) e fala (TTS) no navegador           |

---

## 📂 Estrutura do Projeto

> Obs.: nomes e caminhos podem variar ligeiramente conforme sua organização, mas a ideia geral é essa.

```bash
ia-chat-strands-ollama/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI: rotas /, /chat, /upload, static, CORS
│   ├── agent.py          # Lógica do agente Jasper (Ollama + memória + sanitização)
│   ├── memory/
│   │   ├── __init__.py
│   │   └── database.py   # Funções de init_db, save_message, load_memory (SQLite)
│   └── static/
│       ├── index.html    # Interface web principal do Jasper
│       ├── style.css     # Tema dark/light, sidebar, bolhas, etc.
│       └── app.js        # Lógica do chat, animação, voz, upload, etc.
├── .env                  # Configurações do modelo e do agente
├── .env.example          # Exemplo de configurações
├── requirements.txt      # Dependências Python
├── INSTALACAO.md         # (Opcional) Guia extra de instalação
└── README.md             # Este documento
⚙️ Configuração e Execução
1. Pré-requisitos
Python 3.10+

Ollama instalado na máquina
👉 https://ollama.com/

(Opcional, mas recomendado) Git e VS Code

2. Clonar o repositório
bash
Copiar código
git clone https://github.com/SEU_USUARIO/ia-chat-strands-ollama.git
cd ia-chat-strands-ollama
3. Criar ambiente virtual e instalar dependências
bash
Copiar código
# Criar venv
python -m venv .venv

# Ativar venv (Windows PowerShell)
.\.venv\Scripts\activate

# Ativar venv (Linux/macOS)
source .venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
4. Configurar o Ollama
Inicie o servidor do Ollama:

bash
Copiar código
ollama serve
Baixe o modelo que será usado no .env (ex.: llama3.1):

bash
Copiar código
ollama pull llama3.1
5. Configurar variáveis de ambiente (.env)
Crie um arquivo .env na raiz do projeto (ao lado de requirements.txt), por exemplo:

ini
Copiar código
AGENT_MODEL="llama3.1"
AGENT_TEMPERATURE="0.2"
AGENT_SYSTEM_PROMPT="Você é Jasper Spencer – Assistente IA Local. Responda SEMPRE de forma natural, clara e humana.

REGRAS IMPORTANTES E OBRIGATÓRIAS:
1. NUNCA mostre, mencione, descreva ou revele ferramentas internas como 'calculator'.
2. NUNCA exiba JSON, tool_calls, código, estruturas internas ou metadados.
3. Sempre que houver números, contas ou expressões matemáticas, faça o cálculo internamente e responda apenas com o resultado final.
4. A resposta ao usuário deve ser SOMENTE o resultado final — humano, natural e direto.
5. Para cálculos, responda apenas: 'A resposta é X.' sem mostrar passos.
6. Para perguntas comuns, responda em 1–2 frases claras.
7. Se o modelo tentar responder em JSON ou formato técnico, ignore isso e devolva apenas texto natural em português."
Você pode ajustar modelo, temperatura e prompt do sistema à vontade.

6. Rodar o backend (FastAPI)
Com a venv ativada e o Ollama rodando, execute:

bash
Copiar código
uvicorn app.main:app --reload --host 127.0.0.1 --port 8001
A API estará acessível em:
👉 http://127.0.0.1:8001

A interface web (frontend) está em:
👉 http://127.0.0.1:8001/

O projeto pode abrir automaticamente o navegador, dependendo da função abrir_navegador_automaticamente() em main.py.

🌐 Endpoints principais
1️⃣ GET /
Retorna a página HTML com o chat do Jasper (index.html).

Essa página consome as rotas /chat e /upload via JavaScript (Axios).

2️⃣ POST /chat
Endpoint principal do case.

Request (JSON):

json
Copiar código
{
  "message": "Explique o que é a linguagem Lua.",
  "session_id": "opcional-id-da-sessao"
}
session_id é opcional; se não fornecido, o backend usa um id padrão (default ou similar).

Response (JSON):

json
Copiar código
{
  "response": "Lua é uma linguagem de programação leve, interpretada e muito utilizada em jogos e sistemas embarcados pela sua velocidade e facilidade de integração."
}
Fluxo interno:

main.py recebe a requisição, valida com Pydantic (ChatRequest).

Envia a mensagem para run_agent() em agent.py.

agent.py:

Carrega histórico recente da sessão via SQLite (load_memory).

Monta o prompt com:

system prompt (AGENT_SYSTEM_PROMPT)

memória (últimas mensagens)

mensagem atual do usuário

Comprime o histórico se estiver muito grande (controle de contexto).

Chama o Ollama (POST http://localhost:11434/api/chat).

Sanitiza a resposta (remove marcas de JSON, tool_call, etc.).

Salva a mensagem do usuário e a resposta do bot no banco (save_message).

Retorna apenas texto natural em português no campo response.

3️⃣ POST /upload
Faz upload de arquivos PDF/DOC/DOCX, extrai o texto e gera um resumo com o agente.

Request (multipart/form-data):

http
Copiar código
POST /upload
Content-Type: multipart/form-data

file: meu-documento.pdf
Response (JSON):

json
Copiar código
{
  "summary": "Resumo objetivo do conteúdo do documento..."
}
Fluxo:

main.py recebe o arquivo em UploadFile.

Se for .pdf, usa PyPDF2 para extrair texto.

Se for .doc / .docx, usa python-docx.

Monta um prompt do tipo:
"Resuma o seguinte conteúdo de forma clara e objetiva: ..." (limitando tamanho)

Chama run_agent() passando esse texto.

Retorna o resumo no campo summary.

🧠 Memória Conversacional (SQLite)
O projeto inclui um módulo de memória em app/memory/database.py com:

init_db()
Cria o banco jasper_memory.db e a tabela de mensagens, caso não existam.

save_message(session_id, role, content)
Salva cada mensagem (usuário ou assistente) com:

session_id

role (user ou assistant)

content

created_at (timestamp)

load_memory(session_id, limit=10)
Carrega as últimas N mensagens de uma sessão, para enviar junto ao prompt e gerar contexto.

No agent.py, essas funções são usadas para:

Construir o histórico de conversa

Manter o contexto entre as mensagens

Controlar o tamanho máximo do contexto enviado ao modelo (compressão pelo número de caracteres)

🎨 Frontend – UI estilo ChatGPT/Gemini
Localizado em app/static/:

index.html

style.css

app.js

Principais recursos da UI
Tema dark com gradiente futurista e glassmorphism

Avatar do Jasper (avatar.png) com glow animado

Sidebar com:

Logo + nome do assistente

Botão "Nova conversa" (limpa o histórico local)

Seção de “Histórico” preparada para expansão futura

Área de "Configurações" / "Sobre" (placeholder para futuras features)

Área central de chat com:

Sugestões iniciais de prompts

Bolhas de mensagem do usuário (direita, gradiente azul) e do bot (esquerda, vidro escuro)

Animação de digitação para respostas do bot (texto aparecendo aos poucos)

Indicador "Jasper está digitando..." com 3 bolinhas animadas

Rodapé com:

Botão 📎 para upload de arquivos (PDF/DOCX)

Botão 🎤 para modo voz (fala com o Jasper)

Campo de texto

Botão de envio (ícone de avião de papel)

Botão 🗑 para limpar o chat (limpa localStorage e recarrega sugestões iniciais)

Suporte a tema claro/escuro, persistido via localStorage

🔊 Modo Voz (STT + TTS)
Implementado no app.js usando APIs nativas do navegador:

TTS (Text-to-Speech)
Usa window.speechSynthesis para o Jasper falar as respostas (pode ser acionado onde você desejar).

STT (Speech-to-Text)
Usa SpeechRecognition/webkitSpeechRecognition para:

Ouvir o microfone

Converter fala em texto

Enviar para o backend automaticamente

⚠ O suporte depende do navegador (Chrome/Edge geralmente OK).

📦 Como este projeto atende ao case
Requisitos principais do case: 
Teste - Estágio IA


Configuração do Ambiente

✅ Uso de .env para configurar modelo, sistem prompt e temperatura.

✅ requirements.txt com todas as dependências (FastAPI, dotenv, etc.).

Implementação da API (FastAPI)

✅ Endpoint POST /chat que recebe { "message": "..." } e retorna { "response": "..." }.

✅ Servidor rodando com uvicorn conforme boas práticas.

Agente de IA

✅ Implementação de um agente central em agent.py.

✅ Integração com LLM local via Ollama.

✅ Capacidade de responder perguntas gerais.

✅ Capacidade de lidar com cálculos numéricos via instruções no AGENT_SYSTEM_PROMPT (o modelo faz os cálculos de forma segura e direta).

Extras além do case

🌟 Memória conversacional persistente com SQLite.

🌟 UI rica estilo ChatGPT/Gemini.

🌟 Upload e leitura de documentos (PDF/DOCX) com resumo automático.

🌟 Modo de voz (voz → texto → IA → texto → voz).

🌟 Estrutura preparada para expansão (novas ferramentas, histórico de conversas, etc.).

🧪 Testes rápidos
Swagger (se exposto em /docs, opcional)
http://127.0.0.1:8001/docs

Testar chat via curl:

bash
Copiar código
curl -X POST "http://127.0.0.1:8001/chat" \
  -H "Content-Type: application/json" \
  -d "{\"message\": \"Quanto é 123 * 45?\"}"
Testar upload (via frontend)
Acesse http://127.0.0.1:8001, clique no ícone de clipe 📎 e envie um PDF/DOCX.

🚀 Próximos passos / ideias de evolução
Implementar histórico real de conversas na sidebar (frontend + backend).

Adicionar autenticação simples/token para uso em rede interna.

Containerizar com Docker para rodar backend + Ollama em um ambiente padronizado.

Adaptar o agente para usar um sistema de “ferramentas” mais formal (ex: integrar novamente com Strands Agents ou outro orchestrator).

Deploy em VPS, expondo o Jasper como assistente privado na nuvem.

Se você estiver usando este projeto como case de estágio, este README já:

Explica o contexto (case da empresa)

Mostra arquitetura e decisões técnicas

Demonstra que você foi além do mínimo (memória, UI, voz, uploads)

Facilita a vida de qualquer avaliador para rodar tudo localmente 💜#   i a _ j a s p e r _ s p e n c e r - c h a t - s t r a n d s - o l l a m a _  
 