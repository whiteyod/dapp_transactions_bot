import { useState, useMemo } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Plus, Copy } from "lucide-react";
import { useDApp, useTransactions } from "@/hooks/use-dapps";
import { TransactionItem } from "@/components/TransactionItem";
import { AddTransactionDrawer } from "@/components/AddTransactionDrawer";
import { Skeleton } from "@/components/ui/skeleton";
import { truncateWallet, formatSol, formatUsd, formatDayKey, formatDayLabel } from "@/lib/format";
import { toast } from "sonner";
import type { Transaction } from "@/types/dapp";

function copyToClipboard(text: string, label: string) {
  navigator.clipboard.writeText(text).then(() => {
    toast.success(`${label} copied`);
  });
}

const DAppDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: dapp, isLoading: loadingDApp } = useDApp(id!);
  const { data: transactions, isLoading: loadingTx } = useTransactions(id!);
  const [addOpen, setAddOpen] = useState(false);

  const groupedTransactions = useMemo(() => {
    if (!transactions || transactions.length === 0) return [];
    const groups: { day: string; label: string; items: Transaction[] }[] = [];
    const map = new Map<string, Transaction[]>();
    for (const tx of transactions) {
      const key = formatDayKey(tx.timestamp);
      if (!map.has(key)) map.set(key, []);
      map.get(key)!.push(tx);
    }
    for (const [day, items] of map) {
      items.sort((a, b) => new Date(b.timestamp).getTime() - new Date(a.timestamp).getTime());
      groups.push({ day, label: formatDayLabel(day), items });
    }
    return groups.sort((a, b) => b.day.localeCompare(a.day));
  }, [transactions]);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-primary px-4 py-4 shadow-md">
        <div className="flex items-center gap-3">
          <div className="min-w-0 flex-1">
            {loadingDApp ? (
              <Skeleton className="h-5 w-32 bg-primary-foreground/20" />
            ) : (
              <h1 className="font-bold text-lg text-primary-foreground truncate">
                {dapp?.name}
              </h1>
            )}
          </div>
        </div>
      </header>

      <main className="max-w-[430px] mx-auto">
        {/* Balance card */}
        <div className="px-4 pt-4 pb-2">
          {loadingDApp ? (
            <Skeleton className="h-28 w-full rounded-lg" />
          ) : dapp ? (
            <div className="bg-card rounded-lg border p-4 space-y-3">
              <div className="text-center">
                <p className="text-xs text-muted-foreground uppercase tracking-wider">
                  Total Balance
                </p>
                <p className="font-mono text-3xl font-bold text-success mt-1">
                  {formatSol(dapp.balance)} SOL
                </p>
                <p className="font-mono text-sm text-muted-foreground">
                  {formatUsd(dapp.usdBalance)}
                </p>
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2 border-t border-border">
                <div
                  className="active:opacity-60 transition-opacity cursor-pointer"
                  onClick={() => copyToClipboard(dapp.ownerWallet, "Owner wallet")}
                >
                  <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                    Owner
                  </p>
                  <p className="font-mono text-xs text-foreground/80 mt-0.5 flex items-center gap-1">
                    {truncateWallet(dapp.ownerWallet, 6)}
                    <Copy className="w-3 h-3 text-muted-foreground/50" />
                  </p>
                </div>
                <div
                  className="active:opacity-60 transition-opacity cursor-pointer"
                  onClick={() => copyToClipboard(dapp.treasuryWallet, "Treasury wallet")}
                >
                  <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                    Treasury
                  </p>
                  <p className="font-mono text-xs text-foreground/80 mt-0.5 flex items-center gap-1">
                    {truncateWallet(dapp.treasuryWallet, 6)}
                    <Copy className="w-3 h-3 text-muted-foreground/50" />
                  </p>
                </div>
              </div>
            </div>
          ) : null}
        </div>

        {/* Transactions */}
        <div className="px-4 pt-4 pb-24">
          <h2 className="text-sm font-semibold text-muted-foreground uppercase tracking-wider mb-3">
            Transactions
          </h2>
          {loadingTx ? (
            Array.from({ length: 3 }).map((_, i) => (
              <Skeleton key={i} className="h-14 w-full mb-2 rounded" />
            ))
          ) : groupedTransactions.length > 0 ? (
            <div className="space-y-4">
              {groupedTransactions.map((group) => (
                <div key={group.day}>
                  <p className="text-xs font-semibold text-muted-foreground uppercase tracking-wider mb-2">
                    {group.label}
                  </p>
                  <div className="bg-card rounded-lg border px-3">
                    {group.items.map((tx) => (
                      <TransactionItem key={tx.id} tx={tx} />
                    ))}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <p className="text-center text-sm text-muted-foreground py-8">
              No transactions yet
            </p>
          )}
        </div>
      </main>

      {/* Back FAB */}
      <button
        onClick={() => navigate("/")}
        className="fixed bottom-6 left-6 z-50 w-14 h-14 rounded-full bg-muted text-foreground shadow-lg flex items-center justify-center active:scale-95 transition-transform"
        aria-label="Back to list"
      >
        <ArrowLeft className="w-6 h-6" />
      </button>

      {/* Add FAB */}
      <button
        onClick={() => setAddOpen(true)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-primary text-primary-foreground shadow-lg flex items-center justify-center active:scale-95 transition-transform"
        aria-label="Add Transaction"
      >
        <Plus className="w-6 h-6" />
      </button>

      <AddTransactionDrawer
        open={addOpen}
        onOpenChange={setAddOpen}
        dappId={id!}
      />
    </div>
  );
};

export default DAppDetail;
