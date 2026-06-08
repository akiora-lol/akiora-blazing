import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { FiPlus, FiX, FiUsers, FiClock, FiAward, FiChevronRight } from 'react-icons/fi'
import { useAuthContext } from '../contexts/AuthContext'
import {
    useTournaments, useCreateTournamentMutation,
    type TournamentResponse, type TournamentStatus, type TournamentType, type BracketType, type DraftType,
    type LolTournamentSettings,
} from '../lib/api'

export const Route = createFileRoute('/tournaments/')({ component: TournamentsPage })

const STATUS_COLORS: Record<TournamentStatus, string> = {
    scheduled: '#06B6D4',
    active: '#10B981',
    finished: 'rgba(255,255,255,0.3)',
    canceled: '#FF002A',
}

const STATUS_LABELS: Record<TournamentStatus, string> = {
    scheduled: 'Scheduled',
    active: 'Live',
    finished: 'Finished',
    canceled: 'Canceled',
}

const BRACKET_LABELS: Record<BracketType, string> = {
    single_elimination: 'Single Elim',
    single_elimination_with_third: 'Single Elim + 3rd',
    double_elimination: 'Double Elim',
    swiss: 'Swiss',
    round_robin: 'Round Robin',
}

const DRAFT_LABELS: Record<DraftType, string> = {
    fearless: 'Fearless',
    iron_man: 'Iron Man',
    classic: 'Classic',
    all_random: 'All Random',
}

const TOURNAMENT_TYPE_LABELS: Record<TournamentType, string> = {
    draft: 'Captain Draft',
    presigned: 'Team Signup',
}

function formatTournamentDate(ts: number) {
    const d = new Date(ts * 1000)
    const now = new Date()
    if (d.toDateString() === now.toDateString()) return `Today ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
    const tomorrow = new Date(now); tomorrow.setDate(tomorrow.getDate() + 1)
    if (d.toDateString() === tomorrow.toDateString()) return `Tomorrow ${d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}`
    return d.toLocaleDateString([], { day: 'numeric', month: 'short' }) + ' ' + d.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function TournamentCard({ tournament, onClick }: { tournament: TournamentResponse; onClick: () => void }) {
    const statusColor = STATUS_COLORS[tournament.status]
    return (
        <button onClick={onClick} className="tournament-card" style={{
            width: '100%', textAlign: 'left', cursor: 'pointer',
            padding: '20px', borderRadius: '14px',
            background: 'rgba(0,0,0,0.35)', border: '1px solid rgba(166,0,255,0.08)',
            backdropFilter: 'blur(12px)', transition: 'all 180ms',
        }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '12px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <div style={{
                        width: '8px', height: '8px', borderRadius: '50%',
                        background: statusColor,
                        boxShadow: tournament.status === 'active' ? `0 0 8px ${statusColor}` : 'none',
                    }} />
                    <span style={{ fontSize: '10px', color: statusColor, fontFamily: "'Chakra Petch', monospace", letterSpacing: '0.1em', textTransform: 'uppercase' }}>
                        {STATUS_LABELS[tournament.status]}
                    </span>
                </div>
                <FiChevronRight size={14} color="rgba(255,255,255,0.2)" />
            </div>

            <p style={{ margin: '0 0 6px', fontSize: '15px', fontWeight: 600, color: '#fff', fontFamily: "'Chakra Petch', monospace" }}>
                {tournament.prizepool}
            </p>

            <div style={{ display: 'flex', gap: '16px', flexWrap: 'wrap', marginTop: '12px' }}>
                <span style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '11px', color: 'rgba(255,255,255,0.4)', fontFamily: "'Chakra Petch', monospace" }}>
                    <FiUsers size={12} /> {tournament.participant_pool.length} teams
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '11px', color: 'rgba(255,255,255,0.4)', fontFamily: "'Chakra Petch', monospace" }}>
                    <FiClock size={12} /> {formatTournamentDate(tournament.start)}
                </span>
                <span style={{ display: 'flex', alignItems: 'center', gap: '5px', fontSize: '11px', color: 'rgba(255,255,255,0.4)', fontFamily: "'Chakra Petch', monospace" }}>
                    <FiAward size={12} /> {BRACKET_LABELS[tournament.settings.bracket_type]}
                </span>
            </div>

            <div style={{ marginTop: '10px', display: 'flex', gap: '6px', flexWrap: 'wrap' }}>
                <span style={{ padding: '3px 8px', borderRadius: '6px', fontSize: '10px', background: 'rgba(166,0,255,0.1)', border: '1px solid rgba(166,0,255,0.15)', color: 'rgba(255,255,255,0.6)', fontFamily: "'Chakra Petch', monospace" }}>
                    {TOURNAMENT_TYPE_LABELS[tournament.settings.tournament_type]}
                </span>
                <span style={{ padding: '3px 8px', borderRadius: '6px', fontSize: '10px', background: 'rgba(166,0,255,0.1)', border: '1px solid rgba(166,0,255,0.15)', color: 'rgba(255,255,255,0.6)', fontFamily: "'Chakra Petch', monospace" }}>
                    {tournament.settings.game_settings.team_size}v{tournament.settings.game_settings.team_size}
                </span>
                <span style={{ padding: '3px 8px', borderRadius: '6px', fontSize: '10px', background: 'rgba(166,0,255,0.1)', border: '1px solid rgba(166,0,255,0.15)', color: 'rgba(255,255,255,0.6)', fontFamily: "'Chakra Petch', monospace" }}>
                    {DRAFT_LABELS[tournament.settings.game_series_settings.draft_type]}
                </span>
                {tournament.is_open && (
                    <span style={{ padding: '3px 8px', borderRadius: '6px', fontSize: '10px', background: 'rgba(16,185,129,0.1)', border: '1px solid rgba(16,185,129,0.2)', color: '#10B981', fontFamily: "'Chakra Petch', monospace" }}>
                        Open
                    </span>
                )}
            </div>
        </button>
    )
}

function CreateTournamentModal({ onClose }: { onClose: () => void }) {
    const { user } = useAuthContext()
    const createMutation = useCreateTournamentMutation()
    const [prizepool, setPrizepool] = useState('')
    const [tournamentType, setTournamentType] = useState<TournamentType>('draft')
    const [teamSize, setTeamSize] = useState(5)
    const [bracketType, setBracketType] = useState<BracketType>('single_elimination')
    const [draftType, setDraftType] = useState<DraftType>('classic')
    const [bestOf, setBestOf] = useState(3)
    const [isOpen, setIsOpen] = useState(true)
    const [startDate, setStartDate] = useState('')
    const [startTime, setStartTime] = useState('')
    const [draftDate, setDraftDate] = useState('')
    const [draftTime, setDraftTime] = useState('')
    const [formError, setFormError] = useState('')

    const handleCreate = async () => {
        if (!prizepool.trim() || !startDate || !startTime || !user) return
        setFormError('')
        const startTs = Math.floor(new Date(`${startDate}T${startTime}`).getTime() / 1000)
        const draftStartTs = tournamentType === 'draft' && draftDate && draftTime
            ? Math.floor(new Date(`${draftDate}T${draftTime}`).getTime() / 1000)
            : null
        if (tournamentType === 'draft') {
            if (!draftStartTs) {
                setFormError('Draft date is required for captain draft tournaments.')
                return
            }
            if (startTs - draftStartTs < 2 * 24 * 60 * 60) {
                setFormError('Tournament start must be at least 2 days after the draft.')
                return
            }
        }
        const settings: LolTournamentSettings = {
            tournament_type: tournamentType,
            game_settings: { team_size: teamSize, map: 11 },
            game_series_settings: { game_settings: { team_size: teamSize, map: 11 }, forbidden_champions: [], best_of: bestOf, draft_type: draftType },
            best_of: [bestOf],
            bracket_type: bracketType,
            draft_start: draftStartTs,
        }
        await createMutation.mutateAsync({
            host: { id: user.id, type: 'user' },
            start: startTs,
            is_open: isOpen,
            prizepool: prizepool.trim(),
            settings,
            draft_start: draftStartTs,
        })
        onClose()
    }

    return (
        <div className="modal-overlay" onClick={onClose} style={{ position: 'fixed', inset: 0, zIndex: 1000, display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'rgba(0,0,0,0.7)', backdropFilter: 'blur(4px)' }}>
            <div onClick={e => e.stopPropagation()} style={{ width: '460px', maxHeight: '85vh', overflowY: 'auto', background: 'rgba(10,0,20,0.95)', border: '1px solid rgba(166,0,255,0.15)', borderRadius: '16px', padding: '28px' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '24px' }}>
                    <h2 style={{ margin: 0, fontFamily: "'Russo One', sans-serif", fontSize: '16px', color: '#fff', letterSpacing: '0.05em' }}>Create Tournament</h2>
                    <button onClick={onClose} style={{ background: 'none', border: 'none', color: 'rgba(255,255,255,0.4)', cursor: 'pointer' }}><FiX size={18} /></button>
                </div>

                <div style={{ display: 'flex', flexDirection: 'column', gap: '16px' }}>
                    <label style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <span className="form-label">Prize Pool</span>
                        <input className="form-input" value={prizepool} onChange={e => setPrizepool(e.target.value)} placeholder="e.g. 1000 RP" />
                    </label>

                    <div style={{ display: 'flex', gap: '12px' }}>
                        <label style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
                            <span className="form-label">Date</span>
                            <input className="form-input" type="date" value={startDate} onChange={e => setStartDate(e.target.value)} />
                        </label>
                        <label style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
                            <span className="form-label">Time</span>
                            <input className="form-input" type="time" value={startTime} onChange={e => setStartTime(e.target.value)} />
                        </label>
                    </div>

                    {tournamentType === 'draft' && (
                        <div style={{ display: 'flex', gap: '12px' }}>
                            <label style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                <span className="form-label">Draft Date</span>
                                <input className="form-input" type="date" value={draftDate} onChange={e => setDraftDate(e.target.value)} />
                            </label>
                            <label style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
                                <span className="form-label">Draft Time</span>
                                <input className="form-input" type="time" value={draftTime} onChange={e => setDraftTime(e.target.value)} />
                            </label>
                        </div>
                    )}

                    <div style={{ display: 'flex', gap: '12px' }}>
                        <label style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
                            <span className="form-label">Team Size</span>
                            <select className="form-input" value={teamSize} onChange={e => setTeamSize(+e.target.value)}>
                                <option value={1}>1v1</option>
                                <option value={2}>2v2</option>
                                <option value={3}>3v3</option>
                                <option value={5}>5v5</option>
                            </select>
                        </label>
                        <label style={{ flex: 1, display: 'flex', flexDirection: 'column', gap: '6px' }}>
                            <span className="form-label">Best Of</span>
                            <select className="form-input" value={bestOf} onChange={e => setBestOf(+e.target.value)}>
                                <option value={1}>Bo1</option>
                                <option value={3}>Bo3</option>
                                <option value={5}>Bo5</option>
                            </select>
                        </label>
                    </div>

                    <label style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <span className="form-label">Tournament Type</span>
                        <select className="form-input" value={tournamentType} onChange={e => setTournamentType(e.target.value as TournamentType)}>
                            {Object.entries(TOURNAMENT_TYPE_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                        </select>
                    </label>

                    <label style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <span className="form-label">Bracket Type</span>
                        <select className="form-input" value={bracketType} onChange={e => setBracketType(e.target.value as BracketType)}>
                            {Object.entries(BRACKET_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                        </select>
                    </label>

                    <label style={{ display: 'flex', flexDirection: 'column', gap: '6px' }}>
                        <span className="form-label">Draft Type</span>
                        <select className="form-input" value={draftType} onChange={e => setDraftType(e.target.value as DraftType)}>
                            {Object.entries(DRAFT_LABELS).map(([k, v]) => <option key={k} value={k}>{v}</option>)}
                        </select>
                    </label>

                    <label style={{ display: 'flex', alignItems: 'center', gap: '10px', cursor: 'pointer' }}>
                        <input type="checkbox" checked={isOpen} onChange={e => setIsOpen(e.target.checked)} style={{ accentColor: '#a600ff' }} />
                        <span className="form-label" style={{ margin: 0 }}>Open registration</span>
                    </label>

                    {formError && <p style={{ margin: 0, color: '#FF6B7A', fontFamily: "'Chakra Petch', monospace", fontSize: '11px' }}>{formError}</p>}

                    <button onClick={handleCreate} disabled={!user || !prizepool.trim() || !startDate || !startTime || (tournamentType === 'draft' && (!draftDate || !draftTime)) || createMutation.isPending} className="create-btn">
                        {!user ? 'Sign in to create' : createMutation.isPending ? 'Creating...' : 'Create Tournament'}
                    </button>
                </div>
            </div>
        </div>
    )
}

function TournamentsPage() {
    const navigate = useNavigate()
    const { data: tournaments, isLoading, isError } = useTournaments()
    const [statusFilter, setStatusFilter] = useState<TournamentStatus | 'all'>('all')
    const [showCreate, setShowCreate] = useState(false)

    const filtered = tournaments?.filter(t => statusFilter === 'all' || t.status === statusFilter) || []

    return (
        <>
            <style>{`
                .tournaments-page {
                    position: relative; z-index: 10;
                    min-height: calc(100vh - 52px); margin-top: 52px;
                    padding: 32px clamp(24px, 5vw, 64px);
                    max-width: 900px; margin-left: auto; margin-right: auto;
                }
                .tournaments-header {
                    display: flex; justify-content: space-between; align-items: center;
                    margin-bottom: 28px;
                }
                .tournaments-title {
                    font-family: 'Russo One', sans-serif; font-size: 18px;
                    color: rgba(255,255,255,0.9); letter-spacing: 0.06em;
                    text-transform: uppercase; margin: 0;
                }
                .filter-row {
                    display: flex; gap: 8px; margin-bottom: 24px; flex-wrap: wrap;
                }
                .filter-btn {
                    padding: 7px 14px; border-radius: 8px; font-size: 11px;
                    font-family: 'Chakra Petch', monospace; letter-spacing: 0.05em;
                    border: 1px solid rgba(255,255,255,0.06); background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.4); cursor: pointer; transition: all 150ms;
                }
                .filter-btn:hover { border-color: rgba(166,0,255,0.3); color: rgba(255,255,255,0.6); }
                .filter-btn.active { background: rgba(166,0,255,0.1); border-color: rgba(166,0,255,0.3); color: #fff; }
                .tournament-card { transition: all 180ms !important; }
                .tournament-card:hover { border-color: rgba(166,0,255,0.25) !important; box-shadow: 0 0 20px rgba(166,0,255,0.08); transform: translateY(-1px); }
                .new-btn {
                    display: flex; align-items: center; gap: 7px;
                    padding: 10px 18px; border-radius: 10px;
                    background: rgba(166,0,255,0.12); border: 1px solid rgba(166,0,255,0.2);
                    color: rgba(255,255,255,0.85); font-family: 'Chakra Petch', monospace;
                    font-size: 12px; font-weight: 500; letter-spacing: 0.05em;
                    cursor: pointer; transition: all 180ms;
                }
                .new-btn:hover { background: rgba(166,0,255,0.2); border-color: rgba(166,0,255,0.5); box-shadow: 0 0 12px rgba(166,0,255,0.15); }
                .tournaments-grid { display: flex; flex-direction: column; gap: 12px; }
                .form-label { font-size: 11px; color: rgba(255,255,255,0.5); font-family: 'Chakra Petch', monospace; letter-spacing: 0.05em; }
                .form-input {
                    padding: 10px 12px; border-radius: 8px; font-size: 13px;
                    background: rgba(255,255,255,0.03); border: 1px solid rgba(255,255,255,0.08);
                    color: #fff; font-family: 'Chakra Petch', monospace; outline: none; transition: border-color 180ms;
                }
                .form-input:focus { border-color: rgba(166,0,255,0.5); }
                .create-btn {
                    padding: 12px; border-radius: 10px; font-size: 13px; font-weight: 600;
                    font-family: 'Chakra Petch', monospace; letter-spacing: 0.05em;
                    background: rgba(166,0,255,0.15); border: 1px solid rgba(166,0,255,0.3);
                    color: #fff; cursor: pointer; transition: all 180ms; margin-top: 8px;
                }
                .create-btn:hover:not(:disabled) { background: rgba(166,0,255,0.25); box-shadow: 0 0 16px rgba(166,0,255,0.2); }
                .create-btn:disabled { opacity: 0.4; cursor: not-allowed; }
                .empty-state {
                    text-align: center; padding: 60px 20px;
                    color: rgba(255,255,255,0.2); font-family: 'Chakra Petch', monospace; font-size: 13px;
                }
            `}</style>

            <div className="tournaments-page">
                <div className="tournaments-header">
                    <h1 className="tournaments-title">Tournaments</h1>
                    <button className="new-btn" onClick={() => setShowCreate(true)}>
                        <FiPlus size={14} /> New
                    </button>
                </div>

                <div className="filter-row">
                    {(['all', 'scheduled', 'active', 'finished', 'canceled'] as const).map(s => (
                        <button key={s} className={`filter-btn ${statusFilter === s ? 'active' : ''}`} onClick={() => setStatusFilter(s)}>
                            {s === 'all' ? 'All' : STATUS_LABELS[s]}
                        </button>
                    ))}
                </div>

                <div className="tournaments-grid">
                    {isLoading ? (
                        <p className="empty-state">Loading...</p>
                    ) : isError ? (
                        <p className="empty-state">Could not load tournaments</p>
                    ) : filtered.length > 0 ? (
                        filtered.map(t => (
                            <TournamentCard key={t.id} tournament={t} onClick={() => navigate({ to: '/tournaments/$id', params: { id: t.id } })} />
                        ))
                    ) : (
                        <p className="empty-state">No tournaments found</p>
                    )}
                </div>
            </div>

            {showCreate && <CreateTournamentModal onClose={() => setShowCreate(false)} />}
        </>
    )
}
