import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { FiSend } from 'react-icons/fi'
import { useGameSeries, type Actor } from '../lib/api'

export const Route = createFileRoute('/gameseries/$id/')({ component: GameSeriesLobby })

const BLUE = '#06B6D4'
const RED = '#FF002A'

const TEAM_NAMES: Record<string, string> = {
    'team-1': 'Shadow Wolves', 'team-2': 'Neon Dragons', 'team-3': 'Ice Phoenix', 'team-4': 'Dark Reapers',
    'team-5': 'Storm Riders', 'team-6': 'Cyber Hawks', 'team-7': 'Blood Ravens', 'team-8': 'Iron Titans',
}

const PLAYER_NAMES = [
    ['xShadow', 'NightBlade', 'ColdSteel', 'FuryWolf', 'VoidHunter'],
    ['NeonX', 'DrakeSlayer', 'IceVein', 'PhantomKing', 'StormBreaker'],
]

function teamName(actor: Actor | null) {
    if (!actor) return 'TBD'
    return TEAM_NAMES[actor.id] || actor.id.slice(-6)
}

const MOCK_CHAT = [
    { id: '1', user: 'NeonX', msg: 'gl hf', team: 'red' as const, ts: '2m ago' },
    { id: '2', user: 'xShadow', msg: 'gg lets go', team: 'blue' as const, ts: '1m ago' },
    { id: '3', user: 'DrakeSlayer', msg: 'ban yasuo pls', team: 'red' as const, ts: '30s ago' },
]

function GameSeriesLobby() {
    const navigate = useNavigate()
    const { id } = Route.useParams()
    const { data: series } = useGameSeries(id)
    const [chatMsg, setChatMsg] = useState('')
    const [isReady, setIsReady] = useState(false)

    const blueTeam = series?.teams[0]
    const redTeam = series?.teams[1]

    const handleReady = () => {
        setIsReady(true)
        setTimeout(() => {
            navigate({ to: '/gameseries/$id/draft', params: { id } })
        }, 1000)
    }

    return (
        <>
            <style>{`
                .lobby-page {
                    position: relative; z-index: 10;
                    height: calc(100vh - 52px); margin-top: 52px;
                    display: flex; overflow: hidden;
                }
                .lobby-team {
                    flex: 1; display: flex; flex-direction: column;
                    padding: 24px 20px; gap: 8px;
                }
                .lobby-team-header {
                    font-family: 'Russo One', sans-serif; font-size: 14px;
                    letter-spacing: 0.08em; text-transform: uppercase; margin: 0 0 12px;
                }
                .lobby-player {
                    padding: 10px 14px; border-radius: 8px;
                    font-family: 'Chakra Petch', monospace; font-size: 12px;
                    display: flex; align-items: center; gap: 10px;
                }
                .lobby-player-dot {
                    width: 6px; height: 6px; border-radius: 50%;
                }
                .lobby-center {
                    width: 340px; flex-shrink: 0;
                    display: flex; flex-direction: column;
                    border-left: 1px solid rgba(255,255,255,0.04);
                    border-right: 1px solid rgba(255,255,255,0.04);
                    background: rgba(0,0,0,0.3);
                }
                .lobby-chat {
                    flex: 1; overflow-y: auto; padding: 16px;
                    display: flex; flex-direction: column; gap: 8px;
                }
                .lobby-chat-msg {
                    font-family: 'Chakra Petch', monospace; font-size: 11px;
                    padding: 6px 10px; border-radius: 6px;
                    background: rgba(255,255,255,0.03);
                }
                .lobby-chat-msg .chat-user { font-weight: 600; margin-right: 6px; }
                .lobby-input-row {
                    display: flex; gap: 8px; padding: 12px 16px;
                    border-top: 1px solid rgba(255,255,255,0.04);
                }
                .lobby-input {
                    flex: 1; padding: 8px 12px; border-radius: 8px;
                    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
                    color: #fff; font-family: 'Chakra Petch', monospace; font-size: 12px;
                    outline: none;
                }
                .lobby-input:focus { border-color: rgba(166,0,255,0.4); }
                .lobby-send-btn {
                    padding: 8px 12px; border-radius: 8px;
                    background: rgba(166,0,255,0.1); border: 1px solid rgba(166,0,255,0.2);
                    color: rgba(255,255,255,0.7); cursor: pointer; display: flex; align-items: center;
                }
                .lobby-ready-section {
                    padding: 16px; border-top: 1px solid rgba(255,255,255,0.04);
                    display: flex; justify-content: center;
                }
                .ready-btn {
                    width: 100%; padding: 14px; border-radius: 10px;
                    font-family: 'Russo One', sans-serif; font-size: 14px;
                    letter-spacing: 0.1em; text-transform: uppercase;
                    cursor: pointer; transition: all 200ms; border: none;
                }
                .ready-btn:not(.is-ready) {
                    background: linear-gradient(135deg, rgba(16,185,129,0.2), rgba(16,185,129,0.1));
                    border: 1px solid rgba(16,185,129,0.4);
                    color: #10B981;
                }
                .ready-btn:not(.is-ready):hover {
                    background: linear-gradient(135deg, rgba(16,185,129,0.3), rgba(16,185,129,0.15));
                    box-shadow: 0 0 20px rgba(16,185,129,0.2);
                }
                .ready-btn.is-ready {
                    background: rgba(16,185,129,0.15); border: 1px solid rgba(16,185,129,0.3);
                    color: rgba(16,185,129,0.6); cursor: default;
                }
                .lobby-vs {
                    font-family: 'Russo One', sans-serif; font-size: 11px;
                    color: rgba(255,255,255,0.15); text-align: center;
                    padding: 16px 0; letter-spacing: 0.2em;
                }
            `}</style>

            <div className="lobby-page">
                {/* Blue team */}
                <div className="lobby-team" style={{ background: 'rgba(6,182,212,0.02)' }}>
                    <h3 className="lobby-team-header" style={{ color: BLUE }}>{teamName(blueTeam?.actor ?? null)}</h3>
                    {PLAYER_NAMES[0].map((name, i) => (
                        <div key={i} className="lobby-player" style={{ background: 'rgba(6,182,212,0.05)', border: '1px solid rgba(6,182,212,0.1)' }}>
                            <span className="lobby-player-dot" style={{ background: BLUE, boxShadow: `0 0 6px ${BLUE}` }} />
                            <span style={{ color: BLUE }}>{name}</span>
                        </div>
                    ))}
                </div>

                {/* Center: chat + ready */}
                <div className="lobby-center">
                    <p className="lobby-vs">GAME SERIES LOBBY</p>
                    <div className="lobby-chat">
                        {MOCK_CHAT.map(m => (
                            <div key={m.id} className="lobby-chat-msg">
                                <span className="chat-user" style={{ color: m.team === 'blue' ? BLUE : RED }}>{m.user}</span>
                                <span style={{ color: 'rgba(255,255,255,0.6)' }}>{m.msg}</span>
                            </div>
                        ))}
                    </div>
                    <div className="lobby-input-row">
                        <input className="lobby-input" placeholder="Type..." value={chatMsg} onChange={e => setChatMsg(e.target.value)} />
                        <button className="lobby-send-btn"><FiSend size={14} /></button>
                    </div>
                    <div className="lobby-ready-section">
                        <button className={`ready-btn ${isReady ? 'is-ready' : ''}`} onClick={handleReady} disabled={isReady}>
                            {isReady ? 'READY ✓' : 'READY'}
                        </button>
                    </div>
                </div>

                {/* Red team */}
                <div className="lobby-team" style={{ background: 'rgba(255,0,42,0.02)' }}>
                    <h3 className="lobby-team-header" style={{ color: RED }}>{teamName(redTeam?.actor ?? null)}</h3>
                    {PLAYER_NAMES[1].map((name, i) => (
                        <div key={i} className="lobby-player" style={{ background: 'rgba(255,0,42,0.04)', border: '1px solid rgba(255,0,42,0.1)' }}>
                            <span className="lobby-player-dot" style={{ background: RED, boxShadow: `0 0 6px ${RED}` }} />
                            <span style={{ color: RED }}>{name}</span>
                        </div>
                    ))}
                </div>
            </div>
        </>
    )
}
