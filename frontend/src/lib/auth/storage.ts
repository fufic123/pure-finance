// Access token lives in memory only — never persisted, drops on reload.
// Refresh token lives in localStorage, which is acceptable for a self-use
// PWA with no third-party scripts and no user-generated HTML.

const REFRESH_KEY = "pf.refresh";

let accessToken: string | null = null;

export const tokenStorage = {
  setAccess(token: string | null): void {
    accessToken = token;
  },
  getAccess(): string | null {
    return accessToken;
  },
  setRefresh(token: string | null): void {
    if (typeof window === "undefined") return;
    if (token === null) {
      window.localStorage.removeItem(REFRESH_KEY);
    } else {
      window.localStorage.setItem(REFRESH_KEY, token);
    }
  },
  getRefresh(): string | null {
    if (typeof window === "undefined") return null;
    return window.localStorage.getItem(REFRESH_KEY);
  },
  setPair(pair: { access: string; refresh: string }): void {
    this.setAccess(pair.access);
    this.setRefresh(pair.refresh);
  },
  clear(): void {
    this.setAccess(null);
    this.setRefresh(null);
  },
};
