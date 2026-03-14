import { useNavigate } from "react-router-dom";
import { Trash2, Copy } from "lucide-react";
import { Card } from "@/components/ui/card";
import { truncateWallet, formatSol, formatUsd } from "@/lib/format";
import { toast } from "sonner";
import type { DApp } from "@/types/dapp";

function copyToClipboard(text: string, label: string) {
  navigator.clipboard.writeText(text).then(() => {
    toast.success(`${label} copied`);
  });
}

interface DAppCardProps {
  dapp: DApp;
  onDelete: (dapp: DApp) => void;
}

export function DAppCard({ dapp, onDelete }: DAppCardProps) {
  const navigate = useNavigate();

  return (
    <Card
      className="relative p-4 active:scale-[0.98] transition-transform cursor-pointer animate-slide-up-fade"
      onClick={() => navigate(`/dapp/${dapp.id}`)}
    >
      <div className="flex items-start justify-between gap-3">
        <div className="min-w-0 flex-1">
          <h3 className="font-semibold text-base text-foreground truncate">
            {dapp.name}
          </h3>
          <div className="mt-1.5 space-y-0.5">
            <p
              className="text-xs text-muted-foreground flex items-center gap-1 active:opacity-60 transition-opacity"
              onClick={(e) => { e.stopPropagation(); copyToClipboard(dapp.ownerWallet, "Owner wallet"); }}
            >
              Owner:{" "}
              <span className="font-mono text-foreground/70">
                {truncateWallet(dapp.ownerWallet)}
              </span>
              <Copy className="w-3 h-3 text-muted-foreground/50" />
            </p>
            <p
              className="text-xs text-muted-foreground flex items-center gap-1 active:opacity-60 transition-opacity"
              onClick={(e) => { e.stopPropagation(); copyToClipboard(dapp.treasuryWallet, "Treasury wallet"); }}
            >
              Treasury:{" "}
              <span className="font-mono text-foreground/70">
                {truncateWallet(dapp.treasuryWallet)}
              </span>
              <Copy className="w-3 h-3 text-muted-foreground/50" />
            </p>
          </div>
        </div>
        <div className="flex flex-col items-end gap-2">
          <div className="text-right">
            <span className="font-mono font-medium text-lg text-success">
              {formatSol(dapp.balance)} SOL
            </span>
            <p className="font-mono text-xs text-muted-foreground">
              {formatUsd(dapp.usdBalance)}
            </p>
          </div>
          <button
            onClick={(e) => {
              e.stopPropagation();
              onDelete(dapp);
            }}
            className="p-1.5 rounded-md text-muted-foreground active:bg-destructive/10 active:text-destructive transition-colors"
            aria-label={`Delete ${dapp.name}`}
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>
    </Card>
  );
}
