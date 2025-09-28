// frontend/src/context/AppContext.jsx
import React, { createContext, useContext, useReducer, useEffect } from 'react';
import { apiService } from '../services/api';

// Create Context
const AppContext = createContext();

// Initial State
const initialState = {
  // User data
  currentUser: null,
  
  // Dashboard data
  dashboardData: null,
  
  // UI state
  loading: {
    dashboard: true,
    user: false,
  },
  
  // Error handling
  errors: {
    dashboard: null,
    user: null,
  },
  
  // App settings
  settings: {
    theme: 'light',
    readerId: 1, // Default to first reader as per requirements
    itemsPerPage: 12,
  },
};

// Action Types
const ACTION_TYPES = {
  SET_LOADING: 'SET_LOADING',
  SET_ERROR: 'SET_ERROR',
  SET_USER: 'SET_USER',
  SET_DASHBOARD_DATA: 'SET_DASHBOARD_DATA',
  UPDATE_SETTINGS: 'UPDATE_SETTINGS',
  RESET_ERROR: 'RESET_ERROR',
};

// Reducer Function
function appReducer(state, action) {
  switch (action.type) {
    case ACTION_TYPES.SET_LOADING:
      return {
        ...state,
        loading: {
          ...state.loading,
          ...action.payload,
        },
      };

    case ACTION_TYPES.SET_ERROR:
      return {
        ...state,
        errors: {
          ...state.errors,
          ...action.payload,
        },
        loading: {
          dashboard: false,
          user: false,
        },
      };

    case ACTION_TYPES.SET_USER:
      return {
        ...state,
        currentUser: action.payload,
        loading: {
          ...state.loading,
          user: false,
        },
        errors: {
          ...state.errors,
          user: null,
        },
      };

    case ACTION_TYPES.SET_DASHBOARD_DATA:
      return {
        ...state,
        dashboardData: action.payload,
        loading: {
          ...state.loading,
          dashboard: false,
        },
        errors: {
          ...state.errors,
          dashboard: null,
        },
      };

    case ACTION_TYPES.UPDATE_SETTINGS:
      return {
        ...state,
        settings: {
          ...state.settings,
          ...action.payload,
        },
      };

    case ACTION_TYPES.RESET_ERROR:
      return {
        ...state,
        errors: {
          ...state.errors,
          [action.payload]: null,
        },
      };

    default:
      throw new Error(`Unhandled action type: ${action.type}`);
  }
}

// Action Creators
const actions = {
  setLoading: (loadingState) => ({
    type: ACTION_TYPES.SET_LOADING,
    payload: loadingState,
  }),

  setError: (errorState) => ({
    type: ACTION_TYPES.SET_ERROR,
    payload: errorState,
  }),

  setUser: (userData) => ({
    type: ACTION_TYPES.SET_USER,
    payload: userData,
  }),

  setDashboardData: (dashboardData) => ({
    type: ACTION_TYPES.SET_DASHBOARD_DATA,
    payload: dashboardData,
  }),

  updateSettings: (newSettings) => ({
    type: ACTION_TYPES.UPDATE_SETTINGS,
    payload: newSettings,
  }),

  resetError: (errorKey) => ({
    type: ACTION_TYPES.RESET_ERROR,
    payload: errorKey,
  }),
};

// Custom Hook for using context
export const useApp = () => {
  const context = useContext(AppContext);
  if (!context) {
    throw new Error('useApp must be used within an AppProvider');
  }
  return context;
};

// Provider Component
export const AppProvider = ({ children }) => {
  const [state, dispatch] = useReducer(appReducer, initialState);

  // Action dispatchers
  const dispatchActions = {
    // User actions
    fetchUser: async (readerId = state.settings.readerId) => {
      try {
        dispatch(actions.setLoading({ user: true }));
        
        // In a real app, this would fetch from /users/{id}
        // For now, we'll simulate user data based on readerId
        const userData = {
          id: readerId,
          name: `Reader ${readerId}`,
          email: `reader${readerId}@example.com`,
          joinDate: new Date().toISOString(),
          favoriteGenre: 'Fantasy',
        };
        
        dispatch(actions.setUser(userData));
        return userData;
      } catch (error) {
        dispatch(actions.setError({ user: error.message }));
        throw error;
      }
    },

    // Dashboard actions
    fetchDashboardData: async (readerId = state.settings.readerId) => {
      try {
        dispatch(actions.setLoading({ dashboard: true }));
        
        const dashboardData = await apiService.fetchDashboardData(readerId);
        
        dispatch(actions.setDashboardData(dashboardData));
        return dashboardData;
      } catch (error) {
        const errorMessage = error.message || 'Failed to fetch dashboard data';
        dispatch(actions.setError({ dashboard: errorMessage }));
        throw error;
      }
    },

    // Settings actions
    updateAppSettings: (newSettings) => {
      dispatch(actions.updateSettings(newSettings));
    },

    changeReader: async (newReaderId) => {
      try {
        // Update settings first
        dispatch(actions.updateSettings({ readerId: newReaderId }));
        
        // Then refetch data for the new reader
        await dispatchActions.fetchUser(newReaderId);
        await dispatchActions.fetchDashboardData(newReaderId);
      } catch (error) {
        dispatch(actions.setError({ 
          user: `Failed to switch to reader ${newReaderId}: ${error.message}` 
        }));
        throw error;
      }
    },

    // Error handling
    clearError: (errorKey) => {
      dispatch(actions.resetError(errorKey));
    },

    retryFetch: () => {
      dispatchActions.clearError('dashboard');
      dispatchActions.fetchDashboardData();
    },
  };

  // Effects for initial data loading
  useEffect(() => {
    // Fetch initial data when component mounts
    const initializeApp = async () => {
      try {
        await dispatchActions.fetchUser();
        await dispatchActions.fetchDashboardData();
      } catch (error) {
        console.error('Failed to initialize app:', error);
      }
    };

    initializeApp();
  }, []); // Empty dependency array - runs only on mount

  // Effect to refetch dashboard data when reader changes
  useEffect(() => {
    if (state.currentUser && state.currentUser.id !== state.settings.readerId) {
      dispatchActions.fetchDashboardData(state.settings.readerId);
    }
  }, [state.settings.readerId]);

  // Context value
  const contextValue = {
    // State
    ...state,
    
    // Actions
    ...dispatchActions,
    
    // Derived state
    isDashboardLoading: state.loading.dashboard && !state.dashboardData,
    hasDashboardError: !!state.errors.dashboard,
    isUserLoading: state.loading.user && !state.currentUser,
    
    // Helper functions
    getBookById: (bookId) => {
      if (!state.dashboardData?.most_popular_books) return null;
      return state.dashboardData.most_popular_books.find(book => book.id === bookId);
    },
    
    getAuthorById: (authorId) => {
      if (!state.dashboardData) return null;
      
      // Check most popular author
      if (state.dashboardData.most_popular_author?.id === authorId) {
        return state.dashboardData.most_popular_author;
      }
      
      // Check user's top authors
      const topAuthor = state.dashboardData.user_top_authors?.find(author => author.id === authorId);
      if (topAuthor) return topAuthor;
      
      return null;
    },
    
    // Statistics helpers
    getUserReadingStats: () => {
      if (!state.dashboardData) return null;
      
      return {
        booksRead: state.dashboardData.books_read,
        topAuthors: state.dashboardData.user_top_authors?.length || 0,
        favoriteGenre: state.currentUser?.favoriteGenre || 'Unknown',
      };
    },
  };

  return (
    <AppContext.Provider value={contextValue}>
      {children}
    </AppContext.Provider>
  );
};

// Higher Order Component for class components (optional)
export const withApp = (Component) => {
  return function WrappedComponent(props) {
    const app = useApp();
    return <Component {...props} app={app} />;
  };
};

export default AppContext;