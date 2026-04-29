import {
  HeadContent,
  Scripts,
  createRootRouteWithContext,
  useRouterState,
} from '@tanstack/react-router'

import TanStackQueryDevtools from '../integrations/tanstack-query/devtools'

import { getLocale } from '#/paraglide/runtime'

import appCss from '../styles.css?url'

import type { QueryClient } from '@tanstack/react-query'

import { useState, useRef, useCallback } from 'react'
import {
  FiHome, FiBarChart2, FiUsers, FiSettings, FiInfo, FiList,
} from 'react-icons/fi'
import { GiCrossedSwords } from 'react-icons/gi'
import { Link } from '@tanstack/react-router'

interface MyRouterContext {
  queryClient: QueryClient
}

const NAV_ITEMS = [
  { icon: FiHome,          label: 'Home',      to: '/' },
  { icon: FiBarChart2,     label: 'Stats',     to: '/stats' },
  { icon: GiCrossedSwords, label: 'Champions', to: '/champions' },
  { icon: FiList,          label: 'Tierlist',  to: '/tierlist' },
  { icon: FiUsers,         label: 'Community', to: '/community' },
  { icon: FiInfo,          label: 'About',     to: '/about' },
  { icon: FiSettings,      label: 'Settings',  to: '/settings' },
]

const HIDDEN_ROUTES = new Set(['/', '/login'])

// Magnification config
const BASE_SIZE = 16   // icon px at rest
const MAX_SIZE  = 24   // icon px at peak
const RADIUS    = 1.8  // how many neighbours are affected (in item-widths)

function TopDock() {
  const location = useRouterState({ select: s => s.location.pathname })
  const [mouseIdx, setMouseIdx] = useState<number | null>(null)
  const navRef = useRef<HTMLElement>(null)

  const getScale = useCallback((i: number): number => {
    if (mouseIdx === null) return 1
    const dist = Math.abs(i - mouseIdx)
    if (dist > RADIUS) return 1
    // cosine falloff: 1 → MAX_SIZE/BASE_SIZE at dist=0
    const t = 1 - dist / RADIUS
    const maxScale = MAX_SIZE / BASE_SIZE
    return 1 + (maxScale - 1) * Math.cos((1 - t) * Math.PI * 0.5)
  }, [mouseIdx])

  if (HIDDEN_ROUTES.has(location)) return null

  return (
    <>
      <style>{`
        .top-dock {
          position: fixed;
          top: 12px;
          left: 50%;
          translate: -50% 0;
          z-index: 100;
          display: flex;
          align-items: flex-end;
          gap: 0;
          width: 75vw;
          padding: 6px 32px 8px;
          border-radius: 16px;
          background: rgba(0,0,0,0.82);
          border: 1px solid rgba(255,255,255,0.1);
          box-shadow: 0 0 40px rgba(166,0,255,0.14), inset 0 1px 0 rgba(255,255,255,0.06);
          backdrop-filter: blur(20px);
        }
        .dock-divider {
          width: 1px;
          height: 22px;
          background: rgba(255,255,255,0.08);
          margin: 0 6px;
          flex-shrink: 0;
          align-self: center;
        }
        .dock-item {
          display: flex;
          flex-direction: column;
          align-items: center;
          gap: 3px;
          flex: 1;
          padding: 2px 8px;
          text-decoration: none;
          color: rgba(255,255,255,0.5);
          transform-origin: bottom center;
          transition:
            transform 160ms cubic-bezier(.34,1.56,.64,1),
            color 150ms,
            filter 150ms;
          font-family: 'Chakra Petch', monospace;
          white-space: nowrap;
        }
        .dock-item:hover,
        .dock-item.active {
          color: #fff;
        }
        .dock-item:hover svg {
          filter: drop-shadow(0 0 7px rgba(255,255,255,0.9)) drop-shadow(0 0 18px rgba(255,255,255,0.5));
        }
        .dock-item.active svg {
          filter: drop-shadow(0 0 9px rgba(255,255,255,1)) drop-shadow(0 0 24px rgba(255,255,255,0.7));
        }
        .dock-item-icon {
          display: flex;
          align-items: center;
          justify-content: center;
          transition: transform 160ms cubic-bezier(.34,1.56,.64,1);
        }
        .dock-label {
          font-size: 8px;
          letter-spacing: 0.1em;
          text-transform: uppercase;
          opacity: 0.55;
          line-height: 1;
          transition: opacity 150ms, font-size 160ms cubic-bezier(.34,1.56,.64,1);
        }
        .dock-item:hover .dock-label,
        .dock-item.active .dock-label {
          opacity: 1;
        }
      `}</style>

      <nav
        ref={navRef}
        className="top-dock"
        aria-label="Main navigation"
        onMouseLeave={() => setMouseIdx(null)}
      >
        {NAV_ITEMS.map((item, i) => {
          const scale = getScale(i)
          const iconSize = Math.round(BASE_SIZE * scale)
          const labelSize = Math.max(7, Math.round(8 * scale * 0.7))
          return (
            <span key={item.to} style={{ display: 'contents' }}>
              {i === 6 && <div className="dock-divider" />}
              <Link
                to={item.to}
                className="dock-item"
                activeProps={{ className: 'dock-item active' }}
                aria-label={item.label}
                onMouseEnter={() => setMouseIdx(i)}
                style={{ transform: `scale(${scale})`, transformOrigin: 'bottom center' }}
              >
                <div className="dock-item-icon">
                  <item.icon size={iconSize} />
                </div>
                <span className="dock-label" style={{ fontSize: `${labelSize}px` }}>
                  {item.label}
                </span>
              </Link>
            </span>
          )
        })}
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

function RootDocument({ children }: { children: React.ReactNode }) {
  return (
    <html lang={getLocale()}>
      <head>
        <HeadContent />
      </head>
      <body>
        <TopDock />
        {children}
        <Scripts />
      </body>
    </html>
  )
}

