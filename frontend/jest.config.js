module.exports = {
  testEnvironment: 'jsdom',
  setupFilesAfterEnv: ['<rootDir>/tests/setup.js'],
  moduleNameMapping: {
    '\\.(css|less|scss|sass)$': 'identity-obj-proxy',
  },
  transformIgnorePatterns: [
    'node_modules/(?!(your-module|another-module)/)'
  ],
  testMatch: [
    '<rootDir>/tests/**/*.test.{js,jsx}'
  ],
  moduleDirectories: [
    'node_modules',
    'src'
  ],
  moduleFileExtensions: ['js', 'jsx', 'json'],
};