import { createContext, useContext, useReducer, useEffect, useCallback } from "react";
import { apiService } from "../services/api";

// Configuration
const CONFIG = {
  HARDCODED_READER_ID: 1,
  DEFAULT_ITEMS_PER_PAGE: 12,
  THEME: "light"
};

// Initial State
const initialState = {
  currentUser: null,
  dashboardData: null,
  loading: { dashboard: true, user: false },
  errors: { dashboard: null, user: null },
  settings: { theme: CONFIG.THEME, itemsPerPage: CONFIG.DEFAULT_ITEMS_PER_PAGE }
};

// Action Types
const ACTION_TYPES = {
  SET_LOADING: "SET_LOADING",
  SET_ERROR: "SET_ERROR", 
  SET_USER: "SET_USER",
  SET_DASHBOARD_DATA: "SET_DASHBOARD_DATA",
  UPDATE_SETTINGS: "UPDATE_SETTINGS",
  RESET_ERROR: "RESET_ERROR"
};

// Reducer
const stateUpdaters = {
  [ACTION_TYPES.SET_LOADING]: (state, payload) => ({ 
    ...state, 
    loading: {...state.loading, ...payload } 
  }),

  [ACTION_TYPES.SET_ERROR]: (state, payload) => ({ 
    ...state, 
    errors: { ...state.errors, ...payload }, 
    loading: { dashboard: false, user: false } 
  }),

  [ACTION_TYPES.SET_USER]: (state, payload) => ({ 
    ...state, 
    currentUser: payload, 
    loading: { ...state.loading, user: false }, 
    errors: { ...state.errors, user: null } 
  }),

  [ACTION_TYPES.SET_DASHBOARD_DATA]: (state, payload) => ({ 
    ...state, 
    dashboardData: payload, 
    loading: { ...state.loading, dashboard: false }, 
    errors: { ...state.errors, dashboard: null } 
  }),

  [ACTION_TYPES.UPDATE_SETTINGS]: (state, payload) => ({ 
    ...state, 
    settings: { ...state.settings, ...payload } 
  }),

  [ACTION_TYPES.RESET_ERROR]: (state, payload) => ({ 
    ...state, 
    errors: { ...state.errors, [payload]: null } 
  })
};

const appReducer = (state, action) => {
  const updater = stateUpdaters[action.type];
  if (!updater) throw new Error(`Unhandled action: ${action.type}`);
  return updater(state, action.payload);
};

// Actions
const createAction = (type, payload) => ({ type, payload });
const actions = {
  setLoading: (payload) => createAction(ACTION_TYPES.SET_LOADING, payload),
  setError: (payload) => createAction(ACTION_TYPES.SET_ERROR, payload),
  setUser: (payload) => createAction(ACTION_TYPES.SET_USER, payload),
  setDashboardData: (payload) => createAction(ACTION_TYPES.SET_DASHBOARD_DATA, payload),
  updateSettings: (payload) => createAction(ACTION_TYPES.UPDATE_SETTINGS, payload),
  resetError: (payload) => createAction(ACTION_TYPES.RESET_ERROR, payload)
};

// Context
const AppContext = createContext();

// Hook
export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) throw new Error("useApp must be used within AppProvider");
  return context;
};

// Provider
export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Data fetching
  const fetchUser = useCallback(async () => {
    try {
      dispatch(actions.setLoading({ user: true }));
      const dashboardData = await apiService.fetchDashboardData();
      
      if (dashboardData?.reader_id) {
        const userData = {
          id: dashboardData.reader_id,
          name: dashboardData.reader_name,
          favoriteGenre: "Mystery"
        };
        dispatch(actions.setUser(userData));
        return userData;
      }
      throw new Error("Invalid user data from backend");
    } catch (error) {
      dispatch(actions.setError({ user: error.message || "Failed to load user" }));
      throw error;
    }
  }, []);

  const fetchDashboardData = useCallback(async () => {
    try {
      dispatch(actions.resetError("dashboard"));
      dispatch(actions.setLoading({ dashboard: true }));
      
      const dashboardData = await apiService.fetchDashboardData();
      
      // Auto-set user from dashboard if not set
      if (dashboardData?.reader_id && !state.currentUser) {
        dispatch(actions.setUser({
          id: dashboardData.reader_id,
          name: dashboardData.reader_name,
          joinDate: new Date().toISOString(),
          favoriteGenre: "Mystery"
        }));
      }
      
      dispatch(actions.setDashboardData(dashboardData));
      return dashboardData;
    } catch (error) {
      dispatch(actions.setError({ dashboard: error.message || "Failed to fetch dashboard" }));
      throw error;
    }
  }, [state.currentUser]);

  // Actions
  const updateAppSettings = useCallback((settings) => 
    dispatch(actions.updateSettings(settings)), []);

  const clearError = useCallback((errorKey) => 
    dispatch(actions.resetError(errorKey)), []);

  const retryFetch = useCallback(() => {
    clearError("dashboard");
    fetchDashboardData();
  }, [clearError, fetchDashboardData]);

  // Helpers
  const getBookById = useCallback((bookId) => 
    state.dashboardData?.most_popular_books?.find(book => book.id === bookId) || null, 
    [state.dashboardData]);

  const getAuthorById = useCallback((authorId) => {
    if (!state.dashboardData) return null;
    const { most_popular_author, user_top_authors } = state.dashboardData;
    return most_popular_author?.id === authorId ? most_popular_author 
           : user_top_authors?.find(author => author.id === authorId) || null;
  }, [state.dashboardData]);

  const getUserReadingStats = useCallback(() => ({
    booksRead: state.dashboardData?.user_books_read || [],
    topAuthors: state.dashboardData?.user_top_authors?.length || 0,
    favoriteGenre: state.currentUser?.favoriteGenre || "Unknown",
    totalPages: state.dashboardData?.user_books_read?.reduce((total, book) => total + (book.pages || 0), 0) || 0
  }), [state.dashboardData, state.currentUser]);

  // Initialize app
  useEffect(() => {
    fetchDashboardData();
  }, [fetchDashboardData]);

  // Context value
  const contextValue = {
    // State
    ...state,
    currentReaderId: CONFIG.HARDCODED_READER_ID,
    
    // Computed
    isDashboardLoading: state.loading.dashboard && !state.dashboardData,
    hasDashboardError: !!state.errors.dashboard,
    isUserLoading: state.loading.user && !state.currentUser,
    isAuthenticated: !!state.currentUser,
    
    // Actions
    fetchUser,
    fetchDashboardData,
    updateAppSettings,
    clearError,
    retryFetch,
    
    // Helpers
    getBookById,
    getAuthorById,
    getUserReadingStats
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

// HOC (deprecated)
export const withApp = (Component) => (props) => {
  const app = useApp();
  return <Component {...props} app={app} />;
};

export default AppContext;