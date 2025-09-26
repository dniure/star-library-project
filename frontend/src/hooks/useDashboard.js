// frontend/src/hooks/useDashboard.js
import { useState, useEffect } from 'react';
import { apiService } from '../services/api';

export const useDashboard = (readerId = 1) => {
    const [dashboardData, setDashboardData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);

    useEffect(() => {
        const fetchData = async () => {
            try {
                setLoading(true);
                setError(null);
                const data = await apiService.fetchDashboardData(readerId);
                setDashboardData(data);
            } catch (err) {
                setError(err.message);
                console.error('Error fetching dashboard:', err);
            } finally {
                setLoading(false);
            }
        };

        fetchData();
    }, [readerId]);

    return { dashboardData, loading, error };
};