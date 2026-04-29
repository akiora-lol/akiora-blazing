import type { ReactNode } from 'react'

export function AkioraBackground() {
  return (
    <>
      <style>{`
        @keyframes spin-slow {
          from { transform: rotate(0deg); }
          to   { transform: rotate(360deg); }
        }
        @keyframes logo-breathe {
          0%, 100% { filter: drop-shadow(0 0 60px #a600ffcc) drop-shadow(0 0 140px #a600ff66); }
          50%       { filter: drop-shadow(0 0 100px #a600ffff) drop-shadow(0 0 200px #a600ff88); }
        }

        html, body { background: #000 !important; margin: 0; }

        .ak-page {
          background: #000;
          min-height: 100vh;
          position: relative;
          overflow: hidden;
          font-family: 'Chakra Petch', monospace;
        }
        .ak-bg-logo {
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
        /* Variants */
        .ak-bg-logo--hero {
          top: 50%; left: 22%;
          translate: -50% -50%;
          width: min(52vw, 52vh);
          height: min(52vw, 52vh);
          opacity: 1;
        }
        .ak-bg-logo--center {
          top: 50%; left: 50%;
          translate: -50% -50%;
          width: min(82vw, 82vh);
          height: min(82vw, 82vh);
          opacity: 0.18;
        }
        .ak-bg-logo--large {
          top: 50%; left: 50%;
          translate: -50% -50%;
          width: min(88vw, 88vh);
          height: min(88vw, 88vh);
          opacity: 0.13;
        }
        .ak-scanlines {
          position: fixed; inset: 0; z-index: 1; pointer-events: none;
          background: repeating-linear-gradient(
            to bottom, transparent, transparent 3px,
            rgba(0,0,0,0.2) 3px, rgba(0,0,0,0.2) 4px
          );
        }
        .ak-vignette {
          position: fixed; inset: 0; z-index: 1; pointer-events: none;
          background: radial-gradient(ellipse at center, transparent 25%, rgba(0,0,0,0.85) 100%);
        }
        .ak-lang {
          position: fixed; top: 22px; right: 28px; z-index: 60;
          display: flex; gap: 2px;
          background: rgba(0,0,0,0.75);
          border: 1px solid rgba(166,0,255,0.25);
          border-radius: 8px; padding: 3px;
          backdrop-filter: blur(12px);
        }
        .ak-lang-btn {
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; font-weight: 600; letter-spacing: 0.12em;
          padding: 5px 12px; border-radius: 5px; border: none;
          cursor: pointer; transition: all 180ms ease;
          background: transparent; color: rgba(255,255,255,0.35);
        }
        .ak-lang-btn.active {
          background: rgba(166,0,255,0.2); color: #a600ff;
          box-shadow: 0 0 12px rgba(166,0,255,0.3);
        }
        .ak-lang-btn:not(.active):hover { color: rgba(255,255,255,0.7); }
      `}</style>
      <div className="ak-vignette" aria-hidden="true" />
      <div className="ak-scanlines" aria-hidden="true" />
    </>
  )
}

interface PageShellProps {
  children: ReactNode
  logoVariant?: 'hero' | 'center' | 'large'
  lang: 'en' | 'ru'
  onLangChange: (l: 'en' | 'ru') => void
}

export function PageShell({ children, logoVariant = 'center', lang, onLangChange }: PageShellProps) {
  return (
    <div className="ak-page">
      <img
        src="/violet-yang.svg"
        alt=""
        className={`ak-bg-logo ak-bg-logo--${logoVariant}`}
        aria-hidden="true"
      />
      <AkioraBackground />

      <div className="ak-lang" role="group" aria-label="Language">
        <button className={`ak-lang-btn${lang === 'en' ? ' active' : ''}`} onClick={() => onLangChange('en')} aria-pressed={lang === 'en'}>EN</button>
        <button className={`ak-lang-btn${lang === 'ru' ? ' active' : ''}`} onClick={() => onLangChange('ru')} aria-pressed={lang === 'ru'}>RU</button>
      </div>

      {children}
    </div>
  )
}
