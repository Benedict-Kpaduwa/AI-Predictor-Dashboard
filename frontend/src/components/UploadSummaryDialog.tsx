import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogFooter,
} from "@/components/ui/dialog";
import { Button } from "@/components/ui/button";

interface UploadSummary {
  total: number;
  healthy: number;
  warning: number;
  critical: number;
}

interface UploadSummaryDialogProps {
  open: boolean;
  onClose: () => void;
  summary: UploadSummary;
}

const UploadSummaryDialog: React.FC<UploadSummaryDialogProps> = ({
  open,
  onClose,
  summary,
}) => {
  return (
    <Dialog open={open} onOpenChange={onClose}>
      <DialogContent className="max-w-md">
        <DialogHeader>
          <DialogTitle className="text-xl font-bold">
            Upload Complete ✓
          </DialogTitle>
        </DialogHeader>

        <div className="space-y-3">
          <p className="text-gray-600">
            Successfully processed <strong>{summary.total}</strong> assets.
          </p>

          <ul className="space-y-1 text-sm">
            <li>
              ✅ Healthy: <strong>{summary.healthy}</strong>
            </li>
            <li>
              ⚠️ Warning: <strong>{summary.warning}</strong>
            </li>
            <li>
              ❗ Critical: <strong>{summary.critical}</strong>
            </li>
          </ul>
        </div>

        <DialogFooter>
          <Button onClick={onClose}>Close</Button>
        </DialogFooter>
      </DialogContent>
    </Dialog>
  );
};

export default UploadSummaryDialog;
