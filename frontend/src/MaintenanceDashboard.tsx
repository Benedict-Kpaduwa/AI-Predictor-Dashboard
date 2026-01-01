import { useState, useEffect } from "react";
import axios, { AxiosError } from "axios";
import type { AxiosProgressEvent } from "axios";
import { BarChart3, Download, RefreshCw, Upload } from "lucide-react";
import OverviewDashboard from "@/components/OverviewDashboard";
import DetailView from "@/components/DetailView";
import UploadSummaryDialog from "./components/UploadSummaryDialog";
import UploadProgressDialog from "./components/UploadProgressDialog";
import StatisticsView from "./components/Statatics";

export type Asset = {
  id: number;
  name: string;
  riskLevel: "healthy" | "warning" | "critical" | string;
  temperature: number;
  vibration: number;
  pressure: number;
  riskScore: number;
  runtime: number;
  predictedFailure: number;
  lastMaintenance: string;
  historicalData: HistoricalDataPoint[];
};

export interface RiskDistributionEntry {
  name: string;
  value: number;
  color: string;
}

interface HistoricalDataPoint {
  time: string;
  temperature: number;
  vibration: number;
  pressure: number;
}

interface UploadSummary {
  total: number;
  healthy: number;
  warning: number;
  critical: number;
}

const MaintenanceDashboard: React.FC = () => {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [selectedAsset, setSelectedAsset] = useState<Asset | null>(null);
  const [uploading, setUploading] = useState<boolean>(false);
  const [view, setView] = useState<"overview" | "detail">("overview");
  const [loading, setLoading] = useState<boolean>(false);
  const [error, setError] = useState<string | null>(null);
  const [dialogOpen, setDialogOpen] = useState<boolean>(false);
  const [uploadSummary, setUploadSummary] = useState<UploadSummary | null>(
    null
  );
  const [uploadProgress, setUploadProgress] = useState<number>(0);
  const [progressDialogOpen, setProgressDialogOpen] = useState<boolean>(false);
  const [exportingPDF, setExportingPDF] = useState(false);

  // const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

  const API_URL = import.meta.env.PROD
    ? "" // On Render, same origin (FastAPI serves frontend)
    : "http://localhost:8000";

  const fetchAssets = async () => {
    setLoading(true);
    setError(null);

    try {
      const { data } = await axios.get<Asset[]>(`${API_URL}/assets/`);
      setAssets(data);
    } catch (err) {
      const axiosErr = err as AxiosError<{ detail?: string }>;
      const msg = axiosErr.response?.data?.detail || axiosErr.message;
      setError(msg);
      console.error("Error fetching assets:", msg);
    } finally {
      setLoading(false);
    }
  };

  const fetchAssetDetail = async (assetId: number) => {
    try {
      const { data } = await axios.get<Asset>(`${API_URL}/assets/${assetId}`);
      setSelectedAsset(data);
      setView("detail");
    } catch (err) {
      const axiosErr = err as AxiosError<{ detail?: string }>;
      const msg = axiosErr.response?.data?.detail || axiosErr.message;
      setError(msg);
      console.error("Error fetching asset details:", msg);
    }
  };

  const handleExportPDF = async () => {
    if (assets.length === 0) {
      alert("No assets to export. Please upload a CSV first.");
      return;
    }

    setExportingPDF(true);

    try {
      const response = await axios.get(`${API_URL}/export-report/`, {
        responseType: "blob",
      });

      const url = window.URL.createObjectURL(new Blob([response.data]));
      const a = document.createElement("a");
      a.href = url;
      a.download = `maintenance_report_${
        new Date().toISOString().split("T")[0]
      }.pdf`;

      document.body.appendChild(a);
      a.click();

      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (err) {
      const message =
        err.response?.data?.message || err.message || "Export failed";
      alert(`Export failed: ${message}`);
    } finally {
      setExportingPDF(false);
    }
  };

  const handleFileUpload = async (
    e: React.ChangeEvent<HTMLInputElement>
  ): Promise<void> => {
    const file = e.target.files?.[0];
    if (!file) return;

    setUploading(true);
    setProgressDialogOpen(true);
    setError(null);

    const formData = new FormData();
    formData.append("file", file);

    try {
      const { data } = await axios.post(`${API_URL}/upload/`, formData, {
        headers: { "Content-Type": "multipart/form-data" },
        onUploadProgress: (progressEvent: AxiosProgressEvent) => {
          if (progressEvent.total) {
            const percent = Math.round(
              (progressEvent.loaded * 100) / progressEvent.total
            );
            setUploadProgress(percent);
          }
        },
      });

      setAssets(data.assets);

      const summary: UploadSummary = {
        total: data.assets.length,
        healthy: data.summary.healthy,
        warning: data.summary.warning,
        critical: data.summary.critical,
      };

      setUploadSummary(summary);
      setProgressDialogOpen(false);
      setDialogOpen(true);
    } catch (err) {
      const axiosErr = err as AxiosError<{ detail?: string }>;
      const msg = axiosErr.response?.data?.detail || axiosErr.message;
      setError(msg);
      alert(`Upload failed: ${msg}`);
    } finally {
      setUploading(false);
      e.target.value = "";
    }
  };

  const riskDistribution: RiskDistributionEntry[] = [
    {
      name: "Healthy",
      value: assets.filter((a) => a.riskLevel === "healthy").length,
      color: "#10b981",
    },
    {
      name: "Warning",
      value: assets.filter((a) => a.riskLevel === "warning").length,
      color: "#f59e0b",
    },
    {
      name: "Critical",
      value: assets.filter((a) => a.riskLevel === "critical").length,
      color: "#ef4444",
    },
  ];

  useEffect(() => {
    fetchAssets();
  }, []);

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="bg-black text-white shadow-lg">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold">
                AI Maintenance Predictor Dashboard
              </h1>
              <p className="text-blue-100 mt-1">
                Predictive Maintenance & Asset Risk Analysis
              </p>
            </div>

            <div className="flex items-center space-x-4">
              <button
                onClick={() => setView("statistics")}
                className="bg-white text-black px-4 py-2 rounded-lg font-semibold hover:bg-gray-200 transition-colors flex items-center cursor-pointer"
              >
                <BarChart3 className="w-4 h-4 mr-2" />
                Statistics
              </button>
              <button
                onClick={handleExportPDF}
                disabled={exportingPDF || assets.length === 0}
                className="bg-white text-black px-4 py-2 rounded-lg font-semibold hover:bg-gray-200 transition-colors flex items-center disabled:opacity-50 cursor-pointer disabled:cursor-not-allowed"
              >
                <Download className="w-4 h-4 mr-2" />
                {exportingPDF ? "Exporting..." : "Export PDF"}
              </button>
              <button
                onClick={fetchAssets}
                disabled={loading}
                className="bg-white text-black px-4 py-2 rounded-lg font-semibold hover:bg-gray-200 cursor-pointer transition-colors flex items-center"
              >
                <RefreshCw
                  className={`w-4 h-4 mr-2 ${loading ? "animate-spin" : ""}`}
                />
                Refresh
              </button>

              <label className="cursor-pointer bg-white text-black px-4 py-2 rounded-lg font-semibold hover:bg-gray-200 transition-colors flex items-center">
                <Upload className="w-4 h-4 mr-2" />
                {uploading ? "Processing..." : "Upload CSV"}
                <input
                  type="file"
                  accept=".csv"
                  onChange={handleFileUpload}
                  className="hidden"
                  disabled={uploading}
                />
              </label>
            </div>
          </div>
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 py-8">
        {view === "overview" ? (
          <OverviewDashboard
            assets={assets}
            fetchAssetDetail={fetchAssetDetail}
            loading={loading}
            error={error}
            riskDistribution={riskDistribution}
          />
        ) : view === "statistics" ? (
          <StatisticsView
            assets={assets}
            riskDistribution={riskDistribution}
            setView={setView}
          />
        ) : (
          <DetailView selectedAsset={selectedAsset} setView={setView} />
        )}
      </div>

      <div className="bg-white border-t mt-12">
        <div className="max-w-7xl mx-auto px-4 py-6">
          <div className="flex items-center justify-between text-sm text-gray-600">
            <div>
              <p className="font-semibold">Tech Stack:</p>
              <p>FastAPI • Python • scikit-learn • React • Recharts • Docker</p>
            </div>
            <div>
              <p className="font-semibold">
                API Status:{" "}
                <span className="text-green-600">
                  {loading ? "Loading..." : "Connected ✓"}
                </span>
              </p>
            </div>
          </div>
        </div>
      </div>

      <UploadProgressDialog
        open={progressDialogOpen}
        progress={uploadProgress}
      />
      <UploadSummaryDialog
        open={dialogOpen}
        onClose={() => setDialogOpen(false)}
        summary={
          uploadSummary || { total: 0, healthy: 0, warning: 0, critical: 0 }
        }
      />
    </div>
  );
};

export default MaintenanceDashboard;
