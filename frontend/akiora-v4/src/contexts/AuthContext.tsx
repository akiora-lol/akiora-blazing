import React, { createContext, useContext, useEffect } from 'react'
import { useNavigate } from '@tanstack/react-router'
import { useAuth as useAuthQuery, authQueryOptions } from '../lib/auth'
import { useQueryClient } from '@tanstack/react-query'
import type { AuthUser } from '../lib/api'

interface AuthContextType {
  user: AuthUser | null
  isAuthenticated: boolean
  isLoading: boolean
  error: unknown
  checkAuth: () => void
  redirectIfAuthenticated: () => void
  redirectIfNotAuthenticated: () => void
}

const AuthContext = createContext<AuthContextType | undefined>(undefined)

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const authQuery = useAuthQuery()
  const navigate = useNavigate()
  const queryClient = useQueryClient()

  const checkAuth = () => {
    queryClient.invalidateQueries({ queryKey: authQueryOptions.queryKey })
  }

  const redirectIfAuthenticated = () => {
    if (authQuery.isAuthenticated && !authQuery.isLoading) {
      navigate({ to: '/profile', replace: true })
    }
  }

  const redirectIfNotAuthenticated = () => {
    if (!authQuery.isAuthenticated && !authQuery.isLoading && authQuery.error) {
      navigate({ to: '/login', replace: true })
    }
  }

  // Auto redirect logic for specific routes
  useEffect(() => {
    if (authQuery.isLoading) return

    const currentPath = window.location.pathname

    // Redirect authenticated users away from auth pages
    if (authQuery.isAuthenticated && (currentPath === '/login' || currentPath === '/onboarding')) {
      navigate({ to: '/profile', replace: true })
    }

    // Redirect unauthenticated users away from protected pages
    if (!authQuery.isAuthenticated && authQuery.error && (currentPath === '/profile' || currentPath === '/onboarding')) {
      navigate({ to: '/login', replace: true })
    }
  }, [authQuery.isAuthenticated, authQuery.isLoading, authQuery.error, navigate])

  const value: AuthContextType = {
    user: authQuery.user,
    isAuthenticated: authQuery.isAuthenticated,
    isLoading: authQuery.isLoading,
    error: authQuery.error,
    checkAuth,
    redirectIfAuthenticated,
    redirectIfNotAuthenticated,
  }

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
}

export function useAuthContext() {
  const context = useContext(AuthContext)
  if (context === undefined) {
    throw new Error('useAuthContext must be used within an AuthProvider')
  }
  return context
}

// Convenience hooks for route guards
export function useRequireAuth() {
  const { isAuthenticated, isLoading, redirectIfNotAuthenticated } = useAuthContext()

  useEffect(() => {
    if (!isLoading && !isAuthenticated) {
      redirectIfNotAuthenticated()
    }
  }, [isAuthenticated, isLoading, redirectIfNotAuthenticated])

  return { isAuthenticated, isLoading }
}

export function useRequireGuest() {
  const { isAuthenticated, isLoading, redirectIfAuthenticated } = useAuthContext()

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      redirectIfAuthenticated()
    }
  }, [isAuthenticated, isLoading, redirectIfAuthenticated])

  return { isAuthenticated, isLoading }
}