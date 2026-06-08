import { useQuery } from "@tanstack/react-query"
import { redirect, useNavigate } from "@tanstack/react-router"
import { fetchMe, useLogoutMutation, type MeResponse, ApiError } from "./api"

export const authQueryOptions = {
  queryKey: ["auth", "me"] as const,
  queryFn: fetchMe,
  retry: false,
  staleTime: 5 * 60 * 1000,
}

export function useAuth() {
  const query = useQuery(authQueryOptions)

  return {
    user: query.data?.user ?? null,
    isAuthenticated: query.data?.authenticated ?? false,
    isLoading: query.isLoading,
    error: query.error,
  }
}

export function useLogout() {
  const navigate = useNavigate()
  const mutation = useLogoutMutation()
  return async () => {
    await mutation.mutateAsync(undefined).catch(() => {})
    navigate({ to: "/login" })
  }
}

export async function requireAuth(queryClient: { ensureQueryData: Function }) {
  try {
    const data = await queryClient.ensureQueryData(authQueryOptions)
    if (!data?.authenticated) {
      throw redirect({ to: "/login" })
    }
    return data
  } catch (e) {
    if (e instanceof ApiError && e.status === 401) {
      throw redirect({ to: "/login" })
    }
    throw e
  }
}
