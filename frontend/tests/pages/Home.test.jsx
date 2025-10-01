import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import Home from '../src/pages/Home';
import { useDashboard } from '../src/hooks/useDashboard';
import { mockDashboardData, mockBook } from '../setup';

jest.mock('../../src/hooks/useDashboard', () => ({
  useDashboard: jest.fn()
}));

describe('Home', () => {
  const mockUseDashboard = useDashboard;

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders loading state', () => {
    mockUseDashboard.mockReturnValue({
      dashboardData: null,
      loading: true,
      error: null,
      refresh: jest.fn()
    });

    render(<Home />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders error state', () => {
    mockUseDashboard.mockReturnValue({
      dashboardData: null,
      loading: false,
      error: 'Failed to load',
      refresh: jest.fn()
    });

    render(<Home />);

    expect(screen.getByText('Error loading dashboard: Failed to load')).toBeInTheDocument();
  });

  test('renders complete home page with data', () => {
    mockUseDashboard.mockReturnValue({
      dashboardData: mockDashboardData,
      loading: false,
      error: null,
      refresh: jest.fn()
    });

    render(<Home />);

    expect(screen.getByText('Reading Dashboard')).toBeInTheDocument();
    expect(screen.getByText('Track your journey through worlds of words.')).toBeInTheDocument();
    expect(screen.getByText('Most Popular Books')).toBeInTheDocument();
    expect(screen.getByText('Test Book')).toBeInTheDocument();
    expect(screen.getByText('Welcome, John Doe! 👋')).toBeInTheDocument();
  });
});