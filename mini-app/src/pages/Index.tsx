import { useState } from "react";
import { Plus } from "lucide-react";
import { useDApps, useDeleteDApp } from "@/hooks/use-dapps";
import { DAppCard } from "@/components/DAppCard";
import { AddDAppDrawer } from "@/components/AddDAppDrawer";
import { DeleteDAppDialog } from "@/components/DeleteDAppDialog";
import { Skeleton } from "@/components/ui/skeleton";
import { toast } from "sonner";
import type { DApp } from "@/types/dapp";

const Index = () => {
  const { data: dapps, isLoading } = useDApps();
  const deleteDApp = useDeleteDApp();
  const [addOpen, setAddOpen] = useState(false);
  const [deleteTarget, setDeleteTarget] = useState<DApp | null>(null);

  const handleDelete = async () => {
    if (!deleteTarget) return;
    try {
      await deleteDApp.mutateAsync(deleteTarget.id);
      toast.success(`${deleteTarget.name} deleted`);
      setDeleteTarget(null);
    } catch {
      toast.error("Failed to delete dApp");
    }
  };

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="sticky top-0 z-40 bg-primary px-4 py-4 shadow-md">
        <h1 className="text-lg font-bold text-primary-foreground tracking-tight">
          ◎ SOL Tracker
        </h1>
        <p className="text-xs text-primary-foreground/70 mt-0.5">
          Track transactions across your dApps
        </p>
      </header>

      {/* Content */}
      <main className="p-4 pb-24 space-y-3 max-w-[430px] mx-auto">
        {isLoading ? (
          Array.from({ length: 3 }).map((_, i) => (
            <Skeleton key={i} className="h-24 w-full rounded-lg" />
          ))
        ) : dapps && dapps.length > 0 ? (
          dapps.map((dapp) => (
            <DAppCard key={dapp.id} dapp={dapp} onDelete={setDeleteTarget} />
          ))
        ) : (
          <div className="text-center py-16">
            <p className="text-muted-foreground text-sm">No dApps yet</p>
            <p className="text-muted-foreground text-xs mt-1">
              Tap + to add your first one
            </p>
          </div>
        )}
      </main>

      {/* FAB */}
      <button
        onClick={() => setAddOpen(true)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-primary text-primary-foreground shadow-lg flex items-center justify-center active:scale-95 transition-transform"
        aria-label="Add dApp"
      >
        <Plus className="w-6 h-6" />
      </button>

      <AddDAppDrawer open={addOpen} onOpenChange={setAddOpen} />
      <DeleteDAppDialog
        dapp={deleteTarget}
        open={!!deleteTarget}
        onOpenChange={(open) => !open && setDeleteTarget(null)}
        onConfirm={handleDelete}
        isPending={deleteDApp.isPending}
      />
    </div>
  );
};

export default Index;
