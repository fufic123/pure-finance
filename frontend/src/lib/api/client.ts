import { tokenStorage } from "@/lib/auth/storage";
import type { ApiError, TokenPair } from "@/lib/api/types";

const BASE_URL = process.env.NEXT_PUBLIC_API_BASE_URL;

if (!BASE_URL) {
  // Fail loudly at module load in dev — missing base URL is never recoverable.
  throw new Error("NEXT_PUBLIC_API_BASE_URL is not set");
}

export class ApiRequestError extends Error {
  constructor(
    public readonly status: number,
    public readonly body: ApiError | null,
  ) {
    super(body?.message ?? `Request failed with status ${status}`);
    this.name = "ApiRequestError";
  }
}

type FetchOptions = {
  method?: "GET" | "POST" | "PATCH" | "DELETE";
  body?: unknown;
  auth?: boolean;
  signal?: AbortSignal;
};

async function raw<T>(path: string, opts: FetchOptions = {}): Promise<T> {
  const { method = "GET", body, auth = true, signal } = opts;
  const headers: Record<string, string> = { "Content-Type": "application/json" };
  if (auth) {
    const token = tokenStorage.getAccess();
    if (token) headers.Authorization = `Bearer ${token}`;
  }
  const res = await fetch(`${BASE_URL}${path}`, {
    method,
    headers,
    body: body !== undefined ? JSON.stringify(body) : undefined,
    signal,
  });
  return parse<T>(res);
}

async function parse<T>(res: Response): Promise<T> {
  if (res.status === 204) return undefined as T;
  const text = await res.text();
  const data = text.length > 0 ? (JSON.parse(text) as unknown) : null;
  if (!res.ok) {
    throw new ApiRequestError(res.status, data as ApiError | null);
  }
  return data as T;
}

let refreshInFlight: Promise<TokenPair> | null = null;

async function refreshTokens(): Promise<TokenPair> {
  const refresh = tokenStorage.getRefresh();
  if (!refresh) throw new ApiRequestError(401, { message: "no refresh token" });
  if (refreshInFlight) return refreshInFlight;
  refreshInFlight = raw<TokenPair>("/auth/refresh", {
    method: "POST",
    body: { refresh },
    auth: false,
  }).finally(() => {
    refreshInFlight = null;
  });
  const pair = await refreshInFlight;
  tokenStorage.setPair(pair);
  return pair;
}

// Public request helper. Automatically retries once after a silent refresh
// when an authenticated call hits 401.
export async function apiRequest<T>(path: string, opts: FetchOptions = {}): Promise<T> {
  try {
    return await raw<T>(path, opts);
  } catch (err) {
    if (
      err instanceof ApiRequestError &&
      err.status === 401 &&
      opts.auth !== false &&
      tokenStorage.getRefresh() !== null
    ) {
      await refreshTokens();
      return raw<T>(path, opts);
    }
    throw err;
  }
}
