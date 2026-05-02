import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { SiDiscord, SiYandexcloud } from 'react-icons/si'
import { MdEmail } from 'react-icons/md'
import { FiArrowLeft, FiArrowRight } from 'react-icons/fi'
import { PageShell } from '../components/PageShell'
import { getOAuthUrl, useLoginEmailStartMutation, useLoginEmailFinishMutation } from '../lib/api'
import { useRequireGuest } from '../contexts/AuthContext'

export const Route = createFileRoute('/login')({ component: LoginPage })

const T = {
    en: {
        authTitle: 'Sign In',
        authSubtitle: 'Choose your preferred method',
        email: 'Continue with Email',
        discord: 'Continue with Discord',
        yandex: 'Continue with Yandex',
        back: 'Back',
        emailPlaceholder: 'your@email.com',
        sendCode: 'Send Code',
        codePlaceholder: '6-digit code',
        verify: 'Verify',
        codeSent: 'Check your inbox for the code',
        error: 'Something went wrong. Try again.',
    },
    ru: {
        authTitle: 'Войти',
        authSubtitle: 'Выберите способ входа',
        email: 'Войти через Email',
        discord: 'Войти через Discord',
        yandex: 'Войти через Яндекс',
        back: 'Назад',
        emailPlaceholder: 'ваш@email.com',
        sendCode: 'Отправить код',
        codePlaceholder: '6-значный код',
        verify: 'Подтвердить',
        codeSent: 'Проверьте почту — код отправлен',
        error: 'Что-то пошло не так. Попробуйте снова.',
    },
} as const

type Lang = keyof typeof T
type Step = 'providers' | 'email-input' | 'code-input'

const OAUTH_PROVIDERS = [
    { key: 'discord' as const, Icon: SiDiscord, accent: '#5865F2', border: 'rgba(88,101,242,0.3)', glow: 'rgba(88,101,242,0.2)' },
    { key: 'yandex' as const, Icon: SiYandexcloud, accent: '#FC3F1D', border: 'rgba(252,63,29,0.3)', glow: 'rgba(252,63,29,0.2)' },
]

function LoginPage() {
    const { isLoading } = useRequireGuest() // Redirect if already authenticated
    const [lang, setLang] = useState<Lang>('en')
    const [step, setStep] = useState<Step>('providers')
    const [emailValue, setEmailValue] = useState('')
    const [codeValue, setCodeValue] = useState('')
    const navigate = useNavigate()
    const t = T[lang]

    const startMutation = useLoginEmailStartMutation()
    const finishMutation = useLoginEmailFinishMutation()

    const error = startMutation.error?.message || finishMutation.error?.message || ''
    const loading = startMutation.isPending || finishMutation.isPending

    // Show loading screen while checking auth status
    if (isLoading) {
        return (
            <PageShell lang={lang} onLangChange={setLang}>
                <div style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    height: '100vh',
                    color: '#fff'
                }}>
                    Loading...
                </div>
            </PageShell>
        )
    }

    const handleOAuth = (provider: 'discord' | 'yandex') => {
        window.location.href = getOAuthUrl(provider)
    }

    const handleEmailSubmit = async () => {
        startMutation.reset()
        try {
            await startMutation.mutateAsync(emailValue)
            setStep('code-input')
        } catch {
            // error shown via startMutation.error
        }
    }

    const handleCodeSubmit = async () => {
        finishMutation.reset()
        try {
            await finishMutation.mutateAsync(codeValue)
            const onboarded = localStorage.getItem('akiora_onboarded')
            navigate({ to: onboarded ? '/about' : '/onboarding' })
        } catch {
            // error shown via finishMutation.error
        }
    }

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
        .auth-provider-btn:disabled {
          opacity: 0.5; cursor: not-allowed; transform: none;
        }
        .auth-divider { height: 1px; background: rgba(255,255,255,0.06); margin: 4px 0; }
        .auth-input {
          width: 100%; padding: 13px 18px; border-radius: 10px;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.12);
          color: #fff;
          font-family: 'Chakra Petch', monospace;
          font-size: 13px; letter-spacing: 0.04em;
          outline: none;
          transition: border-color 180ms;
        }
        .auth-input:focus {
          border-color: rgba(166,0,255,0.5);
        }
        .auth-input::placeholder { color: rgba(255,255,255,0.2); }
        .auth-submit {
          display: flex; align-items: center; justify-content: center; gap: 8px;
          width: 100%; padding: 13px 18px; border-radius: 10px;
          background: linear-gradient(135deg, #a600ff, #7000cc);
          border: 1px solid rgba(166,0,255,0.7);
          color: #fff;
          font-family: 'Chakra Petch', monospace;
          font-size: 12px; letter-spacing: 0.12em;
          cursor: pointer;
          transition: box-shadow 180ms, transform 180ms;
        }
        .auth-submit:hover {
          box-shadow: 0 0 28px rgba(166,0,255,0.45);
          transform: translateY(-1px);
        }
        .auth-submit:disabled { opacity: 0.5; cursor: not-allowed; transform: none; }
        .auth-hint {
          font-size: 10px; color: rgba(6,182,212,0.8); text-align: center;
          letter-spacing: 0.08em;
        }
        .auth-error {
          font-size: 10px; color: #ff4466; text-align: center;
          letter-spacing: 0.08em;
        }
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

                        {step === 'providers' && (
                            <>
                                <button
                                    className="auth-provider-btn"
                                    style={{ '--p-border': 'rgba(6,182,212,0.3)', '--p-accent-border': '#06B6D466', '--p-glow': 'rgba(6,182,212,0.2)' } as React.CSSProperties}
                                    onClick={() => setStep('email-input')}
                                >
                                    <MdEmail size={18} style={{ flexShrink: 0, color: '#06B6D4' }} />
                                    {t.email}
                                </button>
                                <div className="auth-divider" />
                                {OAUTH_PROVIDERS.map((p) => (
                                    <button
                                        key={p.key}
                                        className="auth-provider-btn"
                                        style={{ '--p-border': p.border, '--p-accent-border': p.accent + '66', '--p-glow': p.glow } as React.CSSProperties}
                                        onClick={() => handleOAuth(p.key)}
                                    >
                                        <p.Icon size={18} style={{ flexShrink: 0, color: p.accent }} />
                                        {t[p.key]}
                                    </button>
                                ))}
                            </>
                        )}

                        {step === 'email-input' && (
                            <>
                                <input
                                    type="email"
                                    className="auth-input"
                                    placeholder={t.emailPlaceholder}
                                    value={emailValue}
                                    onChange={(e) => setEmailValue(e.target.value)}
                                    autoFocus
                                    onKeyDown={(e) => e.key === 'Enter' && emailValue && handleEmailSubmit()}
                                />
                                <button
                                    className="auth-submit"
                                    disabled={!emailValue || loading}
                                    onClick={handleEmailSubmit}
                                >
                                    {t.sendCode} <FiArrowRight size={14} />
                                </button>
                            </>
                        )}

                        {step === 'code-input' && (
                            <>
                                <p className="auth-hint">{t.codeSent}</p>
                                <input
                                    type="text"
                                    className="auth-input"
                                    placeholder={t.codePlaceholder}
                                    value={codeValue}
                                    onChange={(e) => setCodeValue(e.target.value.slice(0, 6))}
                                    autoFocus
                                    onKeyDown={(e) => e.key === 'Enter' && codeValue.length === 6 && handleCodeSubmit()}
                                />
                                <button
                                    className="auth-submit"
                                    disabled={codeValue.length !== 6 || loading}
                                    onClick={handleCodeSubmit}
                                >
                                    {t.verify} <FiArrowRight size={14} />
                                </button>
                            </>
                        )}

                        {error && <p className="auth-error">{error}</p>}

                        <button
                            className="auth-back"
                            onClick={() => {
                                if (step === 'providers') navigate({ to: '/' })
                                else { setStep('providers'); }
                            }}
                        >
                            <FiArrowLeft size={12} />
                            {t.back}
                        </button>
                    </div>
                </div>
            </PageShell>
        </>
    )
}
