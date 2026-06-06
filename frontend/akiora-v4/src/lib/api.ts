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
}

export interface GetUserChatsResponse {
    chats: ChatResponse[]
}

export interface SendMessageRequest {
    chat_id: string
    creator_id: string
    body: string
    reply_to?: string
    spoiler?: boolean
}

// Dummy data for development
const DUMMY_CHATS: ChatResponse[] = [
    {
        id: 'chat-1',
        owner_id: 'club-1',
        owner_type: 'CLUB',
        type: 'PUBLIC',
        status: 'ACTIVE',
        timestamp: Math.floor(Date.now() / 1000) - 3600,
        allowed_users: [],
    },
    {
        id: 'chat-2',
        owner_id: 'tournament-1',
        owner_type: 'TOURNAMENT',
        type: 'PUBLIC',
        status: 'ACTIVE',
        timestamp: Math.floor(Date.now() / 1000) - 7200,
        allowed_users: [],
    },
]

const DUMMY_MESSAGES: Record<string, MessageResponse[]> = {
    'chat-1': [
        {
            id: 'msg-1',
            chat_id: 'chat-1',
            creator_id: 'user-2',
            body: 'Hey everyone! Ready for the tournament?',
            status: 'READ',
            read_by: [],
            timestamp: Math.floor(Date.now() / 1000) - 3600,
            history: [],
            reply_to: null,
            reactions: [],
            spoiler: false,
        },
        {
            id: 'msg-2',
            chat_id: 'chat-1',
            creator_id: 'user-3',
            body: 'Absolutely! Been practicing all week',
            status: 'READ',
            read_by: [],
            timestamp: Math.floor(Date.now() / 1000) - 3500,
            history: [],
            reply_to: null,
            reactions: [],
            spoiler: false,
        },
        {
            id: 'msg-3',
            chat_id: 'chat-1',
            creator_id: 'user-2',
            body: 'Nice! Who are you maining this season?',
            status: 'READ',
            read_by: [],
            timestamp: Math.floor(Date.now() / 1000) - 3400,
            history: [],
            reply_to: null,
            reactions: [],
            spoiler: false,
        },
        {
            id: 'msg-4',
            chat_id: 'chat-1',
            creator_id: 'user-3',
            body: 'Jinx and Kaisa mainly. You?',
            status: 'READ',
            read_by: [],
            timestamp: Math.floor(Date.now() / 1000) - 3300,
            history: [],
            reply_to: null,
            reactions: [],
            spoiler: false,
        },
    ],
    'chat-2': [
        {
            id: 'msg-5',
            chat_id: 'chat-2',
            creator_id: 'user-4',
            body: 'Tournament starts in 2 hours!',
            status: 'READ',
            read_by: [],
            timestamp: Math.floor(Date.now() / 1000) - 7200,
            history: [],
            reply_to: null,
            reactions: [],
            spoiler: false,
        },
        {
            id: 'msg-6',
            chat_id: 'chat-2',
            creator_id: 'user-5',
            body: 'Good luck everyone! 🍀',
            status: 'READ',
            read_by: [],
            timestamp: Math.floor(Date.now() / 1000) - 7100,
            history: [],
            reply_to: null,
            reactions: [],
            spoiler: false,
        },
    ],
}

// Messenger API
export async function getUserChats(_userId: string) {
    // Return dummy data for development
    return DUMMY_CHATS
}

export async function getChat(chatId: string) {
    try {
        const res = await gatewayApi.get<ChatResponse>(`/v1/chats/${chatId}`)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

export async function getMessages(chatId: string, _limit = 50, _beforeTimestamp?: number) {
    // Return dummy data for development
    return DUMMY_MESSAGES[chatId] || []
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
        },
    })
}

// Tournament types
export type TournamentStatus = 'scheduled' | 'active' | 'finished' | 'canceled'
export type BracketType = 'single_elimination' | 'single_elimination_with_third' | 'double_elimination' | 'swiss' | 'round_robin'
export type DraftType = 'fearless' | 'iron_man' | 'classic' | 'all_random'
export type GameSeriesStatus = 'scheduled' | 'active' | 'finished' | 'canceled'

export interface Actor {
    id: string
    type: 'user' | 'team' | 'club'
}

export interface TeamParticipant {
    actor: Actor | null
    players: string[]
}

export interface MatchResponse {
    game_series_id: string
    team1: Actor | null
    team2: Actor | null
    winner: Actor | null
    round: number
    match_number: number
    next_match_id: number | null
}

export interface BracketResponse {
    rounds: MatchResponse[][]
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
    game_settings: LolGameSettings
    game_series_settings: LolGameSeriesSettings
    best_of: number[]
    bracket_type: BracketType
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
    bracket: BracketResponse | null
}

export interface CreateTournamentRequest {
    start: number
    is_open: boolean
    prizepool: string
    settings: LolTournamentSettings
}

// Dummy tournament data
const DUMMY_TOURNAMENTS: TournamentResponse[] = [
    {
        id: 'tournament-1',
        host: { id: 'user-1', type: 'user' },
        participant_pool: [
            { actor: { id: 'team-1', type: 'team' }, players: ['p1', 'p2', 'p3', 'p4', 'p5'] },
            { actor: { id: 'team-2', type: 'team' }, players: ['p6', 'p7', 'p8', 'p9', 'p10'] },
            { actor: { id: 'team-3', type: 'team' }, players: ['p11', 'p12', 'p13', 'p14', 'p15'] },
            { actor: { id: 'team-4', type: 'team' }, players: ['p16', 'p17', 'p18', 'p19', 'p20'] },
        ],
        prizepool: '500 RP',
        is_open: true,
        wait_list: [],
        status: 'active',
        settings: {
            game_settings: { team_size: 5, map: 11 },
            game_series_settings: { game_settings: { team_size: 5, map: 11 }, forbidden_champions: [], best_of: 3, draft_type: 'classic' },
            best_of: [5, 3, 3],
            bracket_type: 'single_elimination',
        },
        start: Math.floor(Date.now() / 1000) - 3600,
        end: null,
        bracket: {
            rounds: [
                [
                    { game_series_id: 'gs-1', team1: { id: 'team-1', type: 'team' }, team2: { id: 'team-2', type: 'team' }, winner: { id: 'team-1', type: 'team' }, round: 0, match_number: 0, next_match_id: 0 },
                    { game_series_id: 'gs-2', team1: { id: 'team-3', type: 'team' }, team2: { id: 'team-4', type: 'team' }, winner: null, round: 0, match_number: 1, next_match_id: 0 },
                ],
                [
                    { game_series_id: 'gs-3', team1: { id: 'team-1', type: 'team' }, team2: null, winner: null, round: 1, match_number: 0, next_match_id: null },
                ],
            ],
        },
    },
    {
        id: 'tournament-2',
        host: { id: 'club-1', type: 'club' },
        participant_pool: [],
        prizepool: '1000 RP + Skin',
        is_open: true,
        wait_list: [],
        status: 'scheduled',
        settings: {
            game_settings: { team_size: 5, map: 11 },
            game_series_settings: { game_settings: { team_size: 5, map: 11 }, forbidden_champions: [], best_of: 1, draft_type: 'fearless' },
            best_of: [3, 1],
            bracket_type: 'double_elimination',
        },
        start: Math.floor(Date.now() / 1000) + 86400,
        end: null,
        bracket: null,
    },
    {
        id: 'tournament-3',
        host: { id: 'user-2', type: 'user' },
        participant_pool: [
            { actor: { id: 'team-5', type: 'team' }, players: ['p21', 'p22', 'p23', 'p24', 'p25'] },
            { actor: { id: 'team-6', type: 'team' }, players: ['p26', 'p27', 'p28', 'p29', 'p30'] },
        ],
        prizepool: 'Glory',
        is_open: false,
        wait_list: [],
        status: 'finished',
        settings: {
            game_settings: { team_size: 5, map: 11 },
            game_series_settings: { game_settings: { team_size: 5, map: 11 }, forbidden_champions: [], best_of: 3, draft_type: 'classic' },
            best_of: [3],
            bracket_type: 'single_elimination',
        },
        start: Math.floor(Date.now() / 1000) - 172800,
        end: Math.floor(Date.now() / 1000) - 86400,
        bracket: {
            rounds: [
                [
                    { game_series_id: 'gs-4', team1: { id: 'team-5', type: 'team' }, team2: { id: 'team-6', type: 'team' }, winner: { id: 'team-5', type: 'team' }, round: 0, match_number: 0, next_match_id: null },
                ],
            ],
        },
    },
]

// Tournament API
export async function getTournaments() {
    return DUMMY_TOURNAMENTS
}

export async function getTournament(id: string) {
    return DUMMY_TOURNAMENTS.find(t => t.id === id) || null
}

export async function createTournament(data: CreateTournamentRequest) {
    try {
        const res = await gatewayApi.post<TournamentResponse>('/v1/tournaments', data)
        return res.data
    } catch (error) {
        handleAxiosError(error)
    }
}

// Tournament hooks
export function useTournaments() {
    return useQuery({
        queryKey: ['tournaments'],
        queryFn: getTournaments,
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

// Dummy game series data
function generateMockGameSeries(gsId: string): GameSeriesDetailResponse {
    const blueTeam: DraftTeam = { type: 'blue', id: 'team-1' }
    const redTeam: DraftTeam = { type: 'red', id: 'team-2' }

    const makeDraft = (gameId: string, seed: number): DraftResponse => {
        const history: DraftCommand[] = []
        const stages = [
            { team: blueTeam, action: { type: 'ban' as const, champion_id: 1 + seed } },
            { team: redTeam, action: { type: 'ban' as const, champion_id: 3 + seed } },
            { team: blueTeam, action: { type: 'ban' as const, champion_id: 57 } },
            { team: redTeam, action: { type: 'ban' as const, champion_id: 59 } },
            { team: blueTeam, action: { type: 'ban' as const, champion_id: 35 } },
            { team: redTeam, action: { type: 'ban' as const, champion_id: 33 } },
            { team: blueTeam, action: { type: 'pick' as const, champion_id: 26 + seed } },
            { team: redTeam, action: { type: 'pick' as const, champion_id: 16 } },
            { team: redTeam, action: { type: 'pick' as const, champion_id: 36 } },
            { team: blueTeam, action: { type: 'pick' as const, champion_id: 21 } },
            { team: blueTeam, action: { type: 'pick' as const, champion_id: 51 } },
            { team: redTeam, action: { type: 'pick' as const, champion_id: 29 } },
            { team: redTeam, action: { type: 'ban' as const, champion_id: 42 } },
            { team: blueTeam, action: { type: 'ban' as const, champion_id: 30 } },
            { team: redTeam, action: { type: 'ban' as const, champion_id: 22 } },
            { team: blueTeam, action: { type: 'ban' as const, champion_id: 54 } },
            { team: redTeam, action: { type: 'pick' as const, champion_id: 8 + seed } },
            { team: blueTeam, action: { type: 'pick' as const, champion_id: 14 } },
            { team: blueTeam, action: { type: 'pick' as const, champion_id: 37 } },
            { team: redTeam, action: { type: 'pick' as const, champion_id: 46 } },
        ]
        for (const s of stages) history.push(s)
        return { history, deadline: 0, game_id: gameId, teams: [blueTeam, redTeam], forbidden_champions: [], stage: 20, team_size: 5, seconds_per_action: 30 }
    }

    const games: GameResponse[] = [
        {
            id: `${gsId}-g1`, game_series_id: gsId,
            teams: [{ actor: { id: 'team-1', type: 'team' }, players: [] }, { actor: { id: 'team-2', type: 'team' }, players: [] }],
            results: [{ actor: { id: 'team-1', type: 'team' }, players: [] }],
            start: Math.floor(Date.now() / 1000) - 5400, end: Math.floor(Date.now() / 1000) - 3600,
            status: 'finished', settings: { team_size: 5, map: 11 }, draft: makeDraft(`${gsId}-g1`, 0),
        },
        {
            id: `${gsId}-g2`, game_series_id: gsId,
            teams: [{ actor: { id: 'team-1', type: 'team' }, players: [] }, { actor: { id: 'team-2', type: 'team' }, players: [] }],
            results: [{ actor: { id: 'team-2', type: 'team' }, players: [] }],
            start: Math.floor(Date.now() / 1000) - 3500, end: Math.floor(Date.now() / 1000) - 1800,
            status: 'finished', settings: { team_size: 5, map: 11 }, draft: makeDraft(`${gsId}-g2`, 5),
        },
        {
            id: `${gsId}-g3`, game_series_id: gsId,
            teams: [{ actor: { id: 'team-1', type: 'team' }, players: [] }, { actor: { id: 'team-2', type: 'team' }, players: [] }],
            results: [{ actor: { id: 'team-1', type: 'team' }, players: [] }],
            start: Math.floor(Date.now() / 1000) - 1700, end: Math.floor(Date.now() / 1000) - 300,
            status: 'finished', settings: { team_size: 5, map: 11 }, draft: makeDraft(`${gsId}-g3`, 10),
        },
    ]

    return {
        id: gsId, tournament_id: 'tournament-1',
        teams: [{ actor: { id: 'team-1', type: 'team' }, players: [] }, { actor: { id: 'team-2', type: 'team' }, players: [] }],
        start: Math.floor(Date.now() / 1000) - 5400, end: Math.floor(Date.now() / 1000) - 300,
        status: 'finished',
        settings: { game_settings: { team_size: 5, map: 11 }, forbidden_champions: [], best_of: 3, draft_type: 'classic' },
        games,
    }
}

export async function getGameSeries(id: string) {
    return generateMockGameSeries(id)
}

export function useGameSeries(id: string) {
    return useQuery({
        queryKey: ['gameseries', id],
        queryFn: () => getGameSeries(id),
        enabled: !!id,
        staleTime: 30000,
    })
}
