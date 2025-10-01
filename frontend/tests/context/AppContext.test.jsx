import React from 'react';
import { render, screen, act, waitFor } from '@testing-library/react';
import { AppProvider, useApp } from '../src/context/AppContext';
import { apiService } from '../src/services/api';

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

// Test component to use the context
const TestComponent = () => {
  const app = useApp();
  return (
    <div>
      <span data-testid="loading">{app.isDashboardLoading.toString()}</span>
      <span data-testid="error">{app.hasDashboardError.toString()}</span>
    </div>
  );
};

describe('AppContext', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('provides initial state', () => {
    render(
      <AppProvider>
        <TestComponent />
      </AppProvider>
    );

    expect(screen.getByTestId('loading')).toHaveTextContent('true');
    expect(screen.getByTestId('error')).toHaveTextContent('false');
  });

  test('fetches dashboard data on mount', async () => {
    apiService.fetchDashboardData.mockResolvedValue({ reader_id: 1, reader_name: 'Test User' });

    await act(async () => {
      render(
        <AppProvider>
          <TestComponent />
        </AppProvider>
      );
    });

    await waitFor(() => {
      expect(apiService.fetchDashboardData).toHaveBeenCalledTimes(1);
    });
  });

  test('throws error when useApp used outside provider', () => {
    const consoleError = jest.spyOn(console, 'error').mockImplementation(() => {});
    
    expect(() => {
      render(<TestComponent />);
    }).toThrow('useApp must be used within AppProvider');
    
    consoleError.mockRestore();
  });
});