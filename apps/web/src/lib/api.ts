export const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "/api/v1";

export interface StoredUser {
  id: string;
  email: string;
  display_name: string;
  track: string;
  role: string;
}

export function getAuthToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("statskill_token");
}

export function setAuthSession(token: string, user: StoredUser) {
  if (typeof window === "undefined") return;
  localStorage.setItem("statskill_token", token);
  localStorage.setItem("statskill_user", JSON.stringify(user));
}

export function clearAuthSession() {
  if (typeof window === "undefined") return;
  localStorage.removeItem("statskill_token");
  localStorage.removeItem("statskill_user");
}

export function getStoredUser(): StoredUser | null {
  if (typeof window === "undefined") return null;
  const token = localStorage.getItem("statskill_token");
  if (!token) return null;
  const raw = localStorage.getItem("statskill_user");
  if (!raw) return null;
  try {
    return JSON.parse(raw);
  } catch {
    return null;
  }
}

export async function apiRequest<T>(
  endpoint: string,
  options: RequestInit = {}
): Promise<T> {
  const token = getAuthToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string> || {}),
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const cleanEndpoint = endpoint.startsWith("/") ? endpoint : `/${endpoint}`;
  const base = API_BASE_URL.replace(/\/$/, "");
  const path = cleanEndpoint.startsWith(base) ? cleanEndpoint : `${base}${cleanEndpoint}`;

  // If in browser, use relative path so Next.js handles proxying on port 3000
  // If in Node/SSR, use full loopback address
  const url = typeof window !== "undefined"
    ? path
    : (path.startsWith("http") ? path : `http://127.0.0.1:8000${cleanEndpoint}`);

  try {
    const res = await fetch(url, {
      ...options,
      headers,
    });

    if (!res.ok) {
      const errData = await res.json().catch(() => ({ detail: res.statusText }));
      throw new Error(errData.detail || `Request failed with status ${res.status}`);
    }

    return await res.json();
  } catch (err: any) {
    console.warn(`API call to ${url} failed:`, err.message);
    throw err;
  }
}

export const fetchApi = apiRequest;
