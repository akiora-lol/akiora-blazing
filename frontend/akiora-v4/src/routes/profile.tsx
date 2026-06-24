import { createFileRoute, useNavigate } from '@tanstack/react-router'
import { useState } from 'react'
import {
    FiUser, FiSettings, FiShield, FiEdit2, FiSave, FiX,
    FiLogOut, FiCalendar, FiLink, FiAlertCircle, FiCheck,
    FiPlus, FiTrash2, FiImage,
} from 'react-icons/fi'
import { PageShell } from '../components/PageShell'
import { useAuthContext } from '../contexts/AuthContext'
import { useLogout } from '../lib/auth'
import {
    useFinishLolVerificationMutation,
    useStartLolVerificationMutation,
    useUpdateProfileMutation,
    type LolVerificationStartResponse,
    type UpdateProfileData,
} from '../lib/api'

export const Route = createFileRoute('/profile')({
    component: ProfilePage,
})

const T = {
    en: {
        profile: 'Profile', settings: 'Settings', security: 'Security',
        nickname: 'Nickname', email: 'Email', bio: 'Bio', gender: 'Gender',
        birthday: 'Birthday', socials: 'Social Links',
        male: 'Male', female: 'Female',
        edit: 'Edit Profile', save: 'Save Changes', cancel: 'Cancel',
        completeSetup: 'Complete Setup',
        noData: 'Not set',
        MALE: 'Male', FEMALE: 'Female',
        lang: 'Language', theme: 'Theme',
        langEn: 'English', langRu: 'Russian',
        themeDesc: 'Visual appearance of the interface',
        dark: 'Dark', light: 'Light',
        notifSection: 'Notifications',
        notifEmail: 'Email notifications',
        notifDesc: 'Receive updates about tournaments and matches',
        sessionSection: 'Active Sessions',
        logoutAll: 'Log out all devices',
        logoutCurrent: 'Log out',
        currentSession: 'Current session',
        twoFactor: 'Two-factor authentication',
        twoFactorDesc: 'Add an extra layer of security to your account',
        enable: 'Enable',
        memberSince: 'Member since',
        lastActive: 'Last active',
        accountType: 'Account type',
        saveSuccess: 'Changes saved',
        addSocial: 'Add social link',
        removeSocial: 'Remove',
        socialPlatform: 'Platform',
        socialLink: 'Link/Username',
        editSocials: 'Edit social links',
        avatar: 'Avatar',
        avatarUrl: 'Avatar URL',
        avatarFile: 'Upload file',
        avatarUrlPlaceholder: 'https://example.com/avatar.jpg',
        changeAvatar: 'Change avatar',
        leagueAccounts: 'League Accounts',
        linkLeague: 'Link League account',
        server: 'Server',
        riotName: 'Riot name',
        tagline: 'Tag',
        checkAccount: 'Check account',
        confirmAccount: 'Confirm',
        targetIcon: 'Set profile icon',
        linkedAccountsEmpty: 'No linked League accounts',
        verificationReady: 'Change your League profile icon, then confirm here.',
    },
    ru: {
        profile: 'Профиль', settings: 'Настройки', security: 'Безопасность',
        nickname: 'Никнейм', email: 'Email', bio: 'О себе', gender: 'Пол',
        birthday: 'Дата рождения', socials: 'Соцсети',
        male: 'Мужской', female: 'Женский',
        edit: 'Редактировать', save: 'Сохранить', cancel: 'Отмена',
        completeSetup: 'Заполнить профиль',
        noData: 'Не указано',
        MALE: 'Мужской', FEMALE: 'Женский',
        lang: 'Язык', theme: 'Тема',
        langEn: 'Английский', langRu: 'Русский',
        themeDesc: 'Внешний вид интерфейса',
        dark: 'Тёмная', light: 'Светлая',
        notifSection: 'Уведомления',
        notifEmail: 'Email-уведомления',
        notifDesc: 'Получать обновления о турнирах и матчах',
        sessionSection: 'Активные сессии',
        logoutAll: 'Выйти со всех устройств',
        logoutCurrent: 'Выйти',
        currentSession: 'Текущая сессия',
        twoFactor: 'Двухфакторная аутентификация',
        twoFactorDesc: 'Дополнительный уровень защиты аккаунта',
        enable: 'Включить',
        memberSince: 'Участник с',
        lastActive: 'Последняя активность',
        accountType: 'Тип аккаунта',
        saveSuccess: 'Изменения сохранены',
        addSocial: 'Добавить соцсеть',
        removeSocial: 'Удалить',
        socialPlatform: 'Платформа',
        socialLink: 'Ссылка/Никнейм',
        editSocials: 'Редактировать соцсети',
        avatar: 'Аватарка',
        avatarUrl: 'Ссылка на аватарку',
        avatarFile: 'Загрузить файл',
        avatarUrlPlaceholder: 'https://example.com/avatar.jpg',
        changeAvatar: 'Изменить аватарку',
        leagueAccounts: 'League аккаунты',
        linkLeague: 'Привязать League аккаунт',
        server: 'Сервер',
        riotName: 'Riot никнейм',
        tagline: 'Тэг',
        checkAccount: 'Проверить аккаунт',
        confirmAccount: 'Подтвердить',
        targetIcon: 'Поставьте иконку',
        linkedAccountsEmpty: 'Нет привязанных League аккаунтов',
        verificationReady: 'Смените иконку профиля League, затем подтвердите здесь.',
    },
} as const

type Lang = keyof typeof T

const PLATFORM_LABELS: Record<string, string> = {
    vk: 'VK', tg: 'Telegram', ds: 'Discord', yt: 'YouTube', tw: 'Twitch', sc: 'SoundCloud',
    github: 'GitHub', twitter: 'Twitter', instagram: 'Instagram', facebook: 'Facebook',
}

const PLATFORM_OPTIONS = [
    { value: 'vk', label: 'VK' },
    { value: 'tg', label: 'Telegram' },
    { value: 'ds', label: 'Discord' },
    { value: 'yt', label: 'YouTube' },
    { value: 'tw', label: 'Twitch' },
    { value: 'sc', label: 'SoundCloud' },
    { value: 'github', label: 'GitHub' },
    { value: 'twitter', label: 'Twitter' },
    { value: 'instagram', label: 'Instagram' },
    { value: 'facebook', label: 'Facebook' },
]

const PLATFORM_COLORS: Record<string, string> = {
    vk: '#4a76a8', tg: '#229ed9', ds: '#5865f2', yt: '#ff0000', tw: '#9146ff', sc: '#ff5500',
    github: '#24292e', twitter: '#1da1f2', instagram: '#e4405f', facebook: '#1877f2',
}

type Tab = 'profile' | 'settings' | 'security'

const TABS: { id: Tab; icon: typeof FiUser; labelKey: 'profile' | 'settings' | 'security' }[] = [
    { id: 'profile', icon: FiUser, labelKey: 'profile' },
    { id: 'settings', icon: FiSettings, labelKey: 'settings' },
    { id: 'security', icon: FiShield, labelKey: 'security' },
]

function ProfilePage() {
    const [lang, setLang] = useState<Lang>('ru')
    const { user, isAuthenticated, isLoading } = useAuthContext()
    const navigate = useNavigate()
    const logout = useLogout()
    const updateProfile = useUpdateProfileMutation()
    const startLolVerification = useStartLolVerificationMutation()
    const finishLolVerification = useFinishLolVerificationMutation()
    const t = T[lang]

    const [activeTab, setActiveTab] = useState<Tab>('profile')
    const [editing, setEditing] = useState(false)
    const [saveSuccess, setSaveSuccess] = useState(false)
    const [notifEmail, setNotifEmail] = useState(true)
    const [editingSocials, setEditingSocials] = useState(false)
    const [editingAvatar, setEditingAvatar] = useState(false)
    const [lolForm, setLolForm] = useState({
        server: 'na',
        username: '',
        tagline: '',
    })
    const [lolChallenge, setLolChallenge] = useState<LolVerificationStartResponse | null>(null)
    const [lolError, setLolError] = useState('')
    const [lolSuccess, setLolSuccess] = useState(false)
    const [form, setForm] = useState({
        nickname: user?.nickname ?? '',
        bio: user?.bio ?? '',
        gender: user?.gender ?? '',
        avatar: user?.avatar ?? '',
        socials: user?.socials ?? {},
    })

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

    const handleSave = async () => {
        const data: UpdateProfileData = {
            user_id: user.id,
            nickname: form.nickname || undefined,
            bio: form.bio || undefined,
            gender: (form.gender as 'MALE' | 'FEMALE') || undefined,
            avatar: form.avatar || undefined,
            socials: Object.keys(form.socials).length > 0 ? form.socials : undefined,
        }
        await updateProfile.mutateAsync({ userId: user.id, data })
        setEditing(false)
        setEditingSocials(false)
        setEditingAvatar(false)
        setSaveSuccess(true)
        setTimeout(() => setSaveSuccess(false), 2500)
    }

    const addSocial = () => {
        const availablePlatforms = PLATFORM_OPTIONS.filter(
            p => !form.socials[p.value]
        )
        if (availablePlatforms.length === 0) return

        const firstAvailable = availablePlatforms[0].value
        setForm(f => ({
            ...f,
            socials: {
                ...f.socials,
                [firstAvailable]: { link: '', hidden: false }
            }
        }))
    }

    const removeSocial = (platform: string) => {
        setForm(f => {
            const newSocials = { ...f.socials }
            delete newSocials[platform]
            return { ...f, socials: newSocials }
        })
    }

    const updateSocial = (platform: string, link: string) => {
        setForm(f => ({
            ...f,
            socials: {
                ...f.socials,
                [platform]: { link, hidden: false }
            }
        }))
    }

    const handleStartLolVerification = async () => {
        setLolError('')
        setLolSuccess(false)
        setLolChallenge(null)

        try {
            const challenge = await startLolVerification.mutateAsync({
                server: lolForm.server.trim().toLowerCase(),
                username: lolForm.username.trim(),
                tagline: lolForm.tagline.trim(),
            })
            if (challenge) {
                setLolChallenge(challenge)
            }
        } catch (error) {
            setLolError(error instanceof Error ? error.message : 'Failed to start verification')
        }
    }

    const handleFinishLolVerification = async () => {
        if (!lolChallenge) return
        setLolError('')

        try {
            await finishLolVerification.mutateAsync(lolChallenge.verification_id)
            setLolSuccess(true)
            setLolChallenge(null)
            setLolForm({ server: 'na', username: '', tagline: '' })
            setTimeout(() => setLolSuccess(false), 2500)
        } catch (error) {
            setLolError(error instanceof Error ? error.message : 'Failed to confirm account')
        }
    }

    const onboarded = typeof window !== 'undefined' && localStorage.getItem('akiora_onboarded')
    const joinDate = new Date(user.created_at * 1000).toLocaleDateString(lang === 'ru' ? 'ru-RU' : 'en-US', {
        year: 'numeric', month: 'long', day: 'numeric',
    })
    const formatRank = (account: typeof user.league_accounts[number]) => {
        if (!account.solo_tier) return lang === 'ru' ? 'Ранг не найден' : 'Rank unavailable'
        const division = account.solo_division ? ` ${account.solo_division}` : ''
        const lp = typeof account.solo_lp === 'number' ? ` · ${account.solo_lp} LP` : ''
        return `${account.solo_tier}${division}${lp}`
    }

    return (
        <>
            <style>{`
        @keyframes rise-up {
          from { opacity: 0; transform: translateY(20px) scale(0.98); }
          to   { opacity: 1; transform: translateY(0) scale(1); }
        }
        @keyframes fade-in {
          from { opacity: 0; transform: translateX(-8px); }
          to   { opacity: 1; transform: translateX(0); }
        }
        @keyframes success-pop {
          0%   { opacity: 0; transform: scale(0.85); }
          60%  { transform: scale(1.05); }
          100% { opacity: 1; transform: scale(1); }
        }

        .profile-page {
          position: relative; z-index: 10;
          min-height: 100vh;
          display: flex; align-items: center; justify-content: center;
          padding: 88px 24px 48px;
        }

        /* ─── Main panel ─────────────────────────────── */
        .profile-panel {
          width: min(1000px, calc(100vw - 48px));
          min-height: 620px;
          background: rgba(0,0,0,0.86);
          border: 1px solid rgba(166,0,255,0.18);
          border-radius: 20px;
          backdrop-filter: blur(28px);
          box-shadow: 0 0 80px rgba(166,0,255,0.1), 0 0 120px rgba(0,0,0,0.6);
          display: flex;
          overflow: hidden;
          animation: rise-up 0.45s cubic-bezier(.16,1,.3,1) both;
        }

        /* ─── Left sidebar ───────────────────────────── */
        .profile-sidebar {
          width: 220px;
          flex-shrink: 0;
          border-right: 1px solid rgba(255,255,255,0.06);
          background: rgba(0,0,0,0.3);
          display: flex; flex-direction: column;
          padding: 28px 0 20px;
        }

        .profile-user-block {
          padding: 0 20px 24px;
          border-bottom: 1px solid rgba(255,255,255,0.06);
          margin-bottom: 16px;
          display: flex; flex-direction: column; align-items: center; gap: 12px;
        }

        .profile-avatar-wrap {
          position: relative;
          width: 72px; height: 72px;
          transition: all 200ms ease;
        }
        .profile-avatar-wrap:hover {
          transform: scale(1.05);
        }
        .profile-avatar-wrap:hover .profile-avatar-edit-hint {
          opacity: 1;
        }
        .profile-avatar {
          width: 72px; height: 72px; border-radius: 50%;
          background: rgba(166,0,255,0.15);
          border: 2px solid rgba(166,0,255,0.35);
          display: flex; align-items: center; justify-content: center;
          color: rgba(255,255,255,0.5);
          overflow: hidden;
          box-shadow: 0 0 20px rgba(166,0,255,0.2);
        }
        .profile-avatar img { width: 100%; height: 100%; object-fit: cover; }
        .profile-avatar-ring {
          position: absolute; inset: -3px;
          border-radius: 50%;
          border: 1.5px solid transparent;
          background: linear-gradient(135deg, rgba(166,0,255,0.6), rgba(80,0,160,0.3)) border-box;
          -webkit-mask: linear-gradient(#fff 0 0) padding-box, linear-gradient(#fff 0 0);
          -webkit-mask-composite: destination-out;
          mask-composite: exclude;
        }
        .profile-avatar-edit-hint {
          position: absolute; top: -2px; right: -2px;
          width: 24px; height: 24px;
          background: rgba(255,0,255,0.9);
          border: 2px solid rgba(0,0,0,0.8);
          border-radius: 50%;
          display: flex; align-items: center; justify-content: center;
          color: #fff;
          opacity: 0;
          transition: all 200ms ease;
          box-shadow: 0 0 12px rgba(255,0,255,0.6);
        }

        .profile-user-name {
          font-family: 'Russo One', sans-serif;
          font-size: 15px; color: #fff; letter-spacing: 0.04em;
          text-align: center; line-height: 1.2;
        }
        .profile-user-email {
          font-size: 10px; color: rgba(255,255,255,0.3);
          letter-spacing: 0.04em; text-align: center;
          word-break: break-all;
        }
        .profile-badge {
          font-size: 9px; letter-spacing: 0.12em; text-transform: uppercase;
          padding: 3px 10px; border-radius: 20px;
          background: rgba(166,0,255,0.15);
          border: 1px solid rgba(166,0,255,0.3);
          color: rgba(166,0,255,0.9);
        }

        /* ─── Sidebar tabs ───────────────────────────── */
        .profile-tabs {
          display: flex; flex-direction: column; gap: 2px;
          padding: 0 10px;
          flex: 1;
        }
        .profile-tab {
          display: flex; align-items: center; gap: 10px;
          padding: 10px 14px; border-radius: 10px;
          cursor: pointer;
          transition: all 160ms;
          color: rgba(255,255,255,0.4);
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em;
          text-transform: uppercase;
          border: 1px solid transparent;
          user-select: none;
        }
        .profile-tab:hover {
          color: rgba(255,255,255,0.8);
          background: rgba(255,255,255,0.04);
        }
        .profile-tab.active {
          color: #fff;
          background: rgba(166,0,255,0.12);
          border-color: rgba(166,0,255,0.25);
        }
        .profile-tab.active svg {
          filter: drop-shadow(0 0 6px rgba(166,0,255,0.7));
          color: rgba(166,0,255,0.9);
        }
        .profile-tab-dot {
          width: 4px; height: 4px; border-radius: 50%;
          background: rgba(166,0,255,0.8);
          margin-left: auto;
          flex-shrink: 0;
        }

        .profile-sidebar-bottom {
          padding: 0 10px;
          margin-top: auto;
          border-top: 1px solid rgba(255,255,255,0.06);
          padding-top: 16px;
        }
        .profile-logout-btn {
          display: flex; align-items: center; gap: 10px;
          width: 100%; padding: 10px 14px; border-radius: 10px;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;
          color: rgba(255,80,80,0.6); background: transparent;
          border: 1px solid transparent; cursor: pointer;
          transition: all 160ms;
        }
        .profile-logout-btn:hover {
          color: rgba(255,80,80,0.9);
          background: rgba(255,80,80,0.06);
          border-color: rgba(255,80,80,0.2);
        }

        /* ─── Content area ───────────────────────────── */
        .profile-content {
          flex: 1; min-width: 0;
          padding: 36px 40px;
          overflow-y: auto;
          animation: fade-in 0.3s ease both;
        }

        .content-header {
          display: flex; align-items: center; justify-content: space-between;
          margin-bottom: 32px;
          padding-bottom: 20px;
          border-bottom: 1px solid rgba(255,255,255,0.06);
        }
        .content-title {
          font-family: 'Russo One', sans-serif;
          font-size: 22px; color: #fff; letter-spacing: 0.04em;
        }
        .content-subtitle {
          font-size: 11px; color: rgba(255,255,255,0.3);
          letter-spacing: 0.06em; margin-top: 4px;
        }

        .profile-quick-grid {
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 12px;
          margin-bottom: 26px;
        }
        .profile-quick-card {
          min-height: 78px;
          border: 1px solid rgba(255,255,255,0.09);
          border-radius: 8px;
          padding: 14px;
          background:
            linear-gradient(135deg, rgba(45,212,191,0.08), rgba(192,132,252,0.06)),
            rgba(255,255,255,0.025);
          display: flex;
          flex-direction: column;
          justify-content: space-between;
        }
        .profile-quick-label {
          color: rgba(255,255,255,0.42);
          font-family: 'Chakra Petch', monospace;
          font-size: 10px;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }
        .profile-quick-value {
          color: #fff;
          font-family: 'Russo One', sans-serif;
          font-size: 18px;
          letter-spacing: 0;
          overflow-wrap: anywhere;
        }

        /* ─── Success toast ──────────────────────────── */
        .save-success {
          display: flex; align-items: center; gap: 8px;
          padding: 8px 16px; border-radius: 8px;
          background: rgba(0,200,100,0.12);
          border: 1px solid rgba(0,200,100,0.3);
          color: rgba(0,220,110,0.9);
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em;
          animation: success-pop 0.3s ease both;
        }

        /* ─── Field groups ───────────────────────────── */
        .field-grid {
          display: grid;
          grid-template-columns: 1fr 1fr;
          gap: 20px;
          margin-bottom: 24px;
        }
        .field-grid.single { grid-template-columns: 1fr; }
        .field-group {
          display: flex; flex-direction: column; gap: 6px;
        }
        .field-group.span2 { grid-column: span 2; }

        .field-label {
          font-size: 9px; letter-spacing: 0.22em; text-transform: uppercase;
          color: rgba(255,0,255,0.85);
          text-shadow: 0 0 8px rgba(255,0,255,0.4);
          font-family: 'Chakra Petch', monospace;
        }
        .field-value {
          font-size: 14px; color: rgba(255,255,255,0.95);
          letter-spacing: 0.02em; padding: 3px 0;
          line-height: 1.5;
          text-shadow: 0 0 12px rgba(255,255,255,0.1);
        }
        .field-value.empty {
          color: rgba(255,255,255,0.2); font-style: italic; font-size: 13px;
        }

        /* ─── Edit inputs ────────────────────────────── */
        .field-input-wrap {
          position: relative;
        }
        .field-input {
          width: 100%;
          padding: 12px 16px;
          border-radius: 10px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.1);
          color: #fff;
          font-family: 'Chakra Petch', monospace;
          font-size: 13px; letter-spacing: 0.02em;
          outline: none;
          transition: border-color 180ms, box-shadow 180ms, background 180ms;
          box-sizing: border-box;
        }
        .field-input:focus {
          border-color: rgba(255,0,255,0.8);
          background: rgba(255,0,255,0.06);
          box-shadow: 0 0 0 3px rgba(255,0,255,0.12), 0 0 20px rgba(255,0,255,0.3);
        }
        .field-input::placeholder { color: rgba(255,255,255,0.2); }

        textarea.field-input {
          resize: vertical; min-height: 90px;
          line-height: 1.6;
        }

        .field-select {
          width: 100%;
          padding: 12px 16px;
          border-radius: 10px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.1);
          color: #fff;
          font-family: 'Chakra Petch', monospace;
          font-size: 13px; letter-spacing: 0.02em;
          outline: none;
          cursor: pointer;
          appearance: none;
          transition: border-color 180ms, box-shadow 180ms;
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='12' height='8' viewBox='0 0 12 8'%3E%3Cpath d='M1 1l5 5 5-5' stroke='rgba(255,255,255,0.3)' stroke-width='1.5' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
          background-repeat: no-repeat;
          background-position: right 14px center;
          padding-right: 36px;
        }
        .field-select:focus {
          border-color: rgba(255,0,255,0.8);
          box-shadow: 0 0 0 3px rgba(255,0,255,0.12), 0 0 20px rgba(255,0,255,0.3);
        }
        .field-select option { background: #1a0030; color: #fff; }

        /* ─── Section divider ────────────────────────── */
        .section-divider {
          height: 1px; background: rgba(255,255,255,0.06);
          margin: 24px 0;
        }
        .section-title {
          font-family: 'Russo One', sans-serif;
          font-size: 13px; color: rgba(255,255,255,0.5);
          letter-spacing: 0.1em; text-transform: uppercase;
          margin-bottom: 16px;
        }

        /* ─── Socials ────────────────────────────────── */
        .socials-list { display: flex; flex-wrap: wrap; gap: 8px; }
        .social-chip {
          display: flex; align-items: center; gap: 7px;
          padding: 6px 14px; border-radius: 8px;
          font-size: 11px; letter-spacing: 0.06em;
          font-family: 'Chakra Petch', monospace;
          border: 1px solid rgba(255,255,255,0.08);
          background: rgba(255,255,255,0.03);
          color: rgba(255,255,255,0.7);
          transition: all 160ms; cursor: default;
        }
        .social-chip:hover { background: rgba(255,255,255,0.06); color: #fff; }

        .league-account-list {
          display: grid;
          grid-template-columns: repeat(2, minmax(0, 1fr));
          gap: 10px;
          margin-bottom: 14px;
        }
        .league-account-item {
          display: grid;
          grid-template-columns: 46px minmax(0, 1fr);
          align-items: center;
          gap: 12px;
          padding: 12px;
          border: 1px solid rgba(166,0,255,0.18);
          border-radius: 8px;
          background:
            linear-gradient(135deg, rgba(166,0,255,0.1), rgba(255,255,255,0.03)),
            rgba(255,255,255,0.025);
        }
        .league-account-icon {
          width: 46px; height: 46px;
          border-radius: 8px;
          object-fit: cover;
          border: 1px solid rgba(255,255,255,0.16);
          background: rgba(255,255,255,0.06);
        }
        .league-account-main {
          min-width: 0;
          display: flex; flex-direction: column; gap: 3px;
        }
        .league-account-name {
          color: #fff;
          font-family: 'Chakra Petch', monospace;
          font-size: 13px;
          letter-spacing: 0.03em;
          overflow-wrap: anywhere;
        }
        .league-account-meta {
          color: rgba(255,255,255,0.38);
          font-size: 10px;
          letter-spacing: 0.08em;
          text-transform: uppercase;
        }
        .league-rank-row {
          display: flex;
          align-items: center;
          gap: 7px;
          min-height: 24px;
          margin-top: 4px;
        }
        .league-rank-icon {
          width: 22px; height: 22px;
          object-fit: contain;
        }
        .league-rank-text {
          color: rgba(255,255,255,0.78);
          font-size: 11px;
          line-height: 1.25;
        }
        .league-rank-lp {
          color: rgba(255,255,255,0.38);
          font-size: 10px;
        }
        .league-status {
          width: fit-content;
          color: rgba(0,220,110,0.92);
          border: 1px solid rgba(0,200,100,0.28);
          background: rgba(0,200,100,0.1);
          border-radius: 999px;
          padding: 4px 9px;
          font-size: 9px;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }
        .league-link-grid {
          display: grid;
          grid-template-columns: 92px 1fr 92px;
          gap: 10px;
          margin-top: 12px;
        }
        .league-challenge {
          display: grid;
          grid-template-columns: 54px minmax(0, 1fr) auto;
          align-items: center;
          gap: 12px;
          margin-top: 12px;
          padding: 12px;
          border: 1px solid rgba(166,0,255,0.24);
          border-radius: 8px;
          background: rgba(166,0,255,0.08);
        }
        .league-challenge img {
          width: 54px; height: 54px;
          border-radius: 8px;
          object-fit: cover;
          border: 1px solid rgba(255,255,255,0.12);
        }
        .league-challenge-text {
          flex: 1; min-width: 0;
          color: rgba(255,255,255,0.66);
          font-size: 12px;
          line-height: 1.5;
        }
        .league-icon-number {
          color: #fff;
          font-family: 'Russo One', sans-serif;
          font-size: 13px;
          letter-spacing: 0.02em;
        }
        .form-error {
          margin-top: 10px;
          color: rgba(255,90,90,0.9);
          font-size: 11px;
          line-height: 1.45;
        }
        .form-success {
          margin-top: 10px;
          color: rgba(0,220,110,0.92);
          font-size: 11px;
          line-height: 1.45;
        }
        .social-dot { width: 6px; height: 6px; border-radius: 50%; flex-shrink: 0; }

        /* ─── Action buttons ─────────────────────────── */
        .action-row {
          display: flex; gap: 10px; margin-top: 28px;
        }
        .btn {
          display: flex; align-items: center; gap: 7px;
          padding: 11px 22px; border-radius: 10px;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.1em; text-transform: uppercase;
          cursor: pointer; transition: all 180ms;
          border: 1px solid rgba(255,255,255,0.1);
          background: rgba(255,255,255,0.04); color: rgba(255,255,255,0.7);
        }
        .btn:hover { color: #fff; border-color: rgba(255,255,255,0.25); background: rgba(255,255,255,0.07); }
        .btn.primary {
          background: linear-gradient(135deg, #a600ff 0%, #6600bb 100%);
          border-color: rgba(166,0,255,0.6); color: #fff;
        }
        .btn.primary:hover {
          box-shadow: 0 0 24px rgba(166,0,255,0.45);
          transform: translateY(-1px);
        }
        .btn:disabled { opacity: 0.45; cursor: not-allowed; transform: none !important; box-shadow: none !important; }

        /* ─── Settings toggles ───────────────────────── */
        .setting-row {
          display: flex; align-items: center; justify-content: space-between;
          padding: 14px 0;
          border-bottom: 1px solid rgba(255,255,255,0.05);
        }
        .setting-row:last-child { border-bottom: none; }
        .setting-info { flex: 1; }
        .setting-name {
          font-size: 13px; color: rgba(255,255,255,0.85);
          font-family: 'Chakra Petch', monospace; letter-spacing: 0.03em;
          margin-bottom: 3px;
        }
        .setting-desc {
          font-size: 11px; color: rgba(255,255,255,0.3); letter-spacing: 0.03em;
        }

        .toggle {
          position: relative; width: 42px; height: 24px; flex-shrink: 0;
        }
        .toggle input { opacity: 0; width: 0; height: 0; }
        .toggle-track {
          position: absolute; inset: 0;
          border-radius: 24px;
          background: rgba(255,255,255,0.08);
          border: 1px solid rgba(255,255,255,0.12);
          cursor: pointer; transition: all 200ms;
        }
        .toggle-track::after {
          content: '';
          position: absolute; top: 3px; left: 3px;
          width: 16px; height: 16px; border-radius: 50%;
          background: rgba(255,255,255,0.4);
          transition: all 200ms cubic-bezier(.34,1.56,.64,1);
        }
        .toggle input:checked + .toggle-track {
          background: rgba(255,0,255,0.4);
          border-color: rgba(255,0,255,0.7);
          box-shadow: 0 0 15px rgba(255,0,255,0.5);
        }
        .toggle input:checked + .toggle-track::after {
          transform: translateX(18px);
          background: #fff;
        }

        /* Lang / theme selector pills */
        .pill-group { display: flex; gap: 6px; }
        .pill {
          padding: 7px 16px; border-radius: 8px;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em;
          cursor: pointer; transition: all 160ms;
          border: 1px solid rgba(255,255,255,0.1);
          background: rgba(255,255,255,0.03);
          color: rgba(255,255,255,0.5);
        }
        .pill:hover { color: rgba(255,255,255,0.8); background: rgba(255,255,255,0.06); }
        .pill.active {
          background: rgba(255,0,255,0.22);
          border-color: rgba(255,0,255,0.6);
          color: #fff;
          box-shadow: 0 0 12px rgba(255,0,255,0.3);
        }

        /* ─── Security cards ─────────────────────────── */
        .security-card {
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.07);
          border-radius: 12px;
          padding: 18px 20px;
          margin-bottom: 12px;
          display: flex; align-items: center; justify-content: space-between;
          gap: 16px;
        }
        .security-card.danger {
          border-color: rgba(255,60,60,0.15);
          background: rgba(255,30,30,0.03);
        }
        .security-card-info { flex: 1; }
        .security-card-title {
          font-size: 13px; color: rgba(255,255,255,0.85);
          font-family: 'Chakra Petch', monospace; letter-spacing: 0.03em;
          margin-bottom: 4px;
        }
        .security-card-desc {
          font-size: 11px; color: rgba(255,255,255,0.3); letter-spacing: 0.03em;
        }

        .session-tag {
          font-size: 9px; padding: 3px 10px; border-radius: 20px;
          background: rgba(0,200,100,0.12); border: 1px solid rgba(0,200,100,0.25);
          color: rgba(0,220,110,0.8); letter-spacing: 0.08em;
          font-family: 'Chakra Petch', monospace;
          white-space: nowrap;
        }

        .btn-danger {
          display: flex; align-items: center; gap: 7px;
          padding: 9px 18px; border-radius: 10px;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;
          cursor: pointer; transition: all 160ms;
          background: rgba(255,60,60,0.08);
          border: 1px solid rgba(255,60,60,0.2);
          color: rgba(255,100,100,0.8);
          white-space: nowrap;
        }
        .btn-danger:hover {
          background: rgba(255,60,60,0.14);
          border-color: rgba(255,60,60,0.4);
          color: rgba(255,120,120,0.9);
        }

        /* ─── Socials editing ────────────────────────── */
        .socials-edit-section {
          margin-top: 20px;
        }
        .social-edit-item {
          display: flex; align-items: center; gap: 12px;
          padding: 12px 16px; border-radius: 10px;
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.08);
          margin-bottom: 10px;
        }
        .social-platform-select {
          width: 120px; flex-shrink: 0;
          padding: 8px 12px; border-radius: 8px;
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.1);
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 12px; outline: none; cursor: pointer;
          appearance: none;
          background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='10' height='6' viewBox='0 0 10 6'%3E%3Cpath d='M1 1l4 4 4-4' stroke='rgba(255,255,255,0.4)' stroke-width='1.2' fill='none' stroke-linecap='round'/%3E%3C/svg%3E");
          background-repeat: no-repeat;
          background-position: right 8px center;
          padding-right: 28px;
        }
        .social-link-input {
          flex: 1;
          padding: 8px 12px; border-radius: 8px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.1);
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 12px; outline: none;
          transition: border-color 180ms, box-shadow 180ms;
        }
        .social-link-input:focus {
          border-color: rgba(255,0,255,0.6);
          box-shadow: 0 0 0 2px rgba(255,0,255,0.08);
        }
        .social-remove-btn {
          padding: 6px; border-radius: 6px;
          background: rgba(255,60,60,0.1);
          border: 1px solid rgba(255,60,60,0.2);
          color: rgba(255,80,80,0.8);
          cursor: pointer; transition: all 160ms;
          display: flex; align-items: center; justify-content: center;
        }
        .social-remove-btn:hover {
          background: rgba(255,60,60,0.15);
          color: rgba(255,100,100,0.9);
        }
        .add-social-btn {
          display: flex; align-items: center; gap: 8px;
          padding: 10px 16px; border-radius: 10px;
          background: rgba(255,0,255,0.08);
          border: 1px solid rgba(255,0,255,0.2);
          color: rgba(255,0,255,0.8);
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em;
          cursor: pointer; transition: all 160ms;
          text-transform: uppercase;
        }
        .add-social-btn:hover {
          background: rgba(255,0,255,0.12);
          border-color: rgba(255,0,255,0.4);
          color: rgba(255,0,255,0.95);
        }
        .add-social-btn:disabled {
          opacity: 0.4; cursor: not-allowed;
        }

        /* ─── Avatar editing ─────────────────────────── */
        .avatar-edit-section {
          display: flex; align-items: center; gap: 20px;
          padding: 16px 20px; border-radius: 12px;
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.06);
          margin-bottom: 20px;
        }
        .avatar-preview {
          width: 80px; height: 80px; border-radius: 50%;
          background: rgba(255,0,255,0.1);
          border: 2px solid rgba(255,0,255,0.3);
          display: flex; align-items: center; justify-content: center;
          overflow: hidden; position: relative;
          box-shadow: 0 0 20px rgba(255,0,255,0.15);
        }
        .avatar-preview img {
          width: 100%; height: 100%; object-fit: cover;
        }
        .avatar-controls {
          flex: 1; display: flex; flex-direction: column; gap: 12px;
        }
        .avatar-mode-pills {
          display: flex; gap: 8px;
        }
        .avatar-mode-pill {
          padding: 6px 14px; border-radius: 8px;
          font-family: 'Chakra Petch', monospace;
          font-size: 10px; letter-spacing: 0.08em;
          text-transform: uppercase;
          cursor: pointer; transition: all 160ms;
          border: 1px solid rgba(255,255,255,0.1);
          background: rgba(255,255,255,0.03);
          color: rgba(255,255,255,0.5);
        }
        .avatar-mode-pill.active {
          background: rgba(255,0,255,0.15);
          border-color: rgba(255,0,255,0.4);
          color: rgba(255,0,255,0.9);
        }
        .avatar-url-input {
          padding: 10px 14px; border-radius: 8px;
          background: rgba(255,255,255,0.03);
          border: 1px solid rgba(255,255,255,0.1);
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 12px; outline: none;
          transition: border-color 180ms, box-shadow 180ms;
        }
        .avatar-url-input:focus {
          border-color: rgba(255,0,255,0.6);
          box-shadow: 0 0 0 3px rgba(255,0,255,0.08);
        }
        .avatar-file-input {
          display: none;
        }
        .avatar-file-btn {
          display: flex; align-items: center; gap: 8px;
          padding: 10px 16px; border-radius: 8px;
          background: rgba(255,255,255,0.05);
          border: 1px solid rgba(255,255,255,0.15);
          color: rgba(255,255,255,0.7);
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.06em;
          cursor: pointer; transition: all 160ms;
          text-transform: uppercase;
        }
        .avatar-file-btn:hover {
          background: rgba(255,255,255,0.08);
          color: #fff;
        }
        .meta-strip {
          display: flex; gap: 24px; flex-wrap: wrap;
          padding: 16px 20px;
          background: rgba(255,255,255,0.02);
          border: 1px solid rgba(255,255,255,0.06);
          border-radius: 12px;
          margin-top: 28px;
        }
        .meta-item { display: flex; flex-direction: column; gap: 4px; }
        .meta-label {
          font-size: 9px; letter-spacing: 0.2em; text-transform: uppercase;
          color: rgba(255,0,255,0.7); font-family: 'Chakra Petch', monospace;
          text-shadow: 0 0 6px rgba(255,0,255,0.3);
        }
        .meta-value {
          font-size: 12px; color: rgba(255,255,255,0.85); letter-spacing: 0.02em;
          text-shadow: 0 0 8px rgba(255,255,255,0.1);
        }

        @media (max-width: 768px) {
          .profile-panel { flex-direction: column; min-height: auto; }
          .profile-sidebar {
            width: 100%; border-right: none;
            border-bottom: 1px solid rgba(255,255,255,0.06);
            padding: 20px 0 12px;
          }
          .profile-user-block { flex-direction: row; align-items: center; padding: 0 16px 16px; }
          .profile-tabs { flex-direction: row; padding: 0 10px; }
          .profile-tab span { display: none; }
          .profile-content { padding: 24px 20px; }
          .field-grid { grid-template-columns: 1fr; }
          .profile-quick-grid { grid-template-columns: 1fr; }
          .league-account-list { grid-template-columns: 1fr; }
          .league-link-grid { grid-template-columns: 1fr; }
          .league-challenge { grid-template-columns: 54px minmax(0, 1fr); }
          .league-challenge .btn { grid-column: 1 / -1; }
          .field-group.span2 { grid-column: auto; }
        }
      `}</style>

            <PageShell lang={lang} onLangChange={setLang}>
                <div className="profile-page">
                    <div className="profile-panel">

                        {/* ── Left Sidebar ── */}
                        <aside className="profile-sidebar">
                            <div className="profile-user-block">
                                <div className="profile-avatar-wrap" onClick={() => {
                                    setForm(f => ({ ...f, avatar: user.avatar ?? '' }))
                                    setEditingAvatar(true)
                                }} style={{ cursor: 'pointer' }}>
                                    <div className="profile-avatar">
                                        {user.avatar
                                            ? <img src={user.avatar} alt="" />
                                            : <FiUser size={28} />
                                        }
                                    </div>
                                    <div className="profile-avatar-ring" />
                                    <div className="profile-avatar-edit-hint">
                                        <FiEdit2 size={12} />
                                    </div>
                                </div>
                                <div className="profile-user-name">{user.nickname}</div>
                                <div className="profile-user-email">{user.email}</div>
                                <div className="profile-badge">{user.user_type}</div>
                            </div>

                            <nav className="profile-tabs" role="tablist">
                                {TABS.map(tab => (
                                    <button
                                        key={tab.id}
                                        role="tab"
                                        aria-selected={activeTab === tab.id}
                                        className={`profile-tab${activeTab === tab.id ? ' active' : ''}`}
                                        onClick={() => setActiveTab(tab.id)}
                                    >
                                        <tab.icon size={15} />
                                        <span>{t[tab.labelKey]}</span>
                                        {activeTab === tab.id && <div className="profile-tab-dot" />}
                                    </button>
                                ))}
                            </nav>

                            <div className="profile-sidebar-bottom">
                                <button className="profile-logout-btn" onClick={logout}>
                                    <FiLogOut size={14} />
                                    <span>{t.logoutCurrent}</span>
                                </button>
                            </div>
                        </aside>

                        {/* ── Content ── */}
                        <main className="profile-content" key={activeTab}>

                            {/* ── PROFILE TAB ── */}
                            {activeTab === 'profile' && (
                                <>
                                    <div className="content-header">
                                        <div>
                                            <div className="content-title">{t.profile}</div>
                                            <div className="content-subtitle">
                                                {editing
                                                    ? (lang === 'ru' ? 'Редактирование данных' : 'Editing your info')
                                                    : (lang === 'ru' ? 'Ваши личные данные' : 'Your personal information')
                                                }
                                            </div>
                                        </div>
                                        {saveSuccess && (
                                            <div className="save-success">
                                                <FiCheck size={13} /> {t.saveSuccess}
                                            </div>
                                        )}
                                    </div>

                                    {!editing && !editingSocials && !editingAvatar ? (
                                        <>
                                            <div className="field-grid">
                                                <div className="field-group span2">
                                                    <div className="profile-quick-grid">
                                                        <div className="profile-quick-card">
                                                            <span className="profile-quick-label">{t.leagueAccounts}</span>
                                                            <span className="profile-quick-value">{user.league_accounts?.length ?? 0}</span>
                                                        </div>
                                                        <div className="profile-quick-card">
                                                            <span className="profile-quick-label">{t.socials}</span>
                                                            <span className="profile-quick-value">{Object.keys(user.socials ?? {}).length}</span>
                                                        </div>
                                                        <div className="profile-quick-card">
                                                            <span className="profile-quick-label">{t.memberSince}</span>
                                                            <span className="profile-quick-value">{joinDate}</span>
                                                        </div>
                                                    </div>
                                                </div>
                                                <div className="field-group">
                                                    <span className="field-label">{t.nickname}</span>
                                                    <span className="field-value">{user.nickname}</span>
                                                </div>
                                                <div className="field-group">
                                                    <span className="field-label">{t.email}</span>
                                                    <span className="field-value">{user.email}</span>
                                                </div>
                                                <div className="field-group">
                                                    <span className="field-label">{t.gender}</span>
                                                    <span className={`field-value${!user.gender ? ' empty' : ''}`}>
                                                        {user.gender ? t[user.gender] : t.noData}
                                                    </span>
                                                </div>
                                                <div className="field-group">
                                                    <span className="field-label">{t.birthday}</span>
                                                    <span className={`field-value${!user.birth_date ? ' empty' : ''}`}>
                                                        {user.birth_date ? user.birth_date.day : t.noData}
                                                    </span>
                                                </div>
                                                <div className="field-group span2">
                                                    <span className="field-label">{t.bio}</span>
                                                    <span className={`field-value${!user.bio ? ' empty' : ''}`}>
                                                        {user.bio || t.noData}
                                                    </span>
                                                </div>
                                            </div>

                                            <div className="section-divider" />
                                            <div className="section-title">
                                                <FiLink size={11} style={{ marginRight: 6, verticalAlign: 'middle' }} />
                                                {t.socials}
                                            </div>
                                            {user.socials && Object.keys(user.socials).length > 0 ? (
                                                <div className="socials-list">
                                                    {Object.entries(user.socials).map(([platform, data]) => (
                                                        <div key={platform} className="social-chip">
                                                            <div
                                                                className="social-dot"
                                                                style={{ background: PLATFORM_COLORS[platform] ?? 'rgba(255,255,255,0.3)' }}
                                                            />
                                                            <span style={{ color: 'rgba(255,255,255,0.4)', marginRight: 2 }}>
                                                                {PLATFORM_LABELS[platform] || platform}
                                                            </span>
                                                            {data.link}
                                                        </div>
                                                    ))}
                                                </div>
                                            ) : (
                                                <div className="field-value empty">{t.noData}</div>
                                            )}

                                            <div className="section-divider" />
                                            <div className="section-title">
                                                <FiShield size={11} style={{ marginRight: 6, verticalAlign: 'middle' }} />
                                                {t.leagueAccounts}
                                            </div>

                                            {user.league_accounts && user.league_accounts.length > 0 ? (
                                                <div className="league-account-list">
                                                    {user.league_accounts.map((account) => (
                                                        <div
                                                            key={`${account.server}:${account.username}:${account.tagline}`}
                                                            className="league-account-item"
                                                        >
                                                            {account.profile_image_url ? (
                                                                <img
                                                                    className="league-account-icon"
                                                                    src={account.profile_image_url}
                                                                    alt=""
                                                                />
                                                            ) : (
                                                                <div className="league-account-icon" />
                                                            )}
                                                            <div className="league-account-main">
                                                                <span className="league-account-name">
                                                                    {account.username}#{account.tagline}
                                                                </span>
                                                                <span className="league-account-meta">
                                                                    {account.server}
                                                                </span>
                                                                <div className="league-rank-row">
                                                                    {account.solo_tier_image_url && (
                                                                        <img
                                                                            className="league-rank-icon"
                                                                            src={account.solo_tier_image_url}
                                                                            alt=""
                                                                        />
                                                                    )}
                                                                    <div>
                                                                        <div className="league-rank-text">
                                                                            {formatRank(account)}
                                                                        </div>
                                                                        {account.solo_tier && (
                                                                            <div className="league-rank-lp">
                                                                                Solo/Duo
                                                                            </div>
                                                                        )}
                                                                    </div>
                                                                </div>
                                                                <span className="league-status">{account.status}</span>
                                                            </div>
                                                        </div>
                                                    ))}
                                                </div>
                                            ) : (
                                                <div className="field-value empty">{t.linkedAccountsEmpty}</div>
                                            )}

                                            <div className="league-link-grid">
                                                <div className="field-group">
                                                    <label className="field-label" htmlFor="lol-server">{t.server}</label>
                                                    <input
                                                        id="lol-server"
                                                        className="field-input"
                                                        value={lolForm.server}
                                                        onChange={(e) => setLolForm(f => ({ ...f, server: e.target.value }))}
                                                        placeholder="na"
                                                    />
                                                </div>
                                                <div className="field-group">
                                                    <label className="field-label" htmlFor="lol-name">{t.riotName}</label>
                                                    <input
                                                        id="lol-name"
                                                        className="field-input"
                                                        value={lolForm.username}
                                                        onChange={(e) => setLolForm(f => ({ ...f, username: e.target.value }))}
                                                        placeholder="HandOfTheCouncil"
                                                    />
                                                </div>
                                                <div className="field-group">
                                                    <label className="field-label" htmlFor="lol-tagline">{t.tagline}</label>
                                                    <input
                                                        id="lol-tagline"
                                                        className="field-input"
                                                        value={lolForm.tagline}
                                                        onChange={(e) => setLolForm(f => ({ ...f, tagline: e.target.value }))}
                                                        placeholder="NA1"
                                                    />
                                                </div>
                                            </div>

                                            <div className="action-row" style={{ marginTop: 12 }}>
                                                <button
                                                    className="btn"
                                                    disabled={
                                                        startLolVerification.isPending ||
                                                        !lolForm.server.trim() ||
                                                        !lolForm.username.trim() ||
                                                        !lolForm.tagline.trim()
                                                    }
                                                    onClick={handleStartLolVerification}
                                                >
                                                    <FiLink size={13} /> {startLolVerification.isPending ? '...' : t.checkAccount}
                                                </button>
                                            </div>

                                            {lolChallenge && (
                                                <div className="league-challenge">
                                                    <img src={lolChallenge.target_profile_image_url} alt="" />
                                                    <div className="league-challenge-text">
                                                        <div>{t.verificationReady}</div>
                                                        <div>
                                                            <span className="league-icon-number">{t.targetIcon}</span>
                                                        </div>
                                                    </div>
                                                    <button
                                                        className="btn primary"
                                                        disabled={finishLolVerification.isPending}
                                                        onClick={handleFinishLolVerification}
                                                    >
                                                        <FiCheck size={13} /> {finishLolVerification.isPending ? '...' : t.confirmAccount}
                                                    </button>
                                                </div>
                                            )}

                                            {lolError && <div className="form-error">{lolError}</div>}
                                            {lolSuccess && (
                                                <div className="form-success">
                                                    {lang === 'ru' ? 'League аккаунт привязан' : 'League account linked'}
                                                </div>
                                            )}

                                            <div className="action-row">
                                                <button className="btn primary" onClick={() => {
                                                    setForm({
                                                        nickname: user.nickname,
                                                        bio: user.bio ?? '',
                                                        gender: user.gender ?? '',
                                                        avatar: user.avatar ?? '',
                                                        socials: user.socials ?? {},
                                                    })
                                                    setEditing(true)
                                                }}>
                                                    <FiEdit2 size={13} /> {t.edit}
                                                </button>
                                                <button className="btn" onClick={() => {
                                                    setForm(f => ({
                                                        ...f,
                                                        socials: user.socials ?? {},
                                                    }))
                                                    setEditingSocials(true)
                                                }}>
                                                    <FiLink size={13} /> {t.editSocials}
                                                </button>
                                                {!onboarded && (
                                                    <button className="btn" onClick={() => navigate({ to: '/onboarding' })}>
                                                        {t.completeSetup}
                                                    </button>
                                                )}
                                            </div>
                                        </>
                                    ) : editing ? (
                                        <>
                                            <div className="field-grid">
                                                <div className="field-group">
                                                    <label className="field-label" htmlFor="f-nickname">{t.nickname}</label>
                                                    <div className="field-input-wrap">
                                                        <input
                                                            id="f-nickname"
                                                            className="field-input"
                                                            value={form.nickname}
                                                            onChange={e => setForm(f => ({ ...f, nickname: e.target.value }))}
                                                            placeholder={t.nickname}
                                                        />
                                                    </div>
                                                </div>
                                                <div className="field-group">
                                                    <label className="field-label" htmlFor="f-gender">{t.gender}</label>
                                                    <select
                                                        id="f-gender"
                                                        className="field-select"
                                                        value={form.gender}
                                                        onChange={e => setForm(f => ({ ...f, gender: e.target.value }))}
                                                    >
                                                        <option value="">—</option>
                                                        <option value="MALE">{t.male}</option>
                                                        <option value="FEMALE">{t.female}</option>
                                                    </select>
                                                </div>
                                                <div className="field-group span2">
                                                    <label className="field-label" htmlFor="f-bio">{t.bio}</label>
                                                    <textarea
                                                        id="f-bio"
                                                        className="field-input"
                                                        value={form.bio}
                                                        onChange={e => setForm(f => ({ ...f, bio: e.target.value }))}
                                                        placeholder={lang === 'ru' ? 'Расскажите о себе…' : 'Tell something about yourself…'}
                                                    />
                                                </div>
                                            </div>

                                            <div className="action-row">
                                                <button
                                                    className="btn primary"
                                                    disabled={updateProfile.isPending}
                                                    onClick={handleSave}
                                                >
                                                    <FiSave size={13} /> {t.save}
                                                </button>
                                                <button className="btn" onClick={() => setEditing(false)}>
                                                    <FiX size={13} /> {t.cancel}
                                                </button>
                                            </div>
                                        </>
                                    ) : editingAvatar ? (
                                        <>
                                            <div className="section-title">
                                                <FiImage size={11} style={{ marginRight: 6, verticalAlign: 'middle' }} />
                                                {t.changeAvatar}
                                            </div>

                                            <div className="avatar-edit-section">
                                                <div className="avatar-preview">
                                                    {form.avatar ? (
                                                        <img src={form.avatar} alt="" />
                                                    ) : (
                                                        <FiUser size={32} />
                                                    )}
                                                </div>

                                                <div className="avatar-controls">
                                                    <input
                                                        className="avatar-url-input"
                                                        value={form.avatar}
                                                        onChange={(e) => setForm(f => ({ ...f, avatar: e.target.value }))}
                                                        placeholder={t.avatarUrlPlaceholder}
                                                    />
                                                </div>
                                            </div>

                                            <div className="action-row">
                                                <button
                                                    className="btn primary"
                                                    disabled={updateProfile.isPending}
                                                    onClick={handleSave}
                                                >
                                                    <FiSave size={13} /> {t.save}
                                                </button>
                                                <button className="btn" onClick={() => setEditingAvatar(false)}>
                                                    <FiX size={13} /> {t.cancel}
                                                </button>
                                            </div>
                                        </>
                                    ) : editingSocials ? (
                                        <>
                                            <div className="section-title">
                                                <FiLink size={11} style={{ marginRight: 6, verticalAlign: 'middle' }} />
                                                {t.editSocials}
                                            </div>

                                            <div className="socials-edit-section">
                                                {Object.entries(form.socials).map(([platform, data]) => (
                                                    <div key={platform} className="social-edit-item">
                                                        <select
                                                            className="social-platform-select"
                                                            value={platform}
                                                            onChange={(e) => {
                                                                if (e.target.value === platform) return
                                                                const newSocials = { ...form.socials }
                                                                newSocials[e.target.value] = data
                                                                delete newSocials[platform]
                                                                setForm(f => ({ ...f, socials: newSocials }))
                                                            }}
                                                        >
                                                            {PLATFORM_OPTIONS.map(opt => (
                                                                <option key={opt.value} value={opt.value} disabled={form.socials[opt.value] && opt.value !== platform}>
                                                                    {opt.label}
                                                                </option>
                                                            ))}
                                                        </select>
                                                        <input
                                                            className="social-link-input"
                                                            value={data.link}
                                                            onChange={(e) => updateSocial(platform, e.target.value)}
                                                            placeholder={lang === 'ru' ? 'Ссылка или никнейм' : 'Link or username'}
                                                        />
                                                        <button
                                                            className="social-remove-btn"
                                                            onClick={() => removeSocial(platform)}
                                                            type="button"
                                                        >
                                                            <FiTrash2 size={14} />
                                                        </button>
                                                    </div>
                                                ))}

                                                <button
                                                    className="add-social-btn"
                                                    onClick={addSocial}
                                                    disabled={Object.keys(form.socials).length >= PLATFORM_OPTIONS.length}
                                                >
                                                    <FiPlus size={12} /> {t.addSocial}
                                                </button>
                                            </div>

                                            <div className="action-row">
                                                <button
                                                    className="btn primary"
                                                    disabled={updateProfile.isPending}
                                                    onClick={handleSave}
                                                >
                                                    <FiSave size={13} /> {t.save}
                                                </button>
                                                <button className="btn" onClick={() => setEditingSocials(false)}>
                                                    <FiX size={13} /> {t.cancel}
                                                </button>
                                            </div>
                                        </>
                                    ) : (
                                        <>
                                            {/* Эта секция уже обработана выше */}
                                        </>
                                    )}

                                    <div className="meta-strip">
                                        <div className="meta-item">
                                            <span className="meta-label">
                                                <FiCalendar size={8} style={{ marginRight: 4, verticalAlign: 'middle' }} />
                                                {t.memberSince}
                                            </span>
                                            <span className="meta-value">{joinDate}</span>
                                        </div>
                                        <div className="meta-item">
                                            <span className="meta-label">{t.accountType}</span>
                                            <span className="meta-value" style={{ textTransform: 'capitalize' }}>
                                                {user.user_type?.toLowerCase()}
                                            </span>
                                        </div>
                                    </div>
                                </>
                            )}

                            {/* ── SETTINGS TAB ── */}
                            {activeTab === 'settings' && (
                                <>
                                    <div className="content-header">
                                        <div>
                                            <div className="content-title">{t.settings}</div>
                                            <div className="content-subtitle">
                                                {lang === 'ru' ? 'Настройки интерфейса и аккаунта' : 'Interface and account preferences'}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="section-title">{t.lang}</div>
                                    <div className="setting-row">
                                        <div className="setting-info">
                                            <div className="setting-name">{t.lang}</div>
                                            <div className="setting-desc">
                                                {lang === 'ru' ? 'Язык отображения интерфейса' : 'Display language for the interface'}
                                            </div>
                                        </div>
                                        <div className="pill-group">
                                            <button
                                                className={`pill${lang === 'en' ? ' active' : ''}`}
                                                onClick={() => setLang('en')}
                                            >
                                                {t.langEn}
                                            </button>
                                            <button
                                                className={`pill${lang === 'ru' ? ' active' : ''}`}
                                                onClick={() => setLang('ru')}
                                            >
                                                {t.langRu}
                                            </button>
                                        </div>
                                    </div>

                                    <div className="section-divider" />
                                    <div className="section-title">{t.notifSection}</div>
                                    <div className="setting-row">
                                        <div className="setting-info">
                                            <div className="setting-name">{t.notifEmail}</div>
                                            <div className="setting-desc">{t.notifDesc}</div>
                                        </div>
                                        <label className="toggle">
                                            <input
                                                type="checkbox"
                                                checked={notifEmail}
                                                onChange={e => setNotifEmail(e.target.checked)}
                                            />
                                            <div className="toggle-track" />
                                        </label>
                                    </div>

                                    <div className="section-divider" />
                                    <div className="section-title">{t.theme}</div>
                                    <div className="setting-row">
                                        <div className="setting-info">
                                            <div className="setting-name">{t.theme}</div>
                                            <div className="setting-desc">{t.themeDesc}</div>
                                        </div>
                                        <div className="pill-group">
                                            <button className="pill active">{t.dark}</button>
                                            <button className="pill" style={{ opacity: 0.4, cursor: 'not-allowed' }}>
                                                {t.light}
                                            </button>
                                        </div>
                                    </div>
                                </>
                            )}

                            {/* ── SECURITY TAB ── */}
                            {activeTab === 'security' && (
                                <>
                                    <div className="content-header">
                                        <div>
                                            <div className="content-title">{t.security}</div>
                                            <div className="content-subtitle">
                                                {lang === 'ru' ? 'Управление доступом и сессиями' : 'Access management and sessions'}
                                            </div>
                                        </div>
                                    </div>

                                    <div className="section-title">{t.sessionSection}</div>
                                    <div className="security-card">
                                        <div className="security-card-info">
                                            <div className="security-card-title">
                                                {lang === 'ru' ? 'Текущий браузер' : 'Current browser'}
                                            </div>
                                            <div className="security-card-desc">
                                                {typeof navigator !== 'undefined'
                                                    ? navigator.userAgent.split(')')[0].split('(')[1] ?? '—'
                                                    : '—'
                                                }
                                            </div>
                                        </div>
                                        <span className="session-tag">{t.currentSession}</span>
                                    </div>

                                    <div className="section-divider" />
                                    <div className="section-title">
                                        {lang === 'ru' ? 'Действия' : 'Actions'}
                                    </div>

                                    <div className="security-card">
                                        <div className="security-card-info">
                                            <div className="security-card-title">{t.twoFactor}</div>
                                            <div className="security-card-desc">{t.twoFactorDesc}</div>
                                        </div>
                                        <button className="btn" style={{ opacity: 0.5, cursor: 'not-allowed' }}>
                                            <FiShield size={13} /> {t.enable}
                                        </button>
                                    </div>

                                    <div className="security-card danger">
                                        <div className="security-card-info">
                                            <div className="security-card-title">{t.logoutAll}</div>
                                            <div className="security-card-desc">
                                                {lang === 'ru'
                                                    ? 'Завершить все активные сессии на других устройствах'
                                                    : 'Terminate all active sessions on other devices'
                                                }
                                            </div>
                                        </div>
                                        <button className="btn-danger" onClick={logout}>
                                            <FiLogOut size={13} /> {t.logoutAll}
                                        </button>
                                    </div>

                                    <div className="security-card danger">
                                        <div className="security-card-info">
                                            <div className="security-card-title">
                                                {lang === 'ru' ? 'Удалить аккаунт' : 'Delete account'}
                                            </div>
                                            <div className="security-card-desc">
                                                {lang === 'ru'
                                                    ? 'Необратимое удаление всех данных аккаунта'
                                                    : 'Permanently delete all account data'
                                                }
                                            </div>
                                        </div>
                                        <button
                                            className="btn-danger"
                                            style={{ opacity: 0.45, cursor: 'not-allowed' }}
                                        >
                                            <FiAlertCircle size={13} />
                                            {lang === 'ru' ? 'Удалить' : 'Delete'}
                                        </button>
                                    </div>
                                </>
                            )}

                        </main>
                    </div>
                </div>
            </PageShell>
        </>
    )
}
