import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState, useEffect, useCallback, useContext } from 'react'
import { FiArrowLeft } from 'react-icons/fi'
import { CHAMPION_NAMES } from '../lib/api'
import { SocialDockContext } from './__root'

export const Route = createFileRoute('/gameseries/$id/draft')({ component: DraftPage })

const BLUE = '#06B6D4'
const RED = '#FF002A'


// Draft order: CLASSIC_5_DRAFT
const DRAFT_ORDER: { team: 'blue' | 'red'; action: 'ban' | 'pick' }[] = [
    { team: 'blue', action: 'ban' }, { team: 'red', action: 'ban' },
    { team: 'blue', action: 'ban' }, { team: 'red', action: 'ban' },
    { team: 'blue', action: 'ban' }, { team: 'red', action: 'ban' },
    { team: 'blue', action: 'pick' }, { team: 'red', action: 'pick' },
    { team: 'red', action: 'pick' }, { team: 'blue', action: 'pick' },
    { team: 'blue', action: 'pick' }, { team: 'red', action: 'pick' },
    { team: 'red', action: 'ban' }, { team: 'blue', action: 'ban' },
    { team: 'red', action: 'ban' }, { team: 'blue', action: 'ban' },
    { team: 'red', action: 'pick' }, { team: 'blue', action: 'pick' },
    { team: 'blue', action: 'pick' }, { team: 'red', action: 'pick' },
]

const ALL_CHAMPIONS = Object.entries(CHAMPION_NAMES).map(([id, name]) => ({ id: +id, name }))

function DraftPage() {
    const navigate = useNavigate()
    const { id } = Route.useParams()
    const { open: dockOpen } = useContext(SocialDockContext)
    const [stage, setStage] = useState(0)
    const [selected, setSelected] = useState<number | null>(null)
    const [blueBans, setBlueBans] = useState<number[]>([])
    const [redBans, setRedBans] = useState<number[]>([])
    const [bluePicks, setBluePicks] = useState<number[]>([])
    const [redPicks, setRedPicks] = useState<number[]>([])
    const [timer, setTimer] = useState(30)

    const currentStage = DRAFT_ORDER[stage]
    const isComplete = stage >= DRAFT_ORDER.length

    const usedChampions = new Set([...blueBans, ...redBans, ...bluePicks, ...redPicks])

    useEffect(() => {
        if (isComplete) return
        setTimer(30)
        const interval = setInterval(() => {
            setTimer(t => {
                if (t <= 1) { clearInterval(interval); return 0 }
                return t - 1
            })
        }, 1000)
        return () => clearInterval(interval)
    }, [stage, isComplete])

    // Simulate opponent picks (red side auto-picks after 2s)
    useEffect(() => {
        if (isComplete || !currentStage || currentStage.team !== 'red') return
        const timeout = setTimeout(() => {
            const available = ALL_CHAMPIONS.filter(c => !usedChampions.has(c.id))
            if (available.length === 0) return
            const pick = available[Math.floor(Math.random() * available.length)]
            confirmPick(pick.id)
        }, 1500)
        return () => clearTimeout(timeout)
    }, [stage])

    const confirmPick = useCallback((champId: number) => {
        if (isComplete) return
        const s = DRAFT_ORDER[stage]
        if (s.action === 'ban') {
            if (s.team === 'blue') setBlueBans(p => [...p, champId])
            else setRedBans(p => [...p, champId])
        } else {
            if (s.team === 'blue') setBluePicks(p => [...p, champId])
            else setRedPicks(p => [...p, champId])
        }
        setSelected(null)
        setStage(st => st + 1)
    }, [stage, isComplete])

    const handleConfirm = () => {
        if (selected === null || !currentStage || currentStage.team !== 'blue') return
        confirmPick(selected)
    }

    return (
        <>
            <style>{`
                .draft-page {
                    position: relative; z-index: 10;
                    height: calc(100vh - 52px); margin-top: 52px;
                    display: flex; flex-direction: column; overflow: hidden;
                    background: rgba(0,0,0,0.6);
                    padding-right: ${dockOpen ? '240px' : '0'};
                }
                .draft-header {
                    display: flex; justify-content: space-between; align-items: center;
                    padding: 12px 24px; border-bottom: 1px solid rgba(255,255,255,0.04);
                }
                .draft-back {
                    display: flex; align-items: center; gap: 6px;
                    font-family: 'Chakra Petch', monospace; font-size: 11px;
                    color: rgba(255,255,255,0.4); background: none; border: none; cursor: pointer;
                }
                .draft-back:hover { color: rgba(255,255,255,0.7); }
                .draft-timer {
                    font-family: 'Russo One', sans-serif; font-size: 20px;
                    color: ${timer <= 10 ? RED : 'rgba(255,255,255,0.7)'};
                    min-width: 40px; text-align: center;
                }
                .draft-phase {
                    font-family: 'Chakra Petch', monospace; font-size: 11px;
                    color: rgba(255,255,255,0.4); letter-spacing: 0.1em; text-transform: uppercase;
                }
                .draft-main {
                    flex: 1; display: flex; overflow: hidden;
                }
                .draft-side {
                    width: 220px; flex-shrink: 0; display: flex; flex-direction: column;
                    padding: 16px; gap: 6px;
                }
                .draft-side-title {
                    font-family: 'Russo One', sans-serif; font-size: 11px;
                    letter-spacing: 0.1em; margin: 0 0 8px; text-transform: uppercase;
                }
                .draft-slot {
                    padding: 8px 12px; border-radius: 6px; font-family: 'Chakra Petch', monospace;
                    font-size: 11px; display: flex; align-items: center; justify-content: space-between;
                }
                .draft-slot.ban { text-decoration: line-through; opacity: 0.5; }
                .draft-slot.empty { border-style: dashed; opacity: 0.3; }
                .draft-slot.active-slot { animation: pulse-border 1s infinite; }
                @keyframes pulse-border { 0%,100% { opacity: 0.6; } 50% { opacity: 1; } }
                .draft-center {
                    flex: 1; display: flex; flex-direction: column; min-width: 0;
                    border-left: 1px solid rgba(255,255,255,0.04);
                    border-right: 1px solid rgba(255,255,255,0.04);
                }
                .draft-grid-wrap {
                    flex: 1; overflow-y: auto; padding: 12px;
                }
                .draft-grid {
                    display: grid; grid-template-columns: repeat(auto-fill, minmax(80px, 1fr));
                    gap: 6px;
                }
                .champ-btn {
                    padding: 8px 6px; border-radius: 6px; font-family: 'Chakra Petch', monospace;
                    font-size: 10px; text-align: center; cursor: pointer;
                    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06);
                    color: rgba(255,255,255,0.7); transition: all 150ms;
                    white-space: nowrap; overflow: hidden; text-overflow: ellipsis;
                }
                .champ-btn:hover:not(:disabled) { background: rgba(166,0,255,0.08); border-color: rgba(166,0,255,0.2); }
                .champ-btn.selected { background: rgba(166,0,255,0.15); border-color: rgba(166,0,255,0.4); color: #fff; }
                .champ-btn:disabled { opacity: 0.2; cursor: not-allowed; }
                .draft-confirm-row {
                    padding: 12px 16px; border-top: 1px solid rgba(255,255,255,0.04);
                    display: flex; justify-content: center;
                }
                .confirm-btn {
                    padding: 10px 32px; border-radius: 8px;
                    font-family: 'Russo One', sans-serif; font-size: 12px;
                    letter-spacing: 0.08em; cursor: pointer; transition: all 180ms;
                }
                .confirm-btn.blue-turn {
                    background: rgba(6,182,212,0.15); border: 1px solid rgba(6,182,212,0.3); color: ${BLUE};
                }
                .confirm-btn.blue-turn:hover:not(:disabled) { background: rgba(6,182,212,0.25); box-shadow: 0 0 16px rgba(6,182,212,0.2); }
                .confirm-btn:disabled { opacity: 0.3; cursor: not-allowed; }
                .confirm-btn.waiting { background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.06); color: rgba(255,255,255,0.3); }
                .draft-logo {
                    width: 40px; height: 40px; border-radius: 10px;
                    display: flex; align-items: center; justify-content: center;
                    font-family: 'Russo One', sans-serif; font-size: 16px; font-weight: 700;
                    margin: 0 auto 8px;
                }
            `}</style>

            <div className="draft-page">
                <div className="draft-header">
                    <button className="draft-back" onClick={() => navigate({ to: '/gameseries/$id', params: { id } })}>
                        <FiArrowLeft size={13} /> Back
                    </button>
                    <span className="draft-phase">
                        {isComplete ? 'DRAFT COMPLETE' : `${currentStage.team.toUpperCase()} ${currentStage.action.toUpperCase()}`}
                    </span>
                    <span className="draft-timer">{isComplete ? '✓' : timer}</span>
                </div>

                <div className="draft-main">
                    {/* Blue side */}
                    <div className="draft-side" style={{ background: 'rgba(6,182,212,0.02)' }}>
                        <div className="draft-logo" style={{ background: 'rgba(6,182,212,0.1)', border: '1px solid rgba(6,182,212,0.3)', color: BLUE, boxShadow: `0 0 12px rgba(6,182,212,0.15)` }}>A</div>
                        <p className="draft-side-title" style={{ color: BLUE }}>Shadow Wolves</p>
                        <p style={{ fontSize: '9px', color: 'rgba(255,255,255,0.25)', fontFamily: "'Chakra Petch', monospace", margin: '0 0 4px', letterSpacing: '0.1em' }}>BANS</p>
                        {Array.from({ length: 5 }).map((_, i) => (
                            <div key={`bb${i}`} className={`draft-slot ban ${!blueBans[i] ? 'empty' : ''} ${!isComplete && currentStage?.team === 'blue' && currentStage.action === 'ban' && blueBans.length === i ? 'active-slot' : ''}`}
                                style={{ background: 'rgba(6,182,212,0.04)', border: '1px solid rgba(6,182,212,0.1)', color: 'rgba(6,182,212,0.6)' }}>
                                {blueBans[i] ? CHAMPION_NAMES[blueBans[i]] || `#${blueBans[i]}` : '—'}
                            </div>
                        ))}
                        <p style={{ fontSize: '9px', color: 'rgba(255,255,255,0.25)', fontFamily: "'Chakra Petch', monospace", margin: '8px 0 4px', letterSpacing: '0.1em' }}>PICKS</p>
                        {Array.from({ length: 5 }).map((_, i) => (
                            <div key={`bp${i}`} className={`draft-slot ${!bluePicks[i] ? 'empty' : ''} ${!isComplete && currentStage?.team === 'blue' && currentStage.action === 'pick' && bluePicks.length === i ? 'active-slot' : ''}`}
                                style={{ background: 'rgba(6,182,212,0.06)', border: '1px solid rgba(6,182,212,0.15)', color: BLUE }}>
                                {bluePicks[i] ? CHAMPION_NAMES[bluePicks[i]] || `#${bluePicks[i]}` : '—'}
                            </div>
                        ))}
                    </div>

                    {/* Center: champion grid */}
                    <div className="draft-center">
                        <div className="draft-grid-wrap">
                            <div className="draft-grid">
                                {ALL_CHAMPIONS.map(c => (
                                    <button
                                        key={c.id}
                                        className={`champ-btn ${selected === c.id ? 'selected' : ''}`}
                                        disabled={usedChampions.has(c.id) || isComplete || currentStage?.team !== 'blue'}
                                        onClick={() => setSelected(c.id)}
                                    >
                                        {c.name}
                                    </button>
                                ))}
                            </div>
                        </div>
                        <div className="draft-confirm-row">
                            {!isComplete && currentStage?.team === 'blue' ? (
                                <button className="confirm-btn blue-turn" onClick={handleConfirm} disabled={selected === null}>
                                    LOCK IN
                                </button>
                            ) : !isComplete ? (
                                <button className="confirm-btn waiting" disabled>OPPONENT PICKING...</button>
                            ) : (
                                <button className="confirm-btn blue-turn" onClick={() => navigate({ to: '/gameseries/$id', params: { id } })}>
                                    CONTINUE
                                </button>
                            )}
                        </div>
                    </div>

                    {/* Red side */}
                    <div className="draft-side" style={{ background: 'rgba(255,0,42,0.02)' }}>
                        <div className="draft-logo" style={{ background: 'rgba(255,0,42,0.08)', border: '1px solid rgba(255,0,42,0.3)', color: RED, boxShadow: `0 0 12px rgba(255,0,42,0.15)` }}>A</div>
                        <p className="draft-side-title" style={{ color: RED }}>Neon Dragons</p>
                        <p style={{ fontSize: '9px', color: 'rgba(255,255,255,0.25)', fontFamily: "'Chakra Petch', monospace", margin: '0 0 4px', letterSpacing: '0.1em' }}>BANS</p>
                        {Array.from({ length: 5 }).map((_, i) => (
                            <div key={`rb${i}`} className={`draft-slot ban ${!redBans[i] ? 'empty' : ''} ${!isComplete && currentStage?.team === 'red' && currentStage.action === 'ban' && redBans.length === i ? 'active-slot' : ''}`}
                                style={{ background: 'rgba(255,0,42,0.04)', border: '1px solid rgba(255,0,42,0.1)', color: 'rgba(255,0,42,0.6)' }}>
                                {redBans[i] ? CHAMPION_NAMES[redBans[i]] || `#${redBans[i]}` : '—'}
                            </div>
                        ))}
                        <p style={{ fontSize: '9px', color: 'rgba(255,255,255,0.25)', fontFamily: "'Chakra Petch', monospace", margin: '8px 0 4px', letterSpacing: '0.1em' }}>PICKS</p>
                        {Array.from({ length: 5 }).map((_, i) => (
                            <div key={`rp${i}`} className={`draft-slot ${!redPicks[i] ? 'empty' : ''} ${!isComplete && currentStage?.team === 'red' && currentStage.action === 'pick' && redPicks.length === i ? 'active-slot' : ''}`}
                                style={{ background: 'rgba(255,0,42,0.06)', border: '1px solid rgba(255,0,42,0.12)', color: RED }}>
                                {redPicks[i] ? CHAMPION_NAMES[redPicks[i]] || `#${redPicks[i]}` : '—'}
                            </div>
                        ))}
                    </div>
                </div>
            </div>
        </>
    )
}
