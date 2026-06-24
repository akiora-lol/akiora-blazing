import { useMutation, useQuery, useQueryClient } from "@tanstack/react-query"
import axios, { type AxiosError } from "axios"

const AUTH_BASE = import.meta.env.VITE_AUTH_BASE_URL ?? "http://localhost:8000"
const GATEWAY_BASE = import.meta.env.VITE_GATEWAY_BASE_URL ?? "http://localhost:8001"

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
    league_accounts: LeagueAccount[]
    user_type: string
    created_at: string
    last_updated: string
}

export interface LeagueAccount {
    status: "done" | "pending" | string
    username: string
    tagline: string
    server: string
    profile_image_url: string | null
    solo_tier: string | null
    solo_division: number | null
    solo_lp: number | null
    solo_tier_image_url: string | null
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
    owner_id: string
    name: string
}

export interface CreateTeamRequest {
    owner_id: string
    name: string
    tag: string
}

export interface JoinClubRequest {
    club_id: string
    user_id: string
    actor_id?: string | null
    tokens?: string[]
}

export interface CommunityListOptions {
    page?: number
    page_size?: number
    search?: string
}

export interface ListUsersResponse {
    users: AuthUser[]
    total_count: number
    page: number
    page_size: number
    has_next: boolean
}

export interface ListClubsResponse {
    clubs: ClubResponse[]
    total_count: number
    page: number
    page_size: number
    has_next: boolean
}

export interface ListTeamsResponse {
    teams: TeamResponse[]
    total_count: number
    page: number
    page_size: number
    has_next: boolean
}

export interface FriendResponse {
    id: string
    user_id_1: string
    user_id_2: string
    status: string
    created_at: number
    updated_at: number
}

export interface ListFriendsResponse {
    friends: FriendResponse[]
    total_count: number
}

export interface FriendListItem {
    friendship: FriendResponse
    user: AuthUser
}

export interface RespondFriendRequestData {
    request_id: string
    responder_id: string
    accept: boolean
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

export interface LolVerificationStartRequest {
    server: string
    username: string
    tagline: string
}

export interface LolVerificationStartResponse {
    verification_id: string
    current_profile_icon_id: number
    profile_image_url: string
    target_icon_id: number
    target_profile_image_url: string
    solo_tier: string | null
    solo_division: number | null
    solo_lp: number | null
    solo_tier_image_url: string | null
    server: string
    riot_id: string
}

export interface LolVerificationFinishResponse {
    verified: boolean
    profile_icon_id: number
    user: AuthUser
}

export async function startLolAccountVerification(data: LolVerificationStartRequest) {
    try {
        const res = await authApi.post<LolVerificationStartResponse>("/lol/verification/start", data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function finishLolAccountVerification(verificationId: string) {
    try {
        const res = await authApi.post<LolVerificationFinishResponse>("/lol/verification/finish", {
            verification_id: verificationId,
        })
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
export async function listUsers(options: CommunityListOptions = {}) {
    try {
        const res = await gatewayApi.get<ListUsersResponse>("/v1/users", {
            params: {
                page: options.page ?? 1,
                page_size: options.page_size ?? 50,
                search: options.search || undefined,
            },
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function searchUsers(query: string) {
    const data = await listUsers({ search: query, page: 1, page_size: 50 })
    return data?.users ?? []
}

export async function getUser(userId: string) {
    try {
        const res = await gatewayApi.get<AuthUser>(`/v1/users/${userId}`)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getFriends(userId: string, friendStatus = "ACCEPTED") {
    try {
        const res = await gatewayApi.get<ListFriendsResponse>(`/v1/users/${userId}/friends`, {
            params: { friend_status: friendStatus },
        })
        const friends = res.data.friends ?? []
        const items = await Promise.all(
            friends.map(async (friendship) => {
                const otherUserId =
                    friendship.user_id_1 === userId ? friendship.user_id_2 : friendship.user_id_1
                const user = await getUser(otherUserId)
                return { friendship, user }
            }),
        )
        return items
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getPendingFriendRequests(userId: string) {
    try {
        const res = await gatewayApi.get<ListFriendsResponse>(`/v1/users/${userId}/friend-requests/pending`)
        const friends = res.data.friends ?? []
        const items = await Promise.all(
            friends.map(async (friendship) => {
                const senderId = friendship.user_id_1
                const user = await getUser(senderId)
                return { friendship, user }
            }),
        )
        return items
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function listClubs(options: CommunityListOptions = {}) {
    try {
        const res = await gatewayApi.get<ListClubsResponse>("/v1/clubs", {
            params: {
                page: options.page ?? 1,
                page_size: options.page_size ?? 50,
                search: options.search || undefined,
            },
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getClubs() {
    const data = await listClubs()
    return data?.clubs ?? []
}

export async function listTeams(options: CommunityListOptions = {}) {
    try {
        const res = await gatewayApi.get<ListTeamsResponse>("/v1/teams", {
            params: {
                page: options.page ?? 1,
                page_size: options.page_size ?? 50,
                search: options.search || undefined,
            },
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getTeams() {
    const data = await listTeams()
    return data?.teams ?? []
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

export async function joinClubAsUser(clubId: string, userId: string) {
    try {
        const res = await gatewayApi.post<ClubResponse>(`/v1/clubs/${clubId}/members`, {
            club_id: clubId,
            user_id: userId,
            actor_id: userId,
            tokens: [],
        } satisfies JoinClubRequest)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function sendFriendRequest(senderId: string, receiverId: string) {
    try {
        const res = await gatewayApi.post<FriendResponse>('/v1/users/friend-requests', {
            request: {
                sender_id: senderId,
                receiver_id: receiverId,
            },
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function respondFriendRequest(data: RespondFriendRequestData) {
    try {
        const res = await gatewayApi.post<FriendResponse>('/v1/users/friend-requests/respond', {
            response: data,
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

export function useStartLolVerificationMutation() {
    return useMutation({
        mutationFn: startLolAccountVerification,
    })
}

export function useFinishLolVerificationMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: finishLolAccountVerification,
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

export function useCommunityUsers(page: number, search = "", pageSize = 50) {
    return useQuery({
        queryKey: ["users", "list", page, pageSize, search],
        queryFn: () => listUsers({ page, page_size: pageSize, search }),
        staleTime: 30000,
    })
}

export function useUserProfile(userId?: string) {
    return useQuery({
        queryKey: ["users", "profile", userId],
        queryFn: () => getUser(userId as string),
        enabled: !!userId,
        staleTime: 30000,
    })
}

export function useFriends(userId?: string) {
    return useQuery({
        queryKey: ["users", "friends", userId],
        queryFn: () => getFriends(userId as string),
        enabled: !!userId,
        staleTime: 30000,
    })
}

export function usePendingFriendRequests(userId?: string) {
    return useQuery({
        queryKey: ["users", "friend-requests", "pending", userId],
        queryFn: () => getPendingFriendRequests(userId as string),
        enabled: !!userId,
        staleTime: 15000,
        refetchInterval: 30000,
    })
}

export function useCommunityClubs(page: number, pageSize = 50) {
    return useQuery({
        queryKey: ["clubs", "list", page, pageSize],
        queryFn: () => listClubs({ page, page_size: pageSize }),
        staleTime: 60000,
    })
}

export function useClubs() {
    return useQuery({
        queryKey: ["clubs"],
        queryFn: getClubs,
        staleTime: 60000,
    })
}

export function useCommunityTeams(page: number, pageSize = 50) {
    return useQuery({
        queryKey: ["teams", "list", page, pageSize],
        queryFn: () => listTeams({ page, page_size: pageSize }),
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
        mutationFn: ({ clubId, userId }: { clubId: string; userId: string }) => joinClubAsUser(clubId, userId),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["clubs"] })
        },
    })
}

export function useSendFriendRequestMutation() {
    return useMutation({
        mutationFn: ({ senderId, receiverId }: { senderId: string; receiverId: string }) =>
            sendFriendRequest(senderId, receiverId),
    })
}

export function useRespondFriendRequestMutation(userId?: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: respondFriendRequest,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ["users", "friends", userId] })
            queryClient.invalidateQueries({ queryKey: ["users", "friend-requests", "pending", userId] })
        },
    })
}

// Partner search types
export type SearchServer = 'euw' | 'ru' | 'eune' | 'na' | 'tr'
export type SearchRole = 'top' | 'jg' | 'mid' | 'adc' | 'sup'
export type SearchRankName =
    | 'iron'
    | 'bronze'
    | 'silver'
    | 'gold'
    | 'platinum'
    | 'emerald'
    | 'diamond'
    | 'master'
    | 'grandmaster'
    | 'challenger'
export type SearchFormStatus = 'active' | 'frozen'
export type SearchSwipeAction = 'like' | 'dislike' | 'block'

export interface SearchLeagueRank {
    rank: SearchRankName
    division: number
    lp?: number | null
}

export interface SearchRankRange {
    server: SearchServer
    min_rank: SearchLeagueRank
    max_rank: SearchLeagueRank
}

export interface SearchOwnerPreview {
    user_id: string
    username?: string | null
    avatar_url?: string | null
    riot_game_name?: string | null
    riot_tagline?: string | null
    profile_image_url?: string | null
    solo_rank?: SearchLeagueRank | null
    solo_tier_image_url?: string | null
}

export interface ColdFormResponse {
    id: string
    owner_id: string
    owner?: SearchOwnerPreview | null
    liked_by: string[]
    disliked_by: string[]
    blocked_by: string[]
    created_at: string
    rank_range: SearchRankRange[]
    my_roles: SearchRole[]
    looking_for_roles: SearchRole[]
    description: string
    status: SearchFormStatus
    updated_at: string
}

export interface HotFormResponse {
    id: string
    owner_id: string
    owner?: SearchOwnerPreview | null
    liked_by: string[]
    disliked_by: string[]
    created_at: string
    rank_range: SearchRankRange[]
    my_roles: SearchRole[]
    looking_for_roles: SearchRole[]
    description: string
    expires_at?: string | null
}

export interface SearchFormsFilter {
    rank_range?: SearchRankRange[]
    my_roles?: SearchRole[]
    looking_for_roles?: SearchRole[]
    servers?: SearchServer[]
    owner_id?: string
    exclude_owner_id?: string
    exclude_blocked_by?: string
    status?: SearchFormStatus | null
    min_likes?: number | null
    query?: string | null
}

export interface SearchPagination {
    page?: number
    page_size?: number
    skip?: number
    limit?: number
}

export interface CreateSearchFormRequest {
    owner_id: string
    rank_range: SearchRankRange[]
    my_roles: SearchRole[]
    looking_for_roles: SearchRole[]
    description: string
    status?: SearchFormStatus
}

export interface ColdDeckResponse {
    forms: ColdFormResponse[]
}

export interface ListColdFormsResponse {
    forms: ColdFormResponse[]
    total_count: number
    page: number
    page_size: number
    has_next: boolean
}

export interface ListHotFormsResponse {
    forms: HotFormResponse[]
    total_count: number
    page: number
    page_size: number
    has_next: boolean
}

export async function getColdDeck(actorId: string, filter: SearchFormsFilter = {}, limit = 20) {
    try {
        const res = await gatewayApi.post<ColdDeckResponse>('/v1/search/cold-forms/deck', {
            actor_id: actorId,
            filter,
            limit,
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function listHotForms(
    filter: SearchFormsFilter = {},
    pagination: SearchPagination = { page: 1, page_size: 50 },
) {
    try {
        const res = await gatewayApi.post<ListHotFormsResponse>('/v1/search/hot-forms/search', {
            filter,
            pagination,
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function createColdSearchForm(data: CreateSearchFormRequest) {
    try {
        const res = await gatewayApi.post<ColdFormResponse>('/v1/search/cold-forms', data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function createHotSearchForm(data: CreateSearchFormRequest) {
    try {
        const res = await gatewayApi.post<HotFormResponse>('/v1/search/hot-forms', data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function swipeColdSearchForm(formId: string, userId: string, action: SearchSwipeAction) {
    try {
        const res = await gatewayApi.post(`/v1/search/cold-forms/${formId}/swipe`, null, {
            params: { user_id: userId, action },
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function swipeHotSearchForm(formId: string, userId: string, action: SearchSwipeAction) {
    try {
        const res = await gatewayApi.post(`/v1/search/hot-forms/${formId}/swipe`, null, {
            params: { user_id: userId, action },
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export function useColdDeck(actorId?: string, filter: SearchFormsFilter = {}, limit = 20) {
    return useQuery({
        queryKey: ['search', 'cold-deck', actorId, filter, limit],
        queryFn: () => getColdDeck(actorId as string, filter, limit),
        enabled: !!actorId,
        staleTime: 15000,
    })
}

export function useHotForms(
    filter: SearchFormsFilter = {},
    pagination: SearchPagination = { page: 1, page_size: 50 },
) {
    return useQuery({
        queryKey: ['search', 'hot-forms', filter, pagination],
        queryFn: () => listHotForms(filter, pagination),
        staleTime: 15000,
    })
}

export function useCreateColdSearchFormMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: createColdSearchForm,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['search'] })
        },
    })
}

export function useCreateHotSearchFormMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: createHotSearchForm,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['search'] })
        },
    })
}

export function useSwipeColdSearchFormMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ formId, userId, action }: { formId: string; userId: string; action: SearchSwipeAction }) =>
            swipeColdSearchForm(formId, userId, action),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['search', 'cold-deck'] })
        },
    })
}

export function useSwipeHotSearchFormMutation() {
    return useMutation({
        mutationFn: ({ formId, userId, action }: { formId: string; userId: string; action: SearchSwipeAction }) =>
            swipeHotSearchForm(formId, userId, action),
    })
}

// Messenger types
export type ChatOwnerType = 'OWNER_UNSPECIFIED' | 'SYSTEM' | 'CLUB' | 'TOURNAMENT' | 'GAMESERIES'
export type ChatType = 'CHAT_TYPE_UNSPECIFIED' | 'PRIVATE' | 'PUBLIC'
export type ChatStatus = 'CHAT_STATUS_UNSPECIFIED' | 'ACTIVE' | 'FROZEN'
export type MessageStatus = 'MESSAGE_STATUS_UNSPECIFIED' | 'SENT' | 'READ'

export interface Reaction {
    emote_id: string
    user_id: string
}

export interface MessageShort {
    body: string
    timestamp: number
}

export interface ChatResponse {
    id: string
    owner_id: string
    owner_type: ChatOwnerType
    type: ChatType
    status: ChatStatus
    timestamp: number
    allowed_users: string[]
}

export interface MessageResponse {
    id: string
    chat_id: string
    creator_id: string
    body: string
    status: MessageStatus
    read_by: string[]
    timestamp: number
    history: MessageShort[]
    reply_to: string | null
    reactions: Reaction[]
    spoiler: boolean
}

export interface GetMessagesResponse {
    messages: MessageResponse[]
    total_count?: number
}

export interface GetUserChatsResponse {
    chats: ChatResponse[]
    total_count?: number
    page?: number
    page_size?: number
    has_next?: boolean
}

export interface SendMessageRequest {
    chat_id: string
    creator_id: string
    body: string
    reply_to?: string
    spoiler?: boolean
}

export interface CreateChatRequest {
    owner_id: string
    owner_type: ChatOwnerType
    type: ChatType
    allowed_users: string[]
}

// Messenger API
export async function getUserChats(userId: string) {
    try {
        const res = await gatewayApi.get<GetUserChatsResponse>(`/v1/users/${userId}/chats`)
        return res.data.chats
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function createChat(data: CreateChatRequest) {
    try {
        const res = await gatewayApi.post<ChatResponse>('/v1/chats', data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getOrCreatePrivateChat(userId: string, friendId: string) {
    const chats = await getUserChats(userId)
    const existing = chats?.find(chat => {
        if (chat.type !== 'PRIVATE') return false
        const members = new Set([chat.owner_id, ...chat.allowed_users])
        return members.has(userId) && members.has(friendId)
    })
    if (existing) return existing
    return createChat({
        owner_id: userId,
        owner_type: 'SYSTEM',
        type: 'PRIVATE',
        allowed_users: [friendId],
    })
}

export async function getChat(chatId: string) {
    try {
        const res = await gatewayApi.get<ChatResponse>(`/v1/chats/${chatId}`)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getMessages(chatId: string, limit = 50, beforeTimestamp?: number) {
    try {
        const res = await gatewayApi.get<GetMessagesResponse>(`/v1/chats/${chatId}/messages`, {
            params: {
                limit,
                before_timestamp: beforeTimestamp,
            },
        })
        return res.data.messages
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function sendMessage(data: SendMessageRequest) {
    try {
        const res = await gatewayApi.post<MessageResponse>(`/v1/chats/${data.chat_id}/messages`, {
            chat_id: data.chat_id,
            creator_id: data.creator_id,
            body: data.body,
            reply_to: data.reply_to,
            spoiler: data.spoiler,
        })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

// Messenger hooks
export function useUserChats(userId: string) {
    return useQuery({
        queryKey: ['messenger', 'chats', userId],
        queryFn: () => getUserChats(userId),
        enabled: !!userId,
        staleTime: 30000,
    })
}

export function useGetOrCreatePrivateChatMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ userId, friendId }: { userId: string; friendId: string }) =>
            getOrCreatePrivateChat(userId, friendId),
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: ['messenger', 'chats', variables.userId] })
        },
    })
}

export function useMessages(chatId: string, limit = 50) {
    return useQuery({
        queryKey: ['messenger', 'messages', chatId, limit],
        queryFn: () => getMessages(chatId, limit),
        enabled: !!chatId,
        staleTime: 10000,
    })
}

export function useSendMessage() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: sendMessage,
        onSuccess: (_, variables) => {
            queryClient.invalidateQueries({ queryKey: ['messenger', 'messages', variables.chat_id] })
            queryClient.invalidateQueries({ queryKey: ['messenger', 'chats'] })
        },
    })
}

// Tournament types
export type TournamentStatus = 'scheduled' | 'active' | 'finished' | 'canceled'
export type TournamentType = 'draft' | 'presigned'
export type TournamentRole = 'top' | 'jungle' | 'mid' | 'adc' | 'support'
export type BracketType = 'single_elimination' | 'single_elimination_with_third' | 'double_elimination' | 'swiss' | 'round_robin'
export type DraftType = 'fearless' | 'iron_man' | 'classic' | 'all_random'
export type GameSeriesStatus = 'scheduled' | 'active' | 'finished' | 'canceled'
export type TournamentLifecycle =
    | 'registration_open'
    | 'registration_locked'
    | 'captain_setup'
    | 'draft_ready'
    | 'draft_in_progress'
    | 'draft_finished'
    | 'bracket_ready'
    | 'tournament_active'
    | 'tournament_finished'
    | 'tournament_cancelled'
export type DraftPickDirection = 'linear' | 'snake' | 'manual'

export interface Actor {
    id: string
    type: 'user' | 'team' | 'club'
}

export interface TeamParticipant {
    actor: Actor | null
    players: string[]
    draft_roles?: TournamentRole[]
}

export interface MatchResponse {
    game_series_id: string
    team1: Actor | null
    team2: Actor | null
    winner: Actor | null
    round: number
    match_number: number
    next_match_id: number | null
    best_of: number
}

export interface BracketResponse {
    rounds: MatchResponse[][]
    round_settings: BracketRoundSettings[]
    matches: MatchResponse[]
}

export interface BracketRoundSettings {
    round: number
    label?: string | null
    best_of: number
}

export interface DraftCaptainInfo {
    captain: Actor
    order: number
    picked_players: Actor[]
}

export interface DraftConfig {
    captain_count: number
    captains: DraftCaptainInfo[]
    pick_order_captain_ids: string[]
    pick_direction: DraftPickDirection
    max_extra_players_per_team: number
}

export interface DraftState {
    config: DraftConfig
    current_pick_index: number
    current_captain_id?: string | null
    available_player_ids: string[]
    finished: boolean
}

export interface LolGameSettings {
    team_size: number
    map: number
}

export interface LolGameSeriesSettings {
    game_settings: LolGameSettings
    forbidden_champions: number[]
    best_of: number | null
    draft_type: DraftType
}

export interface LolTournamentSettings {
    tournament_type: TournamentType
    game_settings: LolGameSettings
    game_series_settings: LolGameSeriesSettings
    best_of: number[]
    bracket_type: BracketType
    draft_start?: number | null
}

export interface TournamentResponse {
    id: string
    host: Actor
    participant_pool: TeamParticipant[]
    prizepool: string
    is_open: boolean
    wait_list: TeamParticipant[]
    status: TournamentStatus
    settings: LolTournamentSettings
    start: number
    end: number | null
    lifecycle: TournamentLifecycle
    draft_start?: number | null
    registration_locked_at?: number | null
    draft_state?: DraftState | null
    bracket: BracketResponse | null
}

export interface CreateTournamentRequest {
    host: Actor
    start: number
    is_open: boolean
    prizepool: string
    settings: LolTournamentSettings
    draft_start?: number | null
    name?: string
    description?: string
    avatar?: string
}

export type GatewayActorType = 'ACTOR_UNSPECIFIED' | 'USER' | 'TEAM' | 'CLUB'
export type GatewayGameType = 'GAME_TYPE_UNSPECIFIED' | 'LOL' | 'TFT' | 'VALORANT'
export type GatewayStatus = 'STATUS_UNSPECIFIED' | 'SCHEDULED' | 'ACTIVE' | 'FINISHED' | 'CANCELLED'
export type GatewayLolGameMode = 'GAME_MODE_UNSPECIFIED' | 'CLASSIC' | 'FEARLESS' | 'IRON_MAN' | 'ALL_RANDOM'
export type GatewayTournamentLifecycle =
    | 'TOURNAMENT_LIFECYCLE_UNSPECIFIED'
    | 'REGISTRATION_OPEN'
    | 'REGISTRATION_LOCKED'
    | 'CAPTAIN_SETUP'
    | 'DRAFT_READY'
    | 'DRAFT_IN_PROGRESS'
    | 'DRAFT_FINISHED'
    | 'BRACKET_READY'
    | 'TOURNAMENT_ACTIVE'
    | 'TOURNAMENT_FINISHED'
    | 'TOURNAMENT_CANCELLED'
export type GatewayDraftPickDirection = 'DRAFT_PICK_DIRECTION_UNSPECIFIED' | 'LINEAR' | 'SNAKE' | 'MANUAL'
export type GatewayLolBracketMode =
    | 'LOL_BRACKET_MODE_UNSPECIFIED'
    | 'DOUBLE_ELIM'
    | 'SINGLE_ELIM_THIRD_PLACE'
    | 'SINGLE_ELIM_NO_THIRD_PLACE'
    | 'SWISS'
    | 'ROUND_ROBIN'
    | 'SCRIM'

export interface GatewayActor {
    id: string
    actor_type: GatewayActorType
}

export interface GatewayLolTournamentSettings {
    tournament_type?: 'UNSPECIFIED' | 'PRESIGNED' | 'DRAFT' | 'PRESIGN' | 'PICKEM'
    bracket_mode?: GatewayLolBracketMode
    draft_mode?: GatewayLolGameMode[]
    team_size?: number
    map?: number
    forbidden_champions?: number[]
    series_best_of?: number[]
    draft_start?: number | null
}

export interface GatewayTournamentSettings {
    game_type: GatewayGameType
    lol?: GatewayLolTournamentSettings | null
    tft?: { todo?: string | null } | null
    valorant?: { todo?: string | null } | null
}

export interface GatewayTournamentResponse {
    id: string
    host: GatewayActor
    participants?: GatewayActor[]
    settings: GatewayTournamentSettings
    game_series_ids?: string[]
    start: number
    end?: number | null
    status?: GatewayStatus
    prizepool?: string | null
    is_open?: boolean
    lifecycle?: GatewayTournamentLifecycle
    draft_start?: number | null
    registration_locked_at?: number | null
    draft_state?: GatewayDraftState | null
    bracket?: GatewayBracketInfo | null
}

export interface GatewayManyTournamentsResponse {
    tournaments: GatewayTournamentResponse[]
}

export interface GatewayListTournamentsResponse extends GatewayManyTournamentsResponse {
    total_count: number
    page: number
    page_size: number
    has_next: boolean
}

export interface ListTournamentsOptions {
    page?: number
    page_size?: number
    game_type?: GatewayGameType
    status?: GatewayStatus
    host_id?: string
    is_participant?: boolean
    min_start_time?: number
    max_start_time?: number
    is_open?: boolean
}

export interface GatewayParticipantInfo {
    participant: GatewayActor
    user_ids: string[]
    joined_at: number
    draft_roles?: TournamentRole[]
    is_captain?: boolean
    captain_order?: number | null
}

export interface GatewayParticipantsResponse {
    participants: GatewayParticipantInfo[]
    total_count: number
}

export interface GatewayWaitlistResponse {
    participants: GatewayActor[]
    total_count: number
}

export interface GatewayBracketInfo {
    rounds?: GatewayMatchInfo[][]
    round_settings?: GatewayBracketRoundSettings[]
    matches?: GatewayMatchInfo[]
    bracket_id?: string
    participant_ids?: string[]
    round?: number
}

export interface GatewayBracketResponse {
    bracket: GatewayBracketInfo | null
}

export interface GatewayBracketRoundSettings {
    round: number
    label?: string | null
    best_of: number
}

export interface GatewayMatchInfo {
    game_series_id: string
    team1?: GatewayActor | null
    team2?: GatewayActor | null
    winner?: GatewayActor | null
    round: number
    match_number: number
    next_match_id?: number | null
    best_of?: number
}

export interface GatewayDraftCaptainInfo {
    captain: GatewayActor
    order: number
    picked_players?: GatewayActor[]
}

export interface GatewayDraftConfig {
    captain_count: number
    captains?: GatewayDraftCaptainInfo[]
    pick_order_captain_ids?: string[]
    pick_direction?: GatewayDraftPickDirection
    max_extra_players_per_team?: number
}

export interface GatewayDraftState {
    config: GatewayDraftConfig
    current_pick_index: number
    current_captain_id?: string | null
    available_player_ids?: string[]
    finished: boolean
}

export interface GatewayTournamentStats {
    total_participants: number
    total_teams: number
    waitlist_count: number
    status: string
    time_until_start: number
}

export interface GatewayIsParticipantResponse {
    is_participant: boolean
    role?: string | null
}

const STATUS_FROM_GATEWAY: Record<GatewayStatus, TournamentStatus> = {
    STATUS_UNSPECIFIED: 'scheduled',
    SCHEDULED: 'scheduled',
    ACTIVE: 'active',
    FINISHED: 'finished',
    CANCELLED: 'canceled',
}

const LIFECYCLE_FROM_GATEWAY: Record<GatewayTournamentLifecycle, TournamentLifecycle> = {
    TOURNAMENT_LIFECYCLE_UNSPECIFIED: 'registration_open',
    REGISTRATION_OPEN: 'registration_open',
    REGISTRATION_LOCKED: 'registration_locked',
    CAPTAIN_SETUP: 'captain_setup',
    DRAFT_READY: 'draft_ready',
    DRAFT_IN_PROGRESS: 'draft_in_progress',
    DRAFT_FINISHED: 'draft_finished',
    BRACKET_READY: 'bracket_ready',
    TOURNAMENT_ACTIVE: 'tournament_active',
    TOURNAMENT_FINISHED: 'tournament_finished',
    TOURNAMENT_CANCELLED: 'tournament_cancelled',
}

const DRAFT_PICK_DIRECTION_FROM_GATEWAY: Record<GatewayDraftPickDirection, DraftPickDirection> = {
    DRAFT_PICK_DIRECTION_UNSPECIFIED: 'linear',
    LINEAR: 'linear',
    SNAKE: 'snake',
    MANUAL: 'manual',
}

const DRAFT_PICK_DIRECTION_TO_GATEWAY: Record<DraftPickDirection, GatewayDraftPickDirection> = {
    linear: 'LINEAR',
    snake: 'SNAKE',
    manual: 'MANUAL',
}

const BRACKET_TO_GATEWAY: Record<BracketType, GatewayLolBracketMode> = {
    single_elimination: 'SINGLE_ELIM_NO_THIRD_PLACE',
    single_elimination_with_third: 'SINGLE_ELIM_THIRD_PLACE',
    double_elimination: 'DOUBLE_ELIM',
    swiss: 'SWISS',
    round_robin: 'ROUND_ROBIN',
}

const DRAFT_TO_GATEWAY: Record<DraftType, GatewayLolGameMode> = {
    classic: 'CLASSIC',
    fearless: 'FEARLESS',
    iron_man: 'IRON_MAN',
    all_random: 'ALL_RANDOM',
}

const TOURNAMENT_TYPE_TO_GATEWAY: Record<TournamentType, NonNullable<GatewayLolTournamentSettings['tournament_type']>> = {
    presigned: 'PRESIGNED',
    draft: 'DRAFT',
}

function toGatewayActor(actor: Actor): GatewayActor {
    return { id: actor.id, actor_type: actor.type.toUpperCase() as GatewayActorType }
}

function fromGatewayActor(actor?: GatewayActor | null): Actor | null {
    if (!actor || actor.actor_type === 'ACTOR_UNSPECIFIED') return null
    return { id: actor.id, type: actor.actor_type.toLowerCase() as Actor['type'] }
}

function mapMatchResponse(match: GatewayMatchInfo): MatchResponse {
    return {
        game_series_id: match.game_series_id,
        team1: fromGatewayActor(match.team1),
        team2: fromGatewayActor(match.team2),
        winner: fromGatewayActor(match.winner),
        round: match.round,
        match_number: match.match_number,
        next_match_id: match.next_match_id ?? null,
        best_of: match.best_of ?? 1,
    }
}

function mapBracketResponse(bracket?: GatewayBracketInfo | null): BracketResponse | null {
    if (!bracket) return null
    const sourceRounds = bracket.rounds?.length
        ? bracket.rounds.map(round => round.map(mapMatchResponse))
        : null
    const sourceMatches = bracket.matches?.map(mapMatchResponse) ?? sourceRounds?.flat() ?? []
    const rounds = sourceRounds ?? sourceMatches.reduce<MatchResponse[][]>((acc, match) => {
        acc[match.round] = acc[match.round] ?? []
        acc[match.round].push(match)
        return acc
    }, [])
    rounds.forEach(round => round.sort((a, b) => a.match_number - b.match_number))
    return {
        rounds,
        matches: sourceMatches,
        round_settings: bracket.round_settings?.map(setting => ({
            round: setting.round,
            label: setting.label ?? null,
            best_of: setting.best_of,
        })) ?? [],
    }
}

function mapDraftState(state?: GatewayDraftState | null): DraftState | null {
    if (!state) return null
    return {
        config: {
            captain_count: state.config.captain_count,
            captains: (state.config.captains ?? []).map(captain => ({
                captain: fromGatewayActor(captain.captain) ?? { id: captain.captain.id, type: 'user' },
                order: captain.order,
                picked_players: (captain.picked_players ?? []).map(actor => fromGatewayActor(actor)).filter(Boolean) as Actor[],
            })),
            pick_order_captain_ids: state.config.pick_order_captain_ids ?? [],
            pick_direction: DRAFT_PICK_DIRECTION_FROM_GATEWAY[state.config.pick_direction ?? 'LINEAR'],
            max_extra_players_per_team: state.config.max_extra_players_per_team ?? 4,
        },
        current_pick_index: state.current_pick_index,
        current_captain_id: state.current_captain_id ?? null,
        available_player_ids: state.available_player_ids ?? [],
        finished: state.finished,
    }
}

function fromGatewayBracketMode(mode?: GatewayLolBracketMode): BracketType {
    switch (mode) {
        case 'DOUBLE_ELIM':
            return 'double_elimination'
        case 'SINGLE_ELIM_THIRD_PLACE':
            return 'single_elimination_with_third'
        case 'SWISS':
            return 'swiss'
        case 'ROUND_ROBIN':
            return 'round_robin'
        default:
            return 'single_elimination'
    }
}

function fromGatewayDraftMode(mode?: GatewayLolGameMode): DraftType {
    switch (mode) {
        case 'FEARLESS':
            return 'fearless'
        case 'IRON_MAN':
            return 'iron_man'
        case 'ALL_RANDOM':
            return 'all_random'
        default:
            return 'classic'
    }
}

function toGatewayTournamentSettings(settings: LolTournamentSettings): GatewayTournamentSettings {
    return {
        game_type: 'LOL',
        lol: {
            tournament_type: TOURNAMENT_TYPE_TO_GATEWAY[settings.tournament_type],
            bracket_mode: BRACKET_TO_GATEWAY[settings.bracket_type],
            draft_mode: [DRAFT_TO_GATEWAY[settings.game_series_settings.draft_type]],
            team_size: settings.game_settings.team_size,
            map: settings.game_settings.map,
            forbidden_champions: settings.game_series_settings.forbidden_champions,
            series_best_of: settings.best_of.length > 0 ? settings.best_of : [settings.game_series_settings.best_of ?? 1],
            draft_start: settings.draft_start ?? null,
        },
    }
}

function fromGatewayTournamentSettings(settings: GatewayTournamentSettings): LolTournamentSettings {
    const lol = settings.lol
    const teamSize = lol?.team_size ?? 5
    const map = lol?.map ?? 11
    const bestOf = lol?.series_best_of?.length ? lol.series_best_of : [1]
    const draftType = fromGatewayDraftMode(lol?.draft_mode?.[0])
    const gameSettings = { team_size: teamSize, map }

    return {
        tournament_type: lol?.tournament_type === 'DRAFT' || lol?.tournament_type === 'PICKEM' ? 'draft' : 'presigned',
        game_settings: gameSettings,
        game_series_settings: {
            game_settings: gameSettings,
            forbidden_champions: lol?.forbidden_champions ?? [],
            best_of: bestOf[0] ?? null,
            draft_type: draftType,
        },
        best_of: bestOf,
        bracket_type: fromGatewayBracketMode(lol?.bracket_mode),
        draft_start: lol?.draft_start ?? null,
    }
}

function mapTournamentResponse(tournament: GatewayTournamentResponse): TournamentResponse {
    return {
        id: tournament.id,
        host: fromGatewayActor(tournament.host) ?? { id: tournament.host.id, type: 'user' },
        participant_pool: (tournament.participants ?? []).map(participant => ({
            actor: fromGatewayActor(participant),
            players: [],
        })),
        prizepool: tournament.prizepool ?? 'No prize pool',
        is_open: tournament.is_open ?? false,
        wait_list: [],
        status: STATUS_FROM_GATEWAY[tournament.status ?? 'STATUS_UNSPECIFIED'],
        settings: fromGatewayTournamentSettings(tournament.settings),
        start: tournament.start,
        end: tournament.end ?? null,
        lifecycle: LIFECYCLE_FROM_GATEWAY[tournament.lifecycle ?? 'TOURNAMENT_LIFECYCLE_UNSPECIFIED'],
        draft_start: tournament.draft_start ?? tournament.settings.lol?.draft_start ?? null,
        registration_locked_at: tournament.registration_locked_at ?? null,
        draft_state: mapDraftState(tournament.draft_state),
        bracket: mapBracketResponse(tournament.bracket),
    }
}

function toGatewayCreateTournamentRequest(data: CreateTournamentRequest) {
    return {
        host: toGatewayActor(data.host),
        settings: toGatewayTournamentSettings(data.settings),
        start: data.start,
        prizepool: data.prizepool,
        is_open: data.is_open,
        draft_start: data.draft_start ?? data.settings.draft_start ?? null,
        name: data.name,
        description: data.description,
        avatar: data.avatar,
    }
}

// Tournament API
export async function getTournaments(options: ListTournamentsOptions = {}) {
    try {
        const res = await gatewayApi.get<GatewayListTournamentsResponse>('/v1/tournaments/search', { params: options })
        return res.data.tournaments.map(mapTournamentResponse)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getTournament(id: string) {
    try {
        const res = await gatewayApi.get<GatewayManyTournamentsResponse>(`/v1/tournaments/${id}`)
        const tournament = res.data.tournaments[0]
        return tournament ? mapTournamentResponse(tournament) : null
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function createTournament(data: CreateTournamentRequest) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>('/v1/tournaments', toGatewayCreateTournamentRequest(data))
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function updateTournament(
    tournamentId: string,
    data: { actor_id: string; start?: number; draft_start?: number | null; prizepool?: string; is_open?: boolean; status?: GatewayStatus; name?: string; description?: string },
) {
    try {
        const res = await gatewayApi.patch<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}`, {
            tournament_id: tournamentId,
            ...data,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function deleteTournament(tournamentId: string, actorId: string) {
    try {
        await gatewayApi.delete(`/v1/tournaments/${tournamentId}`, { params: { actor_id: actorId } })
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function startTournament(tournamentId: string, actorId?: string) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/start`, null, { params: { actor_id: actorId } })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function lockTournamentRegistration(tournamentId: string, actorId: string) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/lock-registration`, {
            tournament_id: tournamentId,
            actor_id: actorId,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function rescheduleTournament(tournamentId: string, actorId: string, start: number, draftStart?: number | null) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/reschedule`, {
            tournament_id: tournamentId,
            actor_id: actorId,
            start,
            draft_start: draftStart ?? null,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function prebuildTournamentBracket(tournamentId: string, actorId?: string, roundSettings: BracketRoundSettings[] = []) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/prebuild-bracket`, {
            tournament_id: tournamentId,
            actor_id: actorId,
            round_settings: roundSettings,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function setDraftCaptains(
    tournamentId: string,
    actorId: string,
    captainIds: string[],
    pickDirection: DraftPickDirection = 'snake',
    maxExtraPlayersPerTeam = 4,
) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/draft/captains`, {
            tournament_id: tournamentId,
            actor_id: actorId,
            captain_count: captainIds.length,
            captain_ids: captainIds,
            pick_direction: DRAFT_PICK_DIRECTION_TO_GATEWAY[pickDirection],
            max_extra_players_per_team: maxExtraPlayersPerTeam,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function updateDraftPickOrder(tournamentId: string, actorId: string, captainIds: string[]) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/draft/pick-order`, {
            tournament_id: tournamentId,
            actor_id: actorId,
            captain_ids: captainIds,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function draftPickPlayer(tournamentId: string, actorId: string, captainId: string, playerId: string) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/draft/picks`, {
            tournament_id: tournamentId,
            actor_id: actorId,
            captain_id: captainId,
            player_id: playerId,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function updateBracketMatch(
    tournamentId: string,
    gameSeriesId: string,
    data: { actor_id: string; team1?: Actor | null; team2?: Actor | null; best_of?: number | null },
) {
    try {
        const res = await gatewayApi.patch<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/bracket/matches/${gameSeriesId}`, {
            tournament_id: tournamentId,
            game_series_id: gameSeriesId,
            actor_id: data.actor_id,
            team1: data.team1 ? toGatewayActor(data.team1) : null,
            team2: data.team2 ? toGatewayActor(data.team2) : null,
            best_of: data.best_of ?? null,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function finishTournament(tournamentId: string, actorId?: string, winnerId?: string) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/finish`, null, { params: { actor_id: actorId, winner_id: winnerId } })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function addTournamentParticipant(tournamentId: string, participant: Actor, teamName?: string) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/participants`, {
            tournament_id: tournamentId,
            participant: toGatewayActor(participant),
            team_name: teamName,
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function removeTournamentParticipant(tournamentId: string, participantId: string, actorId?: string) {
    try {
        const res = await gatewayApi.delete<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/participants/${participantId}`, {
            params: { actor_id: actorId },
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export function encodeDraftRoles(primaryRole: TournamentRole, secondaryRole: TournamentRole) {
    return `draft_roles:${primaryRole}:${secondaryRole}`
}

export async function addTournamentWaitlistParticipant(tournamentId: string, participant: Actor) {
    try {
        const res = await gatewayApi.post<GatewayTournamentResponse>(`/v1/tournaments/${tournamentId}/waitlist`, {
            tournament_id: tournamentId,
            participant: toGatewayActor(participant),
        })
        return mapTournamentResponse(res.data)
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getTournamentParticipants(tournamentId: string, page = 1, pageSize = 50) {
    try {
        const res = await gatewayApi.get<GatewayParticipantsResponse>(`/v1/tournaments/${tournamentId}/participants`, { params: { page, page_size: pageSize } })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getTournamentWaitlist(tournamentId: string, page = 1, pageSize = 50) {
    try {
        const res = await gatewayApi.get<GatewayWaitlistResponse>(`/v1/tournaments/${tournamentId}/waitlist`, { params: { page, page_size: pageSize } })
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getTournamentBracket(tournamentId: string) {
    try {
        const res = await gatewayApi.get<GatewayBracketResponse>(`/v1/tournaments/${tournamentId}/bracket`)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getTournamentStats(tournamentId: string) {
    try {
        const res = await gatewayApi.get<GatewayTournamentStats>(`/v1/tournaments/${tournamentId}/stats`)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function isTournamentParticipant(tournamentId: string, participantId: string) {
    try {
        const res = await gatewayApi.get<GatewayIsParticipantResponse>(`/v1/tournaments/${tournamentId}/participants/${participantId}`)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

// Tournament hooks
export function useTournaments() {
    return useQuery({
        queryKey: ['tournaments'],
        queryFn: () => getTournaments(),
        staleTime: 30000,
    })
}

export function useTournament(id: string) {
    return useQuery({
        queryKey: ['tournaments', id],
        queryFn: () => getTournament(id),
        enabled: !!id,
        staleTime: 30000,
    })
}

export function useCreateTournamentMutation() {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: createTournament,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tournaments'] })
        },
    })
}

export function useAddTournamentParticipantMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ participant, teamName }: { participant: Actor; teamName?: string }) => addTournamentParticipant(tournamentId, participant, teamName),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tournaments'] })
            queryClient.invalidateQueries({ queryKey: ['tournaments', tournamentId] })
            queryClient.invalidateQueries({ queryKey: ['tournaments', tournamentId, 'participants-info'] })
        },
    })
}

function invalidateTournamentQueries(queryClient: ReturnType<typeof useQueryClient>, tournamentId: string) {
    queryClient.invalidateQueries({ queryKey: ['tournaments'] })
    queryClient.invalidateQueries({ queryKey: ['tournaments', tournamentId] })
    queryClient.invalidateQueries({ queryKey: ['tournaments', tournamentId, 'participants-info'] })
}

export function useStartTournamentMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: (actorId?: string) => startTournament(tournamentId, actorId),
        onSuccess: () => {
            invalidateTournamentQueries(queryClient, tournamentId)
        },
    })
}

export function usePrebuildTournamentBracketMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ actorId, roundSettings }: { actorId?: string; roundSettings?: BracketRoundSettings[] }) =>
            prebuildTournamentBracket(tournamentId, actorId, roundSettings),
        onSuccess: () => {
            invalidateTournamentQueries(queryClient, tournamentId)
        },
    })
}

export function useLockTournamentRegistrationMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: (actorId: string) => lockTournamentRegistration(tournamentId, actorId),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export function useRescheduleTournamentMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ actorId, start, draftStart }: { actorId: string; start: number; draftStart?: number | null }) =>
            rescheduleTournament(tournamentId, actorId, start, draftStart),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export function useSetDraftCaptainsMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ actorId, captainIds, pickDirection, maxExtraPlayersPerTeam }: { actorId: string; captainIds: string[]; pickDirection?: DraftPickDirection; maxExtraPlayersPerTeam?: number }) =>
            setDraftCaptains(tournamentId, actorId, captainIds, pickDirection, maxExtraPlayersPerTeam),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export function useUpdateDraftPickOrderMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ actorId, captainIds }: { actorId: string; captainIds: string[] }) =>
            updateDraftPickOrder(tournamentId, actorId, captainIds),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export function useDraftPickPlayerMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ actorId, captainId, playerId }: { actorId: string; captainId: string; playerId: string }) =>
            draftPickPlayer(tournamentId, actorId, captainId, playerId),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export function useRemoveTournamentParticipantMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ participantId, actorId }: { participantId: string; actorId?: string }) =>
            removeTournamentParticipant(tournamentId, participantId, actorId),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export function useUpdateBracketMatchMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ gameSeriesId, data }: { gameSeriesId: string; data: { actor_id: string; team1?: Actor | null; team2?: Actor | null; best_of?: number | null } }) =>
            updateBracketMatch(tournamentId, gameSeriesId, data),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export function useFinishTournamentMutation(tournamentId: string) {
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({ actorId, winnerId }: { actorId: string; winnerId?: string }) =>
            finishTournament(tournamentId, actorId, winnerId),
        onSuccess: () => invalidateTournamentQueries(queryClient, tournamentId),
    })
}

export async function setGameWinner(
    seriesId: string,
    gameId: string,
    actorId: string,
    winner: Actor,
) {
    try {
        await gatewayApi.post(`/v1/game-series/${seriesId}/games/${gameId}/winner`, {
            series_id: seriesId,
            game_id: gameId,
            actor_id: actorId,
            winner: toGatewayActor(winner),
        })
    } catch (error) {
        handleAxiosError(error)
    }
}

export function useSetGameWinnerMutation(tournamentId: string) {
    // Server propagates the winner through the bracket and may auto-finish the
    // tournament, so we invalidate the whole tournament tree on success.
    const queryClient = useQueryClient()
    return useMutation({
        mutationFn: ({
            seriesId,
            gameId,
            actorId,
            winner,
        }: {
            seriesId: string
            gameId: string
            actorId: string
            winner: Actor
        }) => setGameWinner(seriesId, gameId, actorId, winner),
        onSuccess: (_data, vars) => {
            invalidateTournamentQueries(queryClient, tournamentId)
            queryClient.invalidateQueries({ queryKey: ['gameseries', vars.seriesId] })
        },
    })
}

// GameSeries / Game / Draft types
export type GameStatus = 'scheduled' | 'side_chosen' | 'active' | 'finished' | 'canceled'

export interface DraftTeam {
    type: 'red' | 'blue'
    id: string
}

export interface DraftAction {
    type: 'pick' | 'ban'
    champion_id: number
}

export interface DraftCommand {
    team: DraftTeam
    action: DraftAction
}

export interface DraftResponse {
    history: DraftCommand[]
    deadline: number
    game_id: string
    teams: DraftTeam[]
    forbidden_champions: number[]
    stage: number
    team_size: number
    seconds_per_action: number
}

export interface GameResponse {
    id: string
    game_series_id: string
    teams: TeamParticipant[]
    results: TeamParticipant[]
    start: number
    end: number | null
    status: GameStatus
    settings: LolGameSettings
    draft: DraftResponse | null
}

export interface GameSeriesDetailResponse {
    id: string
    tournament_id: string
    teams: TeamParticipant[]
    start: number | null
    end: number | null
    status: GameSeriesStatus
    settings: LolGameSeriesSettings
    games: GameResponse[]
}

// Mock champion names for display
export const CHAMPION_NAMES: Record<number, string> = {
    1: 'Aatrox', 2: 'Ahri', 3: 'Akali', 4: 'Alistar', 5: 'Amumu',
    6: 'Anivia', 7: 'Annie', 8: 'Ashe', 9: 'Azir', 10: 'Bard',
    11: 'Blitzcrank', 12: 'Brand', 13: 'Braum', 14: 'Caitlyn', 15: 'Camille',
    16: 'Darius', 17: 'Diana', 18: 'Draven', 19: 'Ekko', 20: 'Elise',
    21: 'Ezreal', 22: 'Fiora', 23: 'Garen', 24: 'Gnar', 25: 'Graves',
    26: 'Irelia', 27: 'Jax', 28: 'Jayce', 29: 'Jinx', 30: 'Kaisa',
    31: 'Karma', 32: 'Katarina', 33: 'Kayn', 34: 'Kennen', 35: 'Khazix',
    36: 'Lee Sin', 37: 'Leona', 38: 'Lulu', 39: 'Lux', 40: 'Nautilus',
    41: 'Nidalee', 42: 'Orianna', 43: 'Pantheon', 44: 'Pyke', 45: 'Rakan',
    46: 'Renekton', 47: 'Riven', 48: 'Rumble', 49: 'Sejuani', 50: 'Senna',
    51: 'Thresh', 52: 'Tristana', 53: 'Varus', 54: 'Vayne', 55: 'Viktor',
    56: 'Xayah', 57: 'Yasuo', 58: 'Yone', 59: 'Zed', 60: 'Zeri',
}

// Real game-series fetch. The gateway endpoint `GET /v1/game-series/{id}` is
// not yet wired (only write-side endpoints exist today), so this will 404
// until the backend lands. Callers should degrade gracefully on error rather
// than render stale stub payloads.
export async function getGameSeries(id: string): Promise<GameSeriesDetailResponse | null> {
    try {
        const res = await gatewayApi.get<GameSeriesDetailResponse>(`/v1/game-series/${id}`)
        return res.data
    } catch (error) {
        handleAxiosError(error)
        return null
    }
}

export function useGameSeries(id: string) {
    return useQuery({
        queryKey: ['gameseries', id],
        queryFn: () => getGameSeries(id),
        enabled: !!id,
        staleTime: 30000,
    })
}

// Presence
export interface PresenceCheckResponse {
    online: Record<string, boolean>
}

export async function checkPresence(userIds: string[]): Promise<Record<string, boolean>> {
    if (userIds.length === 0) return {}
    try {
        const res = await gatewayApi.post<PresenceCheckResponse>("/v1/presence/check", { user_ids: userIds })
        return res.data.online ?? {}
    } catch (error) {
        handleAxiosError(error)
    }
}

export function usePresence(userIds: string[], intervalMs = 15000) {
    // Sort keeps the query key stable even if friend order shifts between renders.
    const stableIds = [...userIds].sort()
    return useQuery({
        queryKey: ["presence", stableIds],
        queryFn: () => checkPresence(stableIds),
        enabled: stableIds.length > 0,
        refetchInterval: intervalMs,
        refetchIntervalInBackground: false,
        staleTime: intervalMs / 2,
    })
}

