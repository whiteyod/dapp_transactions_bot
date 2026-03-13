import type { DApp, Transaction } from "@/types/dapp";

export const mockDApps: DApp[] = [
  {
    id: "1",
    name: "SolSwap DEX",
    ownerWallet: "7xKXtg2CW87d97TXJSDpbD5jBkheTqA83TZRuJosgAsU",
    treasuryWallet: "9WzDXwBbmkg8ZTbNMqUxvQRAyrZzDsGYdLVL9zYtAWWM",
    balance: 142.58,
  },
  {
    id: "2",
    name: "NFT Marketplace",
    ownerWallet: "4zMMC9srt5Ri5X14GAgXhaHii3GnPAEERYPJgZJDncDU",
    treasuryWallet: "CuieVDEDtLo7FypA9SbLM9saXFdb1dsshEkyErMqkRQq",
    balance: 89.32,
  },
  {
    id: "3",
    name: "Staking Pool",
    ownerWallet: "HN7cABqLq46Es1jh92dQQisAi5YqAx3arF5CLmSPBg82",
    treasuryWallet: "3Kp8gUfHN7T3PJE4mZcuP6dgGTfLJbqEkRxCYQB8kcMt",
    balance: 1024.0,
  },
];

export const mockTransactions: Record<string, Transaction[]> = {
  "1": [
    { id: "t1", dappId: "1", amount: 50.0, timestamp: "2026-03-12T14:30:00Z", description: "User swap fee" },
    { id: "t2", dappId: "1", amount: -12.5, timestamp: "2026-03-11T09:15:00Z", description: "LP withdrawal" },
    { id: "t3", dappId: "1", amount: 105.08, timestamp: "2026-03-10T18:45:00Z", description: "Pool deposit" },
  ],
  "2": [
    { id: "t4", dappId: "2", amount: 25.0, timestamp: "2026-03-12T11:00:00Z", description: "NFT sale royalty" },
    { id: "t5", dappId: "2", amount: 64.32, timestamp: "2026-03-09T16:20:00Z", description: "Listing fees" },
  ],
  "3": [
    { id: "t6", dappId: "3", amount: 500.0, timestamp: "2026-03-13T08:00:00Z", description: "Staking reward" },
    { id: "t7", dappId: "3", amount: 524.0, timestamp: "2026-03-08T12:00:00Z", description: "Initial deposit" },
  ],
};
