import {
    HeadContent,
    Scripts,
    createRootRouteWithContext,
    useRouterState,
} from '@tanstack/react-router'

import { getLocale } from '#/paraglide/runtime'

import appCss from '../styles.css?url'

import type { QueryClient } from '@tanstack/react-query'

import { useState, useRef, useCallback, useEffect, createContext, useContext } from 'react'
import {
    FiHome, FiBarChart2, FiUsers, FiInfo, FiList, FiUser, FiMessageSquare,
    FiSettings, FiZap, FiChevronRight, FiSend, FiSearch, FiPlay
} from 'react-icons/fi'
import { GiCrossedSwords } from 'react-icons/gi'
import { Link, useNavigate } from '@tanstack/react-router'
import { AuthProvider, useAuthContext } from '../contexts/AuthContext'

interface MyRouterContext {
    queryClient: QueryClient
}

const NAV_ITEMS = [
    { icon: FiHome, label: 'Home', to: '/' },
    { icon: FiPlay, label: 'Play', to: '/gameseries/gs-qf1' },
    { icon: FiMessageSquare, label: 'Messages', to: '/messenger' },
    { icon: FiSearch, label: 'Search', to: '/search' },
    { icon: FiBarChart2, label: 'Stats', to: '/stats' },
    { icon: GiCrossedSwords, label: 'Champions', to: '/champions' },
    { icon: FiList, label: 'Tierlist', to: '/tierlist' },
    { icon: FiZap, label: 'Tournaments', to: '/tournaments' },
    { icon: FiUsers, label: 'Community', to: '/community' },
    { icon: FiInfo, label: 'About', to: '/about' },
]

const HIDDEN_ROUTES = new Set(['/', '/login', '/onboarding'])

// ─── Social Dock Data ─────────────────────────────────────────────
interface DummyFriend { id: string; name: string; tag: string; online: boolean; inGame: boolean }
interface DummyClub { id: string; name: string; tag: string; members: number; rank: string }
interface DummyGroup { id: string; name: string; members: number; activity: string }

const DUMMY_FRIENDS: DummyFriend[] = [
    { id: 'f1', name: 'ProGamer99', tag: '#7731', online: true, inGame: false },
    { id: 'f2', name: 'NightOwl', tag: '#4402', online: true, inGame: true },
    { id: 'f3', name: 'DragonSlayer', tag: '#1190', online: true, inGame: false },
    { id: 'f4', name: 'ShadowStrike', tag: '#8821', online: false, inGame: false },
    { id: 'f5', name: 'CyberNinja', tag: '#3310', online: false, inGame: false },
]

const DUMMY_CLUBS: DummyClub[] = [
    { id: 'c1', name: 'Elite Players', tag: 'ELTP', members: 128, rank: 'Diamond' },
    { id: 'c2', name: 'Pro League', tag: 'PROL', members: 256, rank: 'Master' },
    { id: 'c3', name: 'Casual Gaming', tag: 'CSLG', members: 89, rank: 'Gold' },
]

const DUMMY_GROUPS: DummyGroup[] = [
    { id: 'g1', name: 'Tournament Team', members: 12, activity: 'Playing' },
    { id: 'g2', name: 'Stream Squad', members: 24, activity: 'Active' },
    { id: 'g3', name: 'Practice Group', members: 8, activity: 'Idle' },
    { id: 'g4', name: 'Ranked Pushers', members: 16, activity: 'Ranked' },
]

const RANK_COLORS: Record<string, string> = {
    Diamond: '#06B6D4',
    Master: '#a600ff',
    Gold: '#F59E0B',
}

// Social dock toggle context
export const SocialDockContext = createContext<{ open: boolean; toggle: () => void }>({ open: true, toggle: () => {} })

// Magnification config
const BASE_SIZE = 16   // icon px at rest
const MAX_SIZE = 24   // icon px at peak
const RADIUS = 1.8  // how many neighbours are affected (in item-widths)



function TopDock() {
    const location = useRouterState({ select: s => s.location.pathname })
    const hasError = useRouterState({ select: s => s.matches.some(m => m.status === 'error') })
    const isSplat = useRouterState({ select: s => s.matches.some(m => m.routeId === '/$') })
    const [mouseIdx, setMouseIdx] = useState<number | null>(null)
    const navRef = useRef<HTMLElement>(null)
    const { open: dockOpen, toggle: toggleDock } = useContext(SocialDockContext)
    const { user, isAuthenticated } = useAuthContext()

    const getScale = useCallback((i: number): number => {
        if (mouseIdx === null) return 1
        const dist = Math.abs(i - mouseIdx)
        if (dist > RADIUS) return 1
        // cosine falloff: 1 → MAX_SIZE/BASE_SIZE at dist=0
        const t = 1 - dist / RADIUS
        const maxScale = MAX_SIZE / BASE_SIZE
        return 1 + (maxScale - 1) * Math.cos((1 - t) * Math.PI * 0.5)
    }, [mouseIdx])

    if (HIDDEN_ROUTES.has(location) || isSplat || hasError) return null

    return (
        <>
            <style>{`
        .top-dock {
          position: fixed;
          top: 0;
          left: 0;
          right: 0;
          z-index: 100;
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 0;
          height: 52px;
          padding: 0 40px;
          background: rgba(0,0,0,0.85);
          border-bottom: 1px solid rgba(255,255,255,0.04);
          backdrop-filter: blur(24px);
        }
        .dock-divider {
          width: 1px;
          height: 20px;
          background: rgba(255,255,255,0.06);
          margin: 0 8px;
          flex-shrink: 0;
        }
        .dock-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 2px;
          padding: 6px 16px;
          text-decoration: none;
          color: rgba(255,255,255,0.4);
          border-radius: 8px;
          transition:
            transform 180ms cubic-bezier(.34,1.56,.64,1),
            color 150ms,
            background 150ms,
            box-shadow 150ms;
          font-family: 'Chakra Petch', monospace;
          white-space: nowrap;
        }
        .dock-item:hover {
          color: #c77dff;
          background: rgba(166,0,255,0.08);
          transform: scale(1.08);
          box-shadow: 0 0 16px rgba(166,0,255,0.15);
        }
        .dock-item.active {
          color: #a600ff;
          background: rgba(166,0,255,0.1);
        }
        .dock-item:hover svg {
          filter: drop-shadow(0 0 6px rgba(166,0,255,0.7));
        }
        .dock-item.active svg {
          filter: drop-shadow(0 0 8px rgba(166,0,255,0.9));
        }
        .dock-item-icon {
          display: flex;
          align-items: center;
          justify-content: center;
        }
        .dock-label {
          font-size: 8px;
          letter-spacing: 0.08em;
          text-transform: uppercase;
          opacity: 0.6;
          line-height: 1;
          transition: opacity 150ms;
        }
        .dock-item:hover .dock-label,
        .dock-item.active .dock-label {
          opacity: 1;
        }
        .dock-avatar-btn {
          width: 32px; height: 32px; border-radius: 50%;
          background: rgba(166,0,255,0.08);
          border: 1px solid rgba(166,0,255,0.15);
          cursor: pointer;
          display: flex; align-items: center; justify-content: center;
          transition: all 200ms;
          flex-shrink: 0;
        }
        .dock-avatar-btn:hover {
          background: rgba(166,0,255,0.15);
          border-color: rgba(166,0,255,0.3);
          box-shadow: 0 0 12px rgba(166,0,255,0.2);
        }
        .dock-avatar-btn--active {
          background: rgba(166,0,255,0.15);
          border-color: rgba(166,0,255,0.35);
          box-shadow: 0 0 12px rgba(166,0,255,0.25);
        }
        .dock-avatar-initials {
          font-family: 'Russo One', sans-serif;
          font-size: 11px;
          color: rgba(255,255,255,0.7);
          letter-spacing: 0.03em;
        }
        /* ─── Global spinning logo styles ────────────── */
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to   { transform: rotate(360deg); }
        }
        @keyframes logo-breathe {
          0%, 100% { filter: drop-shadow(0 0 60px #a600ffcc) drop-shadow(0 0 140px #a600ff66); }
          50%       { filter: drop-shadow(0 0 100px #a600ffff) drop-shadow(0 0 200px #a600ff88); }
        }

        .global-spinning-logo {
          position: fixed;
          animation: spin-slow 28s linear infinite, logo-breathe 5s ease-in-out infinite;
          pointer-events: none;
          z-index: 0;
          transition:
            top 0.9s cubic-bezier(.4,0,.2,1),
            left 0.9s cubic-bezier(.4,0,.2,1),
            width 0.9s cubic-bezier(.4,0,.2,1),
            height 0.9s cubic-bezier(.4,0,.2,1),
            opacity 0.9s ease,
            translate 0.9s cubic-bezier(.4,0,.2,1);
        }

        /* Logo variants based on route */
        .global-spinning-logo--hidden {
          opacity: 0 !important;
          pointer-events: none;
        }
        .global-spinning-logo--hero {
          top: 50%; left: 22%;
          translate: -50% -50%;
          width: min(52vw, 52vh);
          height: min(52vw, 52vh);
          opacity: 1;
        }
        .global-spinning-logo--center {
          top: 50%; left: 50%;
          translate: -50% -50%;
          width: min(82vw, 82vh);
          height: min(82vw, 82vh);
          opacity: 0.18;
        }
        .global-spinning-logo--large {
          top: 50%; left: 50%;
          translate: -50% -50%;
          width: min(88vw, 88vh);
          height: min(88vw, 88vh);
          opacity: 0.13;
        }

        `}</style>


            <nav
                ref={navRef}
                className="top-dock"
                aria-label="Main navigation"
                onMouseLeave={() => setMouseIdx(null)}
            >
                {NAV_ITEMS.map((item, i) => {
                    return (
                        <span key={item.to} style={{ display: 'contents' }}>
                            {i === 6 && <div className="dock-divider" />}
                            <Link
                                to={item.to}
                                className="dock-item"
                                activeProps={{ className: 'dock-item active' }}
                                aria-label={item.label}
                                onMouseEnter={() => setMouseIdx(i)}
                            >
                                <div className="dock-item-icon">
                                    <item.icon size={16} />
                                </div>
                                <span className="dock-label">
                                    {item.label}
                                </span>
                            </Link>
                        </span>
                    )
                })}

                {isAuthenticated && (
                    <>
                        <div className="dock-divider" />
                        <button
                            className={`dock-avatar-btn ${dockOpen ? 'dock-avatar-btn--active' : ''}`}
                            onClick={toggleDock}
                            aria-label="Toggle profile panel"
                        >
                            <span className="dock-avatar-initials">
                                {user?.nickname?.slice(0, 2).toUpperCase() ?? '??'}
                            </span>
                        </button>
                    </>
                )}
            </nav>
        </>
    )
}


export const Route = createRootRouteWithContext<MyRouterContext>()({
    beforeLoad: async () => {
        if (typeof document !== 'undefined') {
            document.documentElement.setAttribute('lang', getLocale())
        }
    },

    head: () => ({
        meta: [
            { charSet: 'utf-8' },
            { name: 'viewport', content: 'width=device-width, initial-scale=1' },
            { title: 'Akiora' },
        ],
        links: [{ rel: 'stylesheet', href: appCss }],
    }),
    shellComponent: RootDocument,
})

function UserWidget({ user }: { user: { nickname: string } | null }) {
    const [dropdownOpen, setDropdownOpen] = useState(false)
    const navigate = useNavigate()
    const ref = useRef<HTMLDivElement>(null)

    useEffect(() => {
        function onClickOutside(e: MouseEvent) {
            if (ref.current && !ref.current.contains(e.target as Node)) setDropdownOpen(false)
        }
        document.addEventListener('mousedown', onClickOutside)
        return () => document.removeEventListener('mousedown', onClickOutside)
    }, [])

    const initials = user?.nickname?.slice(0, 2).toUpperCase() ?? '??'

    return (
        <div ref={ref} style={{ position: 'relative', display: 'flex', flexDirection: 'column', alignItems: 'center', gap: '10px' }}>
            <button
                onClick={() => setDropdownOpen(v => !v)}
                style={{
                    width: '44px', height: '44px', borderRadius: '50%',
                    background: 'rgba(166,0,255,0.08)',
                    border: '1px solid rgba(166,0,255,0.15)',
                    boxShadow: dropdownOpen
                        ? '0 0 0 2px rgba(166,0,255,0.15)'
                        : 'none',
                    cursor: 'pointer',
                    display: 'flex', alignItems: 'center', justifyContent: 'center',
                    transition: 'box-shadow 200ms',
                    flexShrink: 0,
                }}
            >
                <span style={{ fontFamily: "'Russo One', sans-serif", fontSize: '13px', color: 'rgba(255,255,255,0.7)', letterSpacing: '0.05em' }}>{initials}</span>
            </button>
            <div style={{ textAlign: 'center' }}>
                <p style={{ margin: 0, fontFamily: "'Chakra Petch', monospace", fontSize: '11px', fontWeight: 500, color: 'rgba(255,255,255,0.8)' }}>
                    {user?.nickname ?? 'Guest'}
                </p>
                <p style={{ margin: '2px 0 0', fontFamily: "'Chakra Petch', monospace", fontSize: '9px', color: 'rgba(16,185,129,0.7)', display: 'flex', alignItems: 'center', gap: '4px', justifyContent: 'center' }}>
                    <span style={{ width: '4px', height: '4px', borderRadius: '50%', background: '#10B981', display: 'inline-block' }} />
                    Online
                </p>
            </div>

            {dropdownOpen && (
                <div style={{
                    position: 'absolute', top: '70px', left: '50%', transform: 'translateX(-50%)',
                    width: '150px', zIndex: 100,
                    background: 'rgba(0,0,0,0.8)',
                    border: '1px solid rgba(166,0,255,0.1)',
                    borderRadius: '10px',
                    boxShadow: '0 8px 32px rgba(0,0,0,0.6), 0 0 12px rgba(166,0,255,0.08)',
                    backdropFilter: 'blur(20px)',
                    overflow: 'hidden',
                    padding: '4px',
                }}>
                    <button
                        onClick={() => { setDropdownOpen(false); navigate({ to: '/profile' }) }}
                        style={{
                            width: '100%', padding: '8px 12px', background: 'transparent',
                            border: 'none', borderRadius: '6px', cursor: 'pointer',
                            display: 'flex', alignItems: 'center', gap: '10px',
                            color: 'rgba(255,255,255,0.85)',
                            fontFamily: "'Chakra Petch', monospace", fontSize: '11px', fontWeight: 500,
                            transition: 'background 150ms, color 150ms',
                        }}
                        onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.background = 'rgba(166,0,255,0.1)'; (e.currentTarget as HTMLButtonElement).style.color = '#fff' }}
                        onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.background = 'transparent'; (e.currentTarget as HTMLButtonElement).style.color = 'rgba(255,255,255,0.85)' }}
                    >
                        <FiUser size={13} /> Profile
                    </button>
                    <button
                        onClick={() => setDropdownOpen(false)}
                        style={{
                            width: '100%', padding: '8px 12px', background: 'transparent',
                            border: 'none', borderRadius: '6px', cursor: 'pointer',
                            display: 'flex', alignItems: 'center', gap: '10px',
                            color: 'rgba(255,255,255,0.85)',
                            fontFamily: "'Chakra Petch', monospace", fontSize: '11px', fontWeight: 500,
                            transition: 'background 150ms, color 150ms',
                        }}
                        onMouseEnter={e => { (e.currentTarget as HTMLButtonElement).style.background = 'rgba(166,0,255,0.1)'; (e.currentTarget as HTMLButtonElement).style.color = '#fff' }}
                        onMouseLeave={e => { (e.currentTarget as HTMLButtonElement).style.background = 'transparent'; (e.currentTarget as HTMLButtonElement).style.color = 'rgba(255,255,255,0.85)' }}
                    >
                        <FiSettings size={13} /> Settings
                    </button>
                </div>
            )}
        </div>
    )
}

function SectionHeader({ icon, label, count, open, onToggle }: { icon: React.ReactNode; label: string; count: number; open: boolean; onToggle: () => void }) {
    return (
        <button
            onClick={onToggle}
            style={{
                width: '100%', display: 'flex', alignItems: 'center', gap: '8px',
                padding: '8px 14px', background: 'transparent', border: 'none',
                cursor: 'pointer',
            }}
        >
            <span style={{ color: 'rgba(166,0,255,0.5)', display: 'flex' }}>{icon}</span>
            <span style={{ flex: 1, textAlign: 'left', fontFamily: "'Chakra Petch', monospace", fontSize: '9px', fontWeight: 600, letterSpacing: '0.14em', textTransform: 'uppercase', color: 'rgba(255,255,255,0.35)' }}>
                {label}
            </span>
            <span style={{ fontFamily: "'Chakra Petch', monospace", fontSize: '9px', color: 'rgba(166,0,255,0.4)' }}>{count}</span>
            <span style={{ color: 'rgba(255,255,255,0.3)', display: 'flex', transition: 'transform 200ms', transform: open ? 'rotate(90deg)' : 'rotate(0deg)' }}>
                <FiChevronRight size={12} />
            </span>
        </button>
    )
}

function SocialDock() {
    const { user, isAuthenticated } = useAuthContext()
    const location = useRouterState({ select: s => s.location.pathname })
    const isSplat = useRouterState({ select: s => s.matches.some(m => m.routeId === '/$') })
    const hasError = useRouterState({ select: s => s.matches.some(m => m.status === 'error') })
    const { open: dockOpen } = useContext(SocialDockContext)
    const [openFriends, setOpenFriends] = useState(true)
    const [openClubs, setOpenClubs] = useState(true)
    const [openGroups, setOpenGroups] = useState(true)
    const [miniChat, setMiniChat] = useState<{ id: string; name: string; type: 'friend' | 'club' | 'group' } | null>(null)
    const [miniMessages, setMiniMessages] = useState<{ id: number; text: string; own: boolean; time: string }[]>([])
    const [miniInput, setMiniInput] = useState('')

    if (!isAuthenticated || !dockOpen || HIDDEN_ROUTES.has(location) || isSplat || hasError) return null

    const onlineFriends = DUMMY_FRIENDS.filter(f => f.online)
    const offlineFriends = DUMMY_FRIENDS.filter(f => !f.online)

    const toggleMiniChat = (id: string, name: string, type: 'friend' | 'club' | 'group') => {
        if (miniChat?.id === id) {
            setMiniChat(null)
        } else {
            setMiniChat({ id, name, type })
            setMiniMessages([
                { id: 1, text: 'Hey! How are you?', own: false, time: '12:30' },
                { id: 2, text: 'All good, just grinding ranked', own: true, time: '12:31' },
                { id: 3, text: 'Nice, want to duo?', own: false, time: '12:32' },
            ])
            setMiniInput('')
        }
    }

    const handleMiniSend = () => {
        if (!miniInput.trim()) return
        setMiniMessages(prev => [...prev, {
            id: Date.now(),
            text: miniInput.trim(),
            own: true,
            time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
        }])
        setMiniInput('')
    }

    return (
        <>
            <style>{`
                @keyframes pulse-dot {
                    0%, 100% { opacity: 1; box-shadow: 0 0 4px currentColor; }
                    50% { opacity: 0.5; box-shadow: 0 0 2px currentColor; }
                }
                .social-dock {
                    position: absolute;
                    top: 52px;
                    right: 0;
                    width: 240px;
                    height: calc(100vh - 52px);
                    background: rgba(0,0,0,0.4);
                    border-left: 1px solid rgba(166,0,255,0.06);
                    display: flex;
                    flex-direction: column;
                    backdrop-filter: blur(24px) saturate(1.1);
                    z-index: 50;
                }
                .social-dock-header {
                    padding: 14px 12px 10px;
                    border-bottom: 1px solid rgba(166,0,255,0.06);
                }
                .social-dock-divider {
                    height: 1px;
                    background: rgba(166,0,255,0.06);
                    margin: 6px 12px;
                }
                .social-dock-scroll {
                    flex: 1;
                    overflow-y: auto;
                    padding: 4px 0 16px;
                }
                .social-dock-scroll::-webkit-scrollbar { width: 2px; }
                .social-dock-scroll::-webkit-scrollbar-thumb { background: rgba(166,0,255,0.1); border-radius: 1px; }
                .dock-card {
                    display: flex; align-items: center; gap: 10px;
                    padding: 6px 12px; margin: 0 6px 1px;
                    border-radius: 8px; cursor: pointer;
                    border: 1px solid transparent;
                    transition: all 150ms ease;
                }
                .dock-card:hover {
                    background: rgba(166,0,255,0.06);
                    border-color: rgba(166,0,255,0.1);
                }
                .dock-avatar {
                    width: 28px; height: 28px; border-radius: 50%;
                    display: flex; align-items: center; justify-content: center;
                    font-family: 'Russo One', sans-serif; font-size: 10px;
                    color: #fff; flex-shrink: 0; position: relative;
                }
                .dock-avatar-square { border-radius: 6px !important; }
                .dock-avatar-online::after {
                    content: ''; position: absolute; bottom: -1px; right: -1px;
                    width: 7px; height: 7px; border-radius: 50%;
                    background: #10B981;
                    border: 2px solid rgba(0,0,0,0.9);
                }
                .dock-avatar-ingame::after {
                    background: #F59E0B;
                    animation: pulse-dot 1.6s ease-in-out infinite;
                }
                .dock-name {
                    font-family: 'Chakra Petch', monospace; font-size: 11px;
                    font-weight: 500; color: rgba(255,255,255,0.85); white-space: nowrap;
                    overflow: hidden; text-overflow: ellipsis;
                }
                .dock-meta {
                    font-family: 'Chakra Petch', monospace; font-size: 9px;
                    color: rgba(255,255,255,0.3); white-space: nowrap;
                }
                .dock-offline { opacity: 0.35; }
                .dock-badge {
                    margin-left: auto; padding: 2px 5px;
                    border-radius: 4px; font-family: 'Chakra Petch', monospace;
                    font-size: 8px; font-weight: 600; letter-spacing: 0.03em;
                    flex-shrink: 0;
                }
                .section-label {
                    margin: 8px 14px 3px;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 8px;
                    letter-spacing: 0.12em;
                    text-transform: uppercase;
                    color: rgba(255,255,255,0.12);
                }
                .mini-chat {
                    position: fixed;
                    bottom: 0;
                    right: 240px;
                    width: 300px;
                    height: 380px;
                    background: rgba(0,0,0,0.85);
                    border: 1px solid rgba(166,0,255,0.1);
                    border-bottom: none;
                    border-radius: 12px 12px 0 0;
                    backdrop-filter: blur(24px);
                    display: flex;
                    flex-direction: column;
                    z-index: 60;
                    box-shadow: 0 -4px 24px rgba(0,0,0,0.5), 0 0 12px rgba(166,0,255,0.06);
                }
                .mini-chat-header {
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    padding: 10px 14px;
                    border-bottom: 1px solid rgba(166,0,255,0.08);
                    cursor: pointer;
                }
                .mini-chat-header:hover { background: rgba(166,0,255,0.04); }
                .mini-chat-title {
                    flex: 1;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 12px;
                    font-weight: 500;
                    color: rgba(255,255,255,0.85);
                }
                .mini-chat-close {
                    background: none; border: none; color: rgba(255,255,255,0.4);
                    cursor: pointer; padding: 2px; display: flex;
                    transition: color 150ms;
                }
                .mini-chat-close:hover { color: #fff; }
                .mini-chat-messages {
                    flex: 1;
                    overflow-y: auto;
                    padding: 10px 12px;
                    display: flex;
                    flex-direction: column;
                    gap: 6px;
                }
                .mini-chat-messages::-webkit-scrollbar { width: 2px; }
                .mini-chat-messages::-webkit-scrollbar-thumb { background: rgba(166,0,255,0.1); }
                .mini-msg {
                    max-width: 80%;
                    padding: 6px 10px;
                    border-radius: 10px;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    color: #fff;
                    line-height: 1.4;
                }
                .mini-msg-own {
                    align-self: flex-end;
                    background: rgba(166,0,255,0.15);
                    border: 1px solid rgba(166,0,255,0.2);
                    border-radius: 10px 10px 3px 10px;
                }
                .mini-msg-other {
                    align-self: flex-start;
                    background: rgba(255,255,255,0.05);
                    border: 1px solid rgba(255,255,255,0.04);
                    border-radius: 10px 10px 10px 3px;
                }
                .mini-msg-time {
                    font-size: 8px;
                    color: rgba(255,255,255,0.25);
                    margin-top: 2px;
                }
                .mini-chat-input-wrap {
                    display: flex;
                    gap: 6px;
                    padding: 8px 10px;
                    border-top: 1px solid rgba(166,0,255,0.08);
                }
                .mini-chat-input {
                    flex: 1;
                    padding: 7px 10px;
                    border-radius: 8px;
                    background: rgba(255,255,255,0.04);
                    border: 1px solid rgba(255,255,255,0.06);
                    color: #fff;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    outline: none;
                    transition: border-color 150ms;
                }
                .mini-chat-input:focus { border-color: rgba(166,0,255,0.3); }
                .mini-chat-input::placeholder { color: rgba(255,255,255,0.15); }
                .mini-chat-send {
                    padding: 7px 12px;
                    border-radius: 8px;
                    background: rgba(166,0,255,0.12);
                    border: 1px solid rgba(166,0,255,0.2);
                    color: rgba(255,255,255,0.8);
                    cursor: pointer;
                    display: flex;
                    align-items: center;
                    transition: all 150ms;
                }
                .mini-chat-send:hover { background: rgba(166,0,255,0.2); }
            `}</style>

            <aside className="social-dock">
                <div className="social-dock-header">
                    <UserWidget user={user} />
                </div>

                <div className="social-dock-divider" />

                <div className="social-dock-scroll">
                    {/* Friends */}
                    <SectionHeader
                        icon={<FiUser size={11} />}
                        label="Friends"
                        count={DUMMY_FRIENDS.length}
                        open={openFriends}
                        onToggle={() => setOpenFriends(v => !v)}
                    />
                    {openFriends && (
                        <>
                            {onlineFriends.map(f => (
                                <div key={f.id} className="dock-card" onClick={() => toggleMiniChat(f.id, f.name, 'friend')}
                                    style={miniChat?.id === f.id ? { background: 'rgba(166,0,255,0.1)', borderColor: 'rgba(166,0,255,0.15)' } : undefined}
                                >
                                    <div
                                        className={`dock-avatar ${f.inGame ? 'dock-avatar-ingame' : 'dock-avatar-online'}`}
                                        style={{ background: 'linear-gradient(135deg, rgba(6,182,212,0.8), rgba(3,105,161,0.9))' }}
                                    >
                                        {f.name[0]}
                                    </div>
                                    <div style={{ flex: 1, minWidth: 0 }}>
                                        <p className="dock-name">{f.name}<span style={{ color: 'rgba(255,255,255,0.25)', fontWeight: 400, fontSize: '9px' }}> {f.tag}</span></p>
                                        <p className="dock-meta">{f.inGame ? '🎮 In game' : '● Online'}</p>
                                    </div>
                                </div>
                            ))}
                            {offlineFriends.length > 0 && (
                                <>
                                    <p className="section-label">Offline</p>
                                    {offlineFriends.map(f => (
                                        <div key={f.id} className="dock-card dock-offline">
                                            <div className="dock-avatar" style={{ background: 'rgba(255,255,255,0.06)' }}>{f.name[0]}</div>
                                            <div style={{ flex: 1, minWidth: 0 }}>
                                                <p className="dock-name">{f.name}<span style={{ color: 'rgba(255,255,255,0.15)', fontWeight: 400, fontSize: '9px' }}> {f.tag}</span></p>
                                                <p className="dock-meta">Offline</p>
                                            </div>
                                        </div>
                                    ))}
                                </>
                            )}
                        </>
                    )}

                    <div className="social-dock-divider" style={{ margin: '10px 12px' }} />

                    {/* Clubs */}
                    <SectionHeader
                        icon={<FiZap size={11} />}
                        label="Clubs"
                        count={DUMMY_CLUBS.length}
                        open={openClubs}
                        onToggle={() => setOpenClubs(v => !v)}
                    />
                    {openClubs && DUMMY_CLUBS.map(c => (
                        <div key={c.id} className="dock-card" onClick={() => toggleMiniChat(c.id, c.name, 'club')}
                            style={miniChat?.id === c.id ? { background: 'rgba(166,0,255,0.1)', borderColor: 'rgba(166,0,255,0.15)' } : undefined}
                        >
                            <div className="dock-avatar dock-avatar-square" style={{
                                background: `linear-gradient(135deg, ${RANK_COLORS[c.rank] ?? '#a600ff'}20, ${RANK_COLORS[c.rank] ?? '#a600ff'}60)`,
                                border: `1px solid ${RANK_COLORS[c.rank] ?? '#a600ff'}70`,
                                boxShadow: `0 0 8px ${RANK_COLORS[c.rank] ?? '#a600ff'}30`
                            }}>
                                <span style={{ fontFamily: "'Russo One', sans-serif", fontSize: '9px', color: RANK_COLORS[c.rank] ?? '#fff', textShadow: `0 0 4px ${RANK_COLORS[c.rank] ?? '#a600ff'}` }}>{c.tag[0]}</span>
                            </div>
                            <div style={{ flex: 1, minWidth: 0 }}>
                                <p className="dock-name">{c.name}</p>
                                <p className="dock-meta">{c.members} members</p>
                            </div>
                            <span className="dock-badge" style={{
                                background: `${RANK_COLORS[c.rank] ?? '#a600ff'}15`,
                                color: RANK_COLORS[c.rank] ?? '#a600ff',
                                border: `1px solid ${RANK_COLORS[c.rank] ?? '#a600ff'}50`,
                                textShadow: `0 0 4px ${RANK_COLORS[c.rank] ?? '#a600ff'}60`
                            }}>
                                {c.rank}
                            </span>
                        </div>
                    ))}

                    <div className="social-dock-divider" style={{ margin: '10px 12px' }} />

                    {/* Groups */}
                    <SectionHeader
                        icon={<FiUsers size={11} />}
                        label="Groups"
                        count={DUMMY_GROUPS.length}
                        open={openGroups}
                        onToggle={() => setOpenGroups(v => !v)}
                    />
                    {openGroups && DUMMY_GROUPS.map(g => (
                        <div key={g.id} className="dock-card" onClick={() => toggleMiniChat(g.id, g.name, 'group')}
                            style={miniChat?.id === g.id ? { background: 'rgba(166,0,255,0.1)', borderColor: 'rgba(166,0,255,0.15)' } : undefined}
                        >
                            <div className="dock-avatar dock-avatar-square" style={{
                                background: 'linear-gradient(135deg, rgba(16,185,129,0.2), rgba(5,150,105,0.4))',
                                border: '1px solid rgba(16,185,129,0.4)',
                                boxShadow: '0 0 8px rgba(16,185,129,0.2)'
                            }}>
                                <FiUsers size={12} color="#10B981" />
                            </div>
                            <div style={{ flex: 1, minWidth: 0 }}>
                                <p className="dock-name">{g.name}</p>
                                <p className="dock-meta">{g.members} members</p>
                            </div>
                            <span className="dock-badge" style={{
                                background: 'rgba(16,185,129,0.12)',
                                color: '#10B981',
                                border: '1px solid rgba(16,185,129,0.35)',
                                textShadow: '0 0 4px rgba(16,185,129,0.5)'
                            }}>
                                {g.activity}
                            </span>
                        </div>
                    ))}
                </div>
            </aside>

            {miniChat && (
                <div className="mini-chat">
                    <div className="mini-chat-header" onClick={() => setMiniChat(null)}>
                        <FiMessageSquare size={13} style={{ color: 'rgba(166,0,255,0.6)' }} />
                        <span className="mini-chat-title">{miniChat.name}</span>
                        <button className="mini-chat-close" onClick={(e) => { e.stopPropagation(); setMiniChat(null) }}>
                            <FiChevronRight size={14} style={{ transform: 'rotate(45deg)' }} />
                        </button>
                    </div>
                    <div className="mini-chat-messages">
                        {miniMessages.map(m => (
                            <div key={m.id} style={{ display: 'flex', flexDirection: 'column', alignItems: m.own ? 'flex-end' : 'flex-start' }}>
                                <div className={`mini-msg ${m.own ? 'mini-msg-own' : 'mini-msg-other'}`}>
                                    {m.text}
                                </div>
                                <span className="mini-msg-time" style={{ textAlign: m.own ? 'right' : 'left' }}>{m.time}</span>
                            </div>
                        ))}
                    </div>
                    <div className="mini-chat-input-wrap">
                        <input
                            className="mini-chat-input"
                            placeholder="Message..."
                            value={miniInput}
                            onChange={e => setMiniInput(e.target.value)}
                            onKeyDown={e => { if (e.key === 'Enter') handleMiniSend() }}
                        />
                        <button className="mini-chat-send" onClick={handleMiniSend}>
                            <FiSend size={12} />
                        </button>
                    </div>
                </div>
            )}
        </>
    )
}

function MainContent({ children }: { children: React.ReactNode }) {
    const { isAuthenticated } = useAuthContext()
    const location = useRouterState({ select: s => s.location.pathname })
    const isSplat = useRouterState({ select: s => s.matches.some(m => m.routeId === '/$') })
    const hasError = useRouterState({ select: s => s.matches.some(m => m.status === 'error') })

    const showSidebar = isAuthenticated && !HIDDEN_ROUTES.has(location) && !isSplat && !hasError

    return (
        <div>
            {children}
        </div>
    )
}

function GlobalBackground() {
    const location = useRouterState({ select: s => s.location.pathname })

    let variant = 'center'
    if (location === '/') return null
    if (location === '/login' || location === '/onboarding') variant = 'center'

    return (
        <>
            <div style={{
                position: 'fixed', inset: 0, zIndex: -1, pointerEvents: 'none',
                background: '#000',
            }} aria-hidden="true" />
            <div style={{
                position: 'fixed', inset: 0, zIndex: 0, pointerEvents: 'none',
                background: 'radial-gradient(ellipse at center, transparent 25%, rgba(0,0,0,0.85) 100%)',
            }} aria-hidden="true" />
            <img
                src="/violet-yang.svg"
                alt=""
                className={`global-spinning-logo global-spinning-logo--${variant}`}
                aria-hidden="true"
            />
        </>
    )
}

function RootDocument({ children }: { children: React.ReactNode }) {
    const [dockOpen, setDockOpen] = useState(true)
    const toggleDock = useCallback(() => setDockOpen(v => !v), [])

    return (
        <html lang={getLocale()}>
            <head>
                <HeadContent />
            </head>
            <body>
                <AuthProvider>
                    <SocialDockContext.Provider value={{ open: dockOpen, toggle: toggleDock }}>
                        <GlobalBackground />
                        <TopDock />
                        <SocialDock />
                        <MainContent>
                            {children}
                        </MainContent>
                    </SocialDockContext.Provider>
                </AuthProvider>
                <Scripts />
            </body>
        </html>
    )
}


