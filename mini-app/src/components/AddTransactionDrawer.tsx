import { useState } from "react";
import { useForm } from "react-hook-form";
import { zodResolver } from "@hookform/resolvers/zod";
import { z } from "zod";
import { format } from "date-fns";
import { CalendarIcon } from "lucide-react";
import {
  Drawer, DrawerContent, DrawerHeader, DrawerTitle, DrawerDescription,
} from "@/components/ui/drawer";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import { Popover, PopoverContent, PopoverTrigger } from "@/components/ui/popover";
import { Calendar } from "@/components/ui/calendar";
import { useCreateTransaction } from "@/hooks/use-dapps";
import { toast } from "sonner";
import { cn } from "@/lib/utils";

const schema = z.object({
  amount: z.coerce.number({ invalid_type_error: "Enter a valid number" }).refine((v) => v !== 0, "Amount cannot be 0"),
  description: z.string().trim().max(200).optional(),
});

type FormData = z.infer<typeof schema>;

interface AddTransactionDrawerProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
  dappId: string;
}

export function AddTransactionDrawer({ open, onOpenChange, dappId }: AddTransactionDrawerProps) {
  const createTx = useCreateTransaction();
  const [date, setDate] = useState<Date>(new Date());
  const {
    register, handleSubmit, reset, formState: { errors },
  } = useForm<FormData>({ resolver: zodResolver(schema) });

  const onSubmit = async (data: FormData) => {
    try {
      await createTx.mutateAsync({
        dappId,
        amount: data.amount,
        timestamp: date.toISOString(),
        description: data.description || undefined,
      });
      toast.success("Transaction added!");
      reset();
      setDate(new Date());
      onOpenChange(false);
    } catch {
      toast.error("Failed to add transaction");
    }
  };

  return (
    <Drawer open={open} onOpenChange={onOpenChange}>
      <DrawerContent>
        <DrawerHeader>
          <DrawerTitle>Add Transaction</DrawerTitle>
          <DrawerDescription>Record a new SOL transaction</DrawerDescription>
        </DrawerHeader>
        <form onSubmit={handleSubmit(onSubmit)} className="px-4 pb-6 space-y-4">
          <div className="space-y-1.5">
            <Label htmlFor="amount">Amount (SOL)</Label>
            <Input
              id="amount"
              type="number"
              step="any"
              placeholder="e.g. 10.5 or -5"
              className="font-mono"
              {...register("amount")}
            />
            {errors.amount && (
              <p className="text-xs text-destructive">{errors.amount.message}</p>
            )}
          </div>
          <div className="space-y-1.5">
            <Label>Timestamp</Label>
            <Popover>
              <PopoverTrigger asChild>
                <Button variant="outline" className={cn("w-full justify-start text-left font-normal")}>
                  <CalendarIcon className="mr-2 h-4 w-4" />
                  {format(date, "PPP p")}
                </Button>
              </PopoverTrigger>
              <PopoverContent className="w-auto p-0" align="start">
                <Calendar
                  mode="single"
                  selected={date}
                  onSelect={(d) => d && setDate(d)}
                  initialFocus
                  className="p-3 pointer-events-auto"
                />
              </PopoverContent>
            </Popover>
          </div>
          <div className="space-y-1.5">
            <Label htmlFor="description">Description (optional)</Label>
            <Input id="description" placeholder="What's this for?" {...register("description")} />
          </div>
          <div className="flex gap-3 pt-2">
            <Button type="button" variant="outline" className="flex-1" onClick={() => { reset(); onOpenChange(false); }}>
              Cancel
            </Button>
            <Button type="submit" className="flex-1" disabled={createTx.isPending}>
              {createTx.isPending ? "Adding..." : "Add Transaction"}
            </Button>
          </div>
        </form>
      </DrawerContent>
    </Drawer>
  );
}
