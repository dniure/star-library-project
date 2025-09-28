/**
 * AppContext.jsx
 * ----------------
 * Provides global state and actions for the app:
 * - User data
 * - Dashboard data
 * - App settings
 * - Loading and error states
 * 
 * Exports:
 * - AppProvider: Wraps the app and provides context
 * - useApp: Hook to access context
 * - withApp: HOC for class components
 */

import React, { createContext, useContext, useReducer, useEffect } from "react";
import { apiService } from "../services/api";

// ------------------------
// Context & Initial State
// ------------------------
const AppContext = createContext();

const initialState = {
    currentUser: null,
    dashboardData: null,
    loading: { dashboard: true, user: false },
    errors: { dashboard: null, user: null },
    settings: { theme: "light", readerId: 1, itemsPerPage: 12 },
};

// ------------------------
// Action Types
// ------------------------
const ACTION_TYPES = {
    SET_LOADING: "SET_LOADING",
    SET_ERROR: "SET_ERROR",
    SET_USER: "SET_USER",
    SET_DASHBOARD_DATA: "SET_DASHBOARD_DATA",
    UPDATE_SETTINGS: "UPDATE_SETTINGS",
    RESET_ERROR: "RESET_ERROR",
};

// ------------------------
// Reducer
// ------------------------
function appReducer(state, action) {
    switch (action.type) {
        case ACTION_TYPES.SET_LOADING:
            return { ...state, loading: { ...state.loading, ...action.payload } };
        case ACTION_TYPES.SET_ERROR:
            return { ...state, errors: { ...state.errors, ...action.payload }, loading: { dashboard: false, user: false } };
        case ACTION_TYPES.SET_USER:
            return { ...state, currentUser: action.payload, loading: { ...state.loading, user: false }, errors: { ...state.errors, user: null } };
        case ACTION_TYPES.SET_DASHBOARD_DATA:
            return { ...state, dashboardData: action.payload, loading: { ...state.loading, dashboard: false }, errors: { ...state.errors, dashboard: null } };
        case ACTION_TYPES.UPDATE_SETTINGS:
            return { ...state, settings: { ...state.settings, ...action.payload } };
        case ACTION_TYPES.RESET_ERROR:
            return { ...state, errors: { ...state.errors, [action.payload]: null } };
        default:
            throw new Error(`Unhandled action type: ${action.type}`);
    }
}

// ------------------------
// Action Creators
// ------------------------
const actions = {
    setLoading: (payload) => ({ type: ACTION_TYPES.SET_LOADING, payload }),
    setError: (payload) => ({ type: ACTION_TYPES.SET_ERROR, payload }),
    setUser: (payload) => ({ type: ACTION_TYPES.SET_USER, payload }),
    setDashboardData: (payload) => ({ type: ACTION_TYPES.SET_DASHBOARD_DATA, payload }),
    updateSettings: (payload) => ({ type: ACTION_TYPES.UPDATE_SETTINGS, payload }),
    resetError: (payload) => ({ type: ACTION_TYPES.RESET_ERROR, payload }),
};

// ------------------------
// useApp Hook
// ------------------------
export const useApp = () => {
    const context = useContext(AppContext);
    if (!context) throw new Error("useApp must be used within AppProvider");
    return context;
};

// ------------------------
// AppProvider Component
// ------------------------
export const AppProvider = ({ children }) => {
    const [state, dispatch] = useReducer(appReducer, initialState);

    // ------------------------
    // Dispatchable actions
    // ------------------------
    const dispatchActions = {
        fetchUser: async (readerId = state.settings.readerId) => {
            try {
                dispatch(actions.setLoading({ user: true }));
                const userData = {
                    id: readerId,
                    name: `Reader ${readerId}`,
                    email: `reader${readerId}@example.com`,
                    joinDate: new Date().toISOString(),
                    favoriteGenre: "Fantasy",
                };
                dispatch(actions.setUser(userData));
                return userData;
            } catch (err) {
                dispatch(actions.setError({ user: err.message }));
                throw err;
            }
        },
        fetchDashboardData: async (readerId = state.settings.readerId) => {
            try {
                dispatch(actions.setLoading({ dashboard: true }));
                const dashboardData = await apiService.fetchDashboardData(readerId);
                dispatch(actions.setDashboardData(dashboardData));
                return dashboardData;
            } catch (err) {
                dispatch(actions.setError({ dashboard: err.message || "Failed to fetch dashboard data" }));
                throw err;
            }
        },
        updateAppSettings: (settings) => dispatch(actions.updateSettings(settings)),
        changeReader: async (readerId) => {
            dispatch(actions.updateSettings({ readerId }));
            await dispatchActions.fetchUser(readerId);
            await dispatchActions.fetchDashboardData(readerId);
        },
        clearError: (key) => dispatch(actions.resetError(key)),
        retryFetch: () => {
            dispatchActions.clearError("dashboard");
            dispatchActions.fetchDashboardData();
        },
    };

    // ------------------------
    // Initial Data Load
    // ------------------------
    useEffect(() => {
        (async () => {
            try { await dispatchActions.fetchUser(); await dispatchActions.fetchDashboardData(); } 
            catch (err) { console.error("Failed to initialize app:", err); }
        })();
    }, []);

    // ------------------------
    // Refetch dashboard if reader changes
    // ------------------------
    useEffect(() => {
        if (state.currentUser && state.currentUser.id !== state.settings.readerId) {
            dispatchActions.fetchDashboardData(state.settings.readerId);
        }
    }, [state.settings.readerId]);

    // ------------------------
    // Context Value
    // ------------------------
    const contextValue = {
        ...state,
        ...dispatchActions,
        isDashboardLoading: state.loading.dashboard && !state.dashboardData,
        hasDashboardError: !!state.errors.dashboard,
        isUserLoading: state.loading.user && !state.currentUser,
        getBookById: (bookId) => state.dashboardData?.most_popular_books?.find(b => b.id === bookId) || null,
        getAuthorById: (authorId) => {
            if (!state.dashboardData) return null;
            if (state.dashboardData.most_popular_author?.id === authorId) return state.dashboardData.most_popular_author;
            return state.dashboardData.user_top_authors?.find(a => a.id === authorId) || null;
        },
        getUserReadingStats: () => ({
            booksRead: state.dashboardData?.books_read || [],
            topAuthors: state.dashboardData?.user_top_authors?.length || 0,
            favoriteGenre: state.currentUser?.favoriteGenre || "Unknown",
        }),
    };

    return <AppContext.Provider value={contextValue}>{children}</AppContext.Provider>;
};

// ------------------------
// HOC for class components
// ------------------------
export const withApp = (Component) => (props) => {
    const app = useApp();
    return <Component {...props} app={app} />;
};

export default AppContext;
