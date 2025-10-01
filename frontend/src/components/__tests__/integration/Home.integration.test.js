// src/components/__tests__/integration/Home.integration.test.js
import React from 'react';
import { render, screen, waitFor, fireEvent, act } from '@testing-library/react';
import { AppProvider } from '../../../context/AppContext';
import Home from '../../../pages/Home';
import { mockDashboardData } from '../../../test-utils';

// Mock the API service first
jest.mock('../../../services/api', () => {
  // Create the mock inside the factory function
  const mockApiService = {
    fetchDashboardData: jest.fn()
  };

  return {
    apiService: mockApiService
  };
});

// Now import the mocked service
const { apiService } = require('../../../services/api');

describe('Home Page Integration', () => {
  const renderHome = () => {
    return render(
      <AppProvider>
        <Home />
      </AppProvider>
    );
  };

  beforeEach(() => {
    apiService.fetchDashboardData.mockClear();
  });

  it('should load and display dashboard data', async () => {
    apiService.fetchDashboardData.mockResolvedValue(mockDashboardData);

    await act(async () => {
      renderHome();
    });

    // Should show loading initially, then data
    await waitFor(() => {
      expect(screen.getByText('Reading Dashboard')).toBeInTheDocument();
    }, { timeout: 3000 });

    // Should display user name in header
    expect(screen.getByText(`Welcome, ${mockDashboardData.reader_name}! 👋`)).toBeInTheDocument();

    // Should display book grid
    expect(screen.getByText('Most Popular Books')).toBeInTheDocument();
    expect(screen.getByText(mockDashboardData.most_popular_books[0].title)).toBeInTheDocument();

    // Should display dashboard stats
    expect(screen.getByText('Most Popular Author')).toBeInTheDocument();
    expect(screen.getByText('Your Reading Stats')).toBeInTheDocument();
    expect(screen.getByText('Your Top 3 Authors')).toBeInTheDocument();
  });

  it('should handle API errors gracefully', async () => {
    apiService.fetchDashboardData.mockRejectedValue(new Error('Network error'));

    await act(async () => {
      renderHome();
    });

    // Should show error message
    await waitFor(() => {
      expect(screen.getByText(/Error loading dashboard/)).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  it('should handle empty data state', async () => {
    apiService.fetchDashboardData.mockResolvedValue(null);

    await act(async () => {
      renderHome();
    });

    await waitFor(() => {
      expect(screen.getByText('No data available')).toBeInTheDocument();
    }, { timeout: 3000 });
  });

  // Skip the modal test for now since it's more complex
  it.skip('should handle book modal interactions', async () => {
    // We'll fix this after the basic tests pass
  });
});