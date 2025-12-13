import { Activity, Clock, TrendingDown } from "lucide-react";
import {
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
  AreaChart,
  Area,
  BarChart,
  Bar,
} from "recharts";

const StatisticsView = ({ assets, setView, riskDistribution }) => {
  const avgTemp =
    assets.reduce((a, b) => a + b.temperature, 0) / assets.length || 0;
  const avgVibration =
    assets.reduce((a, b) => a + b.vibration, 0) / assets.length || 0;
  const avgPressure =
    assets.reduce((a, b) => a + b.pressure, 0) / assets.length || 0;
  const avgRuntime =
    assets.reduce((a, b) => a + b.runtime, 0) / assets.length || 0;
  const avgRisk =
    assets.reduce((a, b) => a + b.riskScore, 0) / assets.length || 0;

  const riskTrendData = assets.map((asset, idx) => ({
    name: asset.name,
    risk: asset.riskScore,
    index: idx + 1,
  }));

  const sensorDistribution = [
    {
      sensor: "Temperature",
      min: Math.min(...assets.map((a) => a.temperature)),
      max: Math.max(...assets.map((a) => a.temperature)),
      avg: avgTemp,
    },
    {
      sensor: "Vibration",
      min: Math.min(...assets.map((a) => a.vibration)),
      max: Math.max(...assets.map((a) => a.vibration)),
      avg: avgVibration,
    },
    {
      sensor: "Pressure",
      min: Math.min(...assets.map((a) => a.pressure)),
      max: Math.max(...assets.map((a) => a.pressure)),
      avg: avgPressure,
    },
  ];

  const failureTimeline = assets
    .map((a) => ({
      name: a.name,
      days: a.predictedFailure,
    }))
    .sort((a, b) => a.days - b.days)
    .slice(0, 10);

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h2 className="text-2xl font-bold text-gray-800">
          Fleet Statistics & Analytics
        </h2>
        <button
          onClick={() => setView("overview")}
          className="text-gray-600 hover:text-gray-800 font-semibold cursor-pointer"
        >
          ← Back to Overview
        </button>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-5 gap-4">
        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between mb-2">
            <TrendingDown className="w-6 h-6 text-blue-500" />
          </div>
          <p className="text-gray-500 text-sm">Avg Risk Score</p>
          <p className="text-2xl font-bold text-gray-800">
            {avgRisk.toFixed(1)}%
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-6 h-6 text-red-500" />
          </div>
          <p className="text-gray-500 text-sm">Avg Temperature</p>
          <p className="text-2xl font-bold text-gray-800">
            {avgTemp.toFixed(1)}°C
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-6 h-6 text-purple-500" />
          </div>
          <p className="text-gray-500 text-sm">Avg Vibration</p>
          <p className="text-2xl font-bold text-gray-800">
            {avgVibration.toFixed(2)} mm/s
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between mb-2">
            <Activity className="w-6 h-6 text-green-500" />
          </div>
          <p className="text-gray-500 text-sm">Avg Pressure</p>
          <p className="text-2xl font-bold text-gray-800">
            {avgPressure.toFixed(1)} PSI
          </p>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <div className="flex items-center justify-between mb-2">
            <Clock className="w-6 h-6 text-orange-500" />
          </div>
          <p className="text-gray-500 text-sm">Avg Runtime</p>
          <p className="text-2xl font-bold text-gray-800">
            {avgRuntime.toFixed(0)}h
          </p>
        </div>
      </div>

      {/* Charts Row 1 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg mb-4 text-gray-800">
            Risk Score Distribution
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={riskTrendData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="index"
                label={{
                  value: "Asset Index",
                  position: "insideBottom",
                  offset: -5,
                }}
              />
              <YAxis
                label={{
                  value: "Risk Score (%)",
                  angle: -90,
                  position: "insideLeft",
                }}
              />
              <Tooltip />
              <Area
                type="monotone"
                dataKey="risk"
                stroke="#000000"
                fill="#808080"
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg mb-4 text-gray-800">
            Sensor Ranges (Min/Avg/Max)
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={sensorDistribution}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="sensor" />
              <YAxis />
              <Tooltip />
              <Legend />
              <Bar dataKey="min" fill="#000000" name="Min" />
              <Bar dataKey="avg" fill="#000000" name="Average" />
              <Bar dataKey="max" fill="#000000" name="Max" />
            </BarChart>
          </ResponsiveContainer>
        </div>
      </div>

      {/* Charts Row 2 */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg mb-4 text-gray-800">
            Next 10 Predicted Failures
          </h3>
          <ResponsiveContainer width="100%" height={300}>
            <BarChart data={failureTimeline} layout="vertical">
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                type="number"
                label={{
                  value: "Days Until Failure",
                  position: "insideBottom",
                  offset: -5,
                }}
              />
              <YAxis type="category" dataKey="name" width={100} />
              <Tooltip />
              <Bar dataKey="days" fill="#ef4444" />
            </BarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white rounded-lg shadow p-4">
          <h3 className="font-bold text-lg mb-4 text-gray-800">
            Fleet Health Overview
          </h3>
          <div className="space-y-4">
            <div className="bg-green-50 p-4 rounded-lg border-l-4 border-green-500">
              <h4 className="font-bold text-green-800 mb-2">Healthy Assets</h4>
              <p className="text-3xl font-bold text-green-600">
                {riskDistribution[0].value}
              </p>
              <p className="text-sm text-green-700 mt-2">
                Operating within normal parameters
              </p>
            </div>

            <div className="bg-yellow-50 p-4 rounded-lg border-l-4 border-yellow-500">
              <h4 className="font-bold text-yellow-800 mb-2">Warning Assets</h4>
              <p className="text-3xl font-bold text-yellow-600">
                {riskDistribution[1].value}
              </p>
              <p className="text-sm text-yellow-700 mt-2">
                Require monitoring & preventive action
              </p>
            </div>

            <div className="bg-red-50 p-4 rounded-lg border-l-4 border-red-500">
              <h4 className="font-bold text-red-800 mb-2">Critical Assets</h4>
              <p className="text-3xl font-bold text-red-600">
                {riskDistribution[2].value}
              </p>
              <p className="text-sm text-red-700 mt-2">
                Immediate maintenance required
              </p>
            </div>
          </div>
        </div>
      </div>

      {/* Insights Panel */}
      <div className="bg-yellow-50 border-l-4 border-yellow-400 p-6 rounded-lg">
        <h3 className="font-bold text-lg text-black mb-4">Key Insights</h3>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-black">
          <div>
            <p className="font-semibold mb-2">• Fleet Performance:</p>
            <p className="text-sm ml-4">
              {riskDistribution[0].value > assets.length * 0.6
                ? "Excellent - majority of assets healthy"
                : riskDistribution[2].value > assets.length * 0.2
                ? "Concerning - high number of critical assets"
                : "Moderate - focus on preventive maintenance"}
            </p>
          </div>
          <div>
            <p className="font-semibold mb-2">• Temperature Trends:</p>
            <p className="text-sm ml-4">
              {avgTemp > 85
                ? "Elevated - check cooling systems"
                : "Normal operating range"}
            </p>
          </div>
          <div>
            <p className="font-semibold mb-2">• Vibration Analysis:</p>
            <p className="text-sm ml-4">
              {avgVibration > 1.8
                ? "High - inspect bearings and alignment"
                : "Within acceptable limits"}
            </p>
          </div>
          <div>
            <p className="font-semibold mb-2">• Maintenance Priority:</p>
            <p className="text-sm ml-4">
              {failureTimeline[0]?.days < 7
                ? `URGENT: ${failureTimeline[0]?.name} needs immediate attention`
                : "Schedule routine maintenance as planned"}
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default StatisticsView;
