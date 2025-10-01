import { apiService, ApiError } from '../src/services/api';
const { apiService, ApiError } = require('../.src/services/api');

global.fetch = jest.fn();

describe('ApiService', () => {
  beforeEach(() => {
    fetch.mockClear();
  });

  describe('fetchDashboardData', () => {
    test('successfully fetches dashboard data', async () => {
      const mockData = { reader_id: 1, most_popular_books: [] };
      fetch.mockResolvedValueOnce({
        ok: true,
        json: async () => mockData,
      });

      const result = await apiService.fetchDashboardData();

      expect(fetch).toHaveBeenCalledWith(
        'http://localhost:8000/dashboardData',
        expect.objectContaining({
          method: 'GET',
          headers: { 'Content-Type': 'application/json' },
        })
      );
      expect(result).toEqual(mockData);
    });

    test('handles HTTP errors', async () => {
      fetch.mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
      });

      await expect(apiService.fetchDashboardData()).rejects.toThrow(ApiError);
    });
  });
});