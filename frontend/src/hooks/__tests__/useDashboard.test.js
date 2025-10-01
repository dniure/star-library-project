// frontend/src/hooks/__tests__/useDashboard.test.js
import { renderHook, waitFor } from '@testing-library/react';
import { useDashboard } from '../useDashboard';
import { useApp } from '../../context/AppContext';

// Mock the AppContext
jest.mock('../../context/AppContext');

describe('useDashboard', () => {
  const mockAppContext = {
    dashboardData: { reader_id: 1, books: [] },
    isDashboardLoading: false,
    hasDashboardError: false,
    retryFetch: jest.fn()
  };

  beforeEach(() => {
    useApp.mockReturnValue(mockAppContext);
  });

  it('should return dashboard data from context', () => {
    const { result } = renderHook(() => useDashboard());

    expect(result.current).toEqual({
      dashboardData: mockAppContext.dashboardData,
      loading: mockAppContext.isDashboardLoading,
      error: mockAppContext.hasDashboardError,
      refresh: mockAppContext.retryFetch
    });
  });

  it('should handle loading state', () => {
    useApp.mockReturnValue({
      ...mockAppContext,
      isDashboardLoading: true
    });

    const { result } = renderHook(() => useDashboard());

    expect(result.current.loading).toBe(true);
  });

  it('should handle error state', () => {
    useApp.mockReturnValue({
      ...mockAppContext,
      hasDashboardError: true
    });

    const { result } = renderHook(() => useDashboard());

    expect(result.current.error).toBe(true);
  });

  it('should provide refresh function', () => {
    const { result } = renderHook(() => useDashboard());

    result.current.refresh();
    expect(mockAppContext.retryFetch).toHaveBeenCalled();
  });
});