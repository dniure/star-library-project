/**
 * api.ts
 * ----------------
 * Singleton API service for:
 * - Dashboard
 * - Books
 * - Authors
 * - Reader info
 */

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
  genre?: string;
  pages?: number;
  published_year?: number;
  author: Author;
  readers_count?: number;
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
  books_read: Book[];
  user_top_authors: Author[];
}

interface RequestOptions extends RequestInit {
  headers?: Record<string, string>;
}

class ApiService {
  private baseURL = process.env.REACT_APP_API_URL || "http://localhost:8000";

  private async request<T>(endpoint: string, options: RequestOptions = {}): Promise<T> {
    try {
      const response = await fetch(`${this.baseURL}${endpoint}`, {
        headers: { "Content-Type": "application/json", ...options.headers },
        ...options,
      });

      if (!response.ok) throw new Error(`HTTP error! Status: ${response.status}`);
      return (await response.json()) as T;
    } catch (error) {
      console.error("API request failed:", error);
      throw error instanceof Error ? new Error(`Failed to fetch data: ${error.message}`) : new Error("Unknown error occurred");
    }
  }

  fetchDashboardData(readerId = 1) {
    return this.request<DashboardStats>(`/dashboard/${readerId}`);
  }

  fetchBooks(skip = 0, limit = 100) {
    return this.request<Book[]>(`/books/?skip=${skip}&limit=${limit}`);
  }

  fetchAuthors() {
    return this.request<Author[]>("/authors/");
  }

  fetchReader(readerId: number) {
    return this.request<Reader>(`/readers/${readerId}`);
  }
}

export const apiService = new ApiService();
export default ApiService;
