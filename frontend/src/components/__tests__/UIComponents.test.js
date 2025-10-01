// src/components/__tests__/UIComponents.test.js
import React from 'react';
import { render, screen, act } from '@testing-library/react';
import { Header, StatCard, LoadingSpinner, StatNumber } from '../UIComponents';

describe('Header', () => {
  it('should render with user name', () => {
    render(<Header userName="John Doe" />);

    expect(screen.getByText('STAR Library')).toBeInTheDocument();
    expect(screen.getByText('Welcome, John Doe! 👋')).toBeInTheDocument();
  });

  it('should render without user name', () => {
    render(<Header userName={null} />);

    expect(screen.getByText('Welcome, ! 👋')).toBeInTheDocument();
  });
});

describe('StatCard', () => {
  it('should render with title, icon, and children', () => {
    render(
      <StatCard title="Test Title" icon="📊">
        <div>Test Content</div>
      </StatCard>
    );

    expect(screen.getByText('Test Title')).toBeInTheDocument();
    expect(screen.getByText('📊')).toBeInTheDocument();
    expect(screen.getByText('Test Content')).toBeInTheDocument();
  });

  it('should apply custom className', () => {
    const { container } = render(
      <StatCard title="Test" icon="📊" className="custom-class">
        <div>Content</div>
      </StatCard>
    );

    expect(container.firstChild).toHaveClass('custom-class');
  });
});

describe('LoadingSpinner', () => {
  it('should render with default message', () => {
    render(<LoadingSpinner />);

    expect(screen.getByText('Loading...')).toBeInTheDocument();
  });

  it('should render with custom message', () => {
    render(<LoadingSpinner message="Custom loading..." />);

    expect(screen.getByText('Custom loading...')).toBeInTheDocument();
  });
});

describe('StatNumber', () => {
  beforeEach(() => {
    jest.useFakeTimers();
  });

  afterEach(() => {
    jest.useRealTimers();
  });

  it('should animate number from 0 to target value', async () => {
    render(<StatNumber value={100} duration={1000} />);

    // Initially should be 0
    expect(screen.getByText('0')).toBeInTheDocument();

    // Fast-forward time within act
    await act(async () => {
      jest.advanceTimersByTime(1000);
    });

    // Should reach target value
    expect(screen.getByText('100')).toBeInTheDocument();
  });

  it('should handle zero value', () => {
    render(<StatNumber value={0} />);
    expect(screen.getByText('0')).toBeInTheDocument();
  });
});