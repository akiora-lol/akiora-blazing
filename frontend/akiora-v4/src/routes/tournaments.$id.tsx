import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useQuery } from '@tanstack/react-query'
import { Fragment, useEffect, useState, useRef } from 'react'
import { createPortal } from 'react-dom'
import { FiArrowLeft, FiUsers, FiClock, FiAward, FiMaximize2, FiX, FiLock, FiTrash2 } from 'react-icons/fi'
import { useAuthContext } from '../contexts/AuthContext'
import {
    getUser,
    getTournamentParticipants,
    encodeDraftRoles,
    type MatchResponse,
    type Actor,
    type AuthUser,
    type GatewayParticipantInfo,
    type TournamentRole,
    type TournamentResponse,
    useAddTournamentParticipantMutation,
    useDraftPickPlayerMutation,
    useLockTournamentRegistrationMutation,
    usePrebuildTournamentBracketMutation,
    useRemoveTournamentParticipantMutation,
    useRescheduleTournamentMutation,
    useSetDraftCaptainsMutation,
    useStartTournamentMutation,
    useTeams,
    useTournament,
    useUpdateDraftPickOrderMutation,
} from '../lib/api'

export const Route = createFileRoute('/tournaments/$id')({ component: TournamentDetailPage })

const STATUS_COLORS: Record<string, string> = {
    scheduled: '#06B6D4', active: '#10B981', finished: 'rgba(255,255,255,0.3)', canceled: '#FF002A',
}

const TEAM_NAMES: Record<string, string> = {
    'team-1': 'Shadow Wolves', 'team-2': 'Neon Dragons', 'team-3': 'Ice Phoenix', 'team-4': 'Dark Reapers',
    'team-5': 'Storm Riders', 'team-6': 'Cyber Hawks', 'team-7': 'Blood Ravens', 'team-8': 'Iron Titans',
    'team-9': 'Void Walkers', 'team-10': 'Frost Giants', 'team-11': 'Solar Flares', 'team-12': 'Lunar Wolves',
    'team-13': 'Thunder Cats', 'team-14': 'Venom Squad', 'team-15': 'Ghost Legion', 'team-16': 'Apex Hunters',
    'team-17': 'Crimson Tide', 'team-18': 'Arctic Fox', 'team-19': 'Blaze United', 'team-20': 'Phantom Force',
    'team-21': 'Omega Rising', 'team-22': 'Nova Burst', 'team-23': 'Dark Matter', 'team-24': 'Star Forge',
    'team-25': 'Viper Strike', 'team-26': 'Chaos Engine', 'team-27': 'Iron Clad', 'team-28': 'Feral Instinct',
    'team-29': 'Pulse Gaming', 'team-30': 'Eclipse eSports', 'team-31': 'Zenith Pro', 'team-32': 'Aether Knights',
    'team-33': 'Rogue Element', 'team-34': 'Prism Effect', 'team-35': 'Nemesis GG', 'team-36': 'Core Breach',
    'team-37': 'Havoc Squad', 'team-38': 'Velocity X', 'team-39': 'Silent Storm', 'team-40': 'Nexus Gaming',
    'team-41': 'Warp Drive', 'team-42': 'Cyber Pulse', 'team-43': 'Titan Fall', 'team-44': 'Genesis Pro',
    'team-45': 'Obsidian', 'team-46': 'Radiant', 'team-47': 'Rift Walkers', 'team-48': 'Summit GG',
    'team-49': 'Cataclysm', 'team-50': 'Fury Esports', 'team-51': 'Sentinel', 'team-52': 'Dominion',
    'team-53': 'Paradigm', 'team-54': 'Mirage Gaming', 'team-55': 'Orion Stars', 'team-56': 'Delta Force',
    'team-57': 'Raven Squad', 'team-58': 'Inferno GG', 'team-59': 'Quantum Leap', 'team-60': 'Aftermath',
    'team-61': 'Phoenix Rise', 'team-62': 'Kraken Esports', 'team-63': 'Eternal Fire', 'team-64': 'Last Stand',
}

function getTeamLabel(actor: Actor | null) {
    if (!actor) return 'TBD'
    return TEAM_NAMES[actor.id] || `${actor.type} ${actor.id.slice(-4)}`
}

const RANK_SCORE: Record<string, number> = {
    IRON: 100,
    BRONZE: 200,
    SILVER: 300,
    GOLD: 400,
    PLATINUM: 500,
    EMERALD: 600,
    DIAMOND: 700,
    MASTER: 800,
    GRANDMASTER: 900,
    CHALLENGER: 1000,
}

const ROLE_LABELS: Record<TournamentRole, string> = {
    top: 'Top',
    jungle: 'Jungle',
    mid: 'Mid',
    adc: 'ADC',
    support: 'Support',
}

const ROLE_ORDER: TournamentRole[] = ['top', 'jungle', 'mid', 'adc', 'support']
const RANK_ROWS = ['CHALLENGER', 'GRANDMASTER', 'MASTER', 'DIAMOND', 'EMERALD', 'PLATINUM', 'GOLD', 'SILVER', 'BRONZE', 'IRON'] as const

function getPrimaryLeagueAccount(user?: AuthUser | null) {
    return user?.league_accounts?.find(account => account.status === 'done') ?? user?.league_accounts?.[0] ?? null
}

function getRankScore(user?: AuthUser | null) {
    const account = getPrimaryLeagueAccount(user)
    if (!account?.solo_tier) return 0
    const tier = account.solo_tier.toUpperCase()
    const divisionOffset = account.solo_division ? 5 - account.solo_division : 0
    return (RANK_SCORE[tier] ?? 0) + divisionOffset * 20 + (account.solo_lp ?? 0)
}

function formatRank(user?: AuthUser | null) {
    const account = getPrimaryLeagueAccount(user)
    if (!account?.solo_tier) return 'Unranked'
    const division = account.solo_division ? ` ${account.solo_division}` : ''
    const lp = typeof account.solo_lp === 'number' ? ` ${account.solo_lp} LP` : ''
    return `${account.solo_tier}${division}${lp}`
}

function getRankRow(user?: AuthUser | null) {
    const tier = getPrimaryLeagueAccount(user)?.solo_tier?.toUpperCase()
    return RANK_ROWS.find(rank => rank === tier) ?? 'IRON'
}

function getStoredDraftRoles(tournamentId: string, userId: string): TournamentRole[] {
    if (typeof window === 'undefined') return []
    const raw = window.localStorage.getItem(`tournament:${tournamentId}:draftRoles:${userId}`)
    const roles = raw?.split(':').filter(role => ROLE_ORDER.includes(role as TournamentRole)) as TournamentRole[] | undefined
    return roles?.slice(0, 2) ?? []
}

function storeDraftRoles(tournamentId: string, userId: string, roles: TournamentRole[]) {
    if (typeof window === 'undefined') return
    window.localStorage.setItem(`tournament:${tournamentId}:draftRoles:${userId}`, roles.join(':'))
}

function useTournamentUsers(tournament?: TournamentResponse | null) {
    const ids = (tournament?.participant_pool ?? [])
        .map(participant => participant.actor)
        .filter((actor): actor is Actor => !!actor && actor.type === 'user')
        .map(actor => actor.id)

    return useQuery({
        queryKey: ['tournaments', tournament?.id, 'participant-users', ids],
        queryFn: async () => {
            const users = await Promise.all(ids.map(id => getUser(id)))
            return users.filter(Boolean) as AuthUser[]
        },
        enabled: ids.length > 0,
        staleTime: 30000,
    })
}

function useTournamentParticipantInfo(tournamentId: string) {
    return useQuery({
        queryKey: ['tournaments', tournamentId, 'participants-info'],
        queryFn: () => getTournamentParticipants(tournamentId, 1, 100),
        enabled: !!tournamentId,
        staleTime: 15000,
    })
}

const ROUND_NAMES = ['Round of 32', 'Round of 16', 'Quarter-Finals', 'Semi-Finals', 'Winners Semi', 'Grand Final']

// Match card dimensions for SVG line calculations
const MATCH_WIDTH = 180
const MATCH_HEIGHT = 56
const ROUND_GAP = 36
const MATCH_GAP = 8
const ROUND_HEADER = 24

function BracketView({ tournament, fullscreen = false }: { tournament: TournamentResponse; fullscreen?: boolean }) {
    const bracket = tournament.bracket
    const containerRef = useRef<HTMLDivElement>(null)

    if (!bracket) return <p style={{ color: 'rgba(255,255,255,0.2)', fontFamily: "'Chakra Petch', monospace", fontSize: '13px', textAlign: 'center', padding: '40px' }}>Bracket not generated yet</p>

    const roundStep = MATCH_WIDTH + ROUND_GAP

    // Pre-compute Y position of each match center, recursively from round 0
    // Round 0: stacked sequentially. Each subsequent round: midpoint of the two feeder matches.
    const matchPositions: number[][] = [] // matchPositions[roundIdx][matchIdx] = centerY

    // Round 0
    const r0: number[] = []
    for (let i = 0; i < bracket.rounds[0].length; i++) {
        r0.push(ROUND_HEADER + i * (MATCH_HEIGHT + MATCH_GAP) + MATCH_HEIGHT / 2)
    }
    matchPositions.push(r0)

    // Subsequent rounds: each match is midpoint of its two feeders
    for (let ri = 1; ri < bracket.rounds.length; ri++) {
        const prev = matchPositions[ri - 1]
        const curr: number[] = []
        for (let mi = 0; mi < bracket.rounds[ri].length; mi++) {
            const feeder1 = mi * 2
            const feeder2 = mi * 2 + 1
            if (feeder2 < prev.length) {
                curr.push((prev[feeder1] + prev[feeder2]) / 2)
            } else if (feeder1 < prev.length) {
                curr.push(prev[feeder1])
            } else {
                curr.push(ROUND_HEADER + mi * (MATCH_HEIGHT + MATCH_GAP) + MATCH_HEIGHT / 2)
            }
        }
        matchPositions.push(curr)
    }

    const maxY = Math.max(...matchPositions[0]) + MATCH_HEIGHT / 2
    const totalHeight = maxY + 32
    const totalWidth = bracket.rounds.length * roundStep - ROUND_GAP + 40

    // Build connector paths (90-degree elbow lines)
    const connectors: { path: string; hasWinner: boolean }[] = []
    for (let ri = 0; ri < bracket.rounds.length - 1; ri++) {
        const currentRound = bracket.rounds[ri]
        const nextRound = bracket.rounds[ri + 1]

        for (let mi = 0; mi < currentRound.length; mi++) {
            const nextMatchIdx = Math.floor(mi / 2)
            if (nextMatchIdx >= nextRound.length) continue

            const fromX = ri * roundStep + MATCH_WIDTH
            const toX = (ri + 1) * roundStep
            const fromY = matchPositions[ri][mi]
            const toY = matchPositions[ri + 1][nextMatchIdx]
            const midX = fromX + (toX - fromX) / 2

            const path = `M ${fromX} ${fromY} H ${midX} V ${toY} H ${toX}`
            connectors.push({ path, hasWinner: currentRound[mi].winner !== null })
        }
    }

    const [isDragging, setIsDragging] = useState(false)
    const dragStart = useRef({ x: 0, y: 0, scrollX: 0, scrollY: 0 })

    const handleMouseDown = (e: React.MouseEvent) => {
        if (!containerRef.current) return
        setIsDragging(true)
        dragStart.current = { x: e.clientX, y: e.clientY, scrollX: containerRef.current.scrollLeft, scrollY: containerRef.current.scrollTop }
    }
    const handleMouseMove = (e: React.MouseEvent) => {
        if (!isDragging || !containerRef.current) return
        containerRef.current.scrollLeft = dragStart.current.scrollX - (e.clientX - dragStart.current.x)
        containerRef.current.scrollTop = dragStart.current.scrollY - (e.clientY - dragStart.current.y)
    }
    const handleMouseUp = () => setIsDragging(false)

    return (
        <div
            ref={containerRef}
            className="bracket-scroll-container"
            onMouseDown={handleMouseDown}
            onMouseMove={handleMouseMove}
            onMouseUp={handleMouseUp}
            onMouseLeave={handleMouseUp}
            style={{
                overflow: 'auto',
                maxHeight: fullscreen ? 'calc(100vh - 80px)' : '500px',
                position: 'relative',
                cursor: isDragging ? 'grabbing' : 'grab',
                userSelect: 'none',
            }}
        >
            <div style={{ position: 'relative', width: `${totalWidth}px`, minHeight: `${totalHeight}px`, padding: '8px 12px' }}>
                {/* SVG connector lines */}
                <svg style={{ position: 'absolute', top: 0, left: 12, width: totalWidth, height: totalHeight, pointerEvents: 'none', zIndex: 0 }}>
                    {connectors.map((c, i) => (
                        <path
                            key={i}
                            d={c.path}
                            fill="none"
                            stroke={c.hasWinner ? 'rgba(166,0,255,0.35)' : 'rgba(255,255,255,0.06)'}
                            strokeWidth={c.hasWinner ? 1.5 : 1}
                            strokeDasharray={c.hasWinner ? 'none' : '3 3'}
                        />
                    ))}
                </svg>

                {/* Rounds */}
                <div style={{ display: 'flex', gap: `${ROUND_GAP}px`, position: 'relative', zIndex: 1 }}>
                    {bracket.rounds.map((round, ri) => (
                        <div key={ri} style={{ width: `${MATCH_WIDTH}px`, flexShrink: 0, position: 'relative' }}>
                            <p className="round-label" style={{ height: `${ROUND_HEADER}px`, display: 'flex', alignItems: 'center' }}>
                                {ROUND_NAMES[ri] || `Round ${ri + 1}`}
                            </p>
                            {round.map((match, mi) => (
                                <div key={mi} style={{ position: 'absolute', top: `${matchPositions[ri][mi] - MATCH_HEIGHT / 2}px`, left: 0, width: '100%' }}>
                                    <MatchCard match={match} />
                                </div>
                            ))}
                        </div>
                    ))}
                </div>
            </div>
        </div>
    )
}

function MatchCard({ match }: { match: MatchResponse }) {
    const navigate = useNavigate()
    const isComplete = match.winner !== null
    const team1Won = match.winner?.id === match.team1?.id
    const team2Won = match.winner?.id === match.team2?.id

    const handleClick = (e: React.MouseEvent) => {
        e.stopPropagation()
        navigate({ to: '/gameseries/$id/results', params: { id: match.game_series_id } })
    }

    return (
        <div className="match-card" style={{ height: `${MATCH_HEIGHT}px` }} onClick={handleClick}>
            <div className={`match-team ${team1Won ? 'winner team1-winner' : ''} ${isComplete && !team1Won ? 'loser' : ''}`}>
                <span className="team-name">{getTeamLabel(match.team1)}</span>
                {team1Won && <span className="win-indicator blue-win">W</span>}
            </div>
            <div className="match-divider" />
            <div className={`match-team ${team2Won ? 'winner team2-winner' : ''} ${isComplete && !team2Won ? 'loser' : ''}`}>
                <span className="team-name">{getTeamLabel(match.team2)}</span>
                {team2Won && <span className="win-indicator red-win">W</span>}
            </div>
        </div>
    )
}

function BracketModal({ tournament, onClose }: { tournament: TournamentResponse; onClose: () => void }) {
    const containerRef = useRef<HTMLDivElement>(null)
    const [isDragging, setIsDragging] = useState(false)
    const [startPos, setStartPos] = useState({ x: 0, y: 0 })
    const [scrollPos, setScrollPos] = useState({ x: 0, y: 0 })

    const handleMouseDown = (e: React.MouseEvent) => {
        if (!containerRef.current) return
        setIsDragging(true)
        setStartPos({ x: e.clientX, y: e.clientY })
        setScrollPos({ x: containerRef.current.scrollLeft, y: containerRef.current.scrollTop })
    }

    const handleMouseMove = (e: React.MouseEvent) => {
        if (!isDragging || !containerRef.current) return
        containerRef.current.scrollLeft = scrollPos.x - (e.clientX - startPos.x)
        containerRef.current.scrollTop = scrollPos.y - (e.clientY - startPos.y)
    }

    const handleMouseUp = () => setIsDragging(false)

    return (
        <div style={{ position: 'fixed', inset: 0, zIndex: 2000, background: 'rgba(0,0,0,0.9)', backdropFilter: 'blur(8px)', display: 'flex', flexDirection: 'column' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 24px', borderBottom: '1px solid rgba(166,0,255,0.1)' }}>
                <h2 style={{ margin: 0, fontFamily: "'Russo One', sans-serif", fontSize: '14px', color: '#fff', letterSpacing: '0.06em' }}>BRACKET VIEW</h2>
                <button onClick={onClose} style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', padding: '8px 14px', color: 'rgba(255,255,255,0.6)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontFamily: "'Chakra Petch', monospace", fontSize: '12px' }}>
                    <FiX size={14} /> Close
                </button>
            </div>
            <div
                ref={containerRef}
                onMouseDown={handleMouseDown}
                onMouseMove={handleMouseMove}
                onMouseUp={handleMouseUp}
                onMouseLeave={handleMouseUp}
                style={{ flex: 1, overflow: 'auto', cursor: isDragging ? 'grabbing' : 'grab', padding: '32px' }}
            >
                <BracketView tournament={tournament} fullscreen />
            </div>
        </div>
    )
}

function DraftBoard({
    tournament,
    players,
    isHost,
    actorId,
    participantInfo,
    onRemovePlayer,
}: {
    tournament: TournamentResponse
    players: AuthUser[]
    isHost: boolean
    actorId?: string
    participantInfo: GatewayParticipantInfo[]
    onRemovePlayer?: (playerId: string) => void
}) {
    const [captainIds, setCaptainIds] = useState<string[]>([])
    const [pickedByCaptain, setPickedByCaptain] = useState<Record<string, string[]>>({})
    const [showDraftPool, setShowDraftPool] = useState(false)
    const [captainCount, setCaptainCount] = useState(2)
    const setCaptainsMutation = useSetDraftCaptainsMutation(tournament.id)
    const updatePickOrderMutation = useUpdateDraftPickOrderMutation(tournament.id)
    const draftPickMutation = useDraftPickPlayerMutation(tournament.id)
    const draftState = tournament.draft_state
    const savedCaptains = draftState?.config.captains ?? []
    const savedCaptainIds = draftState?.config.pick_order_captain_ids.length
        ? draftState.config.pick_order_captain_ids
        : [...savedCaptains].sort((a, b) => a.order - b.order).map(captain => captain.captain.id)
    const selectedCaptainIds = captainIds.filter(Boolean)
    const activeCaptainIds = savedCaptainIds.length ? savedCaptainIds : selectedCaptainIds
    const maxExtraPlayers = draftState?.config.max_extra_players_per_team ?? 4
    const teamSize = tournament.settings.game_settings.team_size
    const roleByUserId = new Map<string, TournamentRole[]>()
    participantInfo.forEach(info => {
        const participantId = info.participant.id
        const roles = info.draft_roles?.length ? info.draft_roles : getStoredDraftRoles(tournament.id, participantId)
        if (roles.length) roleByUserId.set(participantId, roles)
    })
    const sortedPlayers = [...players].sort((a, b) => getRankScore(b) - getRankScore(a))
    const minCaptainCount = sortedPlayers.length >= teamSize * 2 ? Math.max(2, Math.ceil(sortedPlayers.length / teamSize)) : 0
    const maxCaptainCount = sortedPlayers.length
    const effectiveCaptainCount = Math.min(Math.max(captainCount, minCaptainCount || 2), Math.max(maxCaptainCount, 2))
    const savedPickedByCaptain = Object.fromEntries(savedCaptains.map(captain => [
        captain.captain.id,
        captain.picked_players.map(player => player.id),
    ]))
    const effectivePickedByCaptain = savedCaptains.length ? savedPickedByCaptain : pickedByCaptain
    const pickedIds = new Set(Object.values(effectivePickedByCaptain).flat())
    const availablePlayers = sortedPlayers.filter(player => (
        draftState
            ? draftState.available_player_ids.includes(player.id)
            : !activeCaptainIds.includes(player.id) && !pickedIds.has(player.id)
    ))
    const currentCaptainId = draftState?.current_captain_id ?? activeCaptainIds.find(captainId => (effectivePickedByCaptain[captainId]?.length ?? 0) < maxExtraPlayers) ?? null
    const playersByRankAndRole = new Map<string, AuthUser[]>()
    availablePlayers.forEach(player => {
        const primaryRole = roleByUserId.get(player.id)?.[0] ?? 'mid'
        const key = `${getRankRow(player)}:${primaryRole}`
        playersByRankAndRole.set(key, [...(playersByRankAndRole.get(key) ?? []), player])
    })
    const roleCounts = ROLE_ORDER.map(role => ({
        role,
        count: availablePlayers.filter(player => (roleByUserId.get(player.id)?.[0] ?? 'mid') === role).length,
    }))

    useEffect(() => {
        if (minCaptainCount > 0 && captainCount < minCaptainCount) {
            setCaptainCount(minCaptainCount)
        }
    }, [captainCount, minCaptainCount])

    const setCaptainAt = (index: number, playerId: string) => {
        if (!isHost || draftState) return
        setCaptainIds(current => {
            const next = Array.from({ length: effectiveCaptainCount }, (_, i) => current[i] ?? '')
            next[index] = playerId
            return next
        })
        setPickedByCaptain({})
    }

    const pickPlayer = (playerId: string) => {
        if (!isHost || !currentCaptainId) return
        if (draftState && actorId) {
            draftPickMutation.mutateAsync({ actorId, captainId: currentCaptainId, playerId })
            return
        }
        setPickedByCaptain(current => ({
            ...current,
            [currentCaptainId]: [...(current[currentCaptainId] ?? []), playerId],
        }))
    }

    const saveCaptains = () => {
        const normalizedCaptainIds = captainIds.filter(Boolean)
        if (!actorId || normalizedCaptainIds.length !== effectiveCaptainCount) return
        setCaptainsMutation.mutateAsync({ actorId, captainIds: normalizedCaptainIds, pickDirection: 'snake', maxExtraPlayersPerTeam: Math.max(0, teamSize - 1) })
    }

    const moveCaptain = (captainId: string, direction: -1 | 1) => {
        if (!actorId || !draftState) return
        const next = [...activeCaptainIds]
        const index = next.indexOf(captainId)
        const target = index + direction
        if (index < 0 || target < 0 || target >= next.length) return
        ;[next[index], next[target]] = [next[target], next[index]]
        updatePickOrderMutation.mutateAsync({ actorId, captainIds: next })
    }

    const getUserName = (id: string) => players.find(player => player.id === id)?.nickname ?? id.slice(-6)
    const draftPoolGrid = (
        <div className="draft-role-grid">
            <div className="draft-rank-corner" />
            {ROLE_ORDER.map(role => <div key={role} className="draft-role-head">{ROLE_LABELS[role]}</div>)}
            {RANK_ROWS.map(rank => (
                <Fragment key={rank}>
                    <div key={`${rank}:label`} className="draft-rank-label">{rank.toLowerCase()}</div>
                    {ROLE_ORDER.map(role => {
                        const cellPlayers = playersByRankAndRole.get(`${rank}:${role}`) ?? []
                        return (
                            <div key={`${rank}:${role}`} className="draft-role-cell">
                                {cellPlayers.length > 0 ? cellPlayers.map(player => {
                                    const account = getPrimaryLeagueAccount(player)
                                    const roles = roleByUserId.get(player.id) ?? [role]
                                    const secondaryRole = roles[1]
                                    const isCaptain = activeCaptainIds.includes(player.id)
                                    return (
                                        <div
                                            key={player.id}
                                            className={`draft-pool-chip ${isCaptain ? 'captain' : ''}`}
                                        >
                                            <img className="draft-avatar" src={account?.profile_image_url || player.avatar || '/favicon.ico'} alt="" />
                                            <span className="draft-chip-main">
                                                <span className="draft-player-name">{player.nickname || `User ${player.id.slice(-4)}`}</span>
                                                <span className="draft-player-riot">{formatRank(player)}</span>
                                            </span>
                                            {secondaryRole && <span className="draft-secondary">{ROLE_LABELS[secondaryRole]}</span>}
                                        </div>
                                    )
                                }) : <span className="draft-cell-empty">-</span>}
                            </div>
                        )
                    })}
                </Fragment>
            ))}
        </div>
    )

    return (
        <>
            <div className="draft-layout">
                <div className="draft-table-wrap draft-pool-summary">
                    <div className="td-section-header">
                        <h3 className="td-section-title">Draft pool ({players.length})</h3>
                        <button className="fullscreen-btn" onClick={() => setShowDraftPool(true)}>
                            <FiMaximize2 size={12} /> Fullscreen
                        </button>
                    </div>
                    <div className="draft-summary-row">
                        {roleCounts.map(item => (
                            <button key={item.role} className="draft-role-summary" onClick={() => setShowDraftPool(true)}>
                                <span>{ROLE_LABELS[item.role]}</span>
                                <strong>{item.count}</strong>
                            </button>
                        ))}
                    </div>
                    <p className="draft-empty" style={{ marginTop: '12px' }}>
                        Pool is grouped by primary role and ranked from Challenger to Iron.
                    </p>
                    {isHost && sortedPlayers.length > 0 && (
                        <div className="draft-registered-strip">
                            {sortedPlayers.slice(0, 12).map(player => (
                                <span key={player.id} className="draft-registered-player">
                                    {player.nickname || player.id.slice(-6)}
                                    <button onClick={() => onRemovePlayer?.(player.id)} aria-label="Remove player">
                                        <FiTrash2 size={11} />
                                    </button>
                                </span>
                            ))}
                        </div>
                    )}
                </div>

                <div className="draft-teams">
                    <div className="td-section-header">
                        <h3 className="td-section-title">Captain picks</h3>
                        <span className="draft-turn">{currentCaptainId ? `${getUserName(currentCaptainId)} picks` : 'Pick captains'}</span>
                    </div>
                    {!draftState && isHost && (
                        <div className="captain-setup">
                            <p className="draft-empty">
                                {minCaptainCount > 0
                                    ? `${sortedPlayers.length} players require at least ${minCaptainCount} captains for ${teamSize}v${teamSize}.`
                                    : `Draft pool must contain enough players for at least two ${teamSize}v${teamSize} teams.`}
                            </p>
                            {minCaptainCount > 0 && (
                                <label className="captain-select">
                                    <span>Captain count</span>
                                    <select value={effectiveCaptainCount} onChange={event => {
                                        const nextCount = +event.target.value
                                        setCaptainCount(nextCount)
                                        setCaptainIds(current => current.slice(0, nextCount))
                                    }}>
                                        {Array.from({ length: maxCaptainCount - minCaptainCount + 1 }).map((_, index) => {
                                            const count = minCaptainCount + index
                                            return <option key={count} value={count}>{count} captains</option>
                                        })}
                                    </select>
                                </label>
                            )}
                            {Array.from({ length: minCaptainCount > 0 ? effectiveCaptainCount : 0 }).map((_, index) => (
                                <label key={index} className="captain-select">
                                    <span>Captain {index + 1}</span>
                                    <select value={captainIds[index] ?? ''} onChange={event => setCaptainAt(index, event.target.value)}>
                                        <option value="">Select player</option>
                                        {sortedPlayers.map(player => {
                                            const selectedByAnotherSlot = captainIds.some((id, selectedIndex) => id === player.id && selectedIndex !== index)
                                            return (
                                                <option key={player.id} value={player.id} disabled={selectedByAnotherSlot}>
                                                    {player.nickname || player.id.slice(-6)} - {formatRank(player)}
                                                </option>
                                            )
                                        })}
                                    </select>
                                </label>
                            ))}
                            <button className="fullscreen-btn" onClick={saveCaptains} disabled={!actorId || minCaptainCount < 2 || captainIds.filter(Boolean).length !== effectiveCaptainCount || new Set(captainIds.filter(Boolean)).size !== effectiveCaptainCount || setCaptainsMutation.isPending}>
                                <FiLock size={12} /> {setCaptainsMutation.isPending ? 'Saving...' : `Save ${effectiveCaptainCount} captains`}
                            </button>
                        </div>
                    )}
                    {activeCaptainIds.length > 0 ? activeCaptainIds.map((captainId, index) => (
                        <div className={`draft-team ${currentCaptainId === captainId ? 'active' : ''}`} key={captainId}>
                            <div className="draft-team-head">
                                <span>#{index + 1} {getUserName(captainId)}</span>
                                <span>{(effectivePickedByCaptain[captainId]?.length ?? 0)}/{maxExtraPlayers}</span>
                            </div>
                            {draftState && isHost && (
                                <div className="draft-order-controls">
                                    <button onClick={() => moveCaptain(captainId, -1)} disabled={index === 0 || updatePickOrderMutation.isPending}>Up</button>
                                    <button onClick={() => moveCaptain(captainId, 1)} disabled={index === activeCaptainIds.length - 1 || updatePickOrderMutation.isPending}>Down</button>
                                </div>
                            )}
                            <div className="draft-picks">
                                {(effectivePickedByCaptain[captainId] ?? []).map(playerId => <span key={playerId}>{getUserName(playerId)}</span>)}
                            </div>
                        </div>
                    )) : (
                        <p className="draft-empty">Host selects captains from the captain setup panel.</p>
                    )}

                    <div className="draft-pick-list">
                        {availablePlayers.slice(0, 8).map(player => (
                            <button key={player.id} className="draft-pick-btn" onClick={() => pickPlayer(player.id)} disabled={!isHost || !currentCaptainId || draftPickMutation.isPending || (!!draftState && draftState.finished)}>
                                <span>{player.nickname || player.id.slice(-6)}</span>
                                <span>{formatRank(player)}</span>
                            </button>
                        ))}
                    </div>
                </div>
            </div>

            {showDraftPool && typeof document !== 'undefined' && createPortal((
                <div style={{ position: 'fixed', inset: 0, zIndex: 2000, background: 'rgba(0,0,0,0.9)', backdropFilter: 'blur(8px)', display: 'flex', flexDirection: 'column' }}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '16px 24px', borderBottom: '1px solid rgba(166,0,255,0.1)' }}>
                        <div>
                            <h2 style={{ margin: 0, fontFamily: "'Russo One', sans-serif", fontSize: '14px', color: '#fff', letterSpacing: '0.06em' }}>DRAFT POOL</h2>
                            <p style={{ margin: '5px 0 0', fontFamily: "'Chakra Petch', monospace", fontSize: '11px', color: 'rgba(255,255,255,0.38)' }}>Primary roles by columns, solo rank by rows</p>
                        </div>
                        <button onClick={() => setShowDraftPool(false)} style={{ background: 'rgba(255,255,255,0.05)', border: '1px solid rgba(255,255,255,0.1)', borderRadius: '8px', padding: '8px 14px', color: 'rgba(255,255,255,0.6)', cursor: 'pointer', display: 'flex', alignItems: 'center', gap: '6px', fontFamily: "'Chakra Petch', monospace", fontSize: '12px' }}>
                            <FiX size={14} /> Close
                        </button>
                    </div>
                    <div className="draft-pool-modal-body">
                        <div className="draft-table-wrap draft-pool-board">
                            <div className="td-section-header">
                                <h3 className="td-section-title">Draft pool ({players.length})</h3>
                                <span className="draft-turn">Challenger to Iron</span>
                            </div>
                            {draftPoolGrid}
                        </div>
                    </div>
                </div>
            ), document.body)}
        </>
    )
}

function DraftSignup({
    tournamentId,
    userId,
    isPending,
    onJoin,
}: {
    tournamentId: string
    userId: string
    isPending: boolean
    onJoin: (primaryRole: TournamentRole, secondaryRole: TournamentRole) => void
}) {
    const [primaryRole, setPrimaryRole] = useState<TournamentRole>('mid')
    const [secondaryRole, setSecondaryRole] = useState<TournamentRole>('support')
    const [isOpen, setIsOpen] = useState(false)

    const submit = () => {
        if (primaryRole === secondaryRole) return
        storeDraftRoles(tournamentId, userId, [primaryRole, secondaryRole])
        onJoin(primaryRole, secondaryRole)
        setIsOpen(false)
    }

    return (
        <>
            <button className="fullscreen-btn" onClick={() => setIsOpen(true)} disabled={isPending}>
                <FiUsers size={12} /> {isPending ? 'Joining...' : 'Join Draft Pool'}
            </button>
            {isOpen && typeof document !== 'undefined' && createPortal((
                <div className="draft-role-modal-overlay" onClick={() => setIsOpen(false)}>
                    <div className="draft-role-modal" onClick={event => event.stopPropagation()}>
                        <div className="draft-role-modal-head">
                            <div>
                                <h2>Join Draft Pool</h2>
                                <p>Select your main and backup roles.</p>
                            </div>
                            <button className="draft-modal-close" onClick={() => setIsOpen(false)}>
                                <FiX size={14} /> Close
                            </button>
                        </div>
                        <div className="draft-signup">
                            <label className="draft-role-select">
                                <span>Primary</span>
                                <select value={primaryRole} onChange={event => setPrimaryRole(event.target.value as TournamentRole)}>
                                    {ROLE_ORDER.map(role => <option key={role} value={role}>{ROLE_LABELS[role]}</option>)}
                                </select>
                            </label>
                            <label className="draft-role-select">
                                <span>Secondary</span>
                                <select value={secondaryRole} onChange={event => setSecondaryRole(event.target.value as TournamentRole)}>
                                    {ROLE_ORDER.map(role => <option key={role} value={role}>{ROLE_LABELS[role]}</option>)}
                                </select>
                            </label>
                        </div>
                        {primaryRole === secondaryRole && (
                            <p className="draft-role-error">Secondary role must be different from primary.</p>
                        )}
                        <button className="draft-role-submit" onClick={submit} disabled={isPending || primaryRole === secondaryRole}>
                            <FiUsers size={12} /> {isPending ? 'Joining...' : 'Confirm Registration'}
                        </button>
                    </div>
                </div>
            ), document.body)}
        </>
    )
}

function PresignedSignup({ userId, onJoin, isPending }: { userId?: string; onJoin: (teamId: string) => void; isPending: boolean }) {
    const { data: teams } = useTeams()
    const [teamId, setTeamId] = useState('')
    const ownedTeams = (teams ?? []).filter(team => !userId || team.owner_id === userId || team.members.includes(userId))

    return (
        <div className="team-signup">
            <select className="team-select" value={teamId} onChange={event => setTeamId(event.target.value)}>
                <option value="">Select team</option>
                {ownedTeams.map(team => <option key={team.id} value={team.id}>{team.name} [{team.tag}]</option>)}
            </select>
            <button className="fullscreen-btn" onClick={() => teamId && onJoin(teamId)} disabled={!teamId || isPending}>
                <FiUsers size={12} /> {isPending ? 'Registering...' : 'Register Team'}
            </button>
        </div>
    )
}

function TournamentDetailPage() {
    const navigate = useNavigate()
    const { id } = Route.useParams()
    const { user } = useAuthContext()
    const { data: tournament, isLoading, isError } = useTournament(id)
    const { data: tournamentUsers } = useTournamentUsers(tournament)
    const { data: participantInfo } = useTournamentParticipantInfo(id)
    const addParticipantMutation = useAddTournamentParticipantMutation(id)
    const startTournamentMutation = useStartTournamentMutation(id)
    const prebuildBracketMutation = usePrebuildTournamentBracketMutation(id)
    const lockRegistrationMutation = useLockTournamentRegistrationMutation(id)
    const rescheduleMutation = useRescheduleTournamentMutation(id)
    const removeParticipantMutation = useRemoveTournamentParticipantMutation(id)
    const [showFullBracket, setShowFullBracket] = useState(false)
    const [rescheduleDate, setRescheduleDate] = useState('')
    const [rescheduleTime, setRescheduleTime] = useState('')
    const [rescheduleDraftDate, setRescheduleDraftDate] = useState('')
    const [rescheduleDraftTime, setRescheduleDraftTime] = useState('')
    const [flowError, setFlowError] = useState('')

    if (isLoading) {
        return <p style={{ marginTop: '120px', textAlign: 'center', color: 'rgba(255,255,255,0.35)', fontFamily: "'Chakra Petch', monospace" }}>Loading tournament...</p>
    }

    if (isError || !tournament) {
        return (
            <div style={{ marginTop: '120px', textAlign: 'center', color: 'rgba(255,255,255,0.35)', fontFamily: "'Chakra Petch', monospace" }}>
                <p>Tournament not found</p>
                <button className="td-back" onClick={() => navigate({ to: '/tournaments' })}>
                    <FiArrowLeft size={14} /> Back to Tournaments
                </button>
            </div>
        )
    }

    const statusColor = STATUS_COLORS[tournament.status] || '#fff'
    const startDate = new Date(tournament.start * 1000)
    const isHost = user?.id === tournament.host.id
    const isDraftTournament = tournament.settings.tournament_type === 'draft'
    const draftPoolSize = tournament.participant_pool.length
    const tournamentTeamSize = tournament.settings.game_settings.team_size
    const isDraftPoolLockable = !isDraftTournament || draftPoolSize >= tournamentTeamSize * 2
    const canLockRegistration = isHost && tournament.lifecycle === 'registration_open' && isDraftPoolLockable
    const canGenerateBracket = isHost && (
        (!isDraftTournament && tournament.lifecycle === 'registration_locked')
        || (isDraftTournament && tournament.lifecycle === 'draft_finished')
    )
    const canStartTournament = isHost && tournament.lifecycle === 'bracket_ready'
    const isParticipant = !!user && tournament.participant_pool.some(participant => {
        if (isDraftTournament) return participant.actor?.id === user.id
        return participant.actor?.type === 'team' && participant.players.includes(user.id)
    })

    const handleJoinTournament = async (primaryRole: TournamentRole, secondaryRole: TournamentRole) => {
        if (!user || isParticipant) return
        await addParticipantMutation.mutateAsync({
            participant: { id: user.id, type: 'user' },
            teamName: encodeDraftRoles(primaryRole, secondaryRole),
        })
    }

    const handleJoinTeamTournament = async (teamId: string) => {
        await addParticipantMutation.mutateAsync({ participant: { id: teamId, type: 'team' } })
    }

    const handleReschedule = async () => {
        if (!user || !rescheduleDate || !rescheduleTime) return
        setFlowError('')
        const start = Math.floor(new Date(`${rescheduleDate}T${rescheduleTime}`).getTime() / 1000)
        const draftStart = isDraftTournament && rescheduleDraftDate && rescheduleDraftTime
            ? Math.floor(new Date(`${rescheduleDraftDate}T${rescheduleDraftTime}`).getTime() / 1000)
            : tournament.draft_start ?? null
        if (isDraftTournament && draftStart && start - draftStart < 2 * 24 * 60 * 60) {
            setFlowError('Tournament start must be at least 2 days after the draft.')
            return
        }
        await rescheduleMutation.mutateAsync({ actorId: user.id, start, draftStart })
    }

    const removeParticipant = async (participant: Actor | null) => {
        if (!participant || !user) return
        await removeParticipantMutation.mutateAsync({ participantId: participant.id, actorId: user.id })
    }

    return (
        <>
            <style>{`
                .td-page {
                    position: relative; z-index: 10;
                    min-height: calc(100vh - 52px); margin-top: 52px;
                    padding: 32px clamp(24px, 5vw, 64px);
                    max-width: 1100px; margin-left: auto; margin-right: auto;
                }
                .td-back {
                    display: inline-flex; align-items: center; gap: 6px;
                    font-family: 'Chakra Petch', monospace; font-size: 12px;
                    color: rgba(255,255,255,0.4); background: none; border: none;
                    cursor: pointer; margin-bottom: 24px; transition: color 150ms;
                }
                .td-back:hover { color: rgba(255,255,255,0.7); }
                .td-header {
                    display: flex; justify-content: space-between; align-items: flex-start;
                    margin-bottom: 32px; flex-wrap: wrap; gap: 16px;
                }
                .td-title { font-family: 'Russo One', sans-serif; font-size: 22px; color: #fff; margin: 0; }
                .td-meta { display: flex; gap: 16px; flex-wrap: wrap; align-items: center; }
                .td-meta-item {
                    display: flex; align-items: center; gap: 5px;
                    font-family: 'Chakra Petch', monospace; font-size: 12px; color: rgba(255,255,255,0.5);
                }
                .td-status {
                    padding: 4px 10px; border-radius: 6px; font-size: 10px;
                    font-family: 'Chakra Petch', monospace; letter-spacing: 0.1em;
                    text-transform: uppercase; font-weight: 600;
                }
                .td-section {
                    margin-top: 32px; padding: 24px; border-radius: 14px;
                    background: rgba(0,0,0,0.3); border: 1px solid rgba(166,0,255,0.08);
                    backdrop-filter: blur(8px);
                }
                .td-section-header {
                    display: flex; justify-content: space-between; align-items: center; margin-bottom: 18px;
                }
                .td-section-title {
                    font-family: 'Russo One', sans-serif; font-size: 13px;
                    color: rgba(255,255,255,0.7); letter-spacing: 0.06em;
                    text-transform: uppercase; margin: 0;
                }
                .fullscreen-btn {
                    display: flex; align-items: center; gap: 6px;
                    padding: 6px 12px; border-radius: 6px; font-size: 11px;
                    font-family: 'Chakra Petch', monospace;
                    background: rgba(166,0,255,0.08); border: 1px solid rgba(166,0,255,0.15);
                    color: rgba(255,255,255,0.6); cursor: pointer; transition: all 150ms;
                }
                .fullscreen-btn:hover { background: rgba(166,0,255,0.15); color: #fff; border-color: rgba(166,0,255,0.3); }
                .fullscreen-btn:disabled { opacity: 0.42; cursor: not-allowed; }
                .host-panel {
                    margin-bottom: 24px; padding: 16px; border-radius: 12px;
                    background: rgba(0,0,0,0.24); border: 1px solid rgba(255,255,255,0.06);
                    display: grid; gap: 14px;
                }
                .host-flow, .host-actions, .reschedule-panel {
                    display: flex; gap: 8px; flex-wrap: wrap; align-items: center;
                }
                .flow-chip {
                    min-height: 28px; display: inline-flex; align-items: center; padding: 5px 9px; border-radius: 7px;
                    border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.4); font-family: 'Chakra Petch', monospace; font-size: 10px;
                    text-transform: uppercase; letter-spacing: 0.04em;
                }
                .flow-chip.active { border-color: rgba(6,182,212,0.35); background: rgba(6,182,212,0.08); color: #06B6D4; }
                .reschedule-panel label {
                    display: flex; flex-direction: column; gap: 5px; min-width: 132px;
                    font-family: 'Chakra Petch', monospace; font-size: 10px; color: rgba(255,255,255,0.45);
                    text-transform: uppercase; letter-spacing: 0.05em;
                }
                .reschedule-panel input {
                    min-height: 34px; padding: 7px 9px; border-radius: 8px;
                    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
                    color: #fff; font-family: 'Chakra Petch', monospace; font-size: 12px;
                }
                .flow-error { margin: 0; color: #FF6B7A; font-family: 'Chakra Petch', monospace; font-size: 11px; }
                .bracket-scroll-container::-webkit-scrollbar { width: 6px; height: 6px; }
                .bracket-scroll-container::-webkit-scrollbar-track { background: rgba(0,0,0,0.2); border-radius: 3px; }
                .bracket-scroll-container::-webkit-scrollbar-thumb { background: rgba(166,0,255,0.2); border-radius: 3px; }
                .bracket-scroll-container::-webkit-scrollbar-thumb:hover { background: rgba(166,0,255,0.35); }
                .round-label {
                    font-family: 'Chakra Petch', monospace; font-size: 10px;
                    color: rgba(166,0,255,0.6); letter-spacing: 0.12em;
                    text-transform: uppercase; margin: 0; font-weight: 600;
                }
                .match-card {
                    border-radius: 6px; overflow: hidden;
                    background: rgba(0,0,0,0.5); border: 1px solid rgba(166,0,255,0.1);
                    display: flex; flex-direction: column; justify-content: center;
                    transition: border-color 180ms, box-shadow 180ms;
                    cursor: pointer;
                }
                .match-card:hover { border-color: rgba(166,0,255,0.3); box-shadow: 0 0 12px rgba(166,0,255,0.08); }
                .match-team {
                    display: flex; justify-content: space-between; align-items: center;
                    padding: 5px 10px; transition: background 150ms;
                }
                .match-team.winner { background: rgba(166,0,255,0.1); }
                .match-team.team1-winner { background: rgba(6,182,212,0.1); }
                .match-team.team2-winner { background: rgba(255,0,42,0.08); }
                .match-team.loser { opacity: 0.45; }
                .team-name { font-family: 'Chakra Petch', monospace; font-size: 10px; color: rgba(255,255,255,0.75); white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
                .match-team.winner .team-name { color: #fff; font-weight: 600; }
                .match-team.team1-winner .team-name { color: #06B6D4; text-shadow: 0 0 8px rgba(6,182,212,0.4); }
                .match-team.team2-winner .team-name { color: #FF002A; text-shadow: 0 0 8px rgba(255,0,42,0.4); }
                .win-indicator {
                    font-family: 'Chakra Petch', monospace; font-size: 9px;
                    font-weight: 700; padding: 1px 4px;
                    border-radius: 3px; flex-shrink: 0;
                }
                .win-indicator.blue-win {
                    color: #06B6D4; background: rgba(6,182,212,0.15);
                }
                .win-indicator.red-win {
                    color: #FF002A; background: rgba(255,0,42,0.12);
                }
                .match-divider { height: 1px; background: rgba(166,0,255,0.08); }
                .participants-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 10px; }
                .participant-card {
                    padding: 12px 16px; border-radius: 10px;
                    background: rgba(0,0,0,0.3); border: 1px solid rgba(255,255,255,0.05);
                    font-family: 'Chakra Petch', monospace; font-size: 12px; color: rgba(255,255,255,0.6);
                    display: flex; align-items: center; gap: 10px; transition: border-color 150ms;
                }
                .participant-card:hover { border-color: rgba(166,0,255,0.15); }
                .participant-avatar {
                    width: 32px; height: 32px; border-radius: 8px;
                    background: rgba(166,0,255,0.1); border: 1px solid rgba(166,0,255,0.15);
                    display: flex; align-items: center; justify-content: center;
                    font-size: 11px; color: rgba(166,0,255,0.7); font-weight: 700;
                }
                .participant-remove {
                    margin-left: auto; width: 34px; height: 34px; border-radius: 8px;
                    display: inline-flex; align-items: center; justify-content: center;
                    background: rgba(255,0,42,0.08); border: 1px solid rgba(255,0,42,0.16);
                    color: rgba(255,255,255,0.55); cursor: pointer;
                }
                .participant-remove:hover:not(:disabled) { color: #FF6B7A; border-color: rgba(255,0,42,0.32); }
                .participant-remove:disabled { opacity: 0.45; cursor: not-allowed; }
                .settings-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
                .setting-item {
                    padding: 14px; border-radius: 10px;
                    background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.04);
                }
                .setting-label { font-family: 'Chakra Petch', monospace; font-size: 10px; color: rgba(255,255,255,0.3); letter-spacing: 0.05em; margin: 0 0 6px; text-transform: uppercase; }
                .setting-value { font-family: 'Chakra Petch', monospace; font-size: 14px; color: rgba(255,255,255,0.85); margin: 0; font-weight: 500; text-transform: capitalize; }
                .draft-layout { display: grid; grid-template-columns: minmax(0, 1.45fr) minmax(280px, 0.75fr); gap: 18px; align-items: start; }
                .draft-table-wrap, .draft-teams {
                    border-radius: 12px; border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(0,0,0,0.22); padding: 16px;
                }
                .draft-pool-summary { min-height: 132px; }
                .draft-summary-row { display: grid; grid-template-columns: repeat(5, minmax(88px, 1fr)); gap: 8px; }
                .draft-role-summary {
                    min-height: 58px; display: flex; flex-direction: column; align-items: center; justify-content: center; gap: 4px;
                    border-radius: 8px; border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.62); cursor: pointer; font-family: 'Chakra Petch', monospace;
                }
                .draft-role-summary:hover { border-color: rgba(6,182,212,0.28); background: rgba(6,182,212,0.06); color: rgba(255,255,255,0.82); }
                .draft-role-summary span { font-size: 10px; text-transform: uppercase; letter-spacing: 0.05em; }
                .draft-role-summary strong { font-size: 18px; color: #fff; font-weight: 600; }
                .draft-pool-modal-body {
                    flex: 1; overflow: auto; padding: 24px;
                }
                .draft-pool-modal-body .draft-pool-board {
                    min-width: 940px;
                }
                .draft-pool-board { overflow-x: auto; }
                .draft-role-grid {
                    display: grid; grid-template-columns: 92px repeat(5, minmax(150px, 1fr));
                    gap: 8px; min-width: 860px;
                }
                .draft-rank-corner, .draft-role-head, .draft-rank-label, .draft-role-cell {
                    border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(255,255,255,0.025);
                }
                .draft-role-head {
                    min-height: 34px; display: flex; align-items: center; justify-content: center;
                    font-family: 'Chakra Petch', monospace; font-size: 11px; color: rgba(255,255,255,0.7);
                    text-transform: uppercase; letter-spacing: 0.05em;
                }
                .draft-rank-label {
                    min-height: 88px; display: flex; align-items: center; justify-content: center;
                    font-family: 'Chakra Petch', monospace; font-size: 10px; color: rgba(255,255,255,0.45);
                    text-transform: uppercase; writing-mode: vertical-rl; transform: rotate(180deg);
                }
                .draft-role-cell {
                    min-height: 88px; padding: 7px; display: flex; flex-direction: column; gap: 6px;
                }
                .draft-pool-chip {
                    min-height: 46px; display: grid; grid-template-columns: 32px minmax(0, 1fr) auto;
                    gap: 8px; align-items: center; width: 100%; padding: 6px;
                    border-radius: 7px; border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(0,0,0,0.24); color: rgba(255,255,255,0.78);
                    text-align: left;
                }
                .draft-pool-chip.captain { border-color: rgba(16,185,129,0.38); background: rgba(16,185,129,0.08); }
                .captain-setup {
                    display: grid; gap: 10px; margin-bottom: 14px;
                    padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(255,255,255,0.025);
                }
                .captain-select {
                    display: flex; flex-direction: column; gap: 5px;
                    font-family: 'Chakra Petch', monospace; font-size: 10px; color: rgba(255,255,255,0.45);
                    text-transform: uppercase; letter-spacing: 0.05em;
                }
                .captain-select select {
                    min-height: 36px; padding: 8px 9px; border-radius: 8px;
                    background: rgba(0,0,0,0.28); border: 1px solid rgba(255,255,255,0.08);
                    color: #fff; font-family: 'Chakra Petch', monospace; font-size: 12px; text-transform: none;
                }
                .captain-select select:focus { outline: none; border-color: rgba(6,182,212,0.35); }
                .draft-secondary {
                    font-family: 'Chakra Petch', monospace; font-size: 9px; color: #06B6D4;
                    padding: 2px 5px; border-radius: 5px; background: rgba(6,182,212,0.1);
                }
                .draft-cell-empty {
                    margin: auto; font-family: 'Chakra Petch', monospace; font-size: 12px; color: rgba(255,255,255,0.16);
                }
                .draft-table { display: flex; flex-direction: column; gap: 8px; }
                .draft-row {
                    min-height: 58px; display: grid; grid-template-columns: 40px minmax(120px, 1fr) minmax(110px, auto) 72px;
                    align-items: center; gap: 12px; width: 100%; padding: 9px 12px; text-align: left;
                    border-radius: 8px; border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.78); cursor: pointer; transition: border-color 160ms, background 160ms;
                }
                .draft-row:hover:not(:disabled) { border-color: rgba(6,182,212,0.35); background: rgba(6,182,212,0.06); }
                .draft-row.captain { border-color: rgba(16,185,129,0.35); background: rgba(16,185,129,0.07); }
                .draft-row.picked { opacity: 0.45; cursor: default; }
                .draft-avatar { width: 36px; height: 36px; border-radius: 8px; object-fit: cover; background: rgba(255,255,255,0.06); }
                .draft-player-main { min-width: 0; display: flex; flex-direction: column; gap: 3px; }
                .draft-player-name, .draft-rank, .draft-role, .draft-turn, .draft-team-head, .draft-pick-btn { font-family: 'Chakra Petch', monospace; }
                .draft-player-name { font-size: 13px; color: #fff; overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
                .draft-player-riot { font-size: 10px; color: rgba(255,255,255,0.34); overflow: hidden; text-overflow: ellipsis; white-space: nowrap; }
                .draft-rank { font-size: 11px; color: rgba(255,255,255,0.6); text-align: right; }
                .draft-role { justify-self: end; font-size: 10px; color: rgba(255,255,255,0.45); }
                .draft-turn { font-size: 11px; color: #06B6D4; }
                .draft-team { padding: 12px; border-radius: 8px; border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.025); margin-bottom: 10px; }
                .draft-team.active { border-color: rgba(6,182,212,0.32); box-shadow: 0 0 18px rgba(6,182,212,0.06); }
                .draft-team-head { display: flex; justify-content: space-between; gap: 12px; color: rgba(255,255,255,0.78); font-size: 12px; }
                .draft-order-controls { display: flex; gap: 6px; margin-top: 8px; }
                .draft-order-controls button {
                    min-height: 28px; padding: 4px 8px; border-radius: 7px;
                    background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.08);
                    color: rgba(255,255,255,0.5); font-family: 'Chakra Petch', monospace; font-size: 10px; cursor: pointer;
                }
                .draft-order-controls button:hover:not(:disabled) { color: #fff; border-color: rgba(6,182,212,0.28); }
                .draft-order-controls button:disabled { opacity: 0.4; cursor: not-allowed; }
                .draft-picks { display: flex; flex-wrap: wrap; gap: 6px; margin-top: 8px; }
                .draft-picks span {
                    font-family: 'Chakra Petch', monospace; font-size: 10px; padding: 3px 7px; border-radius: 5px;
                    background: rgba(166,0,255,0.1); color: rgba(255,255,255,0.65);
                }
                .draft-empty { margin: 0 0 12px; color: rgba(255,255,255,0.28); font-family: 'Chakra Petch', monospace; font-size: 12px; }
                .draft-pick-list { display: flex; flex-direction: column; gap: 8px; margin-top: 14px; }
                .draft-registered-strip { display: flex; gap: 6px; flex-wrap: wrap; margin-top: 12px; }
                .draft-registered-player {
                    display: inline-flex; align-items: center; gap: 6px; min-height: 28px; padding: 4px 5px 4px 8px; border-radius: 7px;
                    background: rgba(255,255,255,0.035); border: 1px solid rgba(255,255,255,0.07);
                    color: rgba(255,255,255,0.58); font-family: 'Chakra Petch', monospace; font-size: 10px;
                }
                .draft-registered-player button {
                    width: 24px; height: 24px; border-radius: 6px; display: inline-flex; align-items: center; justify-content: center;
                    background: rgba(255,0,42,0.08); border: 1px solid rgba(255,0,42,0.14); color: rgba(255,255,255,0.5); cursor: pointer;
                }
                .draft-registered-player button:hover { color: #FF6B7A; border-color: rgba(255,0,42,0.28); }
                .draft-pick-btn {
                    display: flex; justify-content: space-between; gap: 10px; padding: 9px 10px; border-radius: 8px;
                    border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.7); cursor: pointer; font-size: 11px;
                }
                .draft-pick-btn:hover:not(:disabled) { border-color: rgba(166,0,255,0.25); background: rgba(166,0,255,0.08); }
                .draft-pick-btn:disabled { opacity: 0.45; cursor: not-allowed; }
                .team-signup { display: flex; gap: 10px; flex-wrap: wrap; margin-bottom: 24px; align-items: center; }
                .draft-signup { display: flex; gap: 10px; flex-wrap: wrap; align-items: end; }
                .draft-role-modal-overlay {
                    position: fixed; inset: 0; z-index: 2100;
                    display: flex; align-items: center; justify-content: center;
                    padding: 20px; background: rgba(0,0,0,0.78); backdrop-filter: blur(8px);
                }
                .draft-role-modal {
                    width: min(440px, 100%); border-radius: 12px;
                    background: rgba(8,8,14,0.96); border: 1px solid rgba(166,0,255,0.18);
                    padding: 20px; box-shadow: 0 24px 80px rgba(0,0,0,0.45);
                }
                .draft-role-modal-head {
                    display: flex; justify-content: space-between; gap: 16px; align-items: flex-start;
                    margin-bottom: 18px;
                }
                .draft-role-modal-head h2 {
                    margin: 0; font-family: 'Russo One', sans-serif; font-size: 14px; color: #fff; letter-spacing: 0.06em;
                    text-transform: uppercase;
                }
                .draft-role-modal-head p {
                    margin: 6px 0 0; font-family: 'Chakra Petch', monospace; font-size: 11px; color: rgba(255,255,255,0.4);
                }
                .draft-modal-close {
                    display: inline-flex; align-items: center; gap: 6px; padding: 7px 10px; border-radius: 7px;
                    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
                    color: rgba(255,255,255,0.55); font-family: 'Chakra Petch', monospace; font-size: 11px; cursor: pointer;
                }
                .draft-role-error {
                    margin: 12px 0 0; font-family: 'Chakra Petch', monospace; font-size: 11px; color: #FF6B7A;
                }
                .draft-role-submit {
                    width: 100%; min-height: 40px; margin-top: 18px; border-radius: 9px;
                    display: inline-flex; align-items: center; justify-content: center; gap: 7px;
                    background: rgba(166,0,255,0.15); border: 1px solid rgba(166,0,255,0.32);
                    color: #fff; font-family: 'Chakra Petch', monospace; font-size: 12px; cursor: pointer;
                }
                .draft-role-submit:hover:not(:disabled) { background: rgba(166,0,255,0.24); }
                .draft-role-submit:disabled { opacity: 0.45; cursor: not-allowed; }
                .draft-role-select {
                    display: flex; flex-direction: column; gap: 5px; min-width: 140px;
                    font-family: 'Chakra Petch', monospace; font-size: 10px; color: rgba(255,255,255,0.45);
                    text-transform: uppercase; letter-spacing: 0.05em;
                }
                .draft-role-select select {
                    min-height: 34px; padding: 7px 9px; border-radius: 8px;
                    background: rgba(255,255,255,0.04); border: 1px solid rgba(255,255,255,0.08);
                    color: #fff; font-family: 'Chakra Petch', monospace; font-size: 12px; text-transform: none;
                }
                .team-select {
                    min-width: 220px; padding: 8px 10px; border-radius: 8px; background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.08); color: #fff; font-family: 'Chakra Petch', monospace; font-size: 12px;
                }
                @media (max-width: 900px) {
                    .draft-layout { grid-template-columns: 1fr; }
                    .draft-summary-row { grid-template-columns: repeat(2, minmax(0, 1fr)); }
                    .draft-row { grid-template-columns: 40px minmax(0, 1fr); }
                    .draft-rank, .draft-role { justify-self: start; grid-column: 2; text-align: left; }
                }
            `}</style>

            <div className="td-page">
                <button className="td-back" onClick={() => navigate({ to: '/tournaments' })}>
                    <FiArrowLeft size={14} /> Back to Tournaments
                </button>

                <div className="td-header">
                    <div>
                        <h1 className="td-title">{tournament.prizepool}</h1>
                        <div className="td-meta" style={{ marginTop: '12px' }}>
                            <span className="td-meta-item"><FiUsers size={13} /> {tournament.participant_pool.length} {isDraftTournament ? 'players' : 'teams'}</span>
                            <span className="td-meta-item"><FiClock size={13} /> {startDate.toLocaleDateString()} {startDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                            <span className="td-meta-item"><FiAward size={13} /> Hosted by {getTeamLabel(tournament.host)}</span>
                        </div>
                    </div>
                    <span className="td-status" style={{ background: `${statusColor}15`, color: statusColor, border: `1px solid ${statusColor}30` }}>
                        {tournament.status}
                    </span>
                </div>

                {isDraftTournament ? (
                    <div style={{ display: 'flex', gap: '10px', flexWrap: 'wrap', marginBottom: '24px' }}>
                        {user && !isParticipant && (
                            <DraftSignup
                                tournamentId={tournament.id}
                                userId={user.id}
                                isPending={addParticipantMutation.isPending}
                                onJoin={handleJoinTournament}
                            />
                        )}
                    </div>
                ) : user ? (
                    <PresignedSignup userId={user.id} onJoin={handleJoinTeamTournament} isPending={addParticipantMutation.isPending} />
                ) : null}

                {isHost && user && (
                    <div className="host-panel">
                        <div className="host-flow">
                            {['registration_open', isDraftTournament ? 'captain_setup' : 'registration_locked', isDraftTournament ? 'draft_finished' : 'bracket_ready', 'tournament_active'].map(step => (
                                <span key={step} className={`flow-chip ${tournament.lifecycle === step ? 'active' : ''}`}>{step.replace(/_/g, ' ')}</span>
                            ))}
                        </div>
                        <div className="host-actions">
                            <button className="fullscreen-btn" onClick={() => lockRegistrationMutation.mutateAsync(user.id)} disabled={!canLockRegistration || lockRegistrationMutation.isPending}>
                                <FiLock size={12} /> {lockRegistrationMutation.isPending ? 'Locking...' : 'Lock registration'}
                            </button>
                            <button className="fullscreen-btn" onClick={() => prebuildBracketMutation.mutateAsync({ actorId: user.id })} disabled={!canGenerateBracket || prebuildBracketMutation.isPending}>
                                <FiAward size={12} /> {prebuildBracketMutation.isPending ? 'Building...' : 'Generate bracket'}
                            </button>
                            <button className="fullscreen-btn" onClick={() => startTournamentMutation.mutateAsync(user.id)} disabled={!canStartTournament || startTournamentMutation.isPending}>
                                <FiClock size={12} /> {startTournamentMutation.isPending ? 'Starting...' : 'Start tournament'}
                            </button>
                        </div>
                        {isDraftTournament && !isDraftPoolLockable && tournament.lifecycle === 'registration_open' && (
                            <p className="flow-error">Draft pool must contain enough players for at least two {tournamentTeamSize}v{tournamentTeamSize} teams before registration lock.</p>
                        )}
                        <div className="reschedule-panel">
                            <label>
                                <span>Start date</span>
                                <input type="date" value={rescheduleDate} onChange={event => setRescheduleDate(event.target.value)} />
                            </label>
                            <label>
                                <span>Start time</span>
                                <input type="time" value={rescheduleTime} onChange={event => setRescheduleTime(event.target.value)} />
                            </label>
                            {isDraftTournament && (
                                <>
                                    <label>
                                        <span>Draft date</span>
                                        <input type="date" value={rescheduleDraftDate} onChange={event => setRescheduleDraftDate(event.target.value)} />
                                    </label>
                                    <label>
                                        <span>Draft time</span>
                                        <input type="time" value={rescheduleDraftTime} onChange={event => setRescheduleDraftTime(event.target.value)} />
                                    </label>
                                </>
                            )}
                            <button className="fullscreen-btn" onClick={handleReschedule} disabled={!rescheduleDate || !rescheduleTime || rescheduleMutation.isPending}>
                                <FiClock size={12} /> {rescheduleMutation.isPending ? 'Saving...' : 'Reschedule'}
                            </button>
                        </div>
                        {flowError && <p className="flow-error">{flowError}</p>}
                    </div>
                )}

                <div className="td-section">
                    <div className="td-section-header">
                        <h3 className="td-section-title">Bracket</h3>
                        <button className="fullscreen-btn" onClick={() => setShowFullBracket(true)}>
                            <FiMaximize2 size={12} /> Fullscreen
                        </button>
                    </div>
                    <BracketView tournament={tournament} />
                </div>

                <div className="td-section">
                    {isDraftTournament ? (
                        <DraftBoard
                            tournament={tournament}
                            players={tournamentUsers ?? []}
                            isHost={isHost}
                            actorId={user?.id}
                            participantInfo={participantInfo?.participants ?? []}
                            onRemovePlayer={(playerId) => removeParticipant({ id: playerId, type: 'user' })}
                        />
                    ) : (
                        <>
                            <h3 className="td-section-title" style={{ marginBottom: '18px' }}>Registered teams ({tournament.participant_pool.length})</h3>
                            <div className="participants-grid">
                                {tournament.participant_pool.length > 0 ? tournament.participant_pool.map((p, i) => (
                                    <div key={i} className="participant-card">
                                        <div className="participant-avatar">
                                            {getTeamLabel(p.actor).charAt(0)}
                                        </div>
                                        <div>
                                            <p style={{ margin: 0, color: 'rgba(255,255,255,0.8)', fontSize: '13px', fontWeight: 500 }}>{getTeamLabel(p.actor)}</p>
                                            <p style={{ margin: '2px 0 0', fontSize: '10px', color: 'rgba(255,255,255,0.3)' }}>{p.players.length} players</p>
                                        </div>
                                        {isHost && tournament.status === 'scheduled' && (
                                            <button className="participant-remove" onClick={() => removeParticipant(p.actor)} disabled={removeParticipantMutation.isPending} aria-label="Remove participant">
                                                <FiTrash2 size={13} />
                                            </button>
                                        )}
                                    </div>
                                )) : <p style={{ margin: 0, color: 'rgba(255,255,255,0.25)', fontFamily: "'Chakra Petch', monospace", fontSize: '12px' }}>No teams yet</p>}
                            </div>
                        </>
                    )}
                </div>

                <div className="td-section">
                    <h3 className="td-section-title" style={{ marginBottom: '18px' }}>Settings</h3>
                    <div className="settings-grid">
                        <div className="setting-item">
                            <p className="setting-label">Type</p>
                            <p className="setting-value">{isDraftTournament ? 'Captain Draft' : 'Team Signup'}</p>
                        </div>
                        <div className="setting-item">
                            <p className="setting-label">Format</p>
                            <p className="setting-value">{tournament.settings.game_settings.team_size}v{tournament.settings.game_settings.team_size}</p>
                        </div>
                        <div className="setting-item">
                            <p className="setting-label">Bracket</p>
                            <p className="setting-value">{tournament.settings.bracket_type.replace(/_/g, ' ')}</p>
                        </div>
                        <div className="setting-item">
                            <p className="setting-label">Draft</p>
                            <p className="setting-value">{tournament.settings.game_series_settings.draft_type}</p>
                        </div>
                        <div className="setting-item">
                            <p className="setting-label">Series</p>
                            <p className="setting-value">Bo{tournament.settings.best_of.join(' / Bo')}</p>
                        </div>
                        <div className="setting-item">
                            <p className="setting-label">Registration</p>
                            <p className="setting-value">{tournament.is_open ? 'Open' : 'Closed'}</p>
                        </div>
                        <div className="setting-item">
                            <p className="setting-label">Map</p>
                            <p className="setting-value">Summoner's Rift</p>
                        </div>
                    </div>
                </div>
            </div>

            {showFullBracket && <BracketModal tournament={tournament} onClose={() => setShowFullBracket(false)} />}
        </>
    )
}
