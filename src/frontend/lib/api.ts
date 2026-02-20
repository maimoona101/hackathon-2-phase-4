// API client for the Todo Web Application
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || "http://localhost:8000";

class ApiClient {
  private baseUrl: string;

  constructor() {
    this.baseUrl = API_BASE_URL;
  }

  getAuthToken(): string | null {
    if (typeof window !== "undefined") {
      return localStorage.getItem("auth_token");
    }
    return null;
  }

  setAuthToken(token: string) {
    if (typeof window !== "undefined") {
      localStorage.setItem("auth_token", token);
    }
  }

  clearAuthToken() {
    if (typeof window !== "undefined") {
      localStorage.removeItem("auth_token");
    }
  }

  async request(endpoint: string, options: RequestInit = {}) {
    const url = `${this.baseUrl}${endpoint}`;

    const headers: Record<string, string> = {
      "Content-Type": "application/json",
    };

    const token = this.getAuthToken();
    if (token) {
      headers.Authorization = `Bearer ${token}`;
    }

    try {
      const response = await fetch(url, {
        ...options,
        headers: {
          ...headers,
          ...(options.headers || {}),
        },
      });

      if (!response.ok) {
        // For better debugging, include response details
        const errorMessage = await response.text(); // Get the error response body
        throw new Error(`HTTP error! status: ${response.status}, message: ${errorMessage}`);
      }

      return response.json();
    } catch (error) {
      // Handle network errors and other fetch failures
      if (error instanceof TypeError) {
        throw new Error(`Network error: Unable to connect to the server. Please check your connection and the API URL (${url}).`);
      }
      throw error;
    }
  }

  // ================= AUTH =================

  async register(email: string, password: string, displayName?: string) {
    const response = await fetch(`${this.baseUrl}/api/auth/register`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        email,
        password,
        display_name: displayName, // ✅ backend expects this
      }),
    });

    if (!response.ok) {
      throw new Error("Registration failed");
    }

    return response.json();
  }

  async login(email: string, password: string) {
    const response = await fetch(`${this.baseUrl}/api/auth/login`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Accept: "application/json",
      },
      body: JSON.stringify({ email, password }),
    });

    if (!response.ok) {
      throw new Error("Login failed");
    }

    const data = await response.json();
    this.setAuthToken(data.access_token);
    return data;
  }

  async logout() {
    this.clearAuthToken();
  }

  // ================= USER =================

  async getCurrentUser() {
    return this.request("/api/users/profile");
  }

  // ================= TODOS =================

  async getTodos(status?: string, limit = 50, offset = 0) {
    let endpoint = `/api/todos?limit=${limit}&offset=${offset}`;
    if (status) {
      endpoint += `&status=${status}`;
    }
    return this.request(endpoint);
  }

  async createTodo(
    title: string,
    description?: string,
    priority: string = "medium",
  ) {
    return this.request("/api/todos", {
      method: "POST",
      body: JSON.stringify({ title, description, priority }),
    });
  }

  async updateTodo(
    id: string,
    updates: {
      title?: string;
      description?: string;
      status?: string;
      priority?: string;
    },
  ) {
    return this.request(`/api/todos/${id}`, {
      method: "PUT",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(updates),
    });
  }

  async deleteTodo(id: string) {
    return this.request(`/api/todos/${id}`, {
      method: "DELETE",
    });
  }

  // ================= CHAT =================

  async startChatConversation() {
    return this.request("/api/chat/start", {
      method: "POST",
    });
  }

  async sendChatMessage(messageData: { conversation_id?: string; message: string }) {
    return this.request("/api/chat/message", {
      method: "POST",
      body: JSON.stringify(messageData),
    });
  }

  async getChatHistory(conversationId: string) {
    return this.request(`/api/chat/history/${conversationId}`);
  }
}

export const apiClient = new ApiClient();
