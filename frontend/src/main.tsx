import { StrictMode } from "react";
import { createRoot } from "react-dom/client";
import "./index.css";
import MaintenanceDashboard from "./MaintenanceDashboard.tsx";

createRoot(document.getElementById("root")!).render(
  <StrictMode>
    <MaintenanceDashboard />
  </StrictMode>
);
