import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState, useRef } from 'react'
import { FiArrowLeft, FiUsers, FiClock, FiAward, FiMaximize2, FiX } from 'react-icons/fi'
import { type MatchResponse, type Actor, type TournamentResponse, type BracketResponse } from '../lib/api'

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

// Generate 64-team single elimination bracket
function generateMockBracket(): BracketResponse {
    const rounds: MatchResponse[][] = []
    let teamCount = 64

    // Round of 32 (32 matches)
    const r1: MatchResponse[] = []
    for (let i = 0; i < 32; i++) {
        const t1Id = `team-${i * 2 + 1}`
        const t2Id = `team-${i * 2 + 2}`
        const winnerId = i % 3 === 0 ? t2Id : t1Id // mix up winners
        r1.push({ game_series_id: `gs-r1-${i}`, team1: { id: t1Id, type: 'team' }, team2: { id: t2Id, type: 'team' }, winner: { id: winnerId, type: 'team' }, round: 0, match_number: i, next_match_id: Math.floor(i / 2) })
    }
    rounds.push(r1)

    // Round of 16 (16 matches)
    const r2: MatchResponse[] = []
    for (let i = 0; i < 16; i++) {
        const t1 = r1[i * 2].winner!
        const t2 = r1[i * 2 + 1].winner!
        const winner = i % 2 === 0 ? t1 : t2
        r2.push({ game_series_id: `gs-r2-${i}`, team1: t1, team2: t2, winner, round: 1, match_number: i, next_match_id: Math.floor(i / 2) })
    }
    rounds.push(r2)

    // Quarter-finals (8 matches)
    const r3: MatchResponse[] = []
    for (let i = 0; i < 8; i++) {
        const t1 = r2[i * 2].winner!
        const t2 = r2[i * 2 + 1].winner!
        const winner = i < 4 ? t1 : t2
        r3.push({ game_series_id: `gs-r3-${i}`, team1: t1, team2: t2, winner, round: 2, match_number: i, next_match_id: Math.floor(i / 2) })
    }
    rounds.push(r3)

    // Semi-finals (4 matches)
    const r4: MatchResponse[] = []
    for (let i = 0; i < 4; i++) {
        const t1 = r3[i * 2].winner!
        const t2 = r3[i * 2 + 1].winner!
        const winner = i < 2 ? t1 : null
        r4.push({ game_series_id: `gs-r4-${i}`, team1: t1, team2: t2, winner, round: 3, match_number: i, next_match_id: Math.floor(i / 2) })
    }
    rounds.push(r4)

    // Semi-finals top (2 matches)
    const r5: MatchResponse[] = []
    for (let i = 0; i < 2; i++) {
        const t1 = r4[i * 2].winner
        const t2 = r4[i * 2 + 1].winner
        r5.push({ game_series_id: `gs-r5-${i}`, team1: t1, team2: t2, winner: null, round: 4, match_number: i, next_match_id: 0 })
    }
    rounds.push(r5)

    // Grand Final
    rounds.push([
        { game_series_id: 'gs-final', team1: null, team2: null, winner: null, round: 5, match_number: 0, next_match_id: null },
    ])

    return { rounds }
}

const MOCK_BRACKET = generateMockBracket()

const MOCK_TOURNAMENT: TournamentResponse = {
    id: 'tournament-1',
    host: { id: 'user-1', type: 'user' },
    participant_pool: Array.from({ length: 64 }, (_, i) => ({
        actor: { id: `team-${i + 1}`, type: 'team' as const },
        players: Array.from({ length: 5 }, (_, j) => `p${i * 5 + j + 1}`),
    })),
    prizepool: '2000 RP + Victorious Skin',
    is_open: false,
    wait_list: [],
    status: 'active',
    settings: {
        game_settings: { team_size: 5, map: 11 },
        game_series_settings: { game_settings: { team_size: 5, map: 11 }, forbidden_champions: [], best_of: 3, draft_type: 'classic' },
        best_of: [5, 3, 3, 3, 1, 1],
        bracket_type: 'single_elimination',
    },
    start: Math.floor(Date.now() / 1000) - 7200,
    end: null,
    bracket: MOCK_BRACKET,
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

function TournamentDetailPage() {
    const navigate = useNavigate()
    const { id } = Route.useParams()
    const [showFullBracket, setShowFullBracket] = useState(false)

    const tournament = MOCK_TOURNAMENT
    const statusColor = STATUS_COLORS[tournament.status] || '#fff'
    const startDate = new Date(tournament.start * 1000)

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
                .settings-grid { display: grid; grid-template-columns: repeat(auto-fill, minmax(160px, 1fr)); gap: 12px; }
                .setting-item {
                    padding: 14px; border-radius: 10px;
                    background: rgba(0,0,0,0.2); border: 1px solid rgba(255,255,255,0.04);
                }
                .setting-label { font-family: 'Chakra Petch', monospace; font-size: 10px; color: rgba(255,255,255,0.3); letter-spacing: 0.05em; margin: 0 0 6px; text-transform: uppercase; }
                .setting-value { font-family: 'Chakra Petch', monospace; font-size: 14px; color: rgba(255,255,255,0.85); margin: 0; font-weight: 500; text-transform: capitalize; }
            `}</style>

            <div className="td-page">
                <button className="td-back" onClick={() => navigate({ to: '/tournaments' })}>
                    <FiArrowLeft size={14} /> Back to Tournaments
                </button>

                <div className="td-header">
                    <div>
                        <h1 className="td-title">{tournament.prizepool}</h1>
                        <div className="td-meta" style={{ marginTop: '12px' }}>
                            <span className="td-meta-item"><FiUsers size={13} /> {tournament.participant_pool.length} teams</span>
                            <span className="td-meta-item"><FiClock size={13} /> {startDate.toLocaleDateString()} {startDate.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}</span>
                            <span className="td-meta-item"><FiAward size={13} /> Hosted by user-1</span>
                        </div>
                    </div>
                    <span className="td-status" style={{ background: `${statusColor}15`, color: statusColor, border: `1px solid ${statusColor}30` }}>
                        {tournament.status}
                    </span>
                </div>

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
                    <h3 className="td-section-title" style={{ marginBottom: '18px' }}>Participants ({tournament.participant_pool.length})</h3>
                    <div className="participants-grid">
                        {tournament.participant_pool.map((p, i) => (
                            <div key={i} className="participant-card">
                                <div className="participant-avatar">
                                    {getTeamLabel(p.actor).charAt(0)}
                                </div>
                                <div>
                                    <p style={{ margin: 0, color: 'rgba(255,255,255,0.8)', fontSize: '13px', fontWeight: 500 }}>{getTeamLabel(p.actor)}</p>
                                    <p style={{ margin: '2px 0 0', fontSize: '10px', color: 'rgba(255,255,255,0.3)' }}>{p.players.length} players</p>
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="td-section">
                    <h3 className="td-section-title" style={{ marginBottom: '18px' }}>Settings</h3>
                    <div className="settings-grid">
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
