import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from "recharts";
import { Zap } from "lucide-react";
import type { Asset } from "@/MaintenanceDashboard";

interface DetailViewProps {
  selectedAsset: Asset | null;
  setView: (view: string) => void;
}

const DetailView: React.FC<DetailViewProps> = ({ selectedAsset, setView }) => {
  if (!selectedAsset) return null;

  const getRiskColor = (level: string): string => {
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
    <div className="space-y-6">
      <button
        onClick={() => setView("overview")}
        className="text-gray-600 hover:text-gray-800 font-semibold cursor-pointer"
      >
        ← Back to Overview
      </button>

      <div className="bg-white rounded-lg shadow-lg p-6">
        <div className="flex items-start justify-between mb-6">
          <div>
            <h2 className="text-2xl font-bold text-gray-800">
              {selectedAsset.name}
            </h2>
            <p className="text-gray-500">Detailed Analysis & Predictions</p>
          </div>
          <div
            className="px-4 py-2 rounded-full font-bold text-white"
            style={{ backgroundColor: getRiskColor(selectedAsset.riskLevel) }}
          >
            {selectedAsset.riskLevel.toUpperCase()}
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Risk Score</p>
            <p
              className="text-3xl font-bold"
              style={{ color: getRiskColor(selectedAsset.riskLevel) }}
            >
              {selectedAsset.riskScore}%
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Predicted Failure</p>
            <p className="text-3xl font-bold text-gray-800">
              {selectedAsset.predictedFailure} days
            </p>
          </div>
          <div className="bg-gray-50 p-4 rounded-lg">
            <p className="text-sm text-gray-500">Last Maintenance</p>
            <p className="text-lg font-bold text-gray-800">
              {selectedAsset.lastMaintenance}
            </p>
          </div>
        </div>

        <div className="space-y-6">
          <div>
            <h3 className="font-bold text-lg mb-3 text-gray-800">
              24-Hour Sensor Trends
            </h3>

            <ResponsiveContainer width="100%" height={300}>
              <LineChart data={selectedAsset.historicalData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="time" />
                <YAxis />
                <Tooltip />
                <Legend />

                <Line
                  type="monotone"
                  dataKey="temperature"
                  stroke="#ef4444"
                  name="Temperature (°C)"
                />
                <Line
                  type="monotone"
                  dataKey="vibration"
                  stroke="#3b82f6"
                  name="Vibration (mm/s)"
                />
                <Line
                  type="monotone"
                  dataKey="pressure"
                  stroke="#10b981"
                  name="Pressure (PSI)"
                />
              </LineChart>
            </ResponsiveContainer>
          </div>

          <div className="bg-yellow-50 border-l-4 border-yellow-400 p-4">
            <h4 className="font-bold text-yellow-800 mb-2 flex items-center">
              <Zap className="w-5 h-5 mr-2" />
              AI Recommendations
            </h4>

            <ul className="space-y-1 text-yellow-800">
              {selectedAsset.riskLevel === "critical" && (
                <>
                  <li>• Schedule immediate maintenance inspection</li>
                  <li>
                    • Check vibration sensor readings - elevated levels detected
                  </li>
                  <li>• Review lubrication schedule</li>
                </>
              )}

              {selectedAsset.riskLevel === "warning" && (
                <>
                  <li>• Plan maintenance within the next 7 days</li>
                  <li>• Monitor temperature trends closely</li>
                  <li>• Verify pressure valve functionality</li>
                </>
              )}

              {selectedAsset.riskLevel === "healthy" && (
                <>
                  <li>• Asset operating within normal parameters</li>
                  <li>• Continue routine monitoring</li>
                  <li>
                    • Next scheduled maintenance in{" "}
                    {selectedAsset.predictedFailure} days
                  </li>
                </>
              )}
            </ul>
          </div>
        </div>
      </div>
    </div>
  );
};

export default DetailView;
