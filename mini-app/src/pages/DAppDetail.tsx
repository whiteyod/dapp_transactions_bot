import { useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { ArrowLeft, Plus } from "lucide-react";
import { useDApp, useTransactions } from "@/hooks/use-dapps";
import { TransactionItem } from "@/components/TransactionItem";
import { AddTransactionDrawer } from "@/components/AddTransactionDrawer";
import { Skeleton } from "@/components/ui/skeleton";
import { truncateWallet, formatSol } from "@/lib/format";

const DAppDetail = () => {
  const { id } = useParams<{ id: string }>();
  const navigate = useNavigate();
  const { data: dapp, isLoading: loadingDApp } = useDApp(id!);
  const { data: transactions, isLoading: loadingTx } = useTransactions(id!);
  const [addOpen, setAddOpen] = useState(false);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-primary px-4 py-4 shadow-md">
        <div className="flex items-center gap-3">
          <button
            onClick={() => navigate("/")}
            className="p-1 -ml-1 text-primary-foreground/80 active:text-primary-foreground"
            aria-label="Back"
          >
            <ArrowLeft className="w-5 h-5" />
          </button>
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
              </div>
              <div className="grid grid-cols-2 gap-2 pt-2 border-t border-border">
                <div>
                  <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                    Owner
                  </p>
                  <p className="font-mono text-xs text-foreground/80 mt-0.5">
                    {truncateWallet(dapp.ownerWallet, 6)}
                  </p>
                </div>
                <div>
                  <p className="text-[10px] text-muted-foreground uppercase tracking-wider">
                    Treasury
                  </p>
                  <p className="font-mono text-xs text-foreground/80 mt-0.5">
                    {truncateWallet(dapp.treasuryWallet, 6)}
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
          ) : transactions && transactions.length > 0 ? (
            <div className="bg-card rounded-lg border px-3">
              {transactions.map((tx) => (
                <TransactionItem key={tx.id} tx={tx} />
              ))}
            </div>
          ) : (
            <p className="text-center text-sm text-muted-foreground py-8">
              No transactions yet
            </p>
          )}
        </div>
      </main>

      {/* FAB */}
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
