import { useState, type ReactNode } from 'react'
import { Link } from '@tanstack/react-router'
import { FiHome, FiRefreshCw } from 'react-icons/fi'

interface ErrorPageProps {
    code: string
    title: string
    subtitle: string
    description: string
    primaryAction?: {
        label: string
        to?: string
        onClick?: () => void
        icon?: React.ReactNode
    }
    secondaryAction?: {
        label: string
        onClick: () => void
        icon?: React.ReactNode
    }
}

function GlitchText({ text }: { text: string }) {
    return (
        <span className="glitch-text" data-text={text}>
            {text}
            <style>{`
                .glitch-text {
                    position: relative;
                    display: inline-block;
                    color: #fff;
                    font-family: 'Russo One', sans-serif;
                    letter-spacing: 0.08em;
                }
                .glitch-text::before,
                .glitch-text::after {
                    content: attr(data-text);
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: #000;
                }
                .glitch-text::before {
                    left: 2px;
                    text-shadow: -1px 0 #ff002a;
                    clip: rect(24px, 550px, 90px, 0);
                    animation: glitch-anim-1 2.5s infinite linear alternate-reverse;
                }
                .glitch-text::after {
                    left: -2px;
                    text-shadow: -1px 0 #06b6d4;
                    clip: rect(85px, 550px, 140px, 0);
                    animation: glitch-anim-2 3s infinite linear alternate-reverse;
                }
                @keyframes glitch-anim-1 {
                    0%   { clip: rect(20px, 9999px, 15px, 0); }
                    20%  { clip: rect(60px, 9999px, 70px, 0); }
                    40%  { clip: rect(10px, 9999px, 55px, 0); }
                    60%  { clip: rect(80px, 9999px, 5px, 0); }
                    80%  { clip: rect(40px, 9999px, 90px, 0); }
                    100% { clip: rect(30px, 9999px, 50px, 0); }
                }
                @keyframes glitch-anim-2 {
                    0%   { clip: rect(65px, 9999px, 100px, 0); }
                    20%  { clip: rect(15px, 9999px, 60px, 0); }
                    40%  { clip: rect(90px, 9999px, 30px, 0); }
                    60%  { clip: rect(5px, 9999px, 80px, 0); }
                    80%  { clip: rect(55px, 9999px, 10px, 0); }
                    100% { clip: rect(35px, 9999px, 75px, 0); }
                }
            `}</style>
        </span>
    )
}

function ErrorPageShell({
    code,
    title,
    subtitle,
    description,
    primaryAction,
    secondaryAction,
}: ErrorPageProps) {
    return (
        <>
            <style>{`
                @keyframes rise-up {
                    from { opacity: 0; transform: translateY(18px); }
                    to   { opacity: 1; transform: translateY(0); }
                }
                @keyframes flicker {
                    0%, 19%, 21%, 23%, 25%, 54%, 56%, 100% {
                        opacity: 1;
                        text-shadow: 0 0 8px currentColor, 0 0 20px currentColor;
                    }
                    20%, 24%, 55% {
                        opacity: 0.4;
                        text-shadow: none;
                    }
                }
                @keyframes pulse-glow {
                    0%, 100% { box-shadow: 0 0 30px rgba(166,0,255,0.3), 0 0 80px rgba(166,0,255,0.1); }
                    50%       { box-shadow: 0 0 50px rgba(166,0,255,0.5), 0 0 120px rgba(166,0,255,0.2); }
                }
                @keyframes scan-drift {
                    0%   { transform: translateY(-100%); }
                    100% { transform: translateY(100vh); }
                }
                .error-page {
                    position: relative;
                    z-index: 10;
                    min-height: 100vh;
                    display: flex;
                    align-items: center;
                    justify-content: center;
                    background: #000;
                    overflow: hidden;
                }
                .error-card {
                    position: relative;
                    z-index: 10;
                    display: flex;
                    flex-direction: column;
                    align-items: center;
                    text-align: center;
                    gap: 16px;
                    padding: 48px 40px;
                    max-width: 480px;
                    width: min(480px, calc(100vw - 48px));
                    animation: rise-up 0.6s cubic-bezier(.16,1,.3,1) both;
                    animation-delay: 0.1s;
                }
                .error-logo {
                    width: 56px;
                    height: 56px;
                    margin-bottom: 8px;
                    filter: drop-shadow(0 0 16px #a600ffaa);
                    animation: pulse-glow 3s ease-in-out infinite;
                    border-radius: 50%;
                }
                .error-code {
                    font-family: 'Russo One', sans-serif;
                    font-size: clamp(4rem, 12vw, 7rem);
                    line-height: 1;
                    color: #fff;
                    margin: 0;
                }
                .error-title {
                    font-family: 'Russo One', sans-serif;
                    font-size: clamp(1.2rem, 3.5vw, 1.8rem);
                    line-height: 1.2;
                    color: #fff;
                    margin: 0;
                    text-transform: uppercase;
                    letter-spacing: 0.12em;
                }
                .error-subtitle {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 11px;
                    letter-spacing: 0.2em;
                    text-transform: uppercase;
                    color: #a600ff;
                    margin: 0;
                }
                .error-divider {
                    width: 60px;
                    height: 1px;
                    background: linear-gradient(90deg, transparent, #a600ff, transparent);
                    margin: 4px 0;
                }
                .error-desc {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 13px;
                    line-height: 1.7;
                    color: rgba(255,255,255,0.4);
                    margin: 0;
                    max-width: 320px;
                }
                .error-actions {
                    display: flex;
                    gap: 12px;
                    flex-wrap: wrap;
                    justify-content: center;
                    margin-top: 8px;
                }
                .error-btn-primary {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    font-family: 'Chakra Petch', monospace;
                    font-weight: 600;
                    font-size: 12px;
                    letter-spacing: 0.14em;
                    text-transform: uppercase;
                    padding: 12px 28px;
                    border-radius: 8px;
                    background: linear-gradient(135deg, #a600ff, #7000cc);
                    color: #fff;
                    border: 1px solid rgba(166,0,255,0.7);
                    cursor: pointer;
                    text-decoration: none;
                    box-shadow: 0 0 24px rgba(166,0,255,0.35), 0 0 50px rgba(166,0,255,0.1);
                    transition: box-shadow 200ms, transform 200ms;
                }
                .error-btn-primary:hover {
                    box-shadow: 0 0 40px rgba(166,0,255,0.55), 0 0 80px rgba(166,0,255,0.2);
                    transform: translateY(-2px);
                }
                .error-btn-secondary {
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    font-family: 'Chakra Petch', monospace;
                    font-weight: 500;
                    font-size: 12px;
                    letter-spacing: 0.12em;
                    text-transform: uppercase;
                    padding: 12px 28px;
                    border-radius: 8px;
                    background: transparent;
                    color: rgba(255,255,255,0.5);
                    border: 1px solid rgba(6,182,212,0.3);
                    cursor: pointer;
                    text-decoration: none;
                    transition: color 200ms, border-color 200ms, box-shadow 200ms, transform 200ms;
                }
                .error-btn-secondary:hover {
                    color: #06b6d4;
                    border-color: rgba(6,182,212,0.6);
                    box-shadow: 0 0 20px rgba(6,182,212,0.2);
                    transform: translateY(-2px);
                }
                .error-scanline-bar {
                    position: fixed;
                    left: 0;
                    right: 0;
                    height: 4px;
                    background: linear-gradient(90deg, transparent, rgba(166,0,255,0.25), transparent);
                    animation: scan-drift 4s linear infinite;
                    pointer-events: none;
                    z-index: 5;
                }
                .error-vignette {
                    position: fixed;
                    inset: 0;
                    z-index: 1;
                    pointer-events: none;
                    background: radial-gradient(ellipse at center, transparent 20%, rgba(0,0,0,0.9) 100%);
                }
                .error-scanlines {
                    position: fixed;
                    inset: 0;
                    z-index: 2;
                    pointer-events: none;
                    background: repeating-linear-gradient(
                        to bottom, transparent, transparent 3px,
                        rgba(0,0,0,0.25) 3px, rgba(0,0,0,0.25) 4px
                    );
                }
                .error-static {
                    position: fixed;
                    inset: 0;
                    z-index: 3;
                    pointer-events: none;
                    opacity: 0.04;
                    background-image:
                        radial-gradient(circle at 20% 50%, rgba(255,255,255,0.8) 0%, transparent 25%),
                        radial-gradient(circle at 80% 30%, rgba(166,0,255,0.6) 0%, transparent 20%),
                        radial-gradient(circle at 50% 80%, rgba(6,182,212,0.4) 0%, transparent 30%);
                    background-size: 200% 200%;
                    animation: static-noise 8s ease-in-out infinite alternate;
                }
                @keyframes static-noise {
                    0%   { background-position: 0% 0%; }
                    33%  { background-position: 100% 0%; }
                    66%  { background-position: 0% 100%; }
                    100% { background-position: 100% 100%; }
                }
                .error-noise-lines {
                    position: fixed;
                    inset: 0;
                    z-index: 2;
                    pointer-events: none;
                    opacity: 0.06;
                    background:
                        linear-gradient(rgba(255,255,255,0.08) 1px, transparent 1px),
                        linear-gradient(90deg, rgba(255,255,255,0.06) 1px, transparent 1px);
                    background-size: 32px 32px;
                }
            `}</style>

            <div className="error-page">
                <div className="error-vignette" aria-hidden="true" />
                <div className="error-scanlines" aria-hidden="true" />
                <div className="error-static" aria-hidden="true" />
                <div className="error-noise-lines" aria-hidden="true" />
                <div className="error-scanline-bar" aria-hidden="true" />


                <div className="error-card">
                    <h1 className="error-code">
                        <GlitchText text={code} />
                    </h1>
                    <p className="error-subtitle">{subtitle}</p>
                    <div className="error-divider" />
                    <h2 className="error-title">
                        <GlitchText text={title} />
                    </h2>
                    <p className="error-desc">{description}</p>
                    <div className="error-actions">
                        {primaryAction && primaryAction.to && (
                            <Link to={primaryAction.to} className="error-btn-primary">
                                {primaryAction.icon}
                                {primaryAction.label}
                            </Link>
                        )}
                        {primaryAction && primaryAction.onClick && (
                            <button className="error-btn-primary" onClick={primaryAction.onClick}>
                                {primaryAction.icon}
                                {primaryAction.label}
                            </button>
                        )}
                        {secondaryAction && (
                            <button className="error-btn-secondary" onClick={secondaryAction.onClick}>
                                {secondaryAction.icon}
                                {secondaryAction.label}
                            </button>
                        )}
                    </div>
                </div>
            </div>
        </>
    )
}

export function NotFoundPage() {
    const [lang, setLang] = useState<'en' | 'ru'>('en')

    const T = {
        en: {
            subtitle: 'Signal Lost',
            title: 'Page Not Found',
            desc: 'The sector you are looking for does not exist or has been relocated to another dimension.',
            home: 'Return Home',
        },
        ru: {
            subtitle: 'Сигнал Потерян',
            title: 'Страница Не Найдена',
            desc: 'Сектор, который вы ищете, не существует или был перемещен в другое измерение.',
            home: 'Вернуться',
        },
    }

    const t = T[lang]

    return (
        <div className="ak-page">
            <style>{`
                .ak-page { background: #000; min-height: 100vh; position: relative; overflow: hidden; }
            `}</style>
            <img
                src="/violet-yang.svg"
                alt=""
                style={{
                    position: 'fixed',
                    top: '50%',
                    left: '50%',
                    translate: '-50% -50%',
                    width: 'min(70vw, 70vh)',
                    height: 'min(70vw, 70vh)',
                    opacity: 0.12,
                    animation: 'spin-slow 28s linear infinite, logo-breathe 5s ease-in-out infinite',
                    pointerEvents: 'none',
                    zIndex: 0,
                }}
                aria-hidden="true"
            />
            <div
                style={{
                    position: 'fixed',
                    top: '22px',
                    right: '28px',
                    zIndex: 60,
                    display: 'flex',
                    gap: '2px',
                    background: 'rgba(0,0,0,0.75)',
                    border: '1px solid rgba(166,0,255,0.25)',
                    borderRadius: '8px',
                    padding: '3px',
                    backdropFilter: 'blur(12px)',
                }}
                role="group"
                aria-label="Language"
            >
                <button
                    onClick={() => setLang('en')}
                    aria-pressed={lang === 'en'}
                    style={{
                        fontFamily: "'Chakra Petch', monospace",
                        fontSize: '11px',
                        fontWeight: 600,
                        letterSpacing: '0.12em',
                        padding: '5px 12px',
                        borderRadius: '5px',
                        border: 'none',
                        cursor: 'pointer',
                        transition: 'all 180ms ease',
                        background: lang === 'en' ? 'rgba(166,0,255,0.2)' : 'transparent',
                        color: lang === 'en' ? '#a600ff' : 'rgba(255,255,255,0.35)',
                        boxShadow: lang === 'en' ? '0 0 12px rgba(166,0,255,0.3)' : 'none',
                    }}
                >
                    EN
                </button>
                <button
                    onClick={() => setLang('ru')}
                    aria-pressed={lang === 'ru'}
                    style={{
                        fontFamily: "'Chakra Petch', monospace",
                        fontSize: '11px',
                        fontWeight: 600,
                        letterSpacing: '0.12em',
                        padding: '5px 12px',
                        borderRadius: '5px',
                        border: 'none',
                        cursor: 'pointer',
                        transition: 'all 180ms ease',
                        background: lang === 'ru' ? 'rgba(166,0,255,0.2)' : 'transparent',
                        color: lang === 'ru' ? '#a600ff' : 'rgba(255,255,255,0.35)',
                        boxShadow: lang === 'ru' ? '0 0 12px rgba(166,0,255,0.3)' : 'none',
                    }}
                >
                    RU
                </button>
            </div>
            <ErrorPageShell
                code="404"
                title={t.title}
                subtitle={t.subtitle}
                description={t.desc}
                primaryAction={{
                    label: t.home,
                    to: '/',
                    icon: <FiHome size={14} />,
                }}
            />
        </div>
    )
}

export function ServerErrorPage({ error, onRetry }: { error?: Error; onRetry?: () => void }) {
    const [lang, setLang] = useState<'en' | 'ru'>('en')

    const T = {
        en: {
            subtitle: 'Connection Lost',
            title: 'Server Error',
            desc: 'Our systems are experiencing interference. The servers may be unreachable or overloaded. Please stand by.',
            retry: 'Try Again',
            home: 'Return Home',
        },
        ru: {
            subtitle: 'Связь Потеряна',
            title: 'Ошибка Сервера',
            desc: 'Наши системы испытывают помехи. Серверы могут быть недоступны или перегружены. Пожалуйста, подождите.',
            retry: 'Повторить',
            home: 'Вернуться',
        },
    }

    const t = T[lang]

    return (
        <div className="ak-page">
            <style>{`
                .ak-page { background: #000; min-height: 100vh; position: relative; overflow: hidden; }
            `}</style>
            <img
                src="/violet-yang.svg"
                alt=""
                style={{
                    position: 'fixed',
                    top: '50%',
                    left: '50%',
                    translate: '-50% -50%',
                    width: 'min(70vw, 70vh)',
                    height: 'min(70vw, 70vh)',
                    opacity: 0.12,
                    animation: 'spin-slow 28s linear infinite, logo-breathe 5s ease-in-out infinite',
                    pointerEvents: 'none',
                    zIndex: 0,
                }}
                aria-hidden="true"
            />
            <div
                style={{
                    position: 'fixed',
                    top: '22px',
                    right: '28px',
                    zIndex: 60,
                    display: 'flex',
                    gap: '2px',
                    background: 'rgba(0,0,0,0.75)',
                    border: '1px solid rgba(166,0,255,0.25)',
                    borderRadius: '8px',
                    padding: '3px',
                    backdropFilter: 'blur(12px)',
                }}
                role="group"
                aria-label="Language"
            >
                <button
                    onClick={() => setLang('en')}
                    aria-pressed={lang === 'en'}
                    style={{
                        fontFamily: "'Chakra Petch', monospace",
                        fontSize: '11px',
                        fontWeight: 600,
                        letterSpacing: '0.12em',
                        padding: '5px 12px',
                        borderRadius: '5px',
                        border: 'none',
                        cursor: 'pointer',
                        transition: 'all 180ms ease',
                        background: lang === 'en' ? 'rgba(166,0,255,0.2)' : 'transparent',
                        color: lang === 'en' ? '#a600ff' : 'rgba(255,255,255,0.35)',
                        boxShadow: lang === 'en' ? '0 0 12px rgba(166,0,255,0.3)' : 'none',
                    }}
                >
                    EN
                </button>
                <button
                    onClick={() => setLang('ru')}
                    aria-pressed={lang === 'ru'}
                    style={{
                        fontFamily: "'Chakra Petch', monospace",
                        fontSize: '11px',
                        fontWeight: 600,
                        letterSpacing: '0.12em',
                        padding: '5px 12px',
                        borderRadius: '5px',
                        border: 'none',
                        cursor: 'pointer',
                        transition: 'all 180ms ease',
                        background: lang === 'ru' ? 'rgba(166,0,255,0.2)' : 'transparent',
                        color: lang === 'ru' ? '#a600ff' : 'rgba(255,255,255,0.35)',
                        boxShadow: lang === 'ru' ? '0 0 12px rgba(166,0,255,0.3)' : 'none',
                    }}
                >
                    RU
                </button>
            </div>
            <ErrorPageShell
                code="500"
                title={t.title}
                subtitle={t.subtitle}
                description={error ? `${t.desc} (${error.message})` : t.desc}
                primaryAction={{
                    label: t.home,
                    to: '/',
                    icon: <FiHome size={14} />,
                }}
                secondaryAction={
                    onRetry
                        ? {
                            label: t.retry,
                            onClick: onRetry,
                            icon: <FiRefreshCw size={14} />,
                        }
                        : undefined
                }
            />
        </div>
    )
}
