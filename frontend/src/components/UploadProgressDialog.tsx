import React from "react";
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
} from "@/components/ui/dialog";
import { Progress } from "@/components/ui/progress";

interface UploadProgressDialogProps {
  open: boolean;
  progress: number;
}

const UploadProgressDialog: React.FC<UploadProgressDialogProps> = ({
  open,
  progress,
}) => {
  return (
    <Dialog open={open}>
      <DialogContent className="max-w-sm">
        <DialogHeader>
          <DialogTitle className="font-semibold">Uploading CSV...</DialogTitle>
        </DialogHeader>

        <div className="space-y-3 mt-2">
          <Progress value={progress} />
          <p className="text-sm text-gray-600 text-center">
            {progress}% completed
          </p>
        </div>
      </DialogContent>
    </Dialog>
  );
};

export default UploadProgressDialog;
