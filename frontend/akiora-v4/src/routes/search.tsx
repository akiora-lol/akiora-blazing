import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { FiHeart, FiMessageSquare, FiEyeOff, FiSlash, FiChevronLeft, FiChevronRight, FiGrid, FiSquare, FiFilter, FiX, FiPlus } from 'react-icons/fi'
import { useAuthContext } from '../contexts/AuthContext'

export const Route = createFileRoute('/search')({ component: SearchPage })

// ─── Types matching backend entities ──────────────────────────────
type LolRole = 'top' | 'jg' | 'mid' | 'adc' | 'sup'
type Server = 'euw' | 'ru' | 'eune' | 'na' | 'tr'
type LolRankName = 'iron' | 'bronze' | 'silver' | 'gold' | 'platinum' | 'emerald' | 'diamond' | 'master' | 'grandmaster' | 'challenger'

interface RankRange {
    server: Server
    min_rank: { rank: LolRankName; division: number }
    max_rank: { rank: LolRankName; division: number }
}

interface FormProfile {
    id: string
    owner_id: string
    owner_name: string
    rank_range: RankRange[]
    my_roles: LolRole[]
    looking_for_roles: LolRole[]
    description: string
    created_at: string
    status?: 'active' | 'frozen'
}

// ─── Dummy Data ──────────────────────────────────────────────────
const DUMMY_HOT: FormProfile[] = [
    { id: 'h1', owner_id: 'u1', owner_name: 'AceSniper', rank_range: [{ server: 'euw', min_rank: { rank: 'diamond', division: 2 }, max_rank: { rank: 'master', division: 1 } }], my_roles: ['adc'], looking_for_roles: ['sup'], description: 'ADC main looking for a duo support. Aggressive lane, high KDA player. I want someone who can roam and make plays with me. Diamond+ only.', created_at: '2m ago' },
    { id: 'h2', owner_id: 'u2', owner_name: 'MidOrFeed', rank_range: [{ server: 'na', min_rank: { rank: 'master', division: 1 }, max_rank: { rank: 'challenger', division: 1 } }], my_roles: ['mid'], looking_for_roles: ['jg', 'sup'], description: 'Mechanical god. Will 1v9 your promos. Looking for a jungler who knows how to play around mid. Assassin player, need ganks early.', created_at: '5m ago' },
    { id: 'h3', owner_id: 'u3', owner_name: 'WardMachine', rank_range: [{ server: 'euw', min_rank: { rank: 'diamond', division: 1 }, max_rank: { rank: 'grandmaster', division: 1 } }], my_roles: ['sup'], looking_for_roles: ['adc'], description: 'Support diff every game. Vision score through the roof. Looking for an ADC who can actually follow up on my engages. Thresh/Nautilus specialist.', created_at: '8m ago' },
    { id: 'h4', owner_id: 'u4', owner_name: 'JungleDiff', rank_range: [{ server: 'euw', min_rank: { rank: 'platinum', division: 1 }, max_rank: { rank: 'diamond', division: 2 } }], my_roles: ['jg'], looking_for_roles: ['mid', 'top'], description: 'Early game pressure specialist. Will gank your lane level 3 guaranteed. Lee Sin / Elise / Nidalee player. Need lanes that have CC.', created_at: '12m ago' },
    { id: 'h5', owner_id: 'u5', owner_name: 'TopGap', rank_range: [{ server: 'na', min_rank: { rank: 'master', division: 1 }, max_rank: { rank: 'grandmaster', division: 1 } }], my_roles: ['top'], looking_for_roles: ['jg'], description: 'Split push artist. Give me a lead and I end the game. Looking for a jungler who understands topside pressure and herald timings.', created_at: '15m ago' },
]

const DUMMY_COLD: FormProfile[] = [
    { id: 'c1', owner_id: 'u6', owner_name: 'ChillGamer', rank_range: [{ server: 'euw', min_rank: { rank: 'silver', division: 1 }, max_rank: { rank: 'gold', division: 3 } }], my_roles: ['sup'], looking_for_roles: ['adc', 'mid'], description: 'Casual player, just here for fun. ARAM enjoyer looking for chill people to play normals with. No toxicity please.', created_at: '2h ago', status: 'active' },
    { id: 'c2', owner_id: 'u7', owner_name: 'WeekendWarrior', rank_range: [{ server: 'na', min_rank: { rank: 'bronze', division: 1 }, max_rank: { rank: 'silver', division: 2 } }], my_roles: ['top'], looking_for_roles: ['jg', 'sup'], description: 'Play on weekends only. Looking for a chill group that doesn\'t flame. Garen/Malphite player. Just want to have fun climbing slowly.', created_at: '5h ago', status: 'active' },
    { id: 'c3', owner_id: 'u8', owner_name: 'NormsDude', rank_range: [{ server: 'euw', min_rank: { rank: 'gold', division: 1 }, max_rank: { rank: 'platinum', division: 4 } }], my_roles: ['adc'], looking_for_roles: ['sup'], description: 'No ranked anxiety here. Normals only lifestyle. Looking for a support to duo normals and learn new champs together.', created_at: '1d ago', status: 'active' },
    { id: 'c4', owner_id: 'u9', owner_name: 'ARAMKing', rank_range: [{ server: 'na', min_rank: { rank: 'iron', division: 4 }, max_rank: { rank: 'challenger', division: 1 } }], my_roles: ['top', 'mid', 'jg', 'adc', 'sup'], looking_for_roles: ['top', 'mid', 'jg', 'adc', 'sup'], description: 'ARAM is the true game mode. 5000+ games played. Any rank welcome, just have fun and don\'t int the bush checks.', created_at: '2d ago', status: 'active' },
    { id: 'c5', owner_id: 'u10', owner_name: 'CoachMePlz', rank_range: [{ server: 'eune', min_rank: { rank: 'diamond', division: 4 }, max_rank: { rank: 'challenger', division: 1 } }], my_roles: ['mid', 'sup'], looking_for_roles: ['mid', 'adc', 'top'], description: 'Looking for a high elo player to review my VODs and help me improve. I\'m stuck Emerald and want to finally hit Diamond this split.', created_at: '3d ago', status: 'active' },
]

// ─── Helpers ──────────────────────────────────────────────────────
const RANK_COLORS: Record<LolRankName, string> = {
    iron: '#5e5e5e', bronze: '#8B4513', silver: '#9CA3AF', gold: '#F59E0B',
    platinum: '#06B6D4', emerald: '#10B981', diamond: '#6366F1',
    master: '#a600ff', grandmaster: '#FF002A', challenger: '#F59E0B',
}

const ROLE_LABELS: Record<LolRole, string> = { top: 'Top', jg: 'Jungle', mid: 'Mid', adc: 'ADC', sup: 'Support' }
const SERVER_LABELS: Record<Server, string> = { euw: 'EUW', ru: 'RU', eune: 'EUNE', na: 'NA', tr: 'TR' }
const RANK_LABELS: Record<LolRankName, string> = {
    iron: 'Iron', bronze: 'Bronze', silver: 'Silver', gold: 'Gold',
    platinum: 'Platinum', emerald: 'Emerald', diamond: 'Diamond',
    master: 'Master', grandmaster: 'GM', challenger: 'Challenger',
}

function formatRankRange(rr: RankRange): string {
    const min = `${RANK_LABELS[rr.min_rank.rank]}${rr.min_rank.division > 1 ? ' ' + rr.min_rank.division : ''}`
    const max = `${RANK_LABELS[rr.max_rank.rank]}${rr.max_rank.division > 1 ? ' ' + rr.max_rank.division : ''}`
    return `${min} – ${max}`
}

function getMainRankColor(profile: FormProfile): string {
    if (profile.rank_range.length === 0) return '#a600ff'
    return RANK_COLORS[profile.rank_range[0].max_rank.rank] ?? '#a600ff'
}

// ─── Filter Panel ─────────────────────────────────────────────────
interface Filters {
    roles: LolRole[]
    servers: Server[]
    minRank: LolRankName | null
}

function FilterPanel({ filters, onChange, onClose }: { filters: Filters; onChange: (f: Filters) => void; onClose: () => void }) {
    const allRoles: LolRole[] = ['top', 'jg', 'mid', 'adc', 'sup']
    const allServers: Server[] = ['euw', 'ru', 'eune', 'na', 'tr']
    const allRanks: LolRankName[] = ['iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', 'grandmaster', 'challenger']

    const toggleRole = (r: LolRole) => {
        const roles = filters.roles.includes(r) ? filters.roles.filter(x => x !== r) : [...filters.roles, r]
        onChange({ ...filters, roles })
    }
    const toggleServer = (s: Server) => {
        const servers = filters.servers.includes(s) ? filters.servers.filter(x => x !== s) : [...filters.servers, s]
        onChange({ ...filters, servers })
    }

    return (
        <div className="filter-panel">
            <div className="filter-header">
                <span className="filter-title">Filters</span>
                <button className="filter-close" onClick={onClose}><FiX size={16} /></button>
            </div>

            <div className="filter-section">
                <span className="filter-label">Looking for role</span>
                <div className="filter-chips">
                    {allRoles.map(r => (
                        <button key={r} className={`filter-chip ${filters.roles.includes(r) ? 'active' : ''}`} onClick={() => toggleRole(r)}>
                            {ROLE_LABELS[r]}
                        </button>
                    ))}
                </div>
            </div>

            <div className="filter-section">
                <span className="filter-label">Server</span>
                <div className="filter-chips">
                    {allServers.map(s => (
                        <button key={s} className={`filter-chip ${filters.servers.includes(s) ? 'active' : ''}`} onClick={() => toggleServer(s)}>
                            {SERVER_LABELS[s]}
                        </button>
                    ))}
                </div>
            </div>

            <div className="filter-section">
                <span className="filter-label">Min rank</span>
                <div className="filter-chips">
                    {allRanks.map(r => (
                        <button key={r}
                            className={`filter-chip ${filters.minRank === r ? 'active' : ''}`}
                            style={filters.minRank === r ? { background: `${RANK_COLORS[r]}20`, color: RANK_COLORS[r], borderColor: `${RANK_COLORS[r]}50` } : undefined}
                            onClick={() => onChange({ ...filters, minRank: filters.minRank === r ? null : r })}
                        >
                            {RANK_LABELS[r]}
                        </button>
                    ))}
                </div>
            </div>
        </div>
    )
}

// ─── Profile Card ─────────────────────────────────────────────────
function ProfileCard({ profile, onLike, onMessage, onHide, onBlock, liked, compact }: {
    profile: FormProfile
    onLike: () => void
    onMessage: () => void
    onHide: () => void
    onBlock: () => void
    liked: boolean
    compact?: boolean
}) {
    const rankColor = getMainRankColor(profile)

    return (
        <div className={`profile-card ${compact ? 'profile-card-compact' : ''}`}>
            <div className="profile-card-avatar" style={{ background: `linear-gradient(135deg, ${rankColor}15, ${rankColor}35)`, borderBottom: `1px solid ${rankColor}30` }}>
                <span style={{ fontFamily: "'Russo One', sans-serif", fontSize: compact ? '24px' : '36px', color: rankColor, textShadow: `0 0 20px ${rankColor}60` }}>
                    {profile.owner_name.slice(0, 2).toUpperCase()}
                </span>
            </div>

            <div className="profile-card-info">
                <div style={{ display: 'flex', alignItems: 'center', gap: '10px', marginBottom: '8px' }}>
                    <h3 className="profile-card-name">{profile.owner_name}</h3>
                    <span className="profile-card-time">{profile.created_at}</span>
                </div>

                {/* Rank ranges */}
                <div style={{ display: 'flex', gap: '6px', flexWrap: 'wrap', marginBottom: '10px' }}>
                    {profile.rank_range.map((rr, i) => (
                        <span key={i} className="profile-tag" style={{ background: `${RANK_COLORS[rr.max_rank.rank]}15`, color: RANK_COLORS[rr.max_rank.rank], border: `1px solid ${RANK_COLORS[rr.max_rank.rank]}35` }}>
                            {SERVER_LABELS[rr.server]} {formatRankRange(rr)}
                        </span>
                    ))}
                </div>

                {/* Roles */}
                <div style={{ display: 'flex', gap: '12px', marginBottom: '12px', flexWrap: 'wrap' }}>
                    <div style={{ display: 'flex', gap: '4px', alignItems: 'center' }}>
                        <span className="role-label">My:</span>
                        {profile.my_roles.map(r => (
                            <span key={r} className="role-tag">{ROLE_LABELS[r]}</span>
                        ))}
                    </div>
                    <div style={{ display: 'flex', gap: '4px', alignItems: 'center' }}>
                        <span className="role-label">LF:</span>
                        {profile.looking_for_roles.map(r => (
                            <span key={r} className="role-tag role-tag-looking">{ROLE_LABELS[r]}</span>
                        ))}
                    </div>
                </div>

                {/* Description */}
                <p className="profile-card-bio">{profile.description}</p>

                {/* Actions */}
                <div className="profile-card-actions">
                    <button className={`action-btn action-like ${liked ? 'liked' : ''}`} onClick={onLike} title="Like">
                        <FiHeart size={18} />
                    </button>
                    <button className="action-btn action-message" onClick={onMessage} title="Message">
                        <FiMessageSquare size={18} />
                    </button>
                    <button className="action-btn action-hide" onClick={onHide} title="Hide">
                        <FiEyeOff size={16} />
                    </button>
                    <button className="action-btn action-block" onClick={onBlock} title="Block">
                        <FiSlash size={16} />
                    </button>
                </div>
            </div>
        </div>
    )
}

// ─── Main Page ────────────────────────────────────────────────────
function SearchPage() {
    const { user } = useAuthContext()
    const navigate = useNavigate()
    const [tab, setTab] = useState<'hot' | 'cold'>('hot')
    const [viewMode, setViewMode] = useState<'swipe' | 'list'>('swipe')
    const [hiddenIds, setHiddenIds] = useState<Set<string>>(new Set())
    const [likedIds, setLikedIds] = useState<Set<string>>(new Set())
    const [currentIndex, setCurrentIndex] = useState(0)
    const [showFilters, setShowFilters] = useState(false)
    const [filters, setFilters] = useState<Filters>({ roles: [], servers: [], minRank: null })
    const [showCreateModal, setShowCreateModal] = useState(false)
    const [formData, setFormData] = useState({
        server: 'euw' as Server,
        minRank: 'gold' as LolRankName,
        minDiv: 4,
        maxRank: 'diamond' as LolRankName,
        maxDiv: 1,
        myRoles: [] as LolRole[],
        lookingForRoles: [] as LolRole[],
        description: '',
    })

    const allProfiles = tab === 'hot' ? DUMMY_HOT : DUMMY_COLD

    const RANK_ORDER: LolRankName[] = ['iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', 'grandmaster', 'challenger']

    const profiles = allProfiles.filter(p => {
        if (hiddenIds.has(p.id)) return false
        if (filters.roles.length > 0 && !p.looking_for_roles.some(r => filters.roles.includes(r))) return false
        if (filters.servers.length > 0 && !p.rank_range.some(rr => filters.servers.includes(rr.server))) return false
        if (filters.minRank) {
            const minIdx = RANK_ORDER.indexOf(filters.minRank)
            const hasMatchingRank = p.rank_range.some(rr => RANK_ORDER.indexOf(rr.max_rank.rank) >= minIdx)
            if (!hasMatchingRank) return false
        }
        return true
    })

    const handleLike = (id: string) => {
        setLikedIds(prev => {
            const next = new Set(prev)
            if (next.has(id)) next.delete(id); else next.add(id)
            return next
        })
    }

    const handleMessage = (_id: string) => {
        navigate({ to: '/messenger' })
    }

    const handleHide = (id: string) => {
        setHiddenIds(prev => new Set(prev).add(id))
    }

    const handleBlock = (id: string) => {
        setHiddenIds(prev => new Set(prev).add(id))
    }

    const handlePrev = () => setCurrentIndex(i => Math.max(0, i - 1))
    const handleNext = () => setCurrentIndex(i => Math.min(profiles.length - 1, i + 1))

    const safeIndex = Math.min(currentIndex, Math.max(0, profiles.length - 1))
    const currentProfile = profiles[safeIndex]

    const activeFilterCount = filters.roles.length + filters.servers.length + (filters.minRank ? 1 : 0)

    return (
        <>
            <style>{`
                .search-page {
                    position: relative;
                    z-index: 10;
                    min-height: calc(100vh - 52px);
                    margin-top: 52px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    padding: 32px 20px;
                }

                .search-toolbar {
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    margin-bottom: 64px;
                    flex-wrap: wrap;
                    justify-content: center;
                }

                .search-tabs {
                    display: flex;
                    gap: 2px;
                    background: rgba(0,0,0,0.4);
                    border: 1px solid rgba(166,0,255,0.08);
                    border-radius: 10px;
                    padding: 3px;
                    backdrop-filter: blur(12px);
                    position: relative;
                }
                .search-tab {
                    padding: 8px 24px;
                    border: none;
                    border-radius: 8px;
                    background: transparent;
                    color: rgba(255,255,255,0.4);
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    font-weight: 600;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    cursor: pointer;
                    transition: all 180ms;
                    position: relative;
                }
                .search-tab .tab-tooltip {
                    position: absolute;
                    top: calc(100% + 10px);
                    left: 50%;
                    transform: translateX(-50%);
                    width: 200px;
                    padding: 8px 12px;
                    background: rgba(0,0,0,0.9);
                    border: 1px solid rgba(166,0,255,0.12);
                    border-radius: 8px;
                    font-size: 10px;
                    font-weight: 400;
                    color: rgba(255,255,255,0.6);
                    letter-spacing: 0.02em;
                    text-transform: none;
                    line-height: 1.5;
                    white-space: normal;
                    pointer-events: none;
                    opacity: 0;
                    transition: opacity 150ms;
                    z-index: 10;
                    backdrop-filter: blur(12px);
                }
                .search-tab:hover .tab-tooltip {
                    opacity: 1;
                }
                .search-tab:hover { color: rgba(255,255,255,0.7); }
                .search-tab.active {
                    background: rgba(6,182,212,0.12);
                    color: #06B6D4;
                }
                .search-tab.hot {
                    color: rgba(255,0,42,0.5);
                }
                .search-tab.hot:hover { color: #FF002A; }
                .search-tab.hot.active {
                    background: rgba(255,0,42,0.12);
                    color: #FF002A;
                }
                .search-tab.cold {
                    color: rgba(6,182,212,0.5);
                }
                .search-tab.cold:hover { color: #06B6D4; }
                .search-tab.cold.active {
                    background: rgba(6,182,212,0.12);
                    color: #06B6D4;
                }

                .toolbar-btn {
                    width: 36px; height: 36px;
                    border-radius: 8px;
                    border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(0,0,0,0.4);
                    color: rgba(255,255,255,0.4);
                    cursor: pointer;
                    display: flex; align-items: center; justify-content: center;
                    transition: all 150ms;
                    position: relative;
                    backdrop-filter: blur(8px);
                }
                .toolbar-btn:hover { background: rgba(166,0,255,0.08); color: #c77dff; border-color: rgba(166,0,255,0.15); }
                .toolbar-btn.active { background: rgba(166,0,255,0.12); color: #c77dff; border-color: rgba(166,0,255,0.2); }
                .toolbar-badge {
                    position: absolute; top: -4px; right: -4px;
                    width: 16px; height: 16px; border-radius: 50%;
                    background: #a600ff; color: #fff;
                    font-size: 9px; font-weight: 700;
                    display: flex; align-items: center; justify-content: center;
                    font-family: 'Chakra Petch', monospace;
                }

                /* ─── Filter panel ───── */
                .filter-panel {
                    width: 100%;
                    max-width: 520px;
                    background: rgba(0,0,0,0.6);
                    border: 1px solid rgba(166,0,255,0.08);
                    border-radius: 12px;
                    padding: 16px;
                    margin-bottom: 24px;
                    backdrop-filter: blur(16px);
                }
                .filter-header {
                    display: flex; align-items: center; justify-content: space-between;
                    margin-bottom: 14px;
                }
                .filter-title {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 12px; font-weight: 600;
                    color: rgba(255,255,255,0.6);
                    letter-spacing: 0.1em; text-transform: uppercase;
                }
                .filter-close {
                    background: none; border: none; color: rgba(255,255,255,0.3);
                    cursor: pointer; padding: 4px; display: flex;
                    transition: color 150ms;
                }
                .filter-close:hover { color: #fff; }
                .filter-section { margin-bottom: 12px; }
                .filter-label {
                    display: block;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 9px; font-weight: 600;
                    color: rgba(255,255,255,0.3);
                    letter-spacing: 0.12em; text-transform: uppercase;
                    margin-bottom: 6px;
                }
                .filter-chips { display: flex; gap: 4px; flex-wrap: wrap; }
                .filter-chip {
                    padding: 4px 10px; border-radius: 6px;
                    border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.4);
                    font-family: 'Chakra Petch', monospace;
                    font-size: 10px; font-weight: 500;
                    cursor: pointer; transition: all 150ms;
                }
                .filter-chip:hover { border-color: rgba(166,0,255,0.2); color: rgba(255,255,255,0.7); }
                .filter-chip.active {
                    background: rgba(166,0,255,0.1);
                    border-color: rgba(166,0,255,0.25);
                    color: #c77dff;
                }

                /* ─── Card viewport ───── */
                .card-viewport {
                    position: relative;
                    width: 100%;
                    max-width: 520px;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                }

                .list-viewport {
                    width: 100%;
                    max-width: 1100px;
                    display: grid;
                    grid-template-columns: repeat(3, 1fr);
                    gap: 16px;
                }

                .profile-card {
                    width: 100%;
                    background: rgba(0,0,0,0.45);
                    border: 1px solid rgba(166,0,255,0.06);
                    border-radius: 16px;
                    backdrop-filter: blur(20px);
                    overflow: hidden;
                    transition: transform 300ms cubic-bezier(.34,1.56,.64,1), opacity 300ms;
                }
                .profile-card-compact {
                    border-radius: 12px;
                }
                .profile-card-compact .profile-card-avatar {
                    height: 100px;
                }

                .profile-card-avatar {
                    width: 100%;
                    height: 160px;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                }

                .profile-card-info {
                    padding: 20px 24px 24px;
                }
                .profile-card-name {
                    margin: 0;
                    font-family: 'Russo One', sans-serif;
                    font-size: 22px;
                    color: #fff;
                    letter-spacing: 0.02em;
                }
                .profile-card-compact .profile-card-name { font-size: 16px; }
                .profile-card-time {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 10px;
                    color: rgba(255,255,255,0.2);
                }
                .profile-tag {
                    padding: 3px 9px;
                    border-radius: 5px;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 10px;
                    font-weight: 600;
                    color: rgba(255,255,255,0.5);
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.06);
                    letter-spacing: 0.03em;
                }
                .role-label {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 9px;
                    color: rgba(255,255,255,0.25);
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                }
                .role-tag {
                    padding: 2px 8px;
                    border-radius: 4px;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 10px;
                    font-weight: 500;
                    color: rgba(255,255,255,0.6);
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.06);
                }
                .role-tag-looking {
                    color: rgba(166,0,255,0.7);
                    background: rgba(166,0,255,0.06);
                    border-color: rgba(166,0,255,0.12);
                }
                .profile-card-bio {
                    margin: 0 0 16px;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 12px;
                    color: rgba(255,255,255,0.5);
                    line-height: 1.7;
                }
                .profile-card-compact .profile-card-bio {
                    font-size: 11px;
                    margin-bottom: 12px;
                }

                .profile-card-actions {
                    display: flex;
                    gap: 10px;
                    justify-content: center;
                }
                .action-btn {
                    width: 48px;
                    height: 48px;
                    border-radius: 50%;
                    border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.4);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 180ms;
                }
                .profile-card-compact .action-btn { width: 40px; height: 40px; }
                .action-like:hover, .action-like.liked {
                    background: rgba(255,0,42,0.12);
                    border-color: rgba(255,0,42,0.3);
                    color: #FF002A;
                    box-shadow: 0 0 16px rgba(255,0,42,0.12);
                }
                .action-like.liked { background: rgba(255,0,42,0.2); }
                .action-message:hover {
                    background: rgba(166,0,255,0.1);
                    border-color: rgba(166,0,255,0.25);
                    color: #c77dff;
                    box-shadow: 0 0 16px rgba(166,0,255,0.12);
                }
                .action-hide:hover {
                    background: rgba(255,255,255,0.06);
                    border-color: rgba(255,255,255,0.12);
                    color: rgba(255,255,255,0.8);
                }
                .action-block:hover {
                    background: rgba(255,60,60,0.08);
                    border-color: rgba(255,60,60,0.2);
                    color: #ff4444;
                }

                .nav-arrows {
                    display: flex;
                    gap: 14px;
                    margin-top: 24px;
                    align-items: center;
                }
                .nav-arrow {
                    width: 40px;
                    height: 40px;
                    border-radius: 50%;
                    border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(0,0,0,0.4);
                    color: rgba(255,255,255,0.4);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    transition: all 150ms;
                    backdrop-filter: blur(8px);
                }
                .nav-arrow:hover:not(:disabled) {
                    background: rgba(166,0,255,0.1);
                    border-color: rgba(166,0,255,0.2);
                    color: #c77dff;
                }
                .nav-arrow:disabled { opacity: 0.2; cursor: not-allowed; }
                .nav-counter {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    color: rgba(255,255,255,0.2);
                    letter-spacing: 0.05em;
                    min-width: 50px;
                    text-align: center;
                }

                .empty-state {
                    text-align: center;
                    padding: 80px 20px;
                    color: rgba(255,255,255,0.15);
                    font-family: 'Chakra Petch', monospace;
                    font-size: 13px;
                }

                /* ─── Create button ───── */
                .create-form-btn {
                    padding: 8px 20px;
                    border-radius: 8px;
                    border: 1px solid rgba(166,0,255,0.2);
                    background: rgba(166,0,255,0.1);
                    color: #c77dff;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    font-weight: 600;
                    letter-spacing: 0.08em;
                    text-transform: uppercase;
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    gap: 6px;
                    transition: all 180ms;
                    backdrop-filter: blur(8px);
                }
                .create-form-btn:hover {
                    background: rgba(166,0,255,0.18);
                    border-color: rgba(166,0,255,0.35);
                    box-shadow: 0 0 16px rgba(166,0,255,0.12);
                }

                /* ─── Modal ───── */
                .modal-overlay {
                    position: fixed;
                    inset: 0;
                    z-index: 200;
                    background: rgba(0,0,0,0.7);
                    backdrop-filter: blur(6px);
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    padding: 20px;
                }
                .modal-content {
                    width: 100%;
                    max-width: 480px;
                    max-height: 85vh;
                    overflow-y: auto;
                    background: rgba(8,0,16,0.95);
                    border: 1px solid rgba(166,0,255,0.1);
                    border-radius: 16px;
                    padding: 28px;
                    backdrop-filter: blur(24px);
                    box-shadow: 0 16px 64px rgba(0,0,0,0.6), 0 0 24px rgba(166,0,255,0.06);
                }
                .modal-content::-webkit-scrollbar { width: 2px; }
                .modal-content::-webkit-scrollbar-thumb { background: rgba(166,0,255,0.15); }
                .modal-header {
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                    margin-bottom: 24px;
                }
                .modal-title {
                    font-family: 'Russo One', sans-serif;
                    font-size: 16px;
                    color: #fff;
                    letter-spacing: 0.04em;
                }
                .modal-close {
                    background: none;
                    border: none;
                    color: rgba(255,255,255,0.3);
                    cursor: pointer;
                    padding: 4px;
                    display: flex;
                    transition: color 150ms;
                }
                .modal-close:hover { color: #fff; }
                .modal-section {
                    margin-bottom: 18px;
                }
                .modal-label {
                    display: block;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 9px;
                    font-weight: 600;
                    color: rgba(255,255,255,0.3);
                    letter-spacing: 0.12em;
                    text-transform: uppercase;
                    margin-bottom: 8px;
                }
                .modal-chips {
                    display: flex;
                    gap: 4px;
                    flex-wrap: wrap;
                }
                .modal-chip {
                    padding: 5px 12px;
                    border-radius: 6px;
                    border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(255,255,255,0.03);
                    color: rgba(255,255,255,0.4);
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    font-weight: 500;
                    cursor: pointer;
                    transition: all 150ms;
                }
                .modal-chip:hover { border-color: rgba(166,0,255,0.2); color: rgba(255,255,255,0.7); }
                .modal-chip.active {
                    background: rgba(166,0,255,0.1);
                    border-color: rgba(166,0,255,0.25);
                    color: #c77dff;
                }
                .modal-select {
                    padding: 8px 12px;
                    border-radius: 8px;
                    border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(255,255,255,0.03);
                    color: #fff;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    outline: none;
                    cursor: pointer;
                    transition: border-color 150ms;
                    appearance: none;
                    -webkit-appearance: none;
                }
                .modal-select:focus { border-color: rgba(166,0,255,0.3); }
                .modal-select option { background: #0a0010; color: #fff; }
                .modal-textarea {
                    width: 100%;
                    min-height: 80px;
                    padding: 10px 14px;
                    border-radius: 10px;
                    border: 1px solid rgba(255,255,255,0.06);
                    background: rgba(255,255,255,0.03);
                    color: #fff;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 12px;
                    line-height: 1.6;
                    outline: none;
                    resize: vertical;
                    transition: border-color 150ms;
                    box-sizing: border-box;
                }
                .modal-textarea:focus { border-color: rgba(166,0,255,0.3); }
                .modal-textarea::placeholder { color: rgba(255,255,255,0.15); }
                .modal-rank-row {
                    display: flex;
                    gap: 8px;
                    align-items: center;
                }
                .modal-rank-sep {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 10px;
                    color: rgba(255,255,255,0.2);
                }
                .modal-submit {
                    width: 100%;
                    padding: 12px;
                    border-radius: 10px;
                    border: 1px solid rgba(166,0,255,0.25);
                    background: rgba(166,0,255,0.12);
                    color: #c77dff;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 12px;
                    font-weight: 600;
                    letter-spacing: 0.1em;
                    text-transform: uppercase;
                    cursor: pointer;
                    transition: all 180ms;
                    margin-top: 8px;
                }
                .modal-submit:hover {
                    background: rgba(166,0,255,0.2);
                    border-color: rgba(166,0,255,0.4);
                    box-shadow: 0 0 20px rgba(166,0,255,0.15);
                }
            `}</style>

            <div className="search-page">
                {/* Toolbar */}
                <div className="search-toolbar">
                    <div className="search-tabs">
                        <button className={`search-tab hot ${tab === 'hot' ? 'active' : ''}`} onClick={() => { setTab('hot'); setCurrentIndex(0) }}>
                            Hot
                            <span className="tab-tooltip">Live for 15 min. Quick search for teammates right now.</span>
                        </button>
                        <button className={`search-tab cold ${tab === 'cold' ? 'active' : ''}`} onClick={() => { setTab('cold'); setCurrentIndex(0) }}>
                            Cold
                            <span className="tab-tooltip">Permanent form, 1 per person. Find a long-term duo partner.</span>
                        </button>
                    </div>

                    <button className={`toolbar-btn ${viewMode === 'swipe' ? 'active' : ''}`} onClick={() => setViewMode('swipe')} title="Swipe mode">
                        <FiSquare size={14} />
                    </button>
                    <button className={`toolbar-btn ${viewMode === 'list' ? 'active' : ''}`} onClick={() => setViewMode('list')} title="List mode">
                        <FiGrid size={14} />
                    </button>

                    <button className={`toolbar-btn ${showFilters ? 'active' : ''}`} onClick={() => setShowFilters(v => !v)} title="Filters">
                        <FiFilter size={14} />
                        {activeFilterCount > 0 && <span className="toolbar-badge">{activeFilterCount}</span>}
                    </button>

                    <button className="create-form-btn" onClick={() => setShowCreateModal(true)}>
                        <FiPlus size={14} />
                        Create {tab === 'hot' ? 'Hot' : 'Cold'} Form
                    </button>
                </div>

                {/* Filter panel */}
                {showFilters && (
                    <FilterPanel filters={filters} onChange={setFilters} onClose={() => setShowFilters(false)} />
                )}

                {/* Swipe mode */}
                {viewMode === 'swipe' && (
                    <div className="card-viewport">
                        {profiles.length > 0 && currentProfile ? (
                            <>
                                <ProfileCard
                                    key={currentProfile.id}
                                    profile={currentProfile}
                                    onLike={() => handleLike(currentProfile.id)}
                                    onMessage={() => handleMessage(currentProfile.id)}
                                    onHide={() => handleHide(currentProfile.id)}
                                    onBlock={() => handleBlock(currentProfile.id)}
                                    liked={likedIds.has(currentProfile.id)}
                                />
                                <div className="nav-arrows">
                                    <button className="nav-arrow" onClick={handlePrev} disabled={safeIndex === 0}>
                                        <FiChevronLeft size={18} />
                                    </button>
                                    <span className="nav-counter">
                                        {safeIndex + 1} / {profiles.length}
                                    </span>
                                    <button className="nav-arrow" onClick={handleNext} disabled={safeIndex >= profiles.length - 1}>
                                        <FiChevronRight size={18} />
                                    </button>
                                </div>
                            </>
                        ) : (
                            <div className="empty-state">No profiles match your filters</div>
                        )}
                    </div>
                )}

                {/* List mode */}
                {viewMode === 'list' && (
                    <div className="list-viewport">
                        {profiles.length > 0 ? profiles.map(p => (
                            <ProfileCard
                                key={p.id}
                                profile={p}
                                onLike={() => handleLike(p.id)}
                                onMessage={() => handleMessage(p.id)}
                                onHide={() => handleHide(p.id)}
                                onBlock={() => handleBlock(p.id)}
                                liked={likedIds.has(p.id)}
                                compact
                            />
                        )) : (
                            <div className="empty-state">No profiles match your filters</div>
                        )}
                    </div>
                )}
            </div>

            {/* Create Form Modal */}
            {showCreateModal && (
                <div className="modal-overlay" onClick={() => setShowCreateModal(false)}>
                    <div className="modal-content" onClick={e => e.stopPropagation()}>
                        <div className="modal-header">
                            <span className="modal-title">
                                {tab === 'hot' ? 'Create Hot Form' : 'Create Cold Form'}
                            </span>
                            <button className="modal-close" onClick={() => setShowCreateModal(false)}><FiX size={18} /></button>
                        </div>

                        {tab === 'hot' && (
                            <p style={{ fontFamily: "'Chakra Petch', monospace", fontSize: '10px', color: 'rgba(255,0,42,0.6)', marginBottom: '16px', marginTop: 0, lineHeight: 1.5 }}>
                                Hot forms expire in 15 minutes. Use them to find teammates right now.
                            </p>
                        )}
                        {tab === 'cold' && (
                            <p style={{ fontFamily: "'Chakra Petch', monospace", fontSize: '10px', color: 'rgba(6,182,212,0.6)', marginBottom: '16px', marginTop: 0, lineHeight: 1.5 }}>
                                Cold forms are permanent (1 per person). Find a long-term duo partner.
                            </p>
                        )}

                        <div className="modal-section">
                            <span className="modal-label">Server</span>
                            <div className="modal-chips">
                                {(['euw', 'ru', 'eune', 'na', 'tr'] as Server[]).map(s => (
                                    <button key={s} className={`modal-chip ${formData.server === s ? 'active' : ''}`} onClick={() => setFormData(d => ({ ...d, server: s }))}>
                                        {SERVER_LABELS[s]}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="modal-section">
                            <span className="modal-label">Rank Range</span>
                            <div className="modal-rank-row">
                                <select className="modal-select" value={formData.minRank} onChange={e => setFormData(d => ({ ...d, minRank: e.target.value as LolRankName }))}>
                                    {(['iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', 'grandmaster', 'challenger'] as LolRankName[]).map(r => (
                                        <option key={r} value={r}>{RANK_LABELS[r]}</option>
                                    ))}
                                </select>
                                <select className="modal-select" value={formData.minDiv} onChange={e => setFormData(d => ({ ...d, minDiv: Number(e.target.value) }))}>
                                    {[1, 2, 3, 4].map(d => <option key={d} value={d}>{d}</option>)}
                                </select>
                                <span className="modal-rank-sep">to</span>
                                <select className="modal-select" value={formData.maxRank} onChange={e => setFormData(d => ({ ...d, maxRank: e.target.value as LolRankName }))}>
                                    {(['iron', 'bronze', 'silver', 'gold', 'platinum', 'emerald', 'diamond', 'master', 'grandmaster', 'challenger'] as LolRankName[]).map(r => (
                                        <option key={r} value={r}>{RANK_LABELS[r]}</option>
                                    ))}
                                </select>
                                <select className="modal-select" value={formData.maxDiv} onChange={e => setFormData(d => ({ ...d, maxDiv: Number(e.target.value) }))}>
                                    {[1, 2, 3, 4].map(d => <option key={d} value={d}>{d}</option>)}
                                </select>
                            </div>
                        </div>

                        <div className="modal-section">
                            <span className="modal-label">My Roles</span>
                            <div className="modal-chips">
                                {(['top', 'jg', 'mid', 'adc', 'sup'] as LolRole[]).map(r => (
                                    <button key={r} className={`modal-chip ${formData.myRoles.includes(r) ? 'active' : ''}`}
                                        onClick={() => setFormData(d => ({ ...d, myRoles: d.myRoles.includes(r) ? d.myRoles.filter(x => x !== r) : [...d.myRoles, r] }))}>
                                        {ROLE_LABELS[r]}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="modal-section">
                            <span className="modal-label">Looking For Roles</span>
                            <div className="modal-chips">
                                {(['top', 'jg', 'mid', 'adc', 'sup'] as LolRole[]).map(r => (
                                    <button key={r} className={`modal-chip ${formData.lookingForRoles.includes(r) ? 'active' : ''}`}
                                        onClick={() => setFormData(d => ({ ...d, lookingForRoles: d.lookingForRoles.includes(r) ? d.lookingForRoles.filter(x => x !== r) : [...d.lookingForRoles, r] }))}>
                                        {ROLE_LABELS[r]}
                                    </button>
                                ))}
                            </div>
                        </div>

                        <div className="modal-section">
                            <span className="modal-label">Description</span>
                            <textarea
                                className="modal-textarea"
                                placeholder="Describe what you're looking for..."
                                value={formData.description}
                                onChange={e => setFormData(d => ({ ...d, description: e.target.value }))}
                                maxLength={500}
                            />
                            <span style={{ fontFamily: "'Chakra Petch', monospace", fontSize: '9px', color: 'rgba(255,255,255,0.15)', float: 'right', marginTop: '4px' }}>
                                {formData.description.length}/500
                            </span>
                        </div>

                        <button className="modal-submit" onClick={() => setShowCreateModal(false)}>
                            Publish {tab === 'hot' ? 'Hot' : 'Cold'} Form
                        </button>
                    </div>
                </div>
            )}
        </>
    )
}
