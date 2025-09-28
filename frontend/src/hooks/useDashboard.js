/**
 * useDashboard.ts
 * ----------------
 * Hook to access dashboard data from AppContext.
 * Provides:
 * - dashboardData
 * - loading
 * - error
 * - refresh function
 */

import { useApp } from "../context/AppContext";

export const useDashboard = () => {
  const {
    dashboardData,
    isDashboardLoading: loading,
    hasDashboardError: error,
    retryFetch: refresh,
  } = useApp();

  return { dashboardData, loading, error, refresh };
};
