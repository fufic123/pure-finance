// Mirrors backend DTOs from backend/src/api/dtos/*. Keep in sync manually.

export type TokenPair = { access: string; refresh: string };

export type User = {
  id: string;
  email: string;
  created_at: string;
};

export type Institution = {
  id: string;
  name: string;
  country: string;
  logo_url: string | null;
};

export type ConnectionStatus = "CREATED" | "COMPLETED" | "EXPIRED" | "REVOKED";

export type Connection = {
  id: string;
  institution_id: string;
  status: ConnectionStatus;
  created_at: string;
};

export type StartConnectionResponse = { session_id: string; link: string };

export type Account = {
  id: string;
  institution_external_id: string;
  iban: string | null;
  currency: string;
  name: string;
  created_at: string;
};

export type Balance = { amount: string; currency: string };

export type Transaction = {
  id: string;
  account_id: string;
  amount: string;
  currency: string;
  eur_amount: string | null;
  description: string;
  booked_at: string;
  category_id: string | null;
  note: string | null;
  manually_categorized: boolean;
};

export type Category = {
  id: string;
  parent_id: string | null;
  name: string;
  is_system: boolean;
};

export type CategorizationRule = {
  id: string;
  category_id: string;
  keyword: string;
};

export type AnalyticsSummary = {
  income_eur: string;
  expenses_eur: string;
  net_eur: string;
  transaction_count: number;
  transactions_without_fx: number;
};

export type AnalyticsByCategory = {
  category_id: string | null;
  total_eur: string;
  count: number;
};

export type SyncResult = { added: number };

export type ApiError = { message: string };
