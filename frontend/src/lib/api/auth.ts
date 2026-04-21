import { apiRequest } from "@/lib/api/client";
import { tokenStorage } from "@/lib/auth/storage";
import type { TokenPair, User } from "@/lib/api/types";

export async function startGoogleAuth(redirectUri: string): Promise<string> {
  const res = await apiRequest<{ authorization_url: string }>("/auth/google", {
    method: "POST",
    body: { redirect_uri: redirectUri },
    auth: false,
  });
  return res.authorization_url;
}

export async function completeGoogleAuth(
  code: string,
  redirectUri: string,
  state: string,
): Promise<TokenPair> {
  const pair = await apiRequest<TokenPair>("/auth/google/callback", {
    method: "POST",
    body: { code, redirect_uri: redirectUri, state },
    auth: false,
  });
  tokenStorage.setPair(pair);
  return pair;
}

export async function logout(): Promise<void> {
  const refresh = tokenStorage.getRefresh();
  if (refresh) {
    await apiRequest<void>("/auth/logout", {
      method: "POST",
      body: { refresh },
      auth: false,
    }).catch(() => {
      // revoke is best-effort — client-side clear runs regardless.
    });
  }
  tokenStorage.clear();
}

export async function getCurrentUser(): Promise<User> {
  return apiRequest<User>("/user");
}
