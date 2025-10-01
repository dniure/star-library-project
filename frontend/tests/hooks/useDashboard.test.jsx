import { renderHook, waitFor } from '@testing-library/react';
import { AppProvider } from '../src/context/AppContext';
import { useDashboard } from '../src/hooks/useDashboard';
import { apiService } from '../src/services/api';
import { mockDashboardData } from '../setup';

const wrapper = ({ children }) => <AppProvider>{children}</AppProvider>;

jest.mock('../../src/services/api', () => ({
  apiService: {
    fetchDashboardData: jest.fn(),
    fetchBooks: jest.fn(),
    fetchAuthors: jest.fn(),
    fetchReader: jest.fn(),
  },
  ApiError: class ApiError extends Error {
    constructor(message, status, originalError) {
      super(message);
      this.name = "ApiError";
      this.status = status;
      this.originalError = originalError;
    }
  }
}));

describe('useDashboard', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('returns dashboard data and state', async () => {
    apiService.fetchDashboardData.mockResolvedValue(mockDashboardData);

    const { result } = renderHook(() => useDashboard(), { wrapper });

    await waitFor(() => {
      expect(result.current.loading).toBe(false);
    });

    expect(result.current.dashboardData).toEqual(mockDashboardData);
    expect(result.current.error).toBe(false);
  });
});