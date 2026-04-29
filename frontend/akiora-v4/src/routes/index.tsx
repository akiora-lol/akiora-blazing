import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { PageShell } from '../components/PageShell'

export const Route = createFileRoute('/')({ component: Landing })

const T = {
  en: {
    eyebrow: 'League of Legends Intelligence',
    line1: 'RISE.',
    line2: 'DOMINATE.',
    line3: 'CONQUER.',
    subtitle: 'A next-gen analytics ecosystem for League of Legends. Track your climb, master your champions, and outplay the meta.',
    cta1: 'Get Started',
    cta2: 'Explore Features',
  },
  ru: {
    eyebrow: 'Аналитика League of Legends',
    line1: 'ВОССТАНЬ.',
    line2: 'ДОМИНИРУЙ.',
    line3: 'ЗАВОЮЙ.',
    subtitle: 'Аналитическая экосистема нового поколения для League of Legends. Отслеживай рост, осваивай чемпионов и обыгрывай мету.',
    cta1: 'Начать',
    cta2: 'Узнать больше',
  },
} as const

type Lang = keyof typeof T

function Landing() {
  const [lang, setLang] = useState<Lang>('en')
  const navigate = useNavigate()
  const t = T[lang]

  return (
    <>
      <style>{`
        @keyframes rise-up {
          from { opacity: 0; transform: translateY(18px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .hero-layout {
          position: relative; z-index: 10;
          min-height: 100vh;
          display: flex; align-items: center; justify-content: flex-end;
          padding-right: clamp(48px, 8vw, 120px);
        }
        .hero-text {
          display: flex; flex-direction: column; align-items: flex-start;
          gap: 20px; max-width: 500px; width: 100%;
        }
        .hero-eyebrow {
          font-size: 10px; letter-spacing: 0.32em; text-transform: uppercase;
          color: #a600ff; display: flex; align-items: center; gap: 10px;
          animation: rise-up 0.5s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.05s;
        }
        .hero-eyebrow::before {
          content: ''; display: block; height: 1px; width: 28px;
          background: linear-gradient(90deg, transparent, #a600ff88);
        }
        .hero-title {
          font-family: 'Russo One', sans-serif;
          font-size: clamp(2.6rem, 5.5vw, 5rem);
          line-height: 1.04; color: #fff; margin: 0; text-align: left;
          animation: rise-up 0.5s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.12s;
        }
        .neon-cyan {
          color: #06B6D4;
          text-shadow: 0 0 18px #06B6D4cc, 0 0 45px #06B6D466, 0 0 80px #06B6D422;
        }
        .neon-red {
          color: #FF002A;
          text-shadow: 0 0 18px #FF002Acc, 0 0 45px #FF002A66, 0 0 80px #FF002A22;
        }
        .hero-subtitle {
          font-size: 13px; color: rgba(255,255,255,0.36);
          max-width: 400px; line-height: 1.85; margin: 0;
          animation: rise-up 0.5s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.22s; letter-spacing: 0.02em;
        }
        .cta-row {
          display: flex; gap: 12px; flex-wrap: wrap;
          animation: rise-up 0.5s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.32s;
        }
        .btn-primary {
          font-family: 'Chakra Petch', monospace; font-weight: 600;
          font-size: 12px; letter-spacing: 0.18em; text-transform: uppercase;
          padding: 14px 34px; border-radius: 8px;
          background: linear-gradient(135deg, #a600ff, #7000cc);
          color: #fff; border: 1px solid rgba(166,0,255,0.7); cursor: pointer;
          box-shadow: 0 0 28px rgba(166,0,255,0.45), 0 0 60px rgba(166,0,255,0.15), inset 0 1px 0 rgba(255,255,255,0.12);
          transition: box-shadow 200ms, transform 200ms;
        }
        .btn-primary:hover {
          box-shadow: 0 0 44px rgba(166,0,255,0.65), 0 0 90px rgba(166,0,255,0.25), inset 0 1px 0 rgba(255,255,255,0.15);
          transform: translateY(-2px);
        }
        .btn-secondary {
          font-family: 'Chakra Petch', monospace; font-weight: 500;
          font-size: 12px; letter-spacing: 0.15em; text-transform: uppercase;
          padding: 13px 30px; border-radius: 8px;
          background: transparent; color: rgba(255,255,255,0.45);
          border: 1px solid rgba(6,182,212,0.28); cursor: pointer;
          transition: color 200ms, border-color 200ms, box-shadow 200ms, transform 200ms;
        }
        .btn-secondary:hover {
          color: #06B6D4; border-color: rgba(6,182,212,0.65);
          box-shadow: 0 0 22px rgba(6,182,212,0.25);
          transform: translateY(-2px);
        }
      `}</style>

      <PageShell logoVariant="hero" lang={lang} onLangChange={setLang}>
        <div className="hero-layout">
          <div className="hero-text">
            <p className="hero-eyebrow">{t.eyebrow}</p>
            <h1 className="hero-title">
              {t.line1}<br />
              <span className="neon-cyan">{t.line2}</span><br />
              <span className="neon-red">{t.line3}</span>
            </h1>
            <p className="hero-subtitle">{t.subtitle}</p>
            <div className="cta-row">
              <button className="btn-primary" onClick={() => navigate({ to: '/login' })}>{t.cta1}</button>
              <button className="btn-secondary" onClick={() => navigate({ to: '/about' })}>{t.cta2}</button>
            </div>
          </div>
        </div>
      </PageShell>
    </>
  )
}
