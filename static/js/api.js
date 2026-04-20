window.state = window.state || {
  currentConversationId: null,
  conversations: [],
};

window.api = {
  async request(path, options = {}) {
    const response = await fetch(path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
    const contentType = response.headers.get("content-type") || "";
    const data = contentType.includes("application/json") ? await response.json() : {};
    if (!response.ok) {
      throw new Error(data.error || "Wystąpił błąd API.");
    }
    return data;
  },

  getConversations() {
    return this.request("/api/conversations");
  },

  createConversation() {
    return this.request("/api/conversations", { method: "POST", body: JSON.stringify({}) });
  },

  updateConversation(id, title) {
    return this.request(`/api/conversations/${id}`, {
      method: "PATCH",
      body: JSON.stringify({ title }),
    });
  },

  deleteConversation(id) {
    return this.request(`/api/conversations/${id}`, { method: "DELETE" });
  },

  getMessages(id) {
    return this.request(`/api/conversations/${id}/messages`);
  },

  sendMessage(id, content) {
    return this.request(`/api/conversations/${id}/messages`, {
      method: "POST",
      body: JSON.stringify({ content }),
    });
  },
};
