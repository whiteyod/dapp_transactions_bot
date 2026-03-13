import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import {
  Drawer, DrawerContent, DrawerHeader, DrawerTitle, DrawerDescription,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { useCreateDApp } from "@/hooks/use-dapps";
import { toast } from "sonner";

const schema = z.object({
  name: z.string().trim().min(1, "App name is required").max(100),
  ownerWallet: z.string().trim().min(1, "Owner wallet is required"),
  treasuryWallet: z.string().trim().min(1, "Treasury wallet is required"),
});

type FormData = z.infer<typeof schema>;

interface AddDAppDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

export function AddDAppDrawer({ open, onOpenChange }: AddDAppDrawerProps) {
  const createDApp = useCreateDApp();
  const {
    register,
    handleSubmit,
    reset,
    formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: Required<FormData>) => {
    try {
      await createDApp.mutateAsync(data);
      toast.success("dApp added!");
      reset();
      onOpenChange(false);
    } catch {
      toast.error("Failed to add dApp");
    }
  };

  return (
    <Drawer open={open} onOpenChange={onOpenChange}>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Add New dApp</DrawerTitle>
          <DrawerDescription>
            Enter the details for your Solana dApp
          </DrawerDescription>
        </DrawerHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="px-4 pb-6 space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="name">App Name</Label>
            <Input id="name" placeholder="My dApp" {...register("name")} />
            {errors.name && (
              <p className="text-xs text-destructive">{errors.name.message}</p>
            )}
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="ownerWallet">Owner Wallet</Label>
            <Input
              id="ownerWallet"
              placeholder="Solana wallet address"
              className="font-mono text-sm"
              {...register("ownerWallet")}
            />
            {errors.ownerWallet && (
              <p className="text-xs text-destructive">{errors.ownerWallet.message}</p>
            )}
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="treasuryWallet">Treasury Wallet</Label>
            <Input
              id="treasuryWallet"
              placeholder="Treasury wallet address"
              className="font-mono text-sm"
              {...register("treasuryWallet")}
            />
            {errors.treasuryWallet && (
              <p className="text-xs text-destructive">{errors.treasuryWallet.message}</p>
            )}
          </div>
          <div className="flex gap-3 pt-2">
            <Button
              type="button"
              variant="outline"
              className="flex-1"
              onClick={() => {
                reset();
                onOpenChange(false);
              }}
            >
              Cancel
            </Button>
            <Button
              type="submit"
              className="flex-1"
              disabled={createDApp.isPending}
            >
              {createDApp.isPending ? "Adding..." : "Add dApp"}
            </Button>
          </div>
        </form>
      </DrawerContent>
    </Drawer>
  );
}
