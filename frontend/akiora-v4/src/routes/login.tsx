import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { SiDiscord, SiYandexcloud, SiGoogle } from 'react-icons/si'
import { MdEmail } from 'react-icons/md'
import { FiArrowLeft } from 'react-icons/fi'
import { PageShell } from '../components/PageShell'

export const Route = createFileRoute('/login')({ component: LoginPage })

const T = {
  en: {
    authTitle: 'Sign In',
    authSubtitle: 'Choose your preferred method',
    email: 'Continue with Email',
    discord: 'Continue with Discord',
    yandex: 'Continue with Yandex',
    google: 'Continue with Google',
    back: 'Back',
  },
  ru: {
    authTitle: 'Войти',
    authSubtitle: 'Выберите способ входа',
    email: 'Войти через Email',
    discord: 'Войти через Discord',
    yandex: 'Войти через Яндекс',
    google: 'Войти через Google',
    back: 'Назад',
  },
} as const

type Lang = keyof typeof T

const PROVIDERS = [
  { key: 'email' as const,   Icon: MdEmail,        accent: '#06B6D4', border: 'rgba(6,182,212,0.3)',  glow: 'rgba(6,182,212,0.2)' },
  { key: 'discord' as const, Icon: SiDiscord,      accent: '#5865F2', border: 'rgba(88,101,242,0.3)', glow: 'rgba(88,101,242,0.2)' },
  { key: 'yandex' as const,  Icon: SiYandexcloud,  accent: '#FC3F1D', border: 'rgba(252,63,29,0.3)',  glow: 'rgba(252,63,29,0.2)' },
  { key: 'google' as const,  Icon: SiGoogle,       accent: '#4285F4', border: 'rgba(66,133,244,0.3)', glow: 'rgba(66,133,244,0.2)' },
]

function LoginPage() {
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
        .login-center {
          position: relative; z-index: 10;
          min-height: 100vh;
          display: flex; align-items: center; justify-content: center;
        }
        .auth-card {
          background: rgba(0,0,0,0.82);
          border: 1px solid rgba(166,0,255,0.22);
          border-radius: 18px;
          padding: 44px 40px;
          width: min(400px, calc(100vw - 48px));
          backdrop-filter: blur(24px);
          box-shadow: 0 0 60px rgba(166,0,255,0.12), 0 0 120px rgba(166,0,255,0.06);
          display: flex; flex-direction: column; gap: 10px;
          animation: rise-up 0.5s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.1s;
        }
        .auth-logo {
          width: 36px; height: 36px;
          margin: 0 auto 6px;
          filter: drop-shadow(0 0 12px #a600ffaa);
        }
        .auth-title {
          font-family: 'Russo One', sans-serif;
          font-size: 22px; color: #fff;
          text-align: center; margin: 0 0 2px; letter-spacing: 0.04em;
        }
        .auth-subtitle {
          font-size: 11px; color: rgba(255,255,255,0.3);
          text-align: center; letter-spacing: 0.1em; margin: 0 0 16px;
        }
        .auth-provider-btn {
          display: flex; align-items: center; gap: 12px;
          width: 100%; padding: 13px 18px; border-radius: 10px;
          background: rgba(255,255,255,0.03);
          border: 1px solid var(--p-border);
          color: rgba(255,255,255,0.75);
          font-family: 'Chakra Petch', monospace;
          font-size: 12px; letter-spacing: 0.1em;
          cursor: pointer; text-align: left;
          transition: background 180ms, border-color 180ms, box-shadow 180ms, color 180ms, transform 180ms;
        }
        .auth-provider-btn:hover {
          background: rgba(255,255,255,0.06);
          border-color: var(--p-accent-border);
          box-shadow: 0 0 18px var(--p-glow);
          color: #fff; transform: translateX(3px);
        }
        .auth-divider { height: 1px; background: rgba(255,255,255,0.06); margin: 4px 0; }
        .auth-back {
          display: flex; align-items: center; gap: 6px;
          background: none; border: none;
          color: rgba(255,255,255,0.25);
          font-family: 'Chakra Petch', monospace;
          font-size: 10px; letter-spacing: 0.12em; text-transform: uppercase;
          cursor: pointer; padding: 6px 0 0; margin-top: 4px;
          transition: color 180ms;
        }
        .auth-back:hover { color: rgba(255,255,255,0.6); }
      `}</style>

      <PageShell logoVariant="center" lang={lang} onLangChange={setLang}>
        <div className="login-center">
          <div className="auth-card">
            <img src="/violet-yang.svg" alt="Akiora" className="auth-logo" />
            <h2 className="auth-title">{t.authTitle}</h2>
            <p className="auth-subtitle">{t.authSubtitle}</p>

            {PROVIDERS.map((p, i) => (
              <div key={p.key}>
                {i === 1 && <div className="auth-divider" />}
                <button
                  className="auth-provider-btn"
                  style={{ '--p-border': p.border, '--p-accent-border': p.accent + '66', '--p-glow': p.glow } as React.CSSProperties}
                >
                  <p.Icon size={18} style={{ flexShrink: 0, color: p.accent }} />
                  {t[p.key]}
                </button>
              </div>
            ))}

            <button className="auth-back" onClick={() => navigate({ to: '/' })}>
              <FiArrowLeft size={12} />
              {t.back}
            </button>
          </div>
        </div>
      </PageShell>
    </>
  )
}
