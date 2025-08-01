# Frontend Testing Guide

This document provides comprehensive testing solutions for the React frontend of the todo app.

## Testing Stack

- **Vitest**: Fast unit testing framework
- **React Testing Library**: Component testing utilities
- **@testing-library/jest-dom**: Custom DOM matchers
- **@testing-library/user-event**: User interaction simulation
- **jsdom**: DOM environment for Node.js

## Setup

1. Install testing dependencies:
```bash
cd frontend
npm install
```

2. Run tests:
```bash
# Run all tests
npm test

# Run tests with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run tests in watch mode
npm run test:watch
```

## Test Structure

```
frontend/
├── src/
│   ├── test/
│   │   ├── setup.ts              # Test configuration
│   │   ├── components/            # Component tests
│   │   │   └── Button.test.tsx
│   │   ├── hooks/                 # Hook tests
│   │   │   └── useAuth.test.ts
│   │   └── services/              # Service tests
│   │       └── api.test.ts
├── vitest.config.ts              # Vitest configuration
└── package.json                  # Includes testing scripts
```

## Test Categories

### 1. Component Tests
- UI component rendering
- User interactions (clicks, form submissions)
- Props and state changes
- Accessibility testing

### 2. Hook Tests
- Custom hook behavior
- State management
- Side effects
- Error handling

### 3. Service Tests
- API calls
- Data transformation
- Error handling
- Mock responses

## Key Features

### Component Testing
- Tests user interactions, not implementation details
- Focuses on accessibility and user experience
- Uses semantic queries (getByRole, getByLabelText)

### Hook Testing
- Tests custom hooks in isolation
- Verifies state changes and side effects
- Mocks external dependencies

### API Testing
- Mocks HTTP requests
- Tests success and error scenarios
- Verifies data transformation

## Best Practices

1. **User-Centric Testing**: Test behavior, not implementation
2. **Accessibility**: Use semantic queries and test accessibility
3. **Mocking**: Mock external dependencies appropriately
4. **Clean Tests**: Each test should be independent
5. **Descriptive Names**: Test names should describe the behavior

## Example Test Patterns

### Component Testing
```typescript
import { render, screen, fireEvent } from '@testing-library/react'
import { Button } from './Button'

test('button calls onClick when clicked', () => {
  const handleClick = vi.fn()
  render(<Button onClick={handleClick}>Click me</Button>)
  
  fireEvent.click(screen.getByRole('button'))
  expect(handleClick).toHaveBeenCalledTimes(1)
})
```

### Hook Testing
```typescript
import { renderHook, act } from '@testing-library/react'
import { useCounter } from './useCounter'

test('increments counter', () => {
  const { result } = renderHook(() => useCounter())
  
  act(() => {
    result.current.increment()
  })
  
  expect(result.current.count).toBe(1)
})
```

### API Testing
```typescript
import { vi } from 'vitest'
import { fetchTasks } from './api'

vi.mock('axios')

test('fetches tasks successfully', async () => {
  const mockTasks = [{ id: 1, title: 'Test' }]
  mockedAxios.get.mockResolvedValue({ data: mockTasks })
  
  const result = await fetchTasks()
  expect(result).toEqual(mockTasks)
})
```

## Coverage Goals

- Aim for >70% code coverage
- Focus on user-facing functionality
- Test critical business logic
- Include error scenarios

## Debugging Tests

```bash
# Run single test file
npm test Button.test.tsx

# Run with debug output
npm test -- --reporter=verbose

# Run tests in browser
npm run test:ui
```

## CI/CD Integration

```yaml
# Example GitHub Actions workflow
- name: Run Frontend Tests
  run: |
    cd frontend
    npm install
    npm run test:coverage
```

## Testing Utilities

### Custom Render Function
Create a custom render function for providers:

```typescript
// test-utils.tsx
import { render } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: { retry: false },
    mutations: { retry: false },
  },
})

export const renderWithProviders = (ui: React.ReactElement) => {
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  )
}
```

### Mock Service Worker
For API testing, consider using MSW:

```bash
npm install msw --save-dev
```

This allows you to intercept network requests and provide mock responses.

## Performance Testing

Consider adding performance testing with tools like:
- **@testing-library/react-hooks**: For hook performance
- **@testing-library/user-event**: For interaction performance
- **Lighthouse CI**: For performance metrics 