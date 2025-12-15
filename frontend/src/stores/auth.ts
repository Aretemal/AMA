import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import apiClient from '@/api/client'
import type { User } from '@/api/types/user'

export const useAuthStore = defineStore('auth', () => {
  const user = ref<User | null>(null)
  const isLoading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!user.value)

  async function checkAuth() {
    try {
      isLoading.value = true
      error.value = null
      const { data } = await apiClient.get('/auth/me')
      user.value = data
      return true
    } catch (error) {
      user.value = null
      return false
    } finally {
      isLoading.value = false
    }
  }

  async function login(email: string, password: string) {
    try {
      isLoading.value = true
      error.value = null
      const { data } = await apiClient.post('/auth/login', {
        email,
        password,
      })
      user.value = {
        id: data.user.id,
        email: data.user.email,
        username: data.user.username,
        is_active: true,
        is_superuser: false,
        created_at: '',
        updated_at: '',
      }
      await checkAuth()
      return { success: true }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Login failed'
      error.value = errorMessage
      return {
        success: false,
        error: errorMessage,
      }
    } finally {
      isLoading.value = false
    }
  }

  async function register(email: string, password: string, username: string) {
    try {
      isLoading.value = true
      error.value = null
      const { data } = await apiClient.post('/auth/register', {
        email,
        password,
        username,
      })
      return { success: true, user: data }
    } catch (err: any) {
      const errorMessage = err.response?.data?.detail || 'Registration failed'
      error.value = errorMessage
      return {
        success: false,
        error: errorMessage,
      }
    } finally {
      isLoading.value = false
    }
  }

  async function logout() {
    try {
      await apiClient.post('/auth/logout')
      user.value = null
      error.value = null
    } catch (error) {
      user.value = null
    }
  }

  return {
    user,
    isLoading,
    error,
    isAuthenticated,
    checkAuth,
    login,
    register,
    logout,
  }
})

