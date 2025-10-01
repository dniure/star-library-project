import React from 'react';
import { render, screen } from '@testing-library/react';
import { Header, StatCard, LoadingSpinner } from '../src/components/UIComponents';

describe('Header', () => {
  test('renders header with library name and user', () => {
    render(<Header userName="John Doe" />);
    
    expect(screen.getByText('STAR Library')).toBeInTheDocument();
    expect(screen.getByText('Welcome, John Doe! 👋')).toBeInTheDocument();
  });
});

describe('StatCard', () => {
  test('renders stat card with title and children', () => {
    render(
      <StatCard title="Test Stat" icon="📊">
        <div>Test Content</div>
      </StatCard>
    );
    
    expect(screen.getByText('Test Stat')).toBeInTheDocument();
    expect(screen.getByText('📊')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });
});

describe('LoadingSpinner', () => {
  test('renders with default message', () => {
    render(<LoadingSpinner />);
    
    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  test('renders with custom message', () => {
    render(<LoadingSpinner message="Fetching data..." />);
    
    expect(screen.getByText('Fetching data...')).toBeInTheDocument();
  });
});