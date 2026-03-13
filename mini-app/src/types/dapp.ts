export interface DApp {
  id: string;
  name: string;
  ownerWallet: string;
  treasuryWallet: string;
  balance: number;
}

export interface Transaction {
  id: string;
  dappId: string;
  amount: number;
  timestamp: string;
  description?: string;
}

export interface CreateDAppPayload {
  name: string;
  ownerWallet: string;
  treasuryWallet: string;
}

export interface CreateTransactionPayload {
  dappId: string;
  amount: number;
  timestamp: string;
  description?: string;
}
