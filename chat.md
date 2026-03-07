---
layout: page
title: Chat
permalink: /chat/
---

<div id="chat-root" class="chat-page" data-backend-url="{{ site.llm_backend_url | default: '' }}">
  <h1 class="chat-heading">Chat</h1>
  <p class="chat-subtitle">
    Bu asistan benim bilgisayarımdan yanıt veriyor. Her IP adresi için günde en fazla 5 soru hakkı var.
  </p>

  <div id="chat-messages" class="chat-messages"></div>

  <div id="chat-error" class="chat-error" role="alert" aria-live="polite"></div>

  <div class="chat-input-row">
    <input
      id="chat-input"
      type="text"
      class="chat-input"
      placeholder="Mesajınızı yazın..."
      autocomplete="off"
    />
    <button type="button" id="chat-send" class="chat-button chat-button-primary">Gönder</button>
    <button type="button" id="chat-new" class="chat-button chat-button-secondary">Yeni konuşma</button>
  </div>
</div>

<style>
  .chat-page {
    max-width: 720px;
    margin: 40px auto;
    padding: 24px 24px 28px;
    background: #ffffff;
    border-radius: 16px;
    box-shadow:
      0 12px 30px rgba(15, 23, 42, 0.18),
      0 0 0 1px rgba(148, 163, 184, 0.25);
    box-sizing: border-box;
  }

  .chat-heading {
    margin-top: 0;
    margin-bottom: 4px;
    font-size: 1.6rem;
    font-weight: 800;
    color: #0f172a;
    letter-spacing: 0.02em;
  }

  .chat-subtitle {
    margin-top: 0;
    margin-bottom: 20px;
    font-size: 0.98rem;
    color: #4b5563;
    line-height: 1.5;
  }

  .chat-messages {
    min-height: 120px;
    max-height: 400px;
    overflow-y: auto;
    margin-bottom: 16px;
    padding: 12px 0;
    display: flex;
    flex-direction: column;
    gap: 12px;
  }

  .chat-message {
    max-width: 85%;
    padding: 10px 14px;
    border-radius: 14px;
    line-height: 1.5;
    word-wrap: break-word;
  }

  .chat-message-user {
    align-self: flex-end;
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: #ffffff;
    border-bottom-right-radius: 4px;
  }

  .chat-message-assistant {
    align-self: flex-start;
    background: #f1f5f9;
    color: #0f172a;
    border-bottom-left-radius: 4px;
  }

  .chat-error {
    min-height: 24px;
    margin-bottom: 12px;
    font-size: 0.9rem;
    color: #dc2626;
  }

  .chat-input-row {
    display: flex;
    gap: 10px;
    align-items: center;
    flex-wrap: wrap;
  }

  .chat-input {
    flex: 1;
    min-width: 160px;
    padding: 10px 14px;
    border-radius: 10px;
    border: 1px solid #d1d5db;
    font-size: 0.95rem;
    background: #f9fafb;
    box-sizing: border-box;
  }

  .chat-input:focus {
    outline: none;
    border-color: #16a34a;
    background: #ffffff;
  }

  .chat-button {
    padding: 10px 18px;
    border-radius: 10px;
    font-size: 0.95rem;
    font-weight: 600;
    cursor: pointer;
    border: none;
    transition: transform 120ms ease, filter 120ms ease;
  }

  .chat-button:hover {
    transform: translateY(-1px);
    filter: brightness(1.03);
  }

  .chat-button:active {
    transform: translateY(0);
  }

  .chat-button-primary {
    background: linear-gradient(135deg, #16a34a, #22c55e);
    color: #ffffff;
  }

  .chat-button-secondary {
    background: #e2e8f0;
    color: #334155;
  }

  .chat-button:disabled {
    opacity: 0.6;
    cursor: not-allowed;
    transform: none;
  }

  @media (max-width: 768px) {
    .chat-page {
      margin: 24px auto;
      padding: 20px 18px 24px;
    }

    .chat-message {
      max-width: 92%;
    }
  }
</style>

<script>
(function() {
  const STORAGE_KEY = 'llm_chat_messages';
  const root = document.getElementById('chat-root');
  const messagesEl = document.getElementById('chat-messages');
  const errorEl = document.getElementById('chat-error');
  const inputEl = document.getElementById('chat-input');
  const sendBtn = document.getElementById('chat-send');
  const newBtn = document.getElementById('chat-new');

  const backendUrl = (root && root.dataset.backendUrl) || '';
  if (!backendUrl || backendUrl.includes('YOUR-TUNNEL')) {
    errorEl.textContent = 'Chat backend henüz yapılandırılmamış. llm_backend_url güncelleyin.';
  }

  let messages = [];
  try {
    const stored = sessionStorage.getItem(STORAGE_KEY);
    if (stored) messages = JSON.parse(stored);
  } catch (_) {}

  function saveMessages() {
    try {
      sessionStorage.setItem(STORAGE_KEY, JSON.stringify(messages));
    } catch (_) {}
  }

  function showError(msg) {
    errorEl.textContent = msg || '';
  }

  function renderMessages() {
    messagesEl.innerHTML = '';
    messages.forEach(function(m) {
      const div = document.createElement('div');
      div.className = 'chat-message chat-message-' + m.role;
      div.textContent = m.content;
      messagesEl.appendChild(div);
    });
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function appendAssistantChunk(text) {
    let last = messagesEl.querySelector('.chat-message-assistant:last-child');
    if (!last) {
      last = document.createElement('div');
      last.className = 'chat-message chat-message-assistant';
      messagesEl.appendChild(last);
    }
    last.textContent = (last.textContent || '') + text;
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function setLoading(loading) {
    sendBtn.disabled = loading;
    inputEl.disabled = loading;
  }

  newBtn.addEventListener('click', function() {
    messages = [];
    saveMessages();
    renderMessages();
    showError('');
  });

  sendBtn.addEventListener('click', sendMessage);
  inputEl.addEventListener('keydown', function(e) {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  });

  function sendMessage() {
    const text = (inputEl.value || '').trim();
    if (!text) return;
    if (!backendUrl || backendUrl.includes('YOUR-TUNNEL')) return;

    inputEl.value = '';
    messages.push({ role: 'user', content: text });
    saveMessages();
    renderMessages();
    showError('');
    setLoading(true);

    const payload = { messages: messages.map(function(m) { return { role: m.role, content: m.content }; }) };

    fetch(backendUrl.replace(/\/$/, '') + '/chat', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(payload)
    }).then(function(res) {
      if (!res.ok) {
        if (res.status === 429) return res.json().then(function() { throw new Error('Günlük limit aşıldı (5 soru/gün).'); });
        if (res.status === 401) throw new Error('Yetkisiz istek.');
        throw new Error('Sunucu hatası: ' + res.status);
      }
      return res;
    }).then(function(res) {
      const reader = res.body.getReader();
      const decoder = new TextDecoder();
      let assistantContent = '';
      let buffer = '';

      function processBuffer() {
        const events = buffer.split('\n\n');
        buffer = events.pop() || '';
        events.forEach(function(event) {
          const line = event.trim();
          if (line.startsWith('data: ')) {
            const data = line.slice(6);
            if (!data) return;
            try {
              const obj = JSON.parse(data);
              const content = obj.message && obj.message.content;
              if (content) {
                assistantContent += content;
                appendAssistantChunk(content);
              }
            } catch (_) {}
          }
        });
      }

      function read() {
        return reader.read().then(function(result) {
          if (result.done) {
            processBuffer();
            if (assistantContent) {
              messages.push({ role: 'assistant', content: assistantContent });
              saveMessages();
            }
            setLoading(false);
            return;
          }
          buffer += decoder.decode(result.value, { stream: true });
          processBuffer();
          return read();
        });
      }
      return read();
    }).catch(function(err) {
      showError(err.message || 'Bağlantı hatası.');
      setLoading(false);
    });
  }

  renderMessages();
})();
</script>
