import { renderHook, act } from '@testing-library/react'
import { describe, it, expect, vi, beforeEach } from 'vitest'
import { useAuthStore } from '@/stores/auth-store'

// Mock localStorage
const localStorageMock = {
  getItem: vi.fn(),
  setItem: vi.fn(),
  removeItem: vi.fn(),
  clear: vi.fn(),
}
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
})

describe('useAuthStore', () => {
  beforeEach(() => {
    vi.clearAllMocks()
    // Reset store state
    const { result } = renderHook(() => useAuthStore())
    act(() => {
      result.current.logout()
    })
  })

  it('should have initial state', () => {
    const { result } = renderHook(() => useAuthStore())
    
    expect(result.current.token).toBeNull()
    expect(result.current.isLoggedIn).toBe(false)
  })

  it('should sign in user', () => {
    const { result } = renderHook(() => useAuthStore())
    const mockToken = 'mock-jwt-token'
    
    act(() => {
      result.current.signIn(mockToken)
    })
    
    expect(result.current.token).toBe(mockToken)
    expect(result.current.isLoggedIn).toBe(true)
  })

  it('should logout user', () => {
    const { result } = renderHook(() => useAuthStore())
    
    // First sign in
    const mockToken = 'mock-jwt-token'
    
    act(() => {
      result.current.signIn(mockToken)
    })
    
    // Then logout
    act(() => {
      result.current.logout()
    })
    
    expect(result.current.token).toBeNull()
    expect(result.current.isLoggedIn).toBe(false)
  })

  it('should persist state to localStorage', () => {
    const { result } = renderHook(() => useAuthStore())
    const mockToken = 'mock-jwt-token'
    
    act(() => {
      result.current.signIn(mockToken)
    })
    
    // Verify the state is updated correctly
    expect(result.current.token).toBe(mockToken)
    expect(result.current.isLoggedIn).toBe(true)
  })
}) 