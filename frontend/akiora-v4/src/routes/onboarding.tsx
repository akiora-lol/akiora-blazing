import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import { FiArrowRight, FiArrowLeft, FiCheck, FiSkipForward } from 'react-icons/fi'
import { PageShell } from '../components/PageShell'
import { useAuthContext } from '../contexts/AuthContext'
import { useUpdateProfileMutation, type UpdateProfileData } from '../lib/api'

export const Route = createFileRoute('/onboarding')({
    component: OnboardingPage,
})

const T = {
    en: {
        step1Title: 'Choose your identity',
        step1Sub: 'How should others know you?',
        nickname: 'Nickname',
        step2Title: 'Tell us about yourself',
        step2Sub: 'Optional but helps personalize your experience',
        bio: 'Bio',
        bioPlaceholder: 'A short description about yourself...',
        gender: 'Gender',
        male: 'Male',
        female: 'Female',
        birthday: 'Birthday',
        step3Title: 'Connect your socials',
        step3Sub: 'Let others find you',
        next: 'Next',
        back: 'Back',
        skip: 'Skip',
        finish: 'Finish',
        stepOf: 'Step {n} of 3',
    },
    ru: {
        step1Title: 'Выбери свою личность',
        step1Sub: 'Как тебя будут знать другие?',
        nickname: 'Никнейм',
        step2Title: 'Расскажи о себе',
        step2Sub: 'Необязательно, но поможет персонализировать опыт',
        bio: 'О себе',
        bioPlaceholder: 'Краткое описание...',
        gender: 'Пол',
        male: 'Мужской',
        female: 'Женский',
        birthday: 'Дата рождения',
        step3Title: 'Подключи соцсети',
        step3Sub: 'Чтобы другие могли тебя найти',
        next: 'Далее',
        back: 'Назад',
        skip: 'Пропустить',
        finish: 'Готово',
        stepOf: 'Шаг {n} из 3',
    },
} as const

type Lang = keyof typeof T

const PLATFORMS = [
    { key: 'ds', label: 'Discord' },
    { key: 'tg', label: 'Telegram' },
    { key: 'vk', label: 'VK' },
    { key: 'yt', label: 'YouTube' },
    { key: 'tw', label: 'Twitch' },
] as const

function OnboardingPage() {
    const [lang, setLang] = useState<Lang>('en')
    const { user, isAuthenticated, isLoading } = useAuthContext()
    const navigate = useNavigate()
    const updateProfile = useUpdateProfileMutation()
    const t = T[lang]

    const [step, setStep] = useState(1)
    const [nickname, setNickname] = useState(user?.nickname ?? '')
    const [bio, setBio] = useState('')
    const [gender, setGender] = useState('')
    const [birthday, setBirthday] = useState('')
    const [socials, setSocials] = useState<Record<string, string>>({})

    // Redirect to login if not authenticated
    if (!isLoading && !isAuthenticated) {
        navigate({ to: '/login', replace: true })
        return null
    }

    // Show loading while checking auth
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

    if (!user) return null

    const handleSkip = () => {
        localStorage.setItem('akiora_onboarded', '1')
        navigate({ to: '/about' })
    }

    const handleFinish = async () => {
        if (!user) return
        const data: UpdateProfileData = { user_id: user.id }
        if (nickname && nickname !== user.nickname) data.nickname = nickname
        if (bio) data.bio = bio
        if (gender) data.gender = gender as 'MALE' | 'FEMALE'
        if (birthday) data.birth_date = { day: birthday, hidden: true }

        const socialEntries = Object.entries(socials).filter(([, v]) => v.trim())
        if (socialEntries.length > 0) {
            data.socials = Object.fromEntries(
                socialEntries.map(([k, v]) => [k, { link: v, hidden: false }])
            )
        }

        try {
            await updateProfile.mutateAsync({ userId: user.id, data })
            localStorage.setItem('akiora_onboarded', '1')
            navigate({ to: '/about' })
        } catch {
            // stay on page
        }
    }

    return (
        <>
            <style>{`
        @keyframes rise-up {
          from { opacity: 0; transform: translateY(18px); }
          to   { opacity: 1; transform: translateY(0); }
        }
        .onb-center {
          position: relative; z-index: 10;
          min-height: 100vh;
          display: flex; align-items: center; justify-content: center;
          padding: 40px 20px;
        }
        .onb-card {
          background: rgba(0,0,0,0.82);
          border: 1px solid rgba(166,0,255,0.22);
          border-radius: 18px;
          padding: 44px 40px;
          width: min(440px, calc(100vw - 48px));
          backdrop-filter: blur(24px);
          box-shadow: 0 0 60px rgba(166,0,255,0.12);
          display: flex; flex-direction: column; gap: 16px;
          animation: rise-up 0.4s cubic-bezier(.16,1,.3,1) both;
        }
        .onb-step-indicator {
          font-size: 9px; letter-spacing: 0.2em; text-transform: uppercase;
          color: rgba(166,0,255,0.6); text-align: center;
        }
        .onb-progress {
          display: flex; gap: 6px; justify-content: center;
        }
        .onb-dot {
          width: 28px; height: 3px; border-radius: 2px;
          background: rgba(255,255,255,0.1);
          transition: background 300ms;
        }
        .onb-dot.active { background: #a600ff; box-shadow: 0 0 8px rgba(166,0,255,0.5); }
        .onb-dot.done { background: rgba(166,0,255,0.4); }
        .onb-title {
          font-family: 'Russo One', sans-serif;
          font-size: 20px; color: #fff; text-align: center;
          margin: 8px 0 0; letter-spacing: 0.04em;
        }
        .onb-sub {
          font-size: 11px; color: rgba(255,255,255,0.3);
          text-align: center; letter-spacing: 0.08em; margin-bottom: 8px;
        }
        .onb-label {
          font-size: 9px; letter-spacing: 0.18em; text-transform: uppercase;
          color: rgba(166,0,255,0.7); margin-bottom: 4px;
        }
        .onb-input {
          width: 100%; padding: 12px 16px; border-radius: 10px;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.12);
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 13px; outline: none;
          transition: border-color 180ms;
        }
        .onb-input:focus { border-color: rgba(166,0,255,0.5); }
        .onb-input::placeholder { color: rgba(255,255,255,0.15); }
        .onb-select {
          width: 100%; padding: 12px 16px; border-radius: 10px;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.12);
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 13px; outline: none;
        }
        .onb-row { display: flex; flex-direction: column; gap: 4px; }
        .onb-social-row { display: flex; align-items: center; gap: 10px; }
        .onb-social-label {
          font-size: 11px; color: rgba(255,255,255,0.5);
          width: 70px; letter-spacing: 0.06em;
        }
        .onb-social-input {
          flex: 1; padding: 9px 14px; border-radius: 8px;
          background: rgba(255,255,255,0.04);
          border: 1px solid rgba(255,255,255,0.08);
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 12px; outline: none;
        }
        .onb-social-input:focus { border-color: rgba(166,0,255,0.4); }
        .onb-actions {
          display: flex; justify-content: space-between; align-items: center;
          margin-top: 8px;
        }
        .onb-btn {
          display: flex; align-items: center; gap: 6px;
          padding: 10px 20px; border-radius: 8px;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;
          cursor: pointer; border: none; transition: all 180ms;
        }
        .onb-btn.next {
          background: linear-gradient(135deg, #a600ff, #7000cc);
          color: #fff;
        }
        .onb-btn.next:hover { box-shadow: 0 0 20px rgba(166,0,255,0.4); }
        .onb-btn.back {
          background: transparent; color: rgba(255,255,255,0.3);
          border: 1px solid rgba(255,255,255,0.08);
        }
        .onb-btn.back:hover { color: rgba(255,255,255,0.6); }
        .onb-btn.skip {
          background: transparent; color: rgba(255,255,255,0.2);
        }
        .onb-btn.skip:hover { color: rgba(255,255,255,0.5); }
        .onb-btn:disabled { opacity: 0.5; cursor: not-allowed; }
      `}</style>

            <PageShell lang={lang} onLangChange={setLang}>
                <div className="onb-center">
                    <div className="onb-card">
                        <div className="onb-progress">
                            {[1, 2, 3].map(s => (
                                <div key={s} className={`onb-dot${s === step ? ' active' : s < step ? ' done' : ''}`} />
                            ))}
                        </div>
                        <div className="onb-step-indicator">{t.stepOf.replace('{n}', String(step))}</div>

                        {step === 1 && (
                            <>
                                <h2 className="onb-title">{t.step1Title}</h2>
                                <p className="onb-sub">{t.step1Sub}</p>
                                <div className="onb-row">
                                    <span className="onb-label">{t.nickname}</span>
                                    <input
                                        className="onb-input"
                                        value={nickname}
                                        onChange={(e) => setNickname(e.target.value)}
                                        autoFocus
                                    />
                                </div>
                            </>
                        )}

                        {step === 2 && (
                            <>
                                <h2 className="onb-title">{t.step2Title}</h2>
                                <p className="onb-sub">{t.step2Sub}</p>
                                <div className="onb-row">
                                    <span className="onb-label">{t.bio}</span>
                                    <input
                                        className="onb-input"
                                        placeholder={t.bioPlaceholder}
                                        value={bio}
                                        onChange={(e) => setBio(e.target.value)}
                                        autoFocus
                                    />
                                </div>
                                <div className="onb-row">
                                    <span className="onb-label">{t.gender}</span>
                                    <select className="onb-select" value={gender} onChange={(e) => setGender(e.target.value)}>
                                        <option value="">—</option>
                                        <option value="MALE">{t.male}</option>
                                        <option value="FEMALE">{t.female}</option>
                                    </select>
                                </div>
                                <div className="onb-row">
                                    <span className="onb-label">{t.birthday}</span>
                                    <input
                                        className="onb-input"
                                        type="date"
                                        value={birthday}
                                        onChange={(e) => setBirthday(e.target.value)}
                                    />
                                </div>
                            </>
                        )}

                        {step === 3 && (
                            <>
                                <h2 className="onb-title">{t.step3Title}</h2>
                                <p className="onb-sub">{t.step3Sub}</p>
                                {PLATFORMS.map(p => (
                                    <div key={p.key} className="onb-social-row">
                                        <span className="onb-social-label">{p.label}</span>
                                        <input
                                            className="onb-social-input"
                                            placeholder={`${p.label} link or @`}
                                            value={socials[p.key] ?? ''}
                                            onChange={(e) => setSocials(s => ({ ...s, [p.key]: e.target.value }))}
                                        />
                                    </div>
                                ))}
                            </>
                        )}

                        <div className="onb-actions">
                            <div style={{ display: 'flex', gap: 8 }}>
                                {step > 1 && (
                                    <button className="onb-btn back" onClick={() => setStep(s => s - 1)}>
                                        <FiArrowLeft size={12} /> {t.back}
                                    </button>
                                )}
                                <button className="onb-btn skip" onClick={handleSkip}>
                                    <FiSkipForward size={12} /> {t.skip}
                                </button>
                            </div>
                            {step < 3 ? (
                                <button className="onb-btn next" onClick={() => setStep(s => s + 1)}>
                                    {t.next} <FiArrowRight size={12} />
                                </button>
                            ) : (
                                <button className="onb-btn next" disabled={updateProfile.isPending} onClick={handleFinish}>
                                    {t.finish} <FiCheck size={12} />
                                </button>
                            )}
                        </div>
                    </div>
                </div>
            </PageShell>
        </>
    )
}
