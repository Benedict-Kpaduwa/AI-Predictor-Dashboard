import React from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  PieChart,
  Pie,
  Cell,
} from "recharts";
import {
  AlertTriangle,
  CheckCircle,
  XCircle,
  Activity,
  RefreshCw,
} from "lucide-react";
import AssetCard from "./AssetCard";
import type { Asset, RiskDistributionEntry } from "@/MaintenanceDashboard";

interface OverviewDashboardProps {
  assets: Asset[];
  fetchAssetDetail: (id: string | number) => void;
  loading: boolean;
  error: string | null;
  riskDistribution: RiskDistributionEntry[];
}

interface SensorBarData {
  name: string;
  value: number;
}

const OverviewDashboard: React.FC<OverviewDashboardProps> = ({
  assets,
  fetchAssetDetail,
  loading,
  error,
  riskDistribution,
}) => {
  const sensorData: SensorBarData[] =
    assets.length === 0
      ? []
      : [
          {
            name: "Temperature",
            value:
              assets.reduce((a, b) => a + b.temperature, 0) / assets.length,
          },
          {
            name: "Vibration",
            value:
              (assets.reduce((a, b) => a + b.vibration, 0) / assets.length) *
              20,
          },
          {
            name: "Pressure",
            value: assets.reduce((a, b) => a + b.pressure, 0) / assets.length,
          },
        ];

  return (
    <div className="space-y-6">
      {error && (
        <div className="bg-red-50 border-l-4 border-red-500 p-4 rounded">
          <p className="text-red-700">⚠️ {error}</p>
        </div>
      )}

      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Total Assets</p>
              <p className="text-2xl font-bold text-gray-800">
                {assets.length}
              </p>
            </div>
            <Activity className="w-8 h-8 text-blue-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Healthy</p>
              <p className="text-2xl font-bold text-green-600">
                {assets.filter((a) => a.riskLevel === "healthy").length}
              </p>
            </div>
            <CheckCircle className="w-8 h-8 text-green-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Warning</p>
              <p className="text-2xl font-bold text-yellow-600">
                {assets.filter((a) => a.riskLevel === "warning").length}
              </p>
            </div>
            <AlertTriangle className="w-8 h-8 text-yellow-500" />
          </div>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between">
            <div>
              <p className="text-gray-500 text-sm">Critical</p>
              <p className="text-2xl font-bold text-red-600">
                {assets.filter((a) => a.riskLevel === "critical").length}
              </p>
            </div>
            <XCircle className="w-8 h-8 text-red-500" />
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg mb-4 text-gray-800">
            Risk Distribution
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <PieChart>
              <Pie
                data={riskDistribution}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, value }) => `${name}: ${value}`}
                outerRadius={80}
                dataKey="value"
              >
                {riskDistribution.map((entry, index) => (
                  <Cell key={index} fill={entry.color} />
                ))}
              </Pie>
              <Tooltip />
            </PieChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg mb-4 text-gray-800">
            Average Sensor Readings
          </h3>
          <ResponsiveContainer width="100%" height={250}>
            <BarChart data={sensorData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis />
              <Tooltip />
              <Bar dataKey="value" fill="#000000" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      <div>
        <h3 className="font-bold text-xl mb-4 text-gray-800">Asset Status</h3>

        {loading ? (
          <div className="text-center py-12">
            <RefreshCw className="w-12 h-12 animate-spin mx-auto text-blue-500" />
            <p className="mt-4 text-gray-600">Loading assets...</p>
          </div>
        ) : assets.length === 0 ? (
          <div className="text-center py-12 bg-gray-50 rounded-lg">
            <p className="text-gray-600">
              No assets found. Upload a CSV file to get started.
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            {assets.map((asset) => (
              <AssetCard
                key={asset.id}
                asset={asset}
                fetchAssetDetail={fetchAssetDetail}
              />
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default OverviewDashboard;
