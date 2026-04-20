const titleInput = document.querySelector("#conversation-title");
const saveTitleButton = document.querySelector("#save-title");

function getCurrentConversation() {
  return window.state.conversations.find((conversation) => conversation.id === window.state.currentConversationId);
}

function syncTitle() {
  const conversation = getCurrentConversation();
  titleInput.value = conversation ? conversation.title : "Nowa rozmowa";
  titleInput.disabled = !conversation;
  saveTitleButton.disabled = !conversation;
}

saveTitleButton.addEventListener("click", async () => {
  const title = titleInput.value.trim();
  if (!title || !window.state.currentConversationId) return;

  const updated = await window.api.updateConversation(window.state.currentConversationId, title);
  window.state.conversations = window.state.conversations.map((conversation) =>
    conversation.id === updated.id ? { ...conversation, title: updated.title } : conversation
  );
  window.sidebar.loadConversations(updated.id);
});

window.titleEditor = { syncTitle };
