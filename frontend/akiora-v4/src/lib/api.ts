import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import axios, { type AxiosError } from "axios"

const AUTH_BASE = "http://localhost:8000"
const GATEWAY_BASE = "http://localhost:8001"

const authApi = axios.create({
    baseURL: AUTH_BASE,
    withCredentials: true,
    headers: { "Content-Type": "application/json" },
})

const gatewayApi = axios.create({
    baseURL: GATEWAY_BASE,
    withCredentials: true,
    headers: { "Content-Type": "application/json" },
})

export class ApiError extends Error {
    constructor(
        public status: number,
        public body: string,
    ) {
        super(`API Error ${status}`)
    }
}

function handleAxiosError(error: unknown): never {
    if (axios.isAxiosError(error)) {
        const axiosError = error as AxiosError
        throw new ApiError(
            axiosError.response?.status ?? 0,
            typeof axiosError.response?.data === "string"
                ? axiosError.response.data
                : JSON.stringify(axiosError.response?.data ?? axiosError.message),
        )
    }
    throw error
}

// Auth endpoints
export interface AuthUser {
    id: string
    email: string
    nickname: string
    avatar: string | null
    bio: string | null
    gender: "MALE" | "FEMALE" | null
    birth_date: { day: string; hidden: boolean } | null
    socials: Record<string, { link: string; hidden: boolean }> | null
    user_type: string
    created_at: string
    last_updated: string
}

export interface MeResponse {
    user: AuthUser
    authenticated: boolean
}

// Community types
export interface ClubResponse {
    id: string
    owner_id: string
    name: string
    avatar: string | null
    description: string | null
    members: string[]
    created_at: number
}

export interface TeamResponse {
    id: string
    owner_id: string
    name: string
    avatar: string | null
    tag: string
    members: string[]
    created_at: number
}

export interface CreateClubRequest {
    name: string
}

export interface CreateTeamRequest {
    name: string
    tag: string
}

export interface JoinClubRequest {
    club_id: string
}

export async function fetchMe() {
    try {
        const res = await authApi.get<MeResponse>("/me")
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export function getOAuthUrl(provider: "discord" | "yandex") {
    return `${AUTH_BASE}/${provider}/login`
}

export async function loginEmailStart(email: string) {
    try {
        const res = await authApi.post<{ message: string }>("/email/login/start", { email })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function loginEmailFinish(code: string) {
    try {
        const res = await authApi.post<MeResponse>("/email/login/finish", { code })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

// Gateway user endpoints
export interface UpdateProfileData {
    user_id: string
    nickname?: string
    avatar?: string
    bio?: string
    gender?: "MALE" | "FEMALE" | null
    birth_date?: { day: string; hidden: boolean } | null
    socials?: Record<string, { link: string; hidden: boolean }> | null
}

export async function logout() {
    try {
        const res = await authApi.post<{ message: string }>("/logout")
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function updateProfile(userId: string, data: UpdateProfileData) {
    try {

        const res = await gatewayApi.patch<AuthUser>(`/v1/users/${userId}`, data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

// Community endpoints
export async function searchUsers(query: string) {
    try {
        const res = await gatewayApi.get<{ users: AuthUser[] }>(`/v1/users/search?q=${encodeURIComponent(query)}`)
        return res.data.users
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getClubs() {
    try {
        const res = await gatewayApi.get<{ clubs: ClubResponse[] }>("/v1/clubs")
        return res.data.clubs
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getTeams() {
    try {
        const res = await gatewayApi.get<{ teams: TeamResponse[] }>("/v1/teams")
        return res.data.teams
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function createClub(data: CreateClubRequest) {
    try {
        const res = await gatewayApi.post<ClubResponse>("/v1/clubs", data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function createTeam(data: CreateTeamRequest) {
    try {
        const res = await gatewayApi.post<TeamResponse>("/v1/teams", data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function joinClub(clubId: string) {
    try {
        const res = await gatewayApi.post<ClubResponse>(`/v1/clubs/${clubId}/members`, {
            club_id: clubId
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

// --- TanStack Query hooks ---

export function useLoginEmailStartMutation() {
    return useMutation({
        mutationFn: (email: string) => loginEmailStart(email),
    })
}

export function useLoginEmailFinishMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: (code: string) => loginEmailFinish(code),
        onSuccess: (data) => {
            queryClient.setQueryData(["auth", "me"], data)
        },
    })
}

export function useLogoutMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: logout,
        onSettled: () => {
            queryClient.setQueryData(["auth", "me"], null)
            queryClient.removeQueries({ queryKey: ["auth", "me"] })
        },
    })
}

export function useUpdateProfileMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ userId, data }: { userId: string; data: UpdateProfileData }) =>
            updateProfile(userId, data),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["auth", "me"] })
        },
    })
}

// Community query hooks
export function useSearchUsers(query: string) {
    return useQuery({
        queryKey: ["users", "search", query],
        queryFn: () => searchUsers(query),
        enabled: query.length > 2,
        staleTime: 30000,
    })
}

export function useClubs() {
    return useQuery({
        queryKey: ["clubs"],
        queryFn: getClubs,
        staleTime: 60000,
    })
}

export function useTeams() {
    return useQuery({
        queryKey: ["teams"],
        queryFn: getTeams,
        staleTime: 60000,
    })
}

export function useCreateClubMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: createClub,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["clubs"] })
        },
    })
}

export function useCreateTeamMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: createTeam,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["teams"] })
        },
    })
}

export function useJoinClubMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: joinClub,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["clubs"] })
        },
    })
}
