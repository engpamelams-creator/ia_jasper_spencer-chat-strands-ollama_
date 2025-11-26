📖 Guia de Instalação e Execução – Jasper Spencer (IA Local com Ollama)

Este guia mostra, passo a passo, como baixar, instalar e rodar o projeto na sua máquina, desde zero até abrir o chat no navegador.

✅ Pré-requisitos

Antes de tudo, você precisa ter instalado:

Python 3.10 ou superior
➜ Download: https://www.python.org/downloads/

Ollama (motor da IA local)
➜ Download: https://ollama.com/

💡 Sistema operacional: funciona em Windows, macOS ou Linux (desde que o Ollama seja suportado).

1️⃣ Baixar o projeto

No terminal (PowerShell, cmd ou Linux/macOS):

git clone https://github.com/SEU_USUARIO/ia-chat-strands-ollama.git
cd ia-chat-strands-ollama


Troque SEU_USUARIO pelo seu usuário do GitHub.

2️⃣ Criar e ativar o ambiente virtual (venv)
Windows (PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

Windows (Prompt de Comando – cmd)
python -m venv .venv
.\.venv\Scripts\activate

Linux / macOS
python3 -m venv .venv
source .venv/bin/activate


Você saberá que deu certo quando aparecer algo como (.venv) no começo da linha do terminal.

3️⃣ Instalar as dependências Python

Com a venv ativada:

pip install -r requirements.txt


Caso o projeto não tenha ainda no requirements.txt, instale também as libs usadas no upload de arquivos:

pip install PyPDF2 python-docx

4️⃣ Instalar e configurar o Ollama
4.1 Instalar

Siga o instalador do site:
https://ollama.com/

4.2 Baixar o modelo da IA

No terminal:

ollama pull llama3.1


Se quiser usar outro modelo (ex.: phi3, qwen2.5, etc.), é só mudar o nome depois no .env.

4.3 Deixar o servidor do Ollama ligado

Abra um novo terminal e rode:

ollama serve


Deixe esse terminal aberto.
Ele é o “motor” que o Jasper usa por trás.

5️⃣ Configurar o arquivo .env

Na pasta do projeto (ia-chat-strands-ollama), crie um arquivo chamado .env (se ainda não tiver) com algo assim:

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


AGENT_MODEL → nome do modelo do Ollama (tem que ser o mesmo que você deu ollama pull).

AGENT_TEMPERATURE → 0.2 deixa o modelo mais estável.

AGENT_SYSTEM_PROMPT → personalidade e regras do Jasper.

6️⃣ Rodar o backend (FastAPI)

Volte no terminal onde a venv está ativada (.venv) e rode:

uvicorn app.main:app --reload --host 127.0.0.1 --port 8001


Se tudo estiver ok, você verá algo como:

Uvicorn running on http://127.0.0.1:8001
Application startup complete.

7️⃣ Abrir o chat no navegador

Abra seu navegador (Chrome, Edge, etc.) e acesse:

http://127.0.0.1:8001/


Você verá a interface do Jasper Spencer com:

Sidebar

Avatar

Campo de mensagem

Botões de upload, voz, limpar, etc.

Agora é só conversar com a IA 😄

8️⃣ Testando o endpoint /chat (opcional)

Se quiser testar só a API, sem o frontend:

Via curl:
curl -X POST "http://127.0.0.1:8001/chat" ^
  -H "Content-Type: application/json" ^
  -d "{\"message\": \"Me explique rapidamente o que é FastAPI.\"}"


(Em Linux/macOS, tire o ^ e deixe em uma linha só ou use \).

Resposta esperada (exemplo):

{
  "response": "FastAPI é um framework web em Python focado em alta performance e construção rápida de APIs."
}

9️⃣ Envio de arquivos (PDF/DOCX) – via interface

Pela própria tela do Jasper:

Clique no ícone de clipe 📎

Escolha um arquivo .pdf, .doc ou .docx

O backend vai:

ler o arquivo

extrair o texto

pedir ao Jasper um resumo

A resposta aparecerá como uma mensagem do bot.

🔚 Recap rápido

Clonar o projeto

Criar e ativar .venv

pip install -r requirements.txt

Instalar Ollama + ollama pull llama3.1 + ollama serve

Criar .env com AGENT_MODEL, AGENT_TEMPERATURE, AGENT_SYSTEM_PROMPT

uvicorn app.main:app --reload --host 127.0.0.1 --port 8001

Abrir http://127.0.0.1:8001/ no navegador