import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { FiGithub, FiMail, FiArrowLeft, FiSend } from 'react-icons/fi'
import { PageShell } from '../components/PageShell'
import { requireAuth } from '../lib/auth'

export const Route = createFileRoute('/about')({
  beforeLoad: async ({ context }) => {
    await requireAuth(context.queryClient)
  },
  component: AboutPage,
})

const T = {
  en: {
    eyebrow: 'About',
    title: 'AKIORA',
    subtitle: 'Intelligence for the Rift',
    desc: 'Next-gen analytics for League of Legends. Track your climb, master your champions, dissect the meta.',
    missionLabel: 'MISSION',
    mission: 'To give every player — Iron to Challenger — tools to understand their game deeply and climb confidently.',
    creatorLabel: 'CREATOR',
    creatorName: 'Orion',
    creatorBio: 'Fullstack dev & LoL enthusiast. Building Akiora as a love letter to the game.',
    contactLabel: 'CONTACT',
    github: 'GitHub',
    telegram: 'Telegram',
    email: 'Email',
    back: 'Back',
  },
  ru: {
    eyebrow: 'О проекте',
    title: 'AKIORA',
    subtitle: 'Интеллект для Ущелья',
    desc: 'Аналитика нового поколения для League of Legends. Отслеживай рост, осваивай чемпионов, разбирай мету.',
    missionLabel: 'МИССИЯ',
    mission: 'Дать каждому игроку — от Железа до Претендента — инструменты для осознанного клайма.',
    creatorLabel: 'СОЗДАТЕЛЬ',
    creatorName: 'Orion',
    creatorBio: 'Fullstack-разработчик и фанат LoL. Akiora — посвящение игре и её игрокам.',
    contactLabel: 'СВЯЗЬ',
    github: 'GitHub',
    telegram: 'Telegram',
    email: 'Почта',
    back: 'Назад',
  },
} as const

type Lang = keyof typeof T

function AboutPage() {
  const [lang, setLang] = useState<Lang>('en')
  const navigate = useNavigate()
  const t = T[lang]

  return (
    <>
      <style>{`
        @keyframes rise-up {
          from { opacity: 0; transform: translateY(14px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        @keyframes fade-in {
          from { opacity: 0; }
          to   { opacity: 1; }
        }

        .about-scene {
          position: relative; z-index: 10;
          min-height: 100vh;
          display: flex; align-items: center; justify-content: center;
        }

        /* ── Orbital layout ── */
        .orbit-wrap {
          position: relative;
          width: min(680px, 92vw);
          height: min(680px, 92vw);
          animation: fade-in 0.6s ease both;
        }

        /* Center circle — title */
        .orbit-core {
          position: absolute;
          top: 50%; left: 50%;
          translate: -50% -50%;
          width: 210px; height: 210px;
          border-radius: 50%;
          border: 1px solid rgba(166,0,255,0.28);
          box-shadow: 0 0 40px rgba(166,0,255,0.18), inset 0 0 40px rgba(166,0,255,0.06);
          background: rgba(0,0,0,0.7);
          backdrop-filter: blur(18px);
          display: flex; flex-direction: column;
          align-items: center; justify-content: center; gap: 4px;
          z-index: 4;
          animation: rise-up 0.5s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.1s;
        }
        .orbit-core-eyebrow {
          font-size: 9px; letter-spacing: 0.3em; text-transform: uppercase;
          color: rgba(166,0,255,0.9);
        }
        .orbit-core-title {
          font-family: 'Russo One', sans-serif;
          font-size: 28px; color: #fff; margin: 0;
          letter-spacing: 0.1em;
          text-shadow: 0 0 28px rgba(166,0,255,0.7), 0 0 60px rgba(166,0,255,0.3);
        }
        .orbit-core-subtitle {
          font-size: 10px; color: #06B6D4; letter-spacing: 0.18em;
          text-transform: uppercase;
          text-shadow: 0 0 14px #06B6D4cc;
        }

        /* Orbital ring */
        .orbit-ring {
          position: absolute; inset: 0;
          border-radius: 50%;
          border: 1px solid rgba(166,0,255,0.1);
          pointer-events: none;
        }
        .orbit-ring-inner {
          position: absolute;
          top: 50%; left: 50%;
          translate: -50% -50%;
          width: 75%; height: 75%;
          border-radius: 50%;
          border: 1px dashed rgba(6,182,212,0.12);
          pointer-events: none;
        }

        /* Satellite nodes */
        .sat {
          position: absolute;
          display: flex; flex-direction: column; align-items: center;
          gap: 8px;
          animation: rise-up 0.5s cubic-bezier(.16,1,.3,1) both;
        }
        /* positions: top, right, bottom-left, bottom-right */
        .sat--top    { top: 0; left: 50%; translate: -50% 0; align-items: center; animation-delay: 0.2s; }
        .sat--right  { top: 50%; right: 0; translate: 0 -50%; align-items: flex-start; animation-delay: 0.3s; }
        .sat--btl    { bottom: 4%; left: 5%; align-items: flex-end; animation-delay: 0.4s; }
        .sat--btr    { bottom: 4%; right: 5%; align-items: flex-start; animation-delay: 0.5s; }

        .sat-label {
          font-size: 9px; letter-spacing: 0.28em; text-transform: uppercase;
          color: rgba(166,0,255,0.85);
          text-shadow: 0 0 10px rgba(166,0,255,0.5);
        }
        .sat-bubble {
          background: rgba(0,0,0,0.78);
          border: 1px solid rgba(166,0,255,0.28);
          border-radius: 14px;
          padding: 14px 18px;
          backdrop-filter: blur(16px);
          max-width: 190px;
          box-shadow: 0 0 24px rgba(166,0,255,0.1);
        }
        .sat--right .sat-bubble { border-radius: 4px 14px 14px 14px; }
        .sat--btl   .sat-bubble { border-radius: 14px 14px 4px 14px; }
        .sat--btr   .sat-bubble { border-radius: 14px 14px 14px 4px; }

        .sat-text {
          font-size: 12px; color: rgba(255,255,255,0.75);
          line-height: 1.75; margin: 0; letter-spacing: 0.01em;
        }
        .sat-text strong {
          display: block; margin-bottom: 4px;
          font-family: 'Russo One', sans-serif;
          font-size: 14px; color: #fff; letter-spacing: 0.04em;
        }
        .sat-text em {
          font-style: italic;
          color: rgba(255,255,255,0.65);
        }

        /* Connector dots */
        .orbit-dot {
          position: absolute;
          width: 5px; height: 5px; border-radius: 50%;
          background: #a600ff;
          box-shadow: 0 0 8px #a600ff;
          pointer-events: none;
        }

        /* Contact row */
        .contact-row {
          display: flex; gap: 8px; flex-wrap: wrap; justify-content: center;
          margin-top: 6px;
        }
        .contact-link {
          display: flex; align-items: center; gap: 7px;
          padding: 8px 14px; border-radius: 8px;
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.14);
          color: rgba(255,255,255,0.7);
          font-family: 'Chakra Petch', monospace;
          font-size: 10px; letter-spacing: 0.1em;
          text-decoration: none;
          transition: color 180ms, border-color 180ms, box-shadow 180ms, transform 180ms;
        }
        .contact-link:hover { transform: translateY(-2px); color: #fff; }
        .contact-link.gh:hover  { border-color: rgba(255,255,255,0.3); box-shadow: 0 0 12px rgba(255,255,255,0.08); }
        .contact-link.tg:hover  { border-color: rgba(41,182,246,0.4);  box-shadow: 0 0 12px rgba(41,182,246,0.15); color: #29B6F6; }
        .contact-link.em:hover  { border-color: rgba(6,182,212,0.4);   box-shadow: 0 0 12px rgba(6,182,212,0.15);  color: #06B6D4; }

        /* Back btn */
        .about-back {
          position: fixed; bottom: 28px; left: 50%; translate: -50% 0;
          z-index: 20;
          display: flex; align-items: center; gap: 6px;
          background: none; border: none;
          color: rgba(255,255,255,0.2);
          font-family: 'Chakra Petch', monospace;
          font-size: 10px; letter-spacing: 0.14em; text-transform: uppercase;
          cursor: pointer; transition: color 180ms;
        }
        .about-back:hover { color: rgba(255,255,255,0.6); }
      `}</style>

      <PageShell lang={lang} onLangChange={setLang}>
        <div className="about-scene">
          <div className="orbit-wrap">
            {/* Rings */}
            <div className="orbit-ring" />
            <div className="orbit-ring-inner" />

            {/* Connector dots at cardinal points of inner ring */}
            {[
              { top: '12.5%', left: '50%', translate: '-50% -50%' },
              { top: '50%',   left: '87.5%', translate: '-50% -50%' },
              { top: '87.5%', left: '25%', translate: '-50% -50%' },
              { top: '87.5%', left: '75%', translate: '-50% -50%' },
            ].map((s, i) => (
              <div key={i} className="orbit-dot" style={s as React.CSSProperties} />
            ))}

            {/* Center core */}
            <div className="orbit-core">
              <span className="orbit-core-eyebrow">{t.eyebrow}</span>
              <h1 className="orbit-core-title">{t.title}</h1>
              <span className="orbit-core-subtitle">{t.subtitle}</span>
            </div>

            {/* Top — About */}
            <div className="sat sat--top">
              <div className="sat-bubble">
                <p className="sat-text">{t.desc}</p>
              </div>
              <div className="sat-label">{t.eyebrow}</div>
            </div>

            {/* Right — Mission */}
            <div className="sat sat--right">
              <div className="sat-label">{t.missionLabel}</div>
              <div className="sat-bubble">
                <p className="sat-text"><em>{t.mission}</em></p>
              </div>
            </div>

            {/* Bottom-left — Creator */}
            <div className="sat sat--btl">
              <div className="sat-bubble">
                <p className="sat-text">
                  <strong>{t.creatorName}</strong>
                  {t.creatorBio}
                </p>
              </div>
              <div className="sat-label">{t.creatorLabel}</div>
            </div>

            {/* Bottom-right — Contact */}
            <div className="sat sat--btr">
              <div className="sat-label">{t.contactLabel}</div>
              <div className="sat-bubble">
                <div className="contact-row">
                  <a href="https://github.com/orion" target="_blank" rel="noreferrer" className="contact-link gh">
                    <FiGithub size={12} />{t.github}
                  </a>
                  <a href="https://t.me/orion" target="_blank" rel="noreferrer" className="contact-link tg">
                    <FiSend size={12} />{t.telegram}
                  </a>
                  <a href="mailto:orion@akiora.gg" className="contact-link em">
                    <FiMail size={12} />{t.email}
                  </a>
                </div>
              </div>
            </div>
          </div>
        </div>

        <button className="about-back" onClick={() => navigate({ to: '/' })}>
          <FiArrowLeft size={12} />
          {t.back}
        </button>
      </PageShell>
    </>
  )
}
