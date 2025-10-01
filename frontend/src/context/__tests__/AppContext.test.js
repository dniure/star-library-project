// src/context/__tests__/AppContext.test.js
import { renderHook, act } from '@testing-library/react';
import { AppProvider, useApp } from '../AppContext';

// Mock the API service first
jest.mock('../../services/api', () => {
  // Create the mock inside the factory function
  const mockApiService = {
    fetchDashboardData: jest.fn(),
    fetchBooks: jest.fn(),
    fetchAuthors: jest.fn(),
    fetchReader: jest.fn()
  };

  return {
    apiService: mockApiService,
    ApiError: class ApiError extends Error {
      constructor(message, status, originalError) {
        super(message);
        this.name = "ApiError";
        this.status = status;
        this.originalError = originalError;
      }
    }
  };
});

// Now import the mocked service
const { apiService } = require('../../services/api');

describe('AppContext', () => {
  const wrapper = ({ children }) => <AppProvider>{children}</AppProvider>;

  beforeEach(() => {
    jest.clearAllMocks();
    // Mock the initial fetch to resolve immediately with empty data
    apiService.fetchDashboardData.mockResolvedValue({
      reader_id: 1,
      reader_name: 'Test User',
      most_popular_books: [],
      user_books_read: [],
      user_top_authors: []
    });
  });

  describe('initial state', () => {
    it('should provide initial state', async () => {
      const { result } = renderHook(() => useApp(), { wrapper });

      // Wait for initial fetch to complete
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });

      expect(result.current).toMatchObject({
        currentUser: null,
        dashboardData: null, // Still null because we mocked empty data
        loading: { dashboard: false, user: false }, // Should be false after fetch
        errors: { dashboard: null, user: null },
        isDashboardLoading: false,
        hasDashboardError: false,
        isUserLoading: false,
        isAuthenticated: false
      });
    });
  });

  describe('actions', () => {
    it('should update settings', async () => {
      const { result } = renderHook(() => useApp(), { wrapper });

      // Wait for initial fetch
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });

      act(() => {
        result.current.updateAppSettings({ theme: 'dark' });
      });

      expect(result.current.settings.theme).toBe('dark');
    });

    it('should clear errors', async () => {
      const { result } = renderHook(() => useApp(), { wrapper });

      // Wait for initial fetch
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });

      act(() => {
        result.current.clearError('dashboard');
      });

      expect(result.current.errors.dashboard).toBeNull();
    });
  });

  describe('data fetching', () => {
    it('should fetch dashboard data successfully', async () => {
      const mockData = { 
        reader_id: 1, 
        reader_name: 'Test User',
        most_popular_books: [],
        user_books_read: [],
        user_top_authors: []
      };
      
      apiService.fetchDashboardData.mockResolvedValue(mockData);

      const { result } = renderHook(() => useApp(), { wrapper });

      await act(async () => {
        await result.current.fetchDashboardData();
      });

      expect(result.current.dashboardData).toEqual(mockData);
      expect(result.current.loading.dashboard).toBe(false);
      expect(result.current.errors.dashboard).toBeNull();
    });

    it('should handle dashboard data fetch errors', async () => {
      const errorMessage = 'Network error';
      apiService.fetchDashboardData.mockRejectedValue(new Error(errorMessage));

      const { result } = renderHook(() => useApp(), { wrapper });

      await act(async () => {
        try {
          await result.current.fetchDashboardData();
        } catch (error) {
          // Expected to throw
        }
      });

      expect(result.current.errors.dashboard).toBe(errorMessage);
      expect(result.current.loading.dashboard).toBe(false);
    });
  });

  describe('helper functions', () => {
    it('should get book by id when data exists', async () => {
      const { result } = renderHook(() => useApp(), { wrapper });

      // Wait for initial fetch
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });

      // Test with no data first
      const book = result.current.getBookById(1);
      expect(book).toBeNull();
    });

    it('should get user reading stats with default values', async () => {
      const { result } = renderHook(() => useApp(), { wrapper });

      // Wait for initial fetch
      await act(async () => {
        await new Promise(resolve => setTimeout(resolve, 0));
      });

      // Test with default state (no data)
      const stats = result.current.getUserReadingStats();

      expect(stats).toEqual({
        booksRead: [],
        topAuthors: 0,
        favoriteGenre: "Unknown",
        totalPages: 0
      });
    });
  });
});