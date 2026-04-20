const conversationListEl = document.querySelector("#conversation-list");
const newConversationButton = document.querySelector("#new-conversation");

function renderConversations() {
  conversationListEl.innerHTML = "";
  for (const conversation of window.state.conversations) {
    const item = document.createElement("button");
    item.type = "button";
    item.className = "conversation-item";
    if (conversation.id === window.state.currentConversationId) {
      item.classList.add("active");
    }

    const title = document.createElement("span");
    title.className = "conversation-title";
    title.textContent = conversation.title;
    item.append(title);

    const remove = document.createElement("span");
    remove.className = "delete-conversation";
    remove.textContent = "×";
    remove.title = "Usuń rozmowę";
    item.append(remove);

    item.addEventListener("click", async (event) => {
      if (event.target === remove) {
        event.stopPropagation();
        await deleteConversation(conversation.id);
        return;
      }
      await selectConversation(conversation.id);
    });

    conversationListEl.append(item);
  }
}

async function loadConversations(preferredId = null) {
  window.state.conversations = await window.api.getConversations();
  if (preferredId && window.state.conversations.some((item) => item.id === preferredId)) {
    window.state.currentConversationId = preferredId;
  } else if (!window.state.conversations.some((item) => item.id === window.state.currentConversationId)) {
    window.state.currentConversationId = window.state.conversations[0]?.id || null;
  }
  renderConversations();
  window.titleEditor.syncTitle();
}

async function selectConversation(id) {
  window.state.currentConversationId = id;
  renderConversations();
  window.titleEditor.syncTitle();
  await window.chat.loadMessages();
}

async function createConversation() {
  const conversation = await window.api.createConversation();
  await loadConversations(conversation.id);
  await window.chat.loadMessages();
}

async function deleteConversation(id) {
  await window.api.deleteConversation(id);
  await loadConversations();
  await window.chat.loadMessages();
}

newConversationButton.addEventListener("click", createConversation);

document.addEventListener("DOMContentLoaded", async () => {
  try {
    await loadConversations();
    if (!window.state.currentConversationId) {
      await createConversation();
    } else {
      await window.chat.loadMessages();
    }
  } catch (error) {
    window.chat.renderError(error.message);
  }
});

window.sidebar = { loadConversations, selectConversation, createConversation };
