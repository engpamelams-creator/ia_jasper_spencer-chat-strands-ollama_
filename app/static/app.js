const chat_container = document.getElementById("chatContainer");
const chat_form = document.getElementById("chatForm");
const message_input = document.getElementById("messageInput");
const theme_toggle = document.getElementById("themeToggle");
const clear_chat_btn = document.getElementById("clearChat");
const open_sidebar_btn = document.getElementById("openSidebar");
const close_sidebar_btn = document.getElementById("closeSidebar");
const sidebar = document.getElementById("sidebar");
const suggestion_cards = document.querySelectorAll(".suggestion-card");
const file_btn = document.getElementById("sendFile");
const file_input = document.getElementById("fileInput");
const voice_btn = document.getElementById("voiceBtn");
const new_chat_btn = document.getElementById("newChat");

const API_URL = "/chat";
const SESSION_ID = "pamela-session-1"; // pode mudar se quiser

// Histórico local
let history = JSON.parse(localStorage.getItem("chatHistory") || "[]");
history.forEach(msg => addMessage(msg.text, msg.from, false));

// ============ RENDER MENSAGENS ============
function addMessage(text, from, animate = true) {
  const div = document.createElement("div");
  div.className = `message ${from}`;

  if (from === "bot" && animate) {
    typeWriter(div, text);
  } else {
    div.innerText = text;
  }

  chat_container.appendChild(div);
  chat_container.scrollTop = chat_container.scrollHeight;
}

function saveMessage(text, from) {
  history.push({ text, from });
  localStorage.setItem("chatHistory", JSON.stringify(history));
}

// ============ TYPEWRITER (digitação estilo ChatGPT) ============
function typeWriter(element, text, speed = 15) {
  let i = 0;
  function typing() {
    if (i < text.length) {
      element.innerText += text.charAt(i);
      i++;
      chat_container.scrollTop = chat_container.scrollHeight;
      setTimeout(typing, speed);
    }
  }
  typing();
}

// ============ INDICADOR "Jasper está digitando…" ============
let typingDiv = null;
function showTypingIndicator() {
  if (typingDiv) return;
  typingDiv = document.createElement("div");
  typingDiv.className = "message bot";
  typingDiv.innerHTML = `
    <div class="typing-indicator">
      Jasper está digitando
      <span class="typing-dots">
        <span></span><span></span><span></span>
      </span>
    </div>
  `;
  chat_container.appendChild(typingDiv);
  chat_container.scrollTop = chat_container.scrollHeight;
}

function hideTypingIndicator() {
  if (typingDiv) {
    typingDiv.remove();
    typingDiv = null;
  }
}

// ============ ENVIO AO BACKEND ============
async function sendMessage(text) {
  // Some sugestões
  const suggestions = document.querySelector(".suggestions");
  if (suggestions) suggestions.remove();

  addMessage(text, "user", false);
  saveMessage(text, "user");

  showTypingIndicator();

  try {
    const res = await axios.post(API_URL, {
      message: text,
      session_id: SESSION_ID,
    }, {
      headers: { "Content-Type": "application/json" },
    });

    hideTypingIndicator();

    const data = res.data;
    const botText = data.response || "Sem resposta.";

    addMessage(botText, "bot", true);
    saveMessage(botText, "bot");
  } catch (err) {
    hideTypingIndicator();
    console.error(err);
    const errorText = "⚠️ Erro ao conectar com o assistente.";
    addMessage(errorText, "bot", false);
    saveMessage(errorText, "bot");
  }
}

// Form
chat_form.addEventListener("submit", e => {
  e.preventDefault();
  const text = message_input.value.trim();
  if (!text) return;
  message_input.value = "";
  sendMessage(text);
});

// Sugestões iniciais
suggestion_cards.forEach(card => {
  card.addEventListener("click", () => {
    const text = card.dataset.text;
    message_input.value = "";
    sendMessage(text);
  });
});

// Tema claro/escuro
theme_toggle.onclick = () => {
  const html = document.documentElement;
  const is_dark = html.dataset.theme === "dark";
  html.dataset.theme = is_dark ? "light" : "dark";
  theme_toggle.textContent = is_dark ? "☀️" : "🌙";
  localStorage.setItem("theme", html.dataset.theme);
};

// Inicializa tema
(() => {
  const html = document.documentElement;
  const saved = localStorage.getItem("theme");
  if (saved) {
    html.dataset.theme = saved;
  } else {
    const prefers_dark = window.matchMedia && window.matchMedia("(prefers-color-scheme: dark)").matches;
    html.dataset.theme = prefers_dark ? "dark" : "light";
  }
  theme_toggle.textContent = html.dataset.theme === "dark" ? "🌙" : "☀️";
})();

// Limpar chat (apenas front/localStorage)
clear_chat_btn.addEventListener("click", () => {
  history = [];
  localStorage.removeItem("chatHistory");
  chat_container.innerHTML = "";
  // Recoloca sugestões
  location.reload();
});

// Sidebar abrir/fechar (mobile)
open_sidebar_btn.addEventListener("click", () => {
  sidebar.classList.add("open");
});
close_sidebar_btn.addEventListener("click", () => {
  sidebar.classList.remove("open");
});

// Novo chat (limpa histórico visual/local)
new_chat_btn.addEventListener("click", () => {
  history = [];
  localStorage.removeItem("chatHistory");
  chat_container.innerHTML = "";
  location.reload();
});

// ============ UPLOAD PDF/DOCX (frontend) ============
file_btn.addEventListener("click", () => {
  file_input.click();
});

file_input.addEventListener("change", async (event) => {
  const file = event.target.files[0];
  if (!file) return;

  addMessage(`📎 Arquivo enviado: ${file.name}`, "user", false);
  saveMessage(`Arquivo enviado: ${file.name}`, "user");

  showTypingIndicator();

  try {
    const formData = new FormData();
    formData.append("file", file);

    const res = await axios.post("/upload", formData, {
      headers: { "Content-Type": "multipart/form-data" },
    });

    hideTypingIndicator();

    const summary = res.data.summary || "Arquivo recebido.";
    addMessage(`📄 Resumo do documento:\n${summary}`, "bot", true);
    saveMessage(`Resumo do documento: ${summary}`, "bot");

  } catch (error) {
    hideTypingIndicator();
    console.error(error);
    addMessage("⚠️ Erro ao enviar arquivo.", "bot", false);
  } finally {
    file_input.value = "";
  }
});

// ============ MODO VOZ (STT + TTS) ============

// Fala a resposta
function speak(text) {
  if (!("speechSynthesis" in window)) return;
  const utter = new SpeechSynthesisUtterance(text);
  utter.lang = "pt-BR";
  window.speechSynthesis.speak(utter);
}

// Reconhecimento de voz
let recognizing = false;
let recognition = null;

if ("webkitSpeechRecognition" in window || "SpeechRecognition" in window) {
  const SR = window.SpeechRecognition || window.webkitSpeechRecognition;
  recognition = new SR();
  recognition.lang = "pt-BR";
  recognition.continuous = false;
  recognition.interimResults = false;

  recognition.onresult = function (event) {
    const transcript = event.results[0][0].transcript;
    message_input.value = "";
    sendMessage(transcript);
  };

  recognition.onstart = function () {
    voice_btn.classList.add("recording");
  };

  recognition.onend = function () {
    voice_btn.classList.remove("recording");
    recognizing = false;
  };
}

voice_btn.addEventListener("click", () => {
  if (!recognition) {
    alert("Reconhecimento de voz não suportado neste navegador.");
    return;
  }
  if (!recognizing) {
    recognizing = true;
    recognition.start();
  } else {
    recognizing = false;
    recognition.stop();
  }
});
