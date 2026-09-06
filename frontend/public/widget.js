(function () {
  const currentScript = document.currentScript || document.querySelector('script[data-api-key]');
  const API_KEY = currentScript ? currentScript.getAttribute('data-api-key') : 'spiq_live_apex_demo_key_9921';
  const API_URL = (currentScript ? currentScript.getAttribute('data-api-url') : null) || 'http://localhost:8000/api/v1';

  let conversationId = localStorage.getItem('spiq_conv_id') || null;
  let customerId = localStorage.getItem('spiq_cust_id') || null;
  let isOpen = false;

  const styleEl = document.createElement('style');
  styleEl.textContent = `
    .spiq-widget-container { position: fixed; bottom: 24px; right: 24px; z-index: 999999; font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif; }
    .spiq-launcher { width: 60px; height: 60px; border-radius: 50%; background: linear-gradient(135deg, #4f46e5 0%, #7c3aed 100%); box-shadow: 0 10px 25px -5px rgba(79, 70, 229, 0.4); display: flex; align-items: center; justify-content: center; cursor: pointer; color: white; transition: transform 0.2s; }
    .spiq-launcher:hover { transform: scale(1.08); }
    .spiq-badge { position: absolute; top: -2px; right: -2px; width: 14px; height: 14px; background: #ef4444; border: 2px solid #ffffff; border-radius: 50%; }
    .spiq-window { position: absolute; bottom: 75px; right: 0; width: 380px; height: 580px; max-height: calc(100vh - 120px); background: #ffffff; border-radius: 20px; box-shadow: 0 25px 50px -12px rgba(0, 0, 0, 0.25); display: flex; flex-direction: column; overflow: hidden; opacity: 0; transform: translateY(20px) scale(0.95); pointer-events: none; transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1); }
    .spiq-window.open { opacity: 1; transform: translateY(0) scale(1); pointer-events: all; }
    .spiq-header { background: linear-gradient(135deg, #1e1b4b 0%, #312e81 100%); color: #ffffff; padding: 18px 20px; display: flex; align-items: center; justify-content: space-between; }
    .spiq-header-info h4 { margin: 0; font-size: 15px; font-weight: 600; display: flex; align-items: center; gap: 8px; }
    .spiq-status-dot { width: 8px; height: 8px; background: #10b981; border-radius: 50%; display: inline-block; }
    .spiq-status-text { font-size: 11px; color: #cbd5e1; margin-top: 2px; }
    .spiq-close-btn { background: rgba(255, 255, 255, 0.15); border: none; color: white; width: 28px; height: 28px; border-radius: 50%; cursor: pointer; display: flex; align-items: center; justify-content: center; }
    .spiq-body { flex: 1; padding: 16px; overflow-y: auto; display: flex; flex-direction: column; gap: 12px; background: #f8fafc; }
    .spiq-message { max-width: 82%; padding: 12px 14px; border-radius: 14px; font-size: 13.5px; line-height: 1.45; word-break: break-word; }
    .spiq-message.ai, .spiq-message.agent { align-self: flex-start; background: #ffffff; color: #1e293b; box-shadow: 0 2px 4px rgba(0,0,0,0.04); border-bottom-left-radius: 4px; }
    .spiq-message.customer { align-self: flex-end; background: linear-gradient(135deg, #4f46e5 0%, #6366f1 100%); color: #ffffff; border-bottom-right-radius: 4px; }
    .spiq-message.system { align-self: center; background: #e2e8f0; color: #475569; font-size: 11.5px; padding: 6px 12px; border-radius: 12px; }
    .spiq-citation { margin-top: 8px; padding: 6px 10px; background: #f1f5f9; border-left: 3px solid #6366f1; border-radius: 4px; font-size: 11px; color: #475569; }
    .spiq-chips { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 4px; }
    .spiq-chip { background: #eef2ff; color: #4f46e5; border: 1px solid #c7d2fe; padding: 5px 10px; border-radius: 16px; font-size: 12px; cursor: pointer; }
    .spiq-chip:hover { background: #4f46e5; color: white; }
    .spiq-typing { display: flex; align-items: center; gap: 4px; padding: 10px 14px; background: white; border-radius: 14px; width: fit-content; }
    .spiq-typing-dot { width: 6px; height: 6px; background: #94a3b8; border-radius: 50%; animation: spiqBounce 1.4s infinite ease-in-out; }
    .spiq-typing-dot:nth-child(1) { animation-delay: -0.32s; }
    .spiq-typing-dot:nth-child(2) { animation-delay: -0.16s; }
    @keyframes spiqBounce { 0%, 80%, 100% { transform: scale(0); } 40% { transform: scale(1); } }
    .spiq-footer { padding: 12px 14px; background: #ffffff; border-top: 1px solid #f1f5f9; display: flex; gap: 8px; }
    .spiq-input { flex: 1; border: 1px solid #e2e8f0; border-radius: 10px; padding: 10px 14px; font-size: 13.5px; outline: none; }
    .spiq-input:focus { border-color: #6366f1; }
    .spiq-send-btn { background: #4f46e5; color: white; border: none; border-radius: 10px; width: 40px; cursor: pointer; display: flex; align-items: center; justify-content: center; }
  `;
  document.head.appendChild(styleEl);

  const container = document.createElement('div');
  container.className = 'spiq-widget-container';
  container.innerHTML = `
    <div class="spiq-window" id="spiqWindow">
      <div class="spiq-header">
        <div class="spiq-header-info">
          <h4 id="spiqHeaderTitle"><span class="spiq-status-dot"></span> <span id="spiqAgentName">SupportIQ Agent</span></h4>
          <div class="spiq-status-text" id="spiqStatusText">Powered by SupportIQ AI • 24/7 Live</div>
        </div>
        <button class="spiq-close-btn" id="spiqCloseBtn">✕</button>
      </div>
      <div class="spiq-body" id="spiqBody">
        <div class="spiq-message ai" id="spiqGreeting">Hello! How can I assist you with orders, returns, or product questions today?</div>
        <div class="spiq-chips" id="spiqChips">
          <div class="spiq-chip" onclick="window.spiqQuickSend('Where is my order ORD-10022?')">📦 Track Order ORD-10022</div>
          <div class="spiq-chip" onclick="window.spiqQuickSend('What is your return policy?')">🔄 Return Policy</div>
          <div class="spiq-chip" onclick="window.spiqQuickSend('Do you have headphones in stock?')">🎧 Headphones Stock</div>
          <div class="spiq-chip" onclick="window.spiqQuickSend('Connect me to a human support specialist')">⚡ Talk to Agent</div>
        </div>
      </div>
      <div class="spiq-footer">
        <input type="text" class="spiq-input" id="spiqInput" placeholder="Type your message..." />
        <button class="spiq-send-btn" id="spiqSendBtn">➤</button>
      </div>
    </div>
    <div class="spiq-launcher" id="spiqLauncher">
      <svg width="28" height="28" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
        <path d="M21 15a2 2 0 0 1-2 2H7l-4 4V5a2 2 0 0 1 2-2h14a2 2 0 0 1 2 2z"></path>
      </svg>
      <div class="spiq-badge" id="spiqBadge"></div>
    </div>
  `;
  document.body.appendChild(container);

  const windowEl = document.getElementById('spiqWindow');
  const launcherEl = document.getElementById('spiqLauncher');
  const closeBtn = document.getElementById('spiqCloseBtn');
  const bodyEl = document.getElementById('spiqBody');
  const inputEl = document.getElementById('spiqInput');
  const sendBtn = document.getElementById('spiqSendBtn');
  const agentNameEl = document.getElementById('spiqAgentName');
  const greetingEl = document.getElementById('spiqGreeting');
  const statusTextEl = document.getElementById('spiqStatusText');

  function toggleWidget() {
    isOpen = !isOpen;
    if (isOpen) {
      windowEl.classList.add('open');
      document.getElementById('spiqBadge').style.display = 'none';
      if (!conversationId) initSession();
      setTimeout(() => inputEl.focus(), 200);
    } else {
      windowEl.classList.remove('open');
    }
  }

  launcherEl.addEventListener('click', toggleWidget);
  closeBtn.addEventListener('click', toggleWidget);

  async function initSession() {
    try {
      const res = await fetch(`${API_URL}/widget/init`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
        body: JSON.stringify({ customer_name: 'Website Visitor', conversation_id: conversationId }),
      });
      if (res.ok) {
        const data = await res.json();
        conversationId = data.conversation_id;
        customerId = data.customer_id;
        localStorage.setItem('spiq_conv_id', conversationId);
        localStorage.setItem('spiq_cust_id', customerId);
        if (data.agent_name) agentNameEl.textContent = data.agent_name;
        if (data.greeting_message) greetingEl.textContent = data.greeting_message;
      }
    } catch (e) {}
  }

  function appendMessage(text, sender, sourcesJson) {
    const msg = document.createElement('div');
    msg.className = `spiq-message ${sender}`;
    let formattedText = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>').replace(/`(.*?)`/g, '<code>$1</code>').replace(/\n/g, '<br/>');
    msg.innerHTML = formattedText;
    if (sourcesJson) {
      try {
        const citations = typeof sourcesJson === 'string' ? JSON.parse(sourcesJson) : sourcesJson;
        if (citations && citations.length > 0) {
          const cit = citations[0];
          const citEl = document.createElement('div');
          citEl.className = 'spiq-citation';
          citEl.textContent = `📖 Source: ${cit.document_title}${cit.page_number ? ' (Page ' + cit.page_number + ')' : ''}`;
          msg.appendChild(citEl);
        }
      } catch (e) {}
    }
    bodyEl.appendChild(msg);
    bodyEl.scrollTop = bodyEl.scrollHeight;
  }

  function showTyping() {
    const typing = document.createElement('div');
    typing.className = 'spiq-typing';
    typing.id = 'spiqTypingIndicator';
    typing.innerHTML = `<div class="spiq-typing-dot"></div><div class="spiq-typing-dot"></div><div class="spiq-typing-dot"></div>`;
    bodyEl.appendChild(typing);
    bodyEl.scrollTop = bodyEl.scrollHeight;
  }

  function removeTyping() {
    const typing = document.getElementById('spiqTypingIndicator');
    if (typing) typing.remove();
  }

  async function handleSend(textToSend) {
    const text = textToSend || inputEl.value.trim();
    if (!text) return;
    if (!textToSend) inputEl.value = '';
    appendMessage(text, 'customer');
    showTyping();
    const chips = document.getElementById('spiqChips');
    if (chips) chips.style.display = 'none';

    try {
      if (!conversationId) await initSession();
      const res = await fetch(`${API_URL}/widget/send`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', 'X-API-Key': API_KEY },
        body: JSON.stringify({ conversation_id: conversationId, message: text }),
      });
      removeTyping();
      if (res.ok) {
        const data = await res.json();
        if (data.ai_response) appendMessage(data.ai_response.content, 'ai', data.ai_response.sources_json);
        if (data.handoff_requested) {
          statusTextEl.textContent = 'Transferred to Support Specialist';
          appendMessage('⚠️ A human specialist has been notified and is stepping in.', 'system');
        }
      } else {
        appendMessage("Support server connection error.", 'ai');
      }
    } catch (e) {
      removeTyping();
      appendMessage("Network connection error.", 'ai');
    }
  }

  sendBtn.addEventListener('click', () => handleSend());
  inputEl.addEventListener('keypress', (e) => { if (e.key === 'Enter') handleSend(); });
  window.spiqQuickSend = function (text) { handleSend(text); };
})();
