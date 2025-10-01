import React from 'react';
import { render, screen } from '@testing-library/react';
import Dashboard from '../src/components/Dashboard';
import { mockDashboardData } from '../setup';

describe('Dashboard', () => {
  test('renders dashboard with all stat cards', () => {
    render(<Dashboard data={mockDashboardData} />);
    
    expect(screen.getByText('Most Popular Author')).toBeInTheDocument();
    expect(screen.getByText('Your Reading Stats')).toBeInTheDocument();
    expect(screen.getByText('Your Top 3 Authors')).toBeInTheDocument();
  });

  test('displays most popular author information', () => {
    render(<Dashboard data={mockDashboardData} />);
    
    expect(screen.getByText('Popular Author')).toBeInTheDocument();
    expect(screen.getByText('Best selling author')).toBeInTheDocument();
    expect(screen.getByText('👥 5,000')).toBeInTheDocument();
    expect(screen.getByText('📚 10')).toBeInTheDocument();
  });

  test('handles missing most popular author', () => {
    const dataWithoutAuthor = { ...mockDashboardData, most_popular_author: null };
    render(<Dashboard data={dataWithoutAuthor} />);
    
    expect(screen.getByText('No data available')).toBeInTheDocument();
  });

  test('displays user reading stats', () => {
    render(<Dashboard data={mockDashboardData} />);
    
    expect(screen.getByText('Books Read:')).toBeInTheDocument();
    expect(screen.getByText('1')).toBeInTheDocument();
  });

  test('returns null when no data provided', () => {
    const { container } = render(<Dashboard data={null} />);
    
    expect(container.firstChild).toBeNull();
  });
});