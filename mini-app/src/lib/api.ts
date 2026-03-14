import type { DApp, Transaction, CreateDAppPayload, CreateTransactionPayload } from "@/types/dapp";

declare global {
  interface Window {
    Telegram?: {
      WebApp?: {
        initData?: string;
        ready?: () => void;
        expand?: () => void;
      };
    };
  }
}

const BASE_URL = import.meta.env.VITE_API_BASE_URL || "/api";

const getInitData = () => {
  if (typeof window !== "undefined" && window.Telegram?.WebApp?.initData) {
    return window.Telegram.WebApp.initData;
  }
  return "";
};

async function request<T>(path: string, options?: RequestInit): Promise<T> {
  const initData = getInitData();
  const url = `${BASE_URL}${path}${initData ? `?init_data=${encodeURIComponent(initData)}` : ""}`;
  const res = await fetch(url, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) throw new Error(`API error: ${res.status}`);
  return res.json();
}

type BackendDApp = {
  id: string;
  name: string;
  ownerWallet: string;
  treasuryWallet: string;
  balance: number;
  usdBalance?: number;
};

type BackendTransaction = {
  amount: number;
  timestamp: string;
};

const mapTransaction = (
  appName: string,
  tx: BackendTransaction,
  index: number,
): Transaction => ({
  id: `${appName}-${tx.timestamp}-${tx.amount}-${index}`,
  dappId: appName,
  amount: tx.amount,
  timestamp: tx.timestamp,
});

async function mapDApp(dapp: BackendDApp): Promise<DApp> {
  return {
    id: dapp.id,
    name: dapp.name,
    ownerWallet: dapp.ownerWallet,
    treasuryWallet: dapp.treasuryWallet,
    balance: dapp.balance,
  };
}

export const api = {
  getDApps: async () => {
    const dapps = await request<BackendDApp[]>("/dapps");
    return Promise.all(dapps.map(mapDApp));
  },
  getDApp: async (id: string) => {
    const dapp = await request<BackendDApp>(`/dapps/${encodeURIComponent(id)}`);
    return mapDApp(dapp);
  },
  createDApp: (data: CreateDAppPayload) =>
    request("/dapps", {
      method: "POST",
      body: JSON.stringify({
        name: data.name,
        owner: data.ownerWallet,
        treasury: data.treasuryWallet,
      }),
    }),
  deleteDApp: (id: string) =>
    request<void>(`/dapps/${encodeURIComponent(id)}`, { method: "DELETE" }),
  getTransactions: async (dappId: string) => {
    const transactions = await request<BackendTransaction[]>(`/dapps/${encodeURIComponent(dappId)}/transactions`);
    return transactions.map((tx, index) => mapTransaction(dappId, tx, index));
  },
  createTransaction: (data: CreateTransactionPayload) =>
    request(`/dapps/${encodeURIComponent(data.dappId)}/transactions`, {
      method: "POST",
      body: JSON.stringify({
        app_name: data.dappId,
        trans_amount: data.amount,
      }),
    }),
};
