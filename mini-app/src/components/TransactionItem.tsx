import { formatSol, formatTimestamp } from "@/lib/format";
import type { Transaction } from "@/types/dapp";

interface TransactionItemProps {
  tx: Transaction;
}

export function TransactionItem({ tx }: TransactionItemProps) {
  const isPositive = tx.amount >= 0;

  return (
    <div className="flex items-center justify-between py-3 px-1 border-b border-border last:border-0 animate-slide-up-fade">
      <div className="min-w-0 flex-1">
        <p className="text-sm font-medium text-foreground truncate">
          {tx.description || "Transaction"}
        </p>
        <p className="text-xs text-muted-foreground mt-0.5">
          {formatTimestamp(tx.timestamp)}
        </p>
      </div>
      <span
        className={`font-mono font-medium text-sm ${
          isPositive ? "text-success" : "text-destructive"
        }`}
      >
        {isPositive ? "+" : ""}
        {formatSol(tx.amount)} SOL
      </span>
    </div>
  );
}
