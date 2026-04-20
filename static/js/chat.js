const messagesEl = document.querySelector("#messages");
const messageForm = document.querySelector("#message-form");
const messageInput = document.querySelector("#message-input");

function renderMessages(messages) {
  messagesEl.innerHTML = "";

  if (!messages.length) {
    const empty = document.createElement("p");
    empty.className = "empty-state";
    empty.textContent = "Napisz pierwszą wiadomość. Możesz zapytać o szablon albo wpisać działanie matematyczne.";
    messagesEl.append(empty);
    return;
  }

  for (const message of messages) {
    const item = document.createElement("div");
    item.className = `message ${message.role}`;
    item.textContent = message.content;
    messagesEl.append(item);
  }
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function renderError(message) {
  messagesEl.innerHTML = "";
  const error = document.createElement("p");
  error.className = "empty-state";
  error.textContent = message;
  messagesEl.append(error);
}

async function loadMessages() {
  if (!window.state.currentConversationId) {
    renderMessages([]);
    return;
  }
  const messages = await window.api.getMessages(window.state.currentConversationId);
  renderMessages(messages);
}

function appendMessage(role, content) {
  const empty = messagesEl.querySelector(".empty-state");
  if (empty) empty.remove();

  const item = document.createElement("div");
  item.className = `message ${role}`;
  item.textContent = content;
  messagesEl.append(item);
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

messageForm.addEventListener("submit", async (event) => {
  event.preventDefault();
  const content = messageInput.value.trim();
  if (!content) return;

  if (!window.state.currentConversationId) {
    try {
      await window.sidebar.createConversation();
    } catch (error) {
      renderError(error.message);
      return;
    }
  }

  messageInput.value = "";
  appendMessage("user", content);
  const pending = document.createElement("div");
  pending.className = "message bot status";
  pending.textContent = "Piszę odpowiedź...";
  messagesEl.append(pending);

  try {
    const botMessage = await window.api.sendMessage(window.state.currentConversationId, content);
    pending.remove();
    appendMessage("bot", botMessage.content);
    await window.sidebar.loadConversations(window.state.currentConversationId);
  } catch (error) {
    pending.textContent = error.message;
  }
});

window.chat = { loadMessages, renderMessages, renderError };
