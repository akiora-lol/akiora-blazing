import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { FiArrowLeft } from 'react-icons/fi'
import {
    useGameSeries,
    CHAMPION_NAMES,
    type GameResponse, type DraftResponse, type Actor,
} from '../lib/api'

export const Route = createFileRoute('/gameseries/$id/results')({
    component: GameSeriesPage,
})

const BLUE = '#06B6D4'
const RED = '#FF002A'

const TEAM_NAMES: Record<string, string> = {
    'team-1': 'Shadow Wolves', 'team-2': 'Neon Dragons', 'team-3': 'Ice Phoenix', 'team-4': 'Dark Reapers',
    'team-5': 'Storm Riders', 'team-6': 'Cyber Hawks', 'team-7': 'Blood Ravens', 'team-8': 'Iron Titans',
}

function teamName(actor: Actor | null) {
    if (!actor) return 'TBD'
    return TEAM_NAMES[actor.id] || actor.id.slice(-6)
}

function champName(id: number) {
    return CHAMPION_NAMES[id] || `Champ #${id}`
}

function formatDuration(start: number, end: number | null) {
    if (!end) return 'In progress'
    const s = end - start
    return `${Math.floor(s / 60)}m ${s % 60}s`
}

function DraftView({ draft }: { draft: DraftResponse }) {
    const blueBans: number[] = []
    const redBans: number[] = []
    const bluePicks: number[] = []
    const redPicks: number[] = []

    for (const cmd of draft.history) {
        if (cmd.team.type === 'blue') {
            if (cmd.action.type === 'ban') blueBans.push(cmd.action.champion_id)
            else bluePicks.push(cmd.action.champion_id)
        } else {
            if (cmd.action.type === 'ban') redBans.push(cmd.action.champion_id)
            else redPicks.push(cmd.action.champion_id)
        }
    }

    return (
        <div className="draft-view">
            {/* Bans */}
            <div className="draft-section">
                <p className="draft-label">BANS</p>
                <div className="draft-row">
                    <div className="ban-list blue-side">
                        {blueBans.map((c, i) => (
                            <span key={i} className="ban-chip blue-ban">{champName(c)}</span>
                        ))}
                    </div>
                    <div className="ban-list red-side">
                        {redBans.map((c, i) => (
                            <span key={i} className="ban-chip red-ban">{champName(c)}</span>
                        ))}
                    </div>
                </div>
            </div>

            {/* Picks */}
            <div className="draft-section">
                <p className="draft-label">PICKS</p>
                <div className="draft-row">
                    <div className="pick-list blue-side">
                        {bluePicks.map((c, i) => (
                            <span key={i} className="pick-chip blue-pick">{champName(c)}</span>
                        ))}
                    </div>
                    <div className="pick-list red-side">
                        {redPicks.map((c, i) => (
                            <span key={i} className="pick-chip red-pick">{champName(c)}</span>
                        ))}
                    </div>
                </div>
            </div>
        </div>
    )
}

function GameCard({ game, gameNumber, blueTeamId }: { game: GameResponse; gameNumber: number; blueTeamId: string }) {
    const [expanded, setExpanded] = useState(false)
    const winnerId = game.results[0]?.actor?.id
    const blueWon = winnerId === blueTeamId
    const redWon = winnerId && winnerId !== blueTeamId

    return (
        <div className="game-card">
            <button className="game-header" onClick={() => setExpanded(!expanded)}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '12px' }}>
                    <span className="game-number">Game {gameNumber}</span>
                    <span className="game-status" style={{
                        color: game.status === 'finished' ? 'rgba(255,255,255,0.4)' : '#10B981',
                    }}>
                        {game.status === 'finished' ? formatDuration(game.start, game.end) : game.status.toUpperCase()}
                    </span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    {blueWon && <span className="winner-badge blue-winner">Blue Win</span>}
                    {redWon && <span className="winner-badge red-winner">Red Win</span>}
                    <span style={{ color: 'rgba(255,255,255,0.2)', fontSize: '12px', transition: 'transform 150ms', transform: expanded ? 'rotate(90deg)' : 'none' }}>▶</span>
                </div>
            </button>

            {expanded && game.draft && (
                <div className="game-body">
                    <DraftView draft={game.draft} />
                </div>
            )}
        </div>
    )
}

function GameSeriesPage() {
    const navigate = useNavigate()
    const { id } = Route.useParams()
    const { data: series, isLoading } = useGameSeries(id)

    if (isLoading) return <div className="gs-loading">Loading...</div>
    if (!series) return <div className="gs-loading">Game series not found</div>

    const blueTeam = series.teams[0]
    const redTeam = series.teams[1]
    const blueTeamId = blueTeam?.actor?.id || ''
    const redTeamId = redTeam?.actor?.id || ''

    const blueWins = series.games.filter(g => g.results[0]?.actor?.id === blueTeamId).length
    const redWins = series.games.filter(g => g.results[0]?.actor?.id === redTeamId).length

    return (
        <>
            <style>{`
                .gs-page {
                    position: relative; z-index: 10;
                    min-height: calc(100vh - 52px); margin-top: 52px;
                    padding: 32px clamp(24px, 5vw, 64px);
                    max-width: 900px; margin-left: auto; margin-right: auto;
                }
                .gs-loading {
                    margin-top: 52px; padding: 60px; text-align: center;
                    color: rgba(255,255,255,0.2); font-family: 'Chakra Petch', monospace;
                }
                .gs-back {
                    display: inline-flex; align-items: center; gap: 6px;
                    font-family: 'Chakra Petch', monospace; font-size: 12px;
                    color: rgba(255,255,255,0.4); background: none; border: none;
                    cursor: pointer; margin-bottom: 24px; transition: color 150ms;
                }
                .gs-back:hover { color: rgba(255,255,255,0.7); }

                /* Scoreboard */
                .gs-scoreboard {
                    display: flex; align-items: center; justify-content: center; gap: 0;
                    margin-bottom: 32px; padding: 24px; border-radius: 14px;
                    background: rgba(0,0,0,0.35); border: 1px solid rgba(166,0,255,0.08);
                    backdrop-filter: blur(8px);
                }
                .gs-team {
                    flex: 1; display: flex; flex-direction: column; align-items: center; gap: 6px;
                }
                .gs-team-name {
                    font-family: 'Chakra Petch', monospace; font-size: 15px; font-weight: 600;
                }
                .gs-team-label {
                    font-family: 'Chakra Petch', monospace; font-size: 9px; letter-spacing: 0.15em;
                    text-transform: uppercase; font-weight: 600;
                }
                .gs-score-center {
                    display: flex; align-items: center; gap: 12px; padding: 0 24px;
                }
                .gs-score {
                    font-family: 'Russo One', sans-serif; font-size: 32px;
                }
                .gs-score-sep {
                    font-family: 'Russo One', sans-serif; font-size: 20px; color: rgba(255,255,255,0.15);
                }
                .gs-series-info {
                    font-family: 'Chakra Petch', monospace; font-size: 11px; color: rgba(255,255,255,0.3);
                    text-align: center; margin-top: 8px;
                }

                /* Games list */
                .gs-games-title {
                    font-family: 'Russo One', sans-serif; font-size: 13px;
                    color: rgba(255,255,255,0.7); letter-spacing: 0.06em;
                    text-transform: uppercase; margin: 0 0 16px;
                }
                .game-card {
                    margin-bottom: 8px; border-radius: 10px; overflow: hidden;
                    background: rgba(0,0,0,0.3); border: 1px solid rgba(166,0,255,0.08);
                }
                .game-header {
                    width: 100%; display: flex; justify-content: space-between; align-items: center;
                    padding: 14px 18px; background: none; border: none; cursor: pointer;
                    font-family: 'Chakra Petch', monospace; transition: background 150ms;
                }
                .game-header:hover { background: rgba(166,0,255,0.04); }
                .game-number { font-size: 13px; font-weight: 600; color: rgba(255,255,255,0.85); }
                .game-status { font-size: 11px; }
                .winner-badge {
                    font-size: 10px; font-weight: 600; padding: 3px 8px;
                    border-radius: 4px; letter-spacing: 0.05em;
                }
                .blue-winner { background: rgba(6,182,212,0.12); color: ${BLUE}; border: 1px solid rgba(6,182,212,0.2); }
                .red-winner { background: rgba(255,0,42,0.1); color: ${RED}; border: 1px solid rgba(255,0,42,0.2); }

                .game-body { padding: 0 18px 18px; }

                /* Draft */
                .draft-view { display: flex; flex-direction: column; gap: 16px; }
                .draft-section {}
                .draft-label {
                    font-family: 'Chakra Petch', monospace; font-size: 9px;
                    color: rgba(255,255,255,0.25); letter-spacing: 0.15em;
                    margin: 0 0 8px; font-weight: 600;
                }
                .draft-row {
                    display: flex; gap: 16px; justify-content: space-between;
                }
                .ban-list, .pick-list {
                    display: flex; gap: 4px; flex-wrap: wrap; flex: 1;
                }
                .blue-side { justify-content: flex-start; }
                .red-side { justify-content: flex-end; }
                .ban-chip, .pick-chip {
                    font-family: 'Chakra Petch', monospace; font-size: 10px;
                    padding: 4px 8px; border-radius: 4px; white-space: nowrap;
                }
                .blue-ban {
                    background: rgba(6,182,212,0.06); color: rgba(6,182,212,0.5);
                    border: 1px solid rgba(6,182,212,0.1); text-decoration: line-through;
                }
                .red-ban {
                    background: rgba(255,0,42,0.06); color: rgba(255,0,42,0.5);
                    border: 1px solid rgba(255,0,42,0.1); text-decoration: line-through;
                }
                .blue-pick {
                    background: rgba(6,182,212,0.1); color: ${BLUE};
                    border: 1px solid rgba(6,182,212,0.2);
                }
                .red-pick {
                    background: rgba(255,0,42,0.08); color: ${RED};
                    border: 1px solid rgba(255,0,42,0.15);
                }
            `}</style>

            <div className="gs-page">
                <button className="gs-back" onClick={() => navigate({ to: '/tournaments/$id', params: { id: series.tournament_id } })}>
                    <FiArrowLeft size={14} /> Back to Tournament
                </button>

                {/* Scoreboard */}
                <div className="gs-scoreboard">
                    <div className="gs-team">
                        <span className="gs-team-label" style={{ color: BLUE }}>BLUE SIDE</span>
                        <span className="gs-team-name" style={{ color: BLUE }}>{teamName(blueTeam?.actor)}</span>
                    </div>
                    <div className="gs-score-center">
                        <span className="gs-score" style={{ color: BLUE }}>{blueWins}</span>
                        <span className="gs-score-sep">:</span>
                        <span className="gs-score" style={{ color: RED }}>{redWins}</span>
                    </div>
                    <div className="gs-team">
                        <span className="gs-team-label" style={{ color: RED }}>RED SIDE</span>
                        <span className="gs-team-name" style={{ color: RED }}>{teamName(redTeam?.actor)}</span>
                    </div>
                </div>
                <p className="gs-series-info">Best of {series.settings.best_of} • {series.settings.draft_type} draft • {series.status}</p>

                {/* Games */}
                <h3 className="gs-games-title" style={{ marginTop: '28px' }}>Games ({series.games.length})</h3>
                {series.games.map((game, i) => (
                    <GameCard key={game.id} game={game} gameNumber={i + 1} blueTeamId={blueTeamId} />
                ))}
            </div>
        </>
    )
}
