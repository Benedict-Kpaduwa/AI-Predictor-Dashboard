import React from "react";
import { AlertTriangle, CheckCircle, XCircle, Activity } from "lucide-react";
import type { Asset } from "@/MaintenanceDashboard";

interface AssetsProps {
  asset: Asset;
  fetchAssetDetail: (id: string | number) => void;
}

const AssetCard: React.FC<AssetsProps> = ({ asset, fetchAssetDetail }) => {
  const getRiskIcon = (level: string) => {
    switch (level) {
      case "critical":
        return <XCircle className="w-6 h-6" />;
      case "warning":
        return <AlertTriangle className="w-6 h-6" />;
      case "healthy":
        return <CheckCircle className="w-6 h-6" />;
      default:
        return <Activity className="w-6 h-6" />;
    }
  };

  const getRiskColor = (level: string) => {
    switch (level) {
      case "critical":
        return "#ef4444";
      case "warning":
        return "#f59e0b";
      case "healthy":
        return "#10b981";
      default:
        return "#6b7280";
    }
  };

  return (
    <div
      className="bg-white rounded-lg shadow-md p-4 cursor-pointer hover:shadow-lg transition-shadow border-l-4"
      style={{ borderLeftColor: getRiskColor(asset.riskLevel) }}
      onClick={() => fetchAssetDetail(asset.id)}
    >
      <div className="flex items-start justify-between mb-3">
        <div>
          <h3 className="font-bold text-lg text-gray-800">{asset.name}</h3>
          <p className="text-sm text-gray-500">Asset ID: {asset.id}</p>
        </div>
        <div style={{ color: getRiskColor(asset.riskLevel) }}>
          {getRiskIcon(asset.riskLevel)}
        </div>
      </div>

      <div className="space-y-2">
        <div className="flex justify-between items-center">
          <span className="text-sm text-gray-600">Risk Score</span>
          <span
            className="font-bold text-lg"
            style={{ color: getRiskColor(asset.riskLevel) }}
          >
            {asset.riskScore}%
          </span>
        </div>

        <div className="grid grid-cols-2 gap-2 text-sm">
          <div>
            <p className="text-gray-500">Temperature</p>
            <p className="font-semibold">{asset.temperature.toFixed(1)}°C</p>
          </div>
          <div>
            <p className="text-gray-500">Vibration</p>
            <p className="font-semibold">{asset.vibration.toFixed(2)} mm/s</p>
          </div>
          <div>
            <p className="text-gray-500">Pressure</p>
            <p className="font-semibold">{asset.pressure.toFixed(1)} PSI</p>
          </div>
          <div>
            <p className="text-gray-500">Runtime</p>
            <p className="font-semibold">{asset.runtime}h</p>
          </div>
        </div>

        <div className="pt-2 border-t">
          <p className="text-xs text-gray-500">Predicted failure in</p>
          <p className="font-bold text-sm">{asset.predictedFailure} days</p>
        </div>
      </div>
    </div>
  );
};

export default AssetCard;
