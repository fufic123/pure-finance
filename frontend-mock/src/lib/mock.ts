// Mock data ported from backend/docs/frontend/pf_components.jsx.
// Pure design preview — no backend, no API calls.

export type MockUser = {
  name: string;
  email: string;
  joined: string;
};

export type MockAccount = {
  id: string;
  name: string;
  currency: string;
  balance: string;
  logo: string;
  color: string;
};

export type MockSummary = {
  income: string;
  expenses: string;
  net: string;
  count: number;
  missingFx: number;
};

export type MockTransaction = {
  id: string;
  day: string;
  mon: string;
  desc: string;
  amount: string;
  cat: string;
  expense: boolean;
};

export type MockCategory = {
  name: string;
  total: string;
  pct: number;
  count: number;
};

export type MockBank = {
  id: string;
  name: string;
  abbr: string;
  color: string;
};

export type ConnectionStatus = "CREATED" | "COMPLETED" | "EXPIRED" | "REVOKED";

export type MockConnection = {
  id: string;
  bank: MockBank;
  status: ConnectionStatus;
  created: string;
};

export type CategoryNode = {
  id: string;
  name: string;
  system: boolean;
  children: CategoryNode[];
};

export type MockRule = {
  id: string;
  keyword: string;
  category: string;
};

export const MOCK_USER: MockUser = {
  name: "Mark",
  email: "mark@example.com",
  joined: "Joined Mar 2026",
};

export const MOCK_ACCOUNTS: MockAccount[] = [
  { id: "1", name: "Revolut", currency: "EUR", balance: "2,340.50", logo: "R", color: "#191C1F" },
  { id: "2", name: "SEB", currency: "EUR", balance: "8,120.00", logo: "S", color: "#006B2D" },
];

export const MOCK_SUMMARY: MockSummary = {
  income: "3,200.00",
  expenses: "1,540.30",
  net: "1,659.70",
  count: 28,
  missingFx: 1,
};

export const MOCK_TRANSACTIONS: MockTransaction[] = [
  { id: "1", day: "21", mon: "Apr", desc: "Bolt Food", amount: "−18.90", cat: "Food", expense: true },
  { id: "2", day: "21", mon: "Apr", desc: "Salary — Turing Labs", amount: "+3,200.00", cat: "Income", expense: false },
  { id: "3", day: "20", mon: "Apr", desc: "Rimi", amount: "−42.15", cat: "Groceries", expense: true },
  { id: "4", day: "19", mon: "Apr", desc: "Spotify", amount: "−9.99", cat: "Entertainment", expense: true },
  { id: "5", day: "19", mon: "Apr", desc: "Starbucks", amount: "−5.80", cat: "Coffee", expense: true },
  { id: "6", day: "18", mon: "Apr", desc: "Wolt", amount: "−24.50", cat: "Food", expense: true },
  { id: "7", day: "17", mon: "Apr", desc: "Netflix", amount: "−13.99", cat: "Entertainment", expense: true },
  { id: "8", day: "16", mon: "Apr", desc: "Lidl", amount: "−31.20", cat: "Groceries", expense: true },
  { id: "9", day: "15", mon: "Apr", desc: "Taxify (Bolt)", amount: "−8.40", cat: "Transport", expense: true },
  { id: "10", day: "14", mon: "Apr", desc: "Maxima", amount: "−28.75", cat: "Groceries", expense: true },
];

export const MOCK_CATEGORIES: MockCategory[] = [
  { name: "Food", total: "480.50", pct: 31, count: 9 },
  { name: "Groceries", total: "320.00", pct: 21, count: 6 },
  { name: "Transport", total: "180.00", pct: 12, count: 8 },
  { name: "Entertainment", total: "160.00", pct: 10, count: 4 },
  { name: "Uncategorized", total: "80.00", pct: 5, count: 2 },
];

export type MockInstitution = {
  id: string;
  name: string;
};

// Matches the backend seed so the picker uses the same list.
export const MOCK_INSTITUTIONS: MockInstitution[] = [
  { id: "inst-seb", name: "SEB" },
  { id: "inst-swedbank", name: "Swedbank" },
  { id: "inst-luminor", name: "Luminor" },
  { id: "inst-lhv", name: "LHV" },
  { id: "inst-citadele", name: "Citadele" },
  { id: "inst-revolut", name: "Revolut" },
  { id: "inst-paysera", name: "Paysera" },
  { id: "inst-siauliu", name: "Šiaulių bankas" },
  { id: "inst-monobank", name: "Monobank" },
  { id: "inst-privatbank", name: "PrivatBank" },
  { id: "inst-wise", name: "Wise" },
  { id: "inst-n26", name: "N26" },
  { id: "inst-other", name: "Other" },
];

export const MOCK_BANKS: MockBank[] = [
  { id: "REVOLUT_LT", name: "Revolut", abbr: "R", color: "#191C1F" },
  { id: "SEB_LT", name: "SEB", abbr: "S", color: "#006B2D" },
  { id: "SWEDBANK_LT", name: "Swedbank", abbr: "Sw", color: "#F9941E" },
  { id: "LUMINOR_LT", name: "Luminor", abbr: "L", color: "#2E2AB5" },
  { id: "CITADELE_LT", name: "Citadele", abbr: "C", color: "#FF4A00" },
  { id: "MEDICINOS_LT", name: "Medicinos Bank", abbr: "Mb", color: "#1A4E8A" },
];

export const MOCK_CONNECTIONS: MockConnection[] = [
  {
    id: "c1",
    bank: { id: "REVOLUT_LT", name: "Revolut", abbr: "R", color: "#191C1F" },
    status: "COMPLETED",
    created: "Mar 14, 2026",
  },
  {
    id: "c2",
    bank: { id: "SEB_LT", name: "SEB", abbr: "S", color: "#006B2D" },
    status: "COMPLETED",
    created: "Mar 14, 2026",
  },
  {
    id: "c3",
    bank: { id: "SWEDBANK_LT", name: "Swedbank", abbr: "Sw", color: "#F9941E" },
    status: "EXPIRED",
    created: "Jan 02, 2026",
  },
];

export const MOCK_CATEGORY_TREE: CategoryNode[] = [
  {
    id: "cat-food",
    name: "Food & Drink",
    system: true,
    children: [
      { id: "cat-food-restaurants", name: "Restaurants", system: true, children: [] },
      { id: "cat-food-coffee", name: "Coffee", system: false, children: [] },
      { id: "cat-food-delivery", name: "Delivery", system: false, children: [] },
    ],
  },
  {
    id: "cat-groceries",
    name: "Groceries",
    system: true,
    children: [],
  },
  {
    id: "cat-transport",
    name: "Transport",
    system: true,
    children: [
      { id: "cat-transport-rides", name: "Rides", system: false, children: [] },
      { id: "cat-transport-fuel", name: "Fuel", system: false, children: [] },
    ],
  },
  {
    id: "cat-entertainment",
    name: "Entertainment",
    system: true,
    children: [
      { id: "cat-entertainment-streaming", name: "Streaming", system: false, children: [] },
    ],
  },
  {
    id: "cat-income",
    name: "Income",
    system: true,
    children: [],
  },
];

export type MonthPoint = {
  m: string;
  v: number;
};

export const MOCK_SPEND_TREND: MonthPoint[] = [
  { m: "Nov", v: 1200 },
  { m: "Dec", v: 1800 },
  { m: "Jan", v: 950 },
  { m: "Feb", v: 1100 },
  { m: "Mar", v: 1320 },
  { m: "Apr", v: 1540 },
];

export type MerchantCharge = {
  date: string;
  amount: string;
};

export const MOCK_MERCHANT_HISTORY: MerchantCharge[] = [
  { date: "Apr 14", amount: "−€14.60" },
  { date: "Apr 7", amount: "−€22.10" },
  { date: "Mar 31", amount: "−€17.50" },
];

export const MOCK_MERCHANT_AVG = "−€18.30";

export type AIInsight = {
  icon: string;
  text: string;
};

export const MOCK_AI_INSIGHTS: AIInsight[] = [
  {
    icon: "↑",
    text: "You spent 16% more than last month — driven by Food (+€94) and a new Spotify sub.",
  },
  {
    icon: "◎",
    text: "Food & Groceries are 52% of spend this month. Together they totalled €800.",
  },
  {
    icon: "✓",
    text: "Largest income: Salary on Apr 21 (+€3,200). Net positive month (+€1,659).",
  },
];

export const MOCK_RULES: MockRule[] = [
  { id: "r1", keyword: "Bolt Food", category: "Food · Delivery" },
  { id: "r2", keyword: "wolt", category: "Food · Delivery" },
  { id: "r3", keyword: "spotify", category: "Entertainment · Streaming" },
  { id: "r4", keyword: "netflix", category: "Entertainment · Streaming" },
  { id: "r5", keyword: "rimi", category: "Groceries" },
  { id: "r6", keyword: "lidl", category: "Groceries" },
  { id: "r7", keyword: "starbucks", category: "Food · Coffee" },
];
