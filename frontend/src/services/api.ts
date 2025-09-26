// frontend/src/services/api.ts

// Define types for API responses
export interface Book {
  id: number;
  title: string;
  description?: string;
  genre?: string;
  pages?: number;
  published_year?: number;
  author: Author;
  readers_count?: number;
}

export interface Author {
  id: number;
  name: string;
  bio?: string;
  nationality?: string;
  books_count?: number;
  total_readers?: number;
}

export interface Reader {
  id: number;
  name: string;
  email: string;
  join_date: string;
  favorite_genre?: string;
  books_read_count?: number;
}

export interface DashboardStats {
  most_popular_books: Book[];
  most_popular_author: Author;
  user_books_read_count: number;
  user_top_authors: Author[];
}

// Request options interface
interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

class ApiService {
  private baseURL: string;

  constructor() {
    this.baseURL = process.env.REACT_APP_API_URL || 'http://localhost:8000';
  }

  private async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    const url = `${this.baseURL}${endpoint}`;
    
    const config: RequestInit = {
      headers: {
        'Content-Type': 'application/json',
        ...options.headers,
      },
      ...options,
    };

    try {
      const response = await fetch(url, config);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      return await response.json() as T;
    } catch (error) {
      console.error('API request failed:', error);
      
      // Handle unknown error type safely
      if (error instanceof Error) {
        throw new Error(`Failed to fetch data: ${error.message}`);
      } else {
        throw new Error('Failed to fetch data: Unknown error occurred');
      }
    }
  }

  async fetchDashboardData(readerId: number = 1): Promise<DashboardStats> {
    return this.request<DashboardStats>(`/dashboard/${readerId}`);
  }

  async fetchBooks(skip: number = 0, limit: number = 100): Promise<Book[]> {
    return this.request<Book[]>(`/books/?skip=${skip}&limit=${limit}`);
  }

  async fetchAuthors(): Promise<Author[]> {
    return this.request<Author[]>('/authors/');
  }

  async fetchReader(readerId: number): Promise<Reader> {
    return this.request<Reader>(`/readers/${readerId}`);
  }
}

// Create singleton instance
export const apiService = new ApiService();

export default ApiService;