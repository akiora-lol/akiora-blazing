import {
    HeadContent,
    Scripts,
    createRootRouteWithContext,
    useRouterState,
} from '@tanstack/react-router'

import { getLocale } from '#/paraglide/runtime'

import appCss from '../styles.css?url'

import { useQueryClient, type QueryClient } from '@tanstack/react-query'

import { useState, useRef, useCallback, useEffect, createContext, useContext } from 'react'
import {
    FiHome, FiUsers, FiInfo, FiUser, FiMessageSquare,
    FiSettings, FiZap, FiChevronRight, FiSend, FiSearch, FiBell, FiCheck, FiX, FiExternalLink
} from 'react-icons/fi'
import { Link, useNavigate } from '@tanstack/react-router'
import { AuthProvider, useAuthContext } from '../contexts/AuthContext'
import {
    useFriends,
    useGetOrCreatePrivateChatMutation,
    useMessages,
    usePendingFriendRequests,
    usePresence,
    useRespondFriendRequestMutation,
    useSendMessage,
} from '../lib/api'

interface MyRouterContext {
    queryClient: QueryClient
}

const NAV_ITEMS = [
    { icon: FiHome, label: 'Home', to: '/' },
    { icon: FiMessageSquare, label: 'Messages', to: '/messenger' },
    { icon: FiSearch, label: 'Search', to: '/search' },
    { icon: FiZap, label: 'Tournaments', to: '/tournaments' },
    { icon: FiUsers, label: 'Community', to: '/community' },
    { icon: FiInfo, label: 'About', to: '/about' },
]

const HIDDEN_ROUTES = new Set(['/', '/login', '/onboarding'])
const SOCKETGW_BASE = import.meta.env.VITE_SOCKETGW_BASE_URL ?? 'ws://localhost:8002'

// ─── Social Dock Data ─────────────────────────────────────────────
interface DockFriend { id: string; name: string; tag: string; online: boolean; inGame: boolean }

// Social dock toggle context
export const SocialDockContext = createContext<{ open: boolean; toggle: () => void }>({ open: true, toggle: () => { } })

function buildSocketUrl(path: string) {
    const base = SOCKETGW_BASE.replace(/^http/i, 'ws').replace(/\/$/, '')
    return `${base}${path}`
}

function useNotificationStream(userId?: string, enabled = true) {
    const queryClient = useQueryClient()

    useEffect(() => {
        if (!enabled || !userId) return

        let socket: WebSocket | null = null
        let retryTimer: number | undefined
        let closed = false

        const invalidateFriendQueries = () => {
            queryClient.invalidateQueries({ queryKey: ['users', 'friend-requests', 'pending', userId] })
            queryClient.invalidateQueries({ queryKey: ['users', 'friends', userId] })
        }

        const connect = () => {
            socket = new WebSocket(buildSocketUrl('/ws/v1/notifications'))

            socket.onmessage = (event) => {
                try {
                    const payload = JSON.parse(event.data)
                    const type: string | undefined = payload?.type
                    if (!type || type === 'notification.connected') return

                    // ─── Chat / message events ────────────────────────────
                    if (type.startsWith('chat.message.') || type === 'chat.message.read') {
                        const chatId: string | undefined =
                            payload.chat_id ?? payload.message?.chat_id
                        const messageId: string | undefined =
                            payload.message_id ?? payload.message?.id

                        // Chat list (last-message preview, unread badge).
                        queryClient.invalidateQueries({ queryKey: ['messenger', 'chats'] })

                        if (chatId) {
                            queryClient.invalidateQueries({ queryKey: ['messenger', 'messages', chatId] })
                            queryClient.invalidateQueries({ queryKey: ['messenger', 'unread-count', chatId] })
                        }

                        // Single-message reads (history, reactions, the message itself).
                        if (messageId) {
                            queryClient.invalidateQueries({ queryKey: ['messenger', 'message', messageId] })
                            queryClient.invalidateQueries({ queryKey: ['messenger', 'message', messageId, 'history'] })
                            queryClient.invalidateQueries({ queryKey: ['messenger', 'message', messageId, 'reactions'] })
                        }
                        return
                    }

                    // ─── Chat membership / lifecycle events ──────────────
                    if (type.startsWith('chat.member.') || type === 'chat.created' || type === 'chat.updated' || type === 'chat.deleted') {
                        const chatId: string | undefined = payload.chat_id ?? payload.chat?.id
                        queryClient.invalidateQueries({ queryKey: ['messenger', 'chats'] })
                        if (chatId) {
                            queryClient.invalidateQueries({ queryKey: ['messenger', 'chat', chatId] })
                            queryClient.invalidateQueries({ queryKey: ['messenger', 'members', chatId] })
                        }
                        return
                    }

                    // ─── Friend-request events ───────────────────────────
                    if (type.startsWith('friend.request.') || type === 'friend.removed') {
                        invalidateFriendQueries()
                        return
                    }

                    // ─── Persisted notifications (from notification svc) ─
                    if (type === 'friend_request' || type.startsWith('notification.')) {
                        invalidateFriendQueries()
                        queryClient.invalidateQueries({ queryKey: ['notifications', userId] })
                        return
                    }
                } catch (error) {
                    console.warn('Failed to process notification event', error)
                }
            }

            socket.onclose = () => {
                if (closed) return
                retryTimer = window.setTimeout(connect, 2500)
            }

            socket.onerror = () => {
                socket?.close()
            }
        }

        connect()

        return () => {
            closed = true
            if (retryTimer) window.clearTimeout(retryTimer)
            socket?.close()
        }
    }, [enabled, queryClient, userId])
}

function RealtimeBridge() {
    const { user, isAuthenticated } = useAuthContext()
    useNotificationStream(user?.id, isAuthenticated)
    return null
}

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
    const [notificationsOpen, setNotificationsOpen] = useState(false)
    const { data: pendingRequests = [] } = usePendingFriendRequests(user?.id)
    const respondFriendRequest = useRespondFriendRequestMutation(user?.id)
    const notificationCount = pendingRequests.length

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
        .dock-icon-btn {
          position: relative;
          width: 32px; height: 32px; border-radius: 50%;
          background: rgba(255,255,255,0.035);
          border: 1px solid rgba(255,255,255,0.07);
          color: rgba(255,255,255,0.55);
          cursor: pointer;
          display: inline-flex; align-items: center; justify-content: center;
          transition: background 150ms, color 150ms, border-color 150ms, box-shadow 150ms;
          flex-shrink: 0;
        }
        .dock-icon-btn:hover,
        .dock-icon-btn--active {
          color: #fff;
          background: rgba(166,0,255,0.12);
          border-color: rgba(166,0,255,0.28);
          box-shadow: 0 0 12px rgba(166,0,255,0.18);
        }
        .dock-notification-dot {
          position: absolute; top: -3px; right: -4px;
          min-width: 16px; height: 16px; padding: 0 4px;
          border-radius: 999px;
          background: #FF002A;
          border: 2px solid rgba(0,0,0,0.9);
          color: #fff;
          font-family: 'Chakra Petch', monospace;
          font-size: 9px; font-weight: 700;
          display: inline-flex; align-items: center; justify-content: center;
          line-height: 1;
        }
        .notifications-popover {
          position: absolute;
          top: 44px;
          right: 48px;
          width: 300px;
          padding: 10px;
          border-radius: 12px;
          background: rgba(0,0,0,0.9);
          border: 1px solid rgba(166,0,255,0.16);
          box-shadow: 0 18px 60px rgba(0,0,0,0.55), 0 0 20px rgba(166,0,255,0.08);
          backdrop-filter: blur(22px);
        }
        .notifications-title {
          margin: 2px 2px 10px;
          font-family: 'Russo One', sans-serif;
          font-size: 11px;
          color: rgba(255,255,255,0.78);
          letter-spacing: 0.06em;
          text-transform: uppercase;
        }
        .notification-empty {
          margin: 0;
          padding: 18px 8px;
          color: rgba(255,255,255,0.28);
          font-family: 'Chakra Petch', monospace;
          font-size: 11px;
          text-align: center;
        }
        .notification-item {
          display: grid;
          grid-template-columns: 32px minmax(0, 1fr);
          gap: 9px;
          padding: 9px;
          border-radius: 9px;
          background: rgba(255,255,255,0.035);
          border: 1px solid rgba(255,255,255,0.06);
        }
        .notification-name {
          margin: 0;
          color: rgba(255,255,255,0.84);
          font-family: 'Chakra Petch', monospace;
          font-size: 12px;
          white-space: nowrap;
          overflow: hidden;
          text-overflow: ellipsis;
        }
        .notification-meta {
          margin: 2px 0 8px;
          color: rgba(255,255,255,0.35);
          font-family: 'Chakra Petch', monospace;
          font-size: 10px;
        }
        .notification-actions {
          display: flex;
          gap: 6px;
        }
        .notification-action {
          min-height: 28px;
          padding: 5px 8px;
          border-radius: 7px;
          border: 1px solid rgba(255,255,255,0.08);
          background: rgba(255,255,255,0.04);
          color: rgba(255,255,255,0.65);
          cursor: pointer;
          display: inline-flex; align-items: center; gap: 5px;
          font-family: 'Chakra Petch', monospace; font-size: 10px;
        }
        .notification-action.accept { border-color: rgba(16,185,129,0.25); background: rgba(16,185,129,0.08); }
        .notification-action.decline { border-color: rgba(255,0,42,0.22); background: rgba(255,0,42,0.07); }
        .notification-action:hover:not(:disabled) { color: #fff; }
        .notification-action:disabled { opacity: 0.45; cursor: not-allowed; }
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
                        <div style={{ position: 'relative' }}>
                            <button
                                className={`dock-icon-btn ${notificationsOpen ? 'dock-icon-btn--active' : ''}`}
                                onClick={() => setNotificationsOpen(v => !v)}
                                aria-label="Notifications"
                            >
                                <FiBell size={15} />
                                {notificationCount > 0 && <span className="dock-notification-dot">{notificationCount}</span>}
                            </button>
                            {notificationsOpen && (
                                <div className="notifications-popover">
                                    <h2 className="notifications-title">Notifications</h2>
                                    {pendingRequests.length === 0 ? (
                                        <p className="notification-empty">No new notifications</p>
                                    ) : pendingRequests.map(({ friendship, user: requestUser }) => (
                                        <div key={friendship.id} className="notification-item">
                                            <div className="dock-avatar" style={{ background: 'linear-gradient(135deg, rgba(166,0,255,0.5), rgba(6,182,212,0.55))' }}>
                                                {(requestUser.nickname || requestUser.email || '?')[0]}
                                            </div>
                                            <div style={{ minWidth: 0 }}>
                                                <p className="notification-name">{requestUser.nickname || requestUser.email}</p>
                                                <p className="notification-meta">Sent you a friend request</p>
                                                <div className="notification-actions">
                                                    <button
                                                        className="notification-action accept"
                                                        disabled={respondFriendRequest.isPending}
                                                        onClick={() => respondFriendRequest.mutate({ request_id: friendship.id, responder_id: user?.id ?? '', accept: true })}
                                                    >
                                                        <FiCheck size={12} /> Accept
                                                    </button>
                                                    <button
                                                        className="notification-action decline"
                                                        disabled={respondFriendRequest.isPending}
                                                        onClick={() => respondFriendRequest.mutate({ request_id: friendship.id, responder_id: user?.id ?? '', accept: false })}
                                                    >
                                                        <FiX size={12} /> Decline
                                                    </button>
                                                </div>
                                            </div>
                                        </div>
                                    ))}
                                </div>
                            )}
                        </div>
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
    const navigate = useNavigate()
    const location = useRouterState({ select: s => s.location.pathname })
    const isSplat = useRouterState({ select: s => s.matches.some(m => m.routeId === '/$') })
    const hasError = useRouterState({ select: s => s.matches.some(m => m.status === 'error') })
    const { open: dockOpen } = useContext(SocialDockContext)
    const [openFriends, setOpenFriends] = useState(true)
    const [miniChat, setMiniChat] = useState<{ id: string; name: string; type: 'friend' | 'club' | 'group'; chatId?: string } | null>(null)
    const [demoMiniMessages, setDemoMiniMessages] = useState<{ id: number; text: string; own: boolean; time: string }[]>([])
    const [miniInput, setMiniInput] = useState('')
    const getOrCreatePrivateChat = useGetOrCreatePrivateChatMutation()
    const sendMessage = useSendMessage()
    const {
        data: friendItems = [],
        isError: friendsError,
        isLoading: friendsLoading,
    } = useFriends(user?.id)
    const {
        data: pendingRequests = [],
        isLoading: pendingRequestsLoading,
    } = usePendingFriendRequests(user?.id)
    const respondFriendRequest = useRespondFriendRequestMutation(user?.id)
    const { data: miniApiMessages = [], isLoading: miniMessagesLoading } = useMessages(miniChat?.chatId ?? '', 40)

    const friendIds = friendItems.map(({ user: friendUser }) => friendUser.id)
    const { data: presenceMap = {} } = usePresence(friendIds)

    if (!isAuthenticated || !dockOpen || HIDDEN_ROUTES.has(location) || isSplat || hasError) return null

    const friends: DockFriend[] = friendItems.map(({ user: friendUser }) => ({
        id: friendUser.id,
        name: friendUser.nickname || friendUser.email,
        tag: friendUser.email ? `#${friendUser.email.split('@')[0]}` : '',
        online: Boolean(presenceMap[friendUser.id]),
        inGame: false,
    }))
    const onlineFriends = friends.filter(f => f.online)
    const offlineFriends = friends.filter(f => !f.online)

    const toggleMiniChat = async (id: string, name: string, type: 'friend' | 'club' | 'group') => {
        if (miniChat?.id === id) {
            setMiniChat(null)
        } else {
            if (type === 'friend' && user?.id) {
                const chat = await getOrCreatePrivateChat.mutateAsync({ userId: user.id, friendId: id })
                setMiniChat({ id, name, type, chatId: chat.id })
            } else {
                setMiniChat({ id, name, type })
                setDemoMiniMessages([
                    { id: 1, text: 'Hey! How are you?', own: false, time: '12:30' },
                    { id: 2, text: 'All good, just checking this chat', own: true, time: '12:31' },
                ])
            }
            setMiniInput('')
        }
    }

    const handleMiniSend = async () => {
        if (!miniInput.trim()) return
        if (miniChat?.chatId && user?.id) {
            await sendMessage.mutateAsync({
                chat_id: miniChat.chatId,
                creator_id: user.id,
                body: miniInput.trim(),
            })
        } else {
            setDemoMiniMessages(prev => [...prev, {
                id: Date.now(),
                text: miniInput.trim(),
                own: true,
                time: new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
            }])
        }
        setMiniInput('')
    }

    const openFullMessenger = () => {
        const chatId = miniChat?.chatId
        setMiniChat(null)
        navigate({ to: '/messenger', search: chatId ? { chat: chatId } : undefined })
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
                .dock-offline { opacity: 0.48; }
                .dock-offline:hover { opacity: 0.82; }
                .dock-badge {
                    margin-left: auto; padding: 2px 5px;
                    border-radius: 4px; font-family: 'Chakra Petch', monospace;
                    font-size: 8px; font-weight: 600; letter-spacing: 0.03em;
                    flex-shrink: 0;
                }
                .friend-request-card {
                    display: grid; grid-template-columns: 28px minmax(0, 1fr); gap: 10px;
                    padding: 8px 10px; margin: 0 6px 6px;
                    border-radius: 9px;
                    background: rgba(166,0,255,0.055);
                    border: 1px solid rgba(166,0,255,0.12);
                }
                .friend-request-actions {
                    display: grid; grid-template-columns: 1fr 1fr; gap: 6px; margin-top: 7px;
                }
                .friend-request-action {
                    min-height: 30px; border-radius: 7px;
                    border: 1px solid rgba(255,255,255,0.08);
                    background: rgba(255,255,255,0.035);
                    color: rgba(255,255,255,0.65);
                    cursor: pointer;
                    display: inline-flex; align-items: center; justify-content: center; gap: 5px;
                    font-family: 'Chakra Petch', monospace; font-size: 10px;
                    transition: color 150ms, border-color 150ms, background 150ms;
                }
                .friend-request-action.accept { border-color: rgba(16,185,129,0.26); background: rgba(16,185,129,0.08); }
                .friend-request-action.decline { border-color: rgba(255,0,42,0.22); background: rgba(255,0,42,0.07); }
                .friend-request-action:hover:not(:disabled) { color: #fff; }
                .friend-request-action:disabled { opacity: 0.45; cursor: not-allowed; }
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
                .mini-chat-open {
                    min-height: 28px;
                    padding: 5px 8px;
                    border-radius: 7px;
                    background: rgba(166,0,255,0.1);
                    border: 1px solid rgba(166,0,255,0.18);
                    color: rgba(255,255,255,0.66);
                    cursor: pointer;
                    display: inline-flex;
                    align-items: center;
                    gap: 5px;
                    font-family: 'Chakra Petch', monospace;
                    font-size: 10px;
                    transition: color 150ms, background 150ms, border-color 150ms;
                }
                .mini-chat-open:hover {
                    color: #fff;
                    background: rgba(166,0,255,0.18);
                    border-color: rgba(166,0,255,0.32);
                }
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
                        count={friends.length + pendingRequests.length}
                        open={openFriends}
                        onToggle={() => setOpenFriends(v => !v)}
                    />
                    {openFriends && (
                        <>
                            {(pendingRequestsLoading || pendingRequests.length > 0) && (
                                <p className="section-label">Incoming requests</p>
                            )}
                            {pendingRequestsLoading && (
                                <p className="section-label">Loading requests...</p>
                            )}
                            {pendingRequests.map(({ friendship, user: requestUser }) => (
                                <div key={friendship.id} className="friend-request-card">
                                    <div className="dock-avatar" style={{ background: 'linear-gradient(135deg, rgba(166,0,255,0.5), rgba(6,182,212,0.55))' }}>
                                        {(requestUser.nickname || requestUser.email || '?')[0]}
                                    </div>
                                    <div style={{ minWidth: 0 }}>
                                        <p className="dock-name">{requestUser.nickname || requestUser.email}</p>
                                        <p className="dock-meta">Wants to add you</p>
                                        <div className="friend-request-actions">
                                            <button
                                                className="friend-request-action accept"
                                                disabled={respondFriendRequest.isPending}
                                                onClick={() => respondFriendRequest.mutate({ request_id: friendship.id, responder_id: user?.id ?? '', accept: true })}
                                            >
                                                <FiCheck size={12} /> Accept
                                            </button>
                                            <button
                                                className="friend-request-action decline"
                                                disabled={respondFriendRequest.isPending}
                                                onClick={() => respondFriendRequest.mutate({ request_id: friendship.id, responder_id: user?.id ?? '', accept: false })}
                                            >
                                                <FiX size={12} /> Decline
                                            </button>
                                        </div>
                                    </div>
                                </div>
                            ))}
                            {friendsLoading && (
                                <p className="section-label">Loading friends...</p>
                            )}
                            {friendsError && (
                                <p className="section-label">Could not load friends</p>
                            )}
                            {!friendsLoading && !friendsError && friends.length === 0 && (
                                <p className="section-label">No friends yet</p>
                            )}
                            {onlineFriends.map(f => (
                                <div key={f.id} className="dock-card" onClick={() => void toggleMiniChat(f.id, f.name, 'friend')}
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
                                        <div
                                            key={f.id}
                                            className="dock-card dock-offline"
                                            onClick={() => void toggleMiniChat(f.id, f.name, 'friend')}
                                            style={miniChat?.id === f.id ? { background: 'rgba(166,0,255,0.1)', borderColor: 'rgba(166,0,255,0.15)', opacity: 0.86 } : undefined}
                                        >
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

                </div>
            </aside>

            {miniChat && (
                <div className="mini-chat">
                    <div className="mini-chat-header">
                        <FiMessageSquare size={13} style={{ color: 'rgba(166,0,255,0.6)' }} />
                        <span className="mini-chat-title">{miniChat.name}</span>
                        {miniChat.type === 'friend' && (
                            <button className="mini-chat-open" onClick={openFullMessenger}>
                                <FiExternalLink size={12} /> Open
                            </button>
                        )}
                        <button className="mini-chat-close" onClick={() => setMiniChat(null)} aria-label="Close mini chat">
                            <FiChevronRight size={14} style={{ transform: 'rotate(45deg)' }} />
                        </button>
                    </div>
                    <div className="mini-chat-messages">
                        {miniChat.chatId ? (
                            miniMessagesLoading ? (
                                <p className="section-label">Loading messages...</p>
                            ) : miniApiMessages.length > 0 ? (
                                [...miniApiMessages].sort((a, b) => a.timestamp - b.timestamp).map(m => (
                                    <div key={m.id} style={{ display: 'flex', flexDirection: 'column', alignItems: m.creator_id === user?.id ? 'flex-end' : 'flex-start' }}>
                                        <div className={`mini-msg ${m.creator_id === user?.id ? 'mini-msg-own' : 'mini-msg-other'}`}>
                                            {m.body}
                                        </div>
                                        <span className="mini-msg-time" style={{ textAlign: m.creator_id === user?.id ? 'right' : 'left' }}>
                                            {new Date(m.timestamp * 1000).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })}
                                        </span>
                                    </div>
                                ))
                            ) : (
                                <p className="section-label">No messages yet</p>
                            )
                        ) : demoMiniMessages.map(m => (
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
                            onKeyDown={e => { if (e.key === 'Enter') void handleMiniSend() }}
                        />
                        <button className="mini-chat-send" onClick={() => void handleMiniSend()} disabled={sendMessage.isPending || getOrCreatePrivateChat.isPending}>
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
    if (location === '/' || location === '/login' || location === '/onboarding') return null


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
                        <RealtimeBridge />
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
