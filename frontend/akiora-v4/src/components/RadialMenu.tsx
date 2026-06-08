import { useState } from 'react'
import { useNavigate } from '@tanstack/react-router'
import {
  FiHome, FiBarChart2, FiUsers, FiSettings, FiInfo, FiList,
} from 'react-icons/fi'
import { GiCrossedSwords } from 'react-icons/gi'

interface RadialItem {
  icon: React.ElementType
  label: string
  to: string
  accent?: string
}

const ITEMS: RadialItem[] = [
  { icon: FiHome,         label: 'Home',      to: '/',          accent: '#a600ff' },
  { icon: FiBarChart2,    label: 'Stats',     to: '/stats',     accent: '#06B6D4' },
  { icon: GiCrossedSwords,label: 'Champions', to: '/champions', accent: '#FF002A' },
  { icon: FiList,         label: 'Tierlist',  to: '/tierlist',  accent: '#06B6D4' },
  { icon: FiUsers,        label: 'Community', to: '/community', accent: '#a600ff' },
  { icon: FiInfo,         label: 'About',     to: '/about',     accent: '#06B6D4' },
  { icon: FiSettings,     label: 'Settings',  to: '/settings',  accent: '#FF002A' },
]

interface RadialMenuProps {
  items?: RadialItem[]
  radius?: number
}

export function RadialMenu({ items = ITEMS, radius = 120 }: RadialMenuProps) {
  const [open, setOpen] = useState(false)
  const navigate = useNavigate()

  const count = items.length
  // Distribute items evenly across full 360°, starting from top (-90°)
  const getPos = (i: number) => {
    const angleDeg = -90 + (360 / count) * i
    const angleRad = (angleDeg * Math.PI) / 180
    return {
      x: Math.cos(angleRad) * radius,
      y: Math.sin(angleRad) * radius,
    }
  }

  return (
    <>
      <style>{`
        .rm-wrap {
          position: relative;
          width: 88px;
          height: 88px;
          cursor: pointer;
          flex-shrink: 0;
        }

        /* Static bright center logo */
        .rm-center {
          position: absolute;
          inset: 0;
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          z-index: 5;
          transition: transform 300ms cubic-bezier(.34,1.56,.64,1);
        }
        .rm-wrap:hover .rm-center {
          transform: scale(1.08);
        }
        .rm-logo {
          width: 72px; height: 72px;
          filter:
            drop-shadow(0 0 14px #a600ffff)
            drop-shadow(0 0 36px #a600ffcc)
            drop-shadow(0 0 70px #a600ff88);
        }

        /* Pulse ring */
        .rm-ring {
          position: absolute;
          inset: -8px;
          border-radius: 50%;
          border: 1px solid rgba(166,0,255,0.0);
          transition: border-color 250ms, box-shadow 250ms;
          pointer-events: none;
        }
        .rm-wrap:hover .rm-ring {
          border-color: rgba(166,0,255,0.25);
          box-shadow: 0 0 24px rgba(166,0,255,0.2);
        }

        /* Item nodes */
        .rm-item {
          position: absolute;
          top: 50%; left: 50%;
          width: 44px; height: 44px;
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          background: rgba(0,0,0,0.82);
          border: 1px solid var(--item-border);
          color: rgba(255,255,255,0.5);
          cursor: pointer;
          z-index: 4;
          /* collapsed: center, invisible */
          translate: -50% -50%;
          transform: scale(0.4);
          opacity: 0;
          pointer-events: none;
          transition:
            transform 350ms cubic-bezier(.34,1.56,.64,1),
            opacity 250ms ease,
            color 180ms,
            border-color 180ms,
            box-shadow 180ms;
          backdrop-filter: blur(10px);
        }
        .rm-item.open {
          transform: translate(var(--ix), var(--iy)) scale(1);
          opacity: 1;
          pointer-events: auto;
        }
        .rm-item:hover {
          color: var(--item-accent);
          border-color: var(--item-accent);
          box-shadow: 0 0 18px var(--item-glow);
          transform: translate(var(--ix), var(--iy)) scale(1.15) !important;
        }

        /* Tooltip */
        .rm-tooltip {
          position: absolute;
          bottom: calc(100% + 7px);
          left: 50%; translate: -50% 0;
          white-space: nowrap;
          background: rgba(0,0,0,0.88);
          border: 1px solid rgba(166,0,255,0.25);
          color: #fff;
          font-family: 'Chakra Petch', monospace;
          font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase;
          padding: 3px 9px; border-radius: 5px;
          pointer-events: none;
          opacity: 0;
          transition: opacity 150ms;
        }
        .rm-item:hover .rm-tooltip { opacity: 1; }

        /* Connector lines */
        .rm-svg {
          position: absolute;
          top: 50%; left: 50%;
          translate: -50% -50%;
          pointer-events: none;
          z-index: 3;
          overflow: visible;
        }
        .rm-line {
          stroke: rgba(166,0,255,0.18);
          stroke-width: 1;
          stroke-dasharray: 4 4;
          fill: none;
          opacity: 0;
          transition: opacity 250ms ease;
        }
        .rm-line.open { opacity: 1; }
      `}</style>

      <div
        className="rm-wrap"
        onMouseEnter={() => setOpen(true)}
        onMouseLeave={() => setOpen(false)}
        role="navigation"
        aria-label="Radial menu"
      >
        {/* Connector lines SVG */}
        <svg className="rm-svg" width={0} height={0}>
          {items.map((_, i) => {
            const { x, y } = getPos(i)
            return (
              <line
                key={i}
                className={`rm-line${open ? ' open' : ''}`}
                x1={0} y1={0}
                x2={x} y2={y}
                style={{ transitionDelay: `${i * 30}ms` }}
              />
            )
          })}
        </svg>

        {/* Items */}
        {items.map((item, i) => {
          const { x, y } = getPos(i)
          const accent = item.accent ?? '#a600ff'
          const glow = accent + '55'
          return (
            <button
              key={item.to}
              className={`rm-item${open ? ' open' : ''}`}
              style={{
                '--item-border': accent + '44',
                '--item-accent': accent,
                '--item-glow': glow,
                '--ix': `${x}px`,
                '--iy': `${y}px`,
                transitionDelay: open ? `${i * 35}ms` : `${(count - i) * 20}ms`,
              } as React.CSSProperties}
              onClick={() => navigate({ to: item.to as never })}
              aria-label={item.label}
            >
              <item.icon size={16} />
              <span className="rm-tooltip">{item.label}</span>
            </button>
          )
        })}

        {/* Center */}
        <div className="rm-center">
          <div className="rm-ring" />
          <img src="/violet-yang.svg" alt="Akiora" className="rm-logo" />
        </div>
      </div>
    </>
  )
}
