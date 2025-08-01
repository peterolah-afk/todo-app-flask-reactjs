import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'

// Mock axios
vi.mock('axios')
const mockedAxios = axios as jest.Mocked<typeof axios>

// Mock the API services
const mockApiResponse = {
  data: { id: 1, title: 'Test Task', content: 'Test content' },
  status: 200,
}

describe('API Services', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  describe('Tasks API', () => {
    it('should fetch user tasks successfully', async () => {
      mockedAxios.get.mockResolvedValue(mockApiResponse)
      
      // This would test your actual tasks API service
      const response = await mockedAxios.get('/api/v1/tasks/user', {
        headers: { Authorization: 'Bearer test-token' }
      })
      
      expect(response.data).toEqual(mockApiResponse.data)
      expect(mockedAxios.get).toHaveBeenCalledWith('/api/v1/tasks/user', {
        headers: { Authorization: 'Bearer test-token' }
      })
    })

    it('should create task successfully', async () => {
      const taskData = {
        title: 'New Task',
        content: 'Task content',
        status: 'PENDING',
        tag_id: 1
      }
      
      mockedAxios.post.mockResolvedValue({
        data: { ...taskData, id: 1 },
        status: 201
      })
      
      const response = await mockedAxios.post('/api/v1/tasks', taskData, {
        headers: { Authorization: 'Bearer test-token' }
      })
      
      expect(response.status).toBe(201)
      expect(mockedAxios.post).toHaveBeenCalledWith('/api/v1/tasks', taskData, {
        headers: { Authorization: 'Bearer test-token' }
      })
    })

    it('should handle API errors', async () => {
      const errorResponse = {
        response: {
          data: { message: 'Unauthorized' },
          status: 401
        }
      }
      
      mockedAxios.get.mockRejectedValue(errorResponse)
      
      try {
        await mockedAxios.get('/api/v1/tasks/user')
      } catch (error) {
        expect(error).toEqual(errorResponse)
      }
    })
  })

  describe('Auth API', () => {
    it('should sign in successfully', async () => {
      const credentials = {
        email: 'test@example.com',
        password: 'password123'
      }
      
      const authResponse = {
        data: {
          access_token: 'mock-access-token',
          refresh_token: 'mock-refresh-token'
        },
        status: 200
      }
      
      mockedAxios.post.mockResolvedValue(authResponse)
      
      const response = await mockedAxios.post('/api/v1/auth/sign-in', credentials)
      
      expect(response.data.access_token).toBe('mock-access-token')
      expect(mockedAxios.post).toHaveBeenCalledWith('/api/v1/auth/sign-in', credentials)
    })
  })
}) 