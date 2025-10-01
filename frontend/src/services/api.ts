/**
 * API Service Layer
 * Centralized HTTP client for communicating with backend services.
 * Provides type-safe methods for all data fetching operations.
 */

// Domain Models
export interface Author {
  id: number;
  name: string;
  bio?: string;
  nationality?: string;
  books_count?: number;
  total_readers?: number;
}

export interface Book {
  id: number;
  title: string;
  description?: string;
  genre: string;
  pages: number;
  published_year: number;
  author: Author;
  readers_count?: number;
  reading_time?: number;
  cover_image_url?: string;
  rating?: number;
}

export interface Reader {
  id: number;
  name: string;
  email: string;
  join_date: string;
  favorite_genre?: string;
  books_read_count?: number;
}

export interface DashboardData {
  reader_id: number;
  most_popular_books: Book[];
  most_popular_author?: Author;
  user_books_read: Book[];
  user_top_authors: Author[];
}

// API Configuration
const API_CONFIG = {
  BASE_URL: process.env.REACT_APP_API_URL || "http://localhost:8000",
  DEFAULT_HEADERS: {
    "Content-Type": "application/json",
  },
  TIMEOUT: 10000, // 10 seconds
};

// Custom error class for API-specific errors
class ApiError extends Error {
  constructor(
    message: string,
    public status?: number,
    public originalError?: unknown
  ) {
    super(message);
    this.name = "ApiError";
  }
}

interface RequestOptions extends RequestInit {
  timeout?: number;
}

/**
 * Centralized API service for all backend communications
 */
class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = API_CONFIG.BASE_URL;
  }

  private async request<T>(
    endpoint: string,
    options: RequestOptions = {}
  ): Promise<T> {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), options.timeout || API_CONFIG.TIMEOUT);

    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        signal: controller.signal,
        headers: { ...API_CONFIG.DEFAULT_HEADERS, ...options.headers },
        ...options,
      });

      clearTimeout(timeoutId);

      if (!response.ok) {
        throw new ApiError(`HTTP ${response.status}: ${response.statusText}`, response.status);
      }

      return await response.json() as T;

    } catch (error: unknown) {
      clearTimeout(timeoutId);
      
      // Type-safe error handling
      if (error instanceof ApiError) {
        throw error;
      }

      if (error instanceof DOMException && error.name === "AbortError") {
        throw new ApiError("Request timeout - please try again");
      }

      throw new ApiError(
        `Network error: ${error instanceof Error ? error.message : "Unknown error"}`,
        undefined,
        error
      );
    }
  }

  /**
   * Fetches complete dashboard data for the current user
   */
  async fetchDashboardData(): Promise<DashboardData> {
    return this.request<DashboardData>("/dashboardData");
  }

  /**
   * Fetches paginated books with optional filtering
   */
  async fetchBooks(skip: number = 0, limit: number = 100): Promise<Book[]> {
    const params = new URLSearchParams({
      skip: skip.toString(),
      limit: limit.toString(),
    });

    return this.request<Book[]>(`/books/?${params}`);
  }

  /**
   * Fetches all authors with their statistics
   */
  async fetchAuthors(): Promise<Author[]> {
    return this.request<Author[]>("/authors/");
  }

  /**
   * Fetches specific reader details by ID
   */
  async fetchReader(readerId: number): Promise<Reader> {
    return this.request<Reader>(`/readers/${readerId}`);
  }
}

// Singleton instance for application-wide use
export const apiService = new ApiService();
export default ApiService;