import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { mockDApps, mockTransactions } from "@/lib/mock-data";
import type { DApp, Transaction, CreateDAppPayload, CreateTransactionPayload } from "@/types/dapp";

// Set to true to use your real backend via api.ts
const USE_REAL_API = true;

// Mock implementations with simulated delay
let dapps = [...mockDApps];
let transactions = { ...mockTransactions };
let nextId = 100;

const delay = (ms: number) => new Promise((r) => setTimeout(r, ms));

export function useDApps() {
  return useQuery<DApp[]>({
    queryKey: ["dapps"],
    queryFn: async () => {
      if (USE_REAL_API) {
        const { api } = await import("@/lib/api");
        return api.getDApps();
      }
      await delay(300);
      return [...dapps];
    },
  });
}

export function useDApp(id: string) {
  return useQuery<DApp | undefined>({
    queryKey: ["dapp", id],
    queryFn: async () => {
      if (USE_REAL_API) {
        const { api } = await import("@/lib/api");
        return api.getDApp(id);
      }
      await delay(200);
      return dapps.find((d) => d.id === id);
    },
  });
}

export function useTransactions(dappId: string) {
  return useQuery<Transaction[]>({
    queryKey: ["transactions", dappId],
    queryFn: async () => {
      if (USE_REAL_API) {
        const { api } = await import("@/lib/api");
        return api.getTransactions(dappId);
      }
      await delay(300);
      return transactions[dappId] || [];
    },
  });
}

export function useCreateDApp() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (data: CreateDAppPayload) => {
      if (USE_REAL_API) {
        const { api } = await import("@/lib/api");
        return api.createDApp(data);
      }
      await delay(400);
      const newDApp: DApp = { id: String(nextId++), ...data, balance: 0 };
      dapps.push(newDApp);
      return newDApp;
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["dapps"] }),
  });
}

export function useDeleteDApp() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (id: string) => {
      if (USE_REAL_API) {
        const { api } = await import("@/lib/api");
        return api.deleteDApp(id);
      }
      await delay(300);
      dapps = dapps.filter((d) => d.id !== id);
      delete transactions[id];
    },
    onSuccess: () => qc.invalidateQueries({ queryKey: ["dapps"] }),
  });
}

export function useCreateTransaction() {
  const qc = useQueryClient();
  return useMutation({
    mutationFn: async (data: CreateTransactionPayload) => {
      if (USE_REAL_API) {
        const { api } = await import("@/lib/api");
        return api.createTransaction(data);
      }
      await delay(400);
      const tx: Transaction = { id: String(nextId++), ...data };
      if (!transactions[data.dappId]) transactions[data.dappId] = [];
      transactions[data.dappId].unshift(tx);
      // Update balance
      const dapp = dapps.find((d) => d.id === data.dappId);
      if (dapp) dapp.balance += data.amount;
      return tx;
    },
    onSuccess: (_, vars) => {
      qc.invalidateQueries({ queryKey: ["transactions", vars.dappId] });
      qc.invalidateQueries({ queryKey: ["dapps"] });
      qc.invalidateQueries({ queryKey: ["dapp", vars.dappId] });
    },
  });
}
