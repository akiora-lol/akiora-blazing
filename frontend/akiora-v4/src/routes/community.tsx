import { createFileRoute } from '@tanstack/react-router'
import { useState } from 'react'
import { FiExternalLink, FiSearch, FiUsers, FiShield, FiPlus, FiUser, FiTag, FiUserPlus, FiX } from 'react-icons/fi'
import { PageShell } from '../components/PageShell'
import {
  useCommunityUsers,
  useCommunityClubs,
  useCommunityTeams,
  useCreateClubMutation,
  useCreateTeamMutation,
  useJoinClubMutation,
  useSendFriendRequestMutation,
  type AuthUser,
  type ClubResponse,
  type TeamResponse
} from '../lib/api'
import { useAuthContext } from '../contexts/AuthContext'

export const Route = createFileRoute('/community')({
  component: CommunityPage,
})

const T = {
  en: {
    eyebrow: 'Community',
    title: 'CONNECT',
    subtitle: 'Find teammates, join clubs, dominate together',
    searchPlaceholder: 'Search players by nickname...',
    users: 'Players',
    clubs: 'Clubs',
    teams: 'Teams',
    create: 'Create',
    noResults: 'No results found',
    loading: 'Loading...',
    members: 'members',
    joinClub: 'Join Club',
    applyTeam: 'Apply to Team',
    createClub: 'Create Club',
    createTeam: 'Create Team',
    clubName: 'Club name',
    teamName: 'Team name',
    teamTag: 'Team tag',
    tagPlaceholder: 'e.g., AKIRA',
    maxChars: 'Maximum 5 characters',
    creating: 'Creating...',
    loginRequired: 'Login to join',
    loginToCreate: 'Login to create clubs and teams',
    addFriend: 'Add friend',
    openProfile: 'Open profile',
    preview: 'Preview',
    friendRequestSent: 'Friend request sent',
    previous50: 'Previous 50',
    next50: 'Next 50',
    page: 'Page',
  },
  ru: {
    eyebrow: 'Сообщество',
    title: 'ОБЪЕДИНЯЙСЯ',
    subtitle: 'Находи союзников, вступай в клубы, доминируй вместе',
    searchPlaceholder: 'Поиск игроков по nickname...',
    users: 'Игроки',
    clubs: 'Клубы',
    teams: 'Команды',
    create: 'Создать',
    noResults: 'Ничего не найдено',
    loading: 'Загрузка...',
    members: 'участников',
    joinClub: 'Вступить',
    applyTeam: 'Подать заявку',
    createClub: 'Создать клуб',
    createTeam: 'Создать команду',
    clubName: 'Название клуба',
    teamName: 'Название команды',
    teamTag: 'Тег команды',
    tagPlaceholder: 'например: AKIRA',
    maxChars: 'Максимум 5 символов',
    creating: 'Создание...',
    loginRequired: 'Войдите для участия',
    loginToCreate: 'Войдите для создания клубов и команд',
    addFriend: 'Добавить',
    openProfile: 'Профиль',
    preview: 'Превью',
    friendRequestSent: 'Заявка отправлена',
    previous50: 'Предыдущие 50',
    next50: 'Следующие 50',
    page: 'Страница',
  },
} as const

type Lang = keyof typeof T
const PAGE_SIZE = 50

interface TabType {
  id: 'users' | 'clubs' | 'teams' | 'create'
  icon: React.ComponentType<{ size: number }>
  labelKey: keyof typeof T['en']
}

const tabs: TabType[] = [
  { id: 'users', icon: FiUser, labelKey: 'users' },
  { id: 'clubs', icon: FiShield, labelKey: 'clubs' },
  { id: 'teams', icon: FiUsers, labelKey: 'teams' },
  { id: 'create', icon: FiPlus, labelKey: 'create' },
]

interface PaginationControlsProps {
  page: number
  hasNext?: boolean
  totalCount?: number
  isFetching?: boolean
  labels: typeof T[Lang]
  onPageChange: (page: number) => void
}

function PaginationControls({ page, hasNext, totalCount, isFetching, labels, onPageChange }: PaginationControlsProps) {
  const from = totalCount && totalCount > 0 ? (page - 1) * PAGE_SIZE + 1 : 0
  const to = totalCount ? Math.min(page * PAGE_SIZE, totalCount) : page * PAGE_SIZE

  return (
    <div className="pagination-row">
      <button
        className="btn"
        disabled={page <= 1 || isFetching}
        onClick={() => onPageChange(Math.max(1, page - 1))}
      >
        {labels.previous50}
      </button>
      <div className="pagination-meta">
        {labels.page} {page}
        {typeof totalCount === 'number' && totalCount > 0 ? ` · ${from}-${to} / ${totalCount}` : ''}
      </div>
      <button
        className="btn btn-primary"
        disabled={!hasNext || isFetching}
        onClick={() => onPageChange(page + 1)}
      >
        {isFetching ? labels.loading : labels.next50}
      </button>
    </div>
  )
}

function CommunityPage() {
  const [lang, setLang] = useState<Lang>('ru')
  const { user: currentUser, isAuthenticated } = useAuthContext()
  const [activeTab, setActiveTab] = useState<TabType['id']>('users')
  const [previewUser, setPreviewUser] = useState<AuthUser | null>(null)
  const [friendSentIds, setFriendSentIds] = useState<Set<string>>(new Set())
  const [searchQuery, setSearchQuery] = useState('')
  const [usersPage, setUsersPage] = useState(1)
  const [clubsPage, setClubsPage] = useState(1)
  const [teamsPage, setTeamsPage] = useState(1)
  const [createType, setCreateType] = useState<'club' | 'team'>('club')
  const [createName, setCreateName] = useState('')
  const [createTag, setCreateTag] = useState('')
  const t = T[lang]

  // Queries
  const { data: usersResponse, isLoading: isLoadingUsers, isFetching: isFetchingUsers } = useCommunityUsers(usersPage, searchQuery, PAGE_SIZE)
  const { data: clubsResponse, isLoading: isLoadingClubs, isFetching: isFetchingClubs } = useCommunityClubs(clubsPage, PAGE_SIZE)
  const { data: teamsResponse, isLoading: isLoadingTeams, isFetching: isFetchingTeams } = useCommunityTeams(teamsPage, PAGE_SIZE)
  const users = usersResponse?.users ?? []
  const clubs = clubsResponse?.clubs ?? []
  const teams = teamsResponse?.teams ?? []

  // Mutations
  const createClubMutation = useCreateClubMutation()
  const createTeamMutation = useCreateTeamMutation()
  const joinClubMutation = useJoinClubMutation()
  const sendFriendMutation = useSendFriendRequestMutation()

  const handleCreateSubmit = () => {
    if (!createName.trim()) return

    if (createType === 'club') {
      if (!currentUser) return
      createClubMutation.mutate({
        owner_id: currentUser.id,
        name: createName
      }, {
        onSuccess: () => {
          setCreateName('')
        }
      })
    } else {
      if (!createTag.trim()) return
      if (!currentUser) return
      createTeamMutation.mutate({
        owner_id: currentUser.id,
        name: createName,
        tag: createTag
      }, {
        onSuccess: () => {
          setCreateName('')
          setCreateTag('')
        }
      })
    }
  }

  const handleJoinClub = (clubId: string) => {
    if (!currentUser) return
    joinClubMutation.mutate({ clubId, userId: currentUser.id })
  }

  const handleSendFriendRequest = (targetUser: AuthUser) => {
    if (!currentUser || targetUser.id === currentUser.id) return
    sendFriendMutation.mutate(
      { senderId: currentUser.id, receiverId: targetUser.id },
      {
        onSuccess: () => {
          setFriendSentIds((current) => new Set(current).add(targetUser.id))
        },
      },
    )
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
        @keyframes pulse-glow {
          0%, 100% { box-shadow: 0 0 20px rgba(166,0,255,0.3), 0 0 40px rgba(166,0,255,0.1); }
          50%      { box-shadow: 0 0 30px rgba(166,0,255,0.5), 0 0 60px rgba(166,0,255,0.2); }
        }

        .community-scene {
          position: relative; z-index: 10;
          min-height: 100vh;
          padding: 88px 24px 48px;
        }

        .community-header {
          text-align: left; margin: 0 auto 28px;
          max-width: 1200px;
          animation: rise-up 0.6s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.1s;
        }
        .community-eyebrow {
          font-size: 9px; letter-spacing: 0.3em; text-transform: uppercase;
          color: #a600ff; margin-bottom: 12px;
          text-shadow: 0 0 12px rgba(166,0,255,0.6);
        }
        .community-title {
          font-family: 'Russo One', sans-serif;
          font-size: clamp(2.4rem, 6vw, 4rem);
          color: #fff; margin: 0 0 16px;
          text-shadow: 0 0 40px rgba(255,255,255,0.3);
        }
        .community-subtitle {
          font-size: 13px; color: rgba(255,255,255,0.4);
          letter-spacing: 0.02em; line-height: 1.6;
          max-width: 520px; margin: 0;
        }

        /* ─── Navigation Panel ───────────────────────── */
        .community-layout {
          max-width: 1200px;
          margin: 0 auto;
          display: grid;
          grid-template-columns: 220px minmax(0, 1fr);
          gap: 22px;
          align-items: start;
        }
        .nav-panel {
          position: sticky; top: 88px;
          margin: 0;
          background: rgba(0,0,0,0.75);
          border: 1px solid rgba(166,0,255,0.2);
          border-radius: 8px; padding: 8px;
          backdrop-filter: blur(20px);
          box-shadow: 0 0 40px rgba(166,0,255,0.15);
          animation: rise-up 0.6s cubic-bezier(.16,1,.3,1) both;
          animation-delay: 0.2s;
        }
        .nav-tabs {
          display: grid; gap: 6px;
        }
        .nav-tab {
          display: flex; align-items: center; justify-content: flex-start; gap: 10px;
          padding: 12px 14px; border-radius: 6px;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;
          cursor: pointer; transition: all 200ms;
          color: rgba(255,255,255,0.4);
          border: 1px solid transparent;
          background: transparent;
        }
        .nav-tab:hover {
          color: rgba(255,255,255,0.7);
          background: rgba(255,255,255,0.04);
        }
        .nav-tab.active {
          color: #fff;
          background: rgba(166,0,255,0.15);
          border-color: rgba(166,0,255,0.35);
          box-shadow: 0 0 20px rgba(166,0,255,0.2);
        }
        .nav-tab.active svg {
          filter: drop-shadow(0 0 8px rgba(166,0,255,0.8));
          color: #a600ff;
        }
        .nav-tab-count {
          margin-left: auto;
          min-width: 28px;
          height: 22px;
          border-radius: 999px;
          display: inline-flex;
          align-items: center;
          justify-content: center;
          background: rgba(255,255,255,0.08);
          color: rgba(255,255,255,0.62);
          font-size: 10px;
        }

        /* ─── Content Area ────────────────────────────── */
        .content-area {
          min-width: 0;
          margin: 0;
          animation: fade-in 0.5s ease both;
          animation-delay: 0.3s;
        }

        .community-summary {
          margin: 0 0 18px;
          display: grid;
          grid-template-columns: repeat(3, minmax(0, 1fr));
          gap: 12px;
        }
        .community-summary-card {
          border: 1px solid rgba(255,255,255,0.09);
          border-radius: 8px;
          padding: 14px 16px;
          background:
            linear-gradient(135deg, rgba(45,212,191,0.08), rgba(192,132,252,0.06)),
            rgba(0,0,0,0.58);
          backdrop-filter: blur(16px);
        }
        .community-summary-label {
          display: block;
          margin-bottom: 8px;
          color: rgba(255,255,255,0.42);
          font-family: 'Chakra Petch', monospace;
          font-size: 10px;
          letter-spacing: 0.12em;
          text-transform: uppercase;
        }
        .community-summary-value {
          color: #fff;
          font-family: 'Russo One', sans-serif;
          font-size: 24px;
          letter-spacing: 0;
        }

        /* ─── Search Section ──────────────────────────── */
        .search-section {
          max-width: 480px; margin: 0 auto 40px;
          position: relative;
        }
        .search-input {
          width: 100%; padding: 16px 20px 16px 50px;
          background: rgba(0,0,0,0.6);
          border: 1px solid rgba(166,0,255,0.25);
          border-radius: 14px;
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 13px; letter-spacing: 0.02em;
          outline: none; transition: all 200ms;
          backdrop-filter: blur(12px);
        }
        .search-input:focus {
          border-color: rgba(166,0,255,0.6);
          box-shadow: 0 0 0 3px rgba(166,0,255,0.15), 0 0 30px rgba(166,0,255,0.3);
        }
        .search-input::placeholder { color: rgba(255,255,255,0.25); }
        .search-icon {
          position: absolute; left: 18px; top: 50%; transform: translateY(-50%);
          color: rgba(166,0,255,0.6);
        }

        /* ─── Grid Layout ─────────────────────────────── */
        .entity-grid {
          display: grid;
          grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
          gap: 20px;
        }

        /* ─── Entity Cards ────────────────────────────── */
        .entity-card {
          background: rgba(0,0,0,0.6);
          border: 1px solid rgba(255,255,255,0.08);
          border-radius: 14px; padding: 20px;
          backdrop-filter: blur(16px);
          transition: all 200ms;
          position: relative; overflow: hidden;
        }
        .entity-card.user-card {
          display: grid;
          grid-template-rows: auto 1fr auto;
          min-height: 210px;
        }
        .entity-avatar img {
          width: 100%; height: 100%; object-fit: cover; border-radius: inherit;
        }
        .entity-card:hover {
          border-color: rgba(166,0,255,0.3);
          box-shadow: 0 0 30px rgba(166,0,255,0.15);
          transform: translateY(-2px);
        }
        .entity-card::before {
          content: ''; position: absolute; top: 0; left: 0; right: 0;
          height: 1px; background: linear-gradient(90deg, transparent, rgba(166,0,255,0.4), transparent);
          opacity: 0; transition: opacity 200ms;
        }
        .entity-card:hover::before { opacity: 1; }

        .entity-header {
          display: flex; align-items: center; gap: 14px; margin-bottom: 14px;
        }
        .entity-avatar {
          width: 48px; height: 48px; border-radius: 12px;
          display: flex; align-items: center; justify-content: center;
          font-family: 'Russo One', sans-serif;
          font-size: 16px; font-weight: bold; color: #fff;
          position: relative;
        }
        .entity-avatar.user {
          background: linear-gradient(135deg, #a600ff, #6600cc);
          border-radius: 50%;
        }
        .entity-avatar.club {
          background: linear-gradient(135deg, #0ea5e9, #3b82f6);
        }
        .entity-avatar.team {
          background: linear-gradient(135deg, #f59e0b, #ef4444);
        }
        .entity-info { flex: 1; }
        .entity-name {
          font-family: 'Russo One', sans-serif;
          font-size: 15px; color: #fff; margin: 0 0 4px;
          letter-spacing: 0.02em;
        }
        .entity-meta {
          font-size: 11px; color: rgba(255,255,255,0.4);
          letter-spacing: 0.02em;
        }
        .entity-bio {
          font-size: 12px; color: rgba(255,255,255,0.6);
          line-height: 1.5; margin-bottom: 16px;
        }

        .entity-footer {
          display: flex; align-items: center; justify-content: space-between;
          gap: 10px; flex-wrap: wrap;
        }
        .entity-tag {
          font-family: 'Chakra Petch', monospace;
          font-size: 10px; letter-spacing: 0.1em; text-transform: uppercase;
          padding: 4px 10px; border-radius: 6px;
          background: rgba(166,0,255,0.12);
          border: 1px solid rgba(166,0,255,0.25);
          color: rgba(166,0,255,0.9);
        }

        /* ─── Action Buttons ──────────────────────────── */
        .btn {
          display: flex; align-items: center; gap: 6px;
          padding: 8px 16px; border-radius: 8px;
          font-family: 'Chakra Petch', monospace;
          font-size: 10px; letter-spacing: 0.08em; text-transform: uppercase;
          cursor: pointer; transition: all 180ms;
          border: 1px solid rgba(255,255,255,0.1);
          background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.7);
        }
        .btn:hover { color: #fff; border-color: rgba(255,255,255,0.25); background: rgba(255,255,255,0.08); }
        .btn:disabled { opacity: 0.4; cursor: not-allowed; transform: none !important; }

        .btn-primary {
          background: linear-gradient(135deg, #a600ff, #6600cc);
          border-color: rgba(166,0,255,0.6); color: #fff;
        }
        .btn-primary:hover {
          box-shadow: 0 0 20px rgba(166,0,255,0.4);
          transform: translateY(-1px);
        }

        .btn-secondary {
          background: rgba(6,182,212,0.1);
          border-color: rgba(6,182,212,0.3);
          color: rgba(6,182,212,0.9);
        }
        .btn-secondary:hover {
          background: rgba(6,182,212,0.15);
          border-color: rgba(6,182,212,0.5);
          color: #06B6D4;
          box-shadow: 0 0 15px rgba(6,182,212,0.3);
        }

        .btn-danger {
          background: rgba(239,68,68,0.1);
          border-color: rgba(239,68,68,0.3);
          color: rgba(239,68,68,0.9);
        }
        .btn-danger:hover {
          background: rgba(239,68,68,0.15);
          border-color: rgba(239,68,68,0.5);
          color: #ef4444;
        }
        .preview-backdrop {
          position: fixed; inset: 0; z-index: 80;
          background: rgba(0,0,0,0.64);
          backdrop-filter: blur(10px);
          display: grid; place-items: center;
          padding: 20px;
        }
        .user-preview {
          width: min(430px, calc(100vw - 40px));
          border: 1px solid rgba(255,255,255,0.12);
          border-radius: 8px;
          background:
            linear-gradient(135deg, rgba(45,212,191,0.1), rgba(166,0,255,0.08)),
            rgba(5,8,18,0.96);
          box-shadow: 0 24px 90px rgba(0,0,0,0.5);
          padding: 18px;
        }
        .user-preview-head {
          display: flex; align-items: center; gap: 14px;
          margin-bottom: 14px;
        }
        .user-preview-close {
          margin-left: auto;
          width: 34px; height: 34px;
          border-radius: 50%;
          border: 1px solid rgba(255,255,255,0.12);
          background: rgba(255,255,255,0.05);
          color: #fff;
          display: grid; place-items: center;
          cursor: pointer;
        }
        .user-preview-name {
          margin: 0 0 4px;
          color: #fff;
          font-family: 'Russo One', sans-serif;
          font-size: 20px;
          letter-spacing: 0;
        }
        .user-preview-email {
          color: rgba(255,255,255,0.42);
          font-size: 11px;
          overflow-wrap: anywhere;
        }
        .user-preview-bio {
          color: rgba(255,255,255,0.68);
          line-height: 1.55;
          font-size: 13px;
          margin: 14px 0;
        }
        .user-preview-actions {
          display: flex;
          gap: 10px;
          flex-wrap: wrap;
        }

        .pagination-row {
          display: flex; align-items: center; justify-content: center; gap: 12px;
          margin-top: 28px; flex-wrap: wrap;
        }
        .pagination-meta {
          min-width: 160px; text-align: center;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.04em;
          color: rgba(255,255,255,0.45);
        }

        /* ─── Loading & Empty States ──────────────────── */
        .loading-state, .empty-state {
          text-align: center; padding: 60px 20px;
          color: rgba(255,255,255,0.4);
        }
        .loading-spinner {
          width: 32px; height: 32px; margin: 0 auto 16px;
          border: 2px solid rgba(166,0,255,0.2);
          border-top: 2px solid #a600ff;
          border-radius: 50%;
          animation: spin 1s linear infinite;
        }
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }

        /* ─── Create Form ─────────────────────────────── */
        .create-section {
          max-width: 600px; margin: 0 auto;
        }
        .type-selector {
          display: flex; gap: 12px; margin-bottom: 32px;
          justify-content: center;
        }
        .type-btn {
          display: flex; align-items: center; gap: 8px;
          padding: 12px 24px; border-radius: 12px;
          font-family: 'Chakra Petch', monospace;
          font-size: 11px; letter-spacing: 0.08em; text-transform: uppercase;
          cursor: pointer; transition: all 200ms;
          border: 1px solid rgba(255,255,255,0.1);
          background: rgba(255,255,255,0.05); color: rgba(255,255,255,0.7);
        }
        .type-btn:hover { color: #fff; background: rgba(255,255,255,0.08); }
        .type-btn.active.club {
          background: rgba(59,130,246,0.15);
          border-color: rgba(59,130,246,0.4);
          color: #3b82f6;
        }
        .type-btn.active.team {
          background: rgba(239,68,68,0.15);
          border-color: rgba(239,68,68,0.4);
          color: #ef4444;
        }

        .create-form {
          background: rgba(0,0,0,0.6);
          border: 1px solid rgba(166,0,255,0.2);
          border-radius: 16px; padding: 32px;
          backdrop-filter: blur(20px);
        }
        .form-group {
          margin-bottom: 20px;
        }
        .form-label {
          display: block; margin-bottom: 8px;
          font-size: 10px; letter-spacing: 0.15em; text-transform: uppercase;
          color: rgba(166,0,255,0.8);
          text-shadow: 0 0 8px rgba(166,0,255,0.4);
        }
        .form-input {
          width: 100%; padding: 14px 18px; border-radius: 10px;
          background: rgba(0,0,0,0.4);
          border: 1px solid rgba(255,255,255,0.1);
          color: #fff; font-family: 'Chakra Petch', monospace;
          font-size: 13px; letter-spacing: 0.02em;
          outline: none; transition: all 200ms;
          box-sizing: border-box;
        }
        .form-input:focus {
          border-color: rgba(166,0,255,0.6);
          box-shadow: 0 0 0 3px rgba(166,0,255,0.15);
          background: rgba(166,0,255,0.05);
        }
        .form-input::placeholder { color: rgba(255,255,255,0.3); }
        .form-hint {
          font-size: 10px; color: rgba(255,255,255,0.4);
          margin-top: 6px; letter-spacing: 0.02em;
        }

        .auth-notice {
          background: rgba(251,191,36,0.1);
          border: 1px solid rgba(251,191,36,0.3);
          border-radius: 12px; padding: 20px;
          text-align: center; color: rgba(251,191,36,0.9);
          font-size: 12px; letter-spacing: 0.02em;
        }

        @media (max-width: 768px) {
          .community-scene { padding: 88px 16px 32px; }
          .community-layout { grid-template-columns: 1fr; }
          .nav-panel { position: static; }
          .nav-tabs { grid-template-columns: repeat(2, minmax(0, 1fr)); gap: 6px; }
          .community-summary { grid-template-columns: 1fr; }
          .nav-tab { padding: 10px 16px; }
          .entity-grid { grid-template-columns: 1fr; }
          .type-selector { flex-direction: column; align-items: center; }
          .entity-footer { flex-direction: column; gap: 8px; align-items: flex-start; }
        }
      `}</style>

      <PageShell lang={lang} onLangChange={setLang} logoVariant="center">
        <div className="community-scene">
          {/* Header */}
          <div className="community-header">
            <div className="community-eyebrow">{t.eyebrow}</div>
            <h1 className="community-title">{t.title}</h1>
            <p className="community-subtitle">{t.subtitle}</p>
          </div>

          <div className="community-layout">
            {/* Navigation */}
            <div className="nav-panel">
              <div className="nav-tabs">
                {tabs.map((tab) => {
                  const count = tab.id === 'users'
                    ? usersResponse?.total_count ?? users.length
                    : tab.id === 'clubs'
                      ? clubsResponse?.total_count ?? clubs.length
                      : tab.id === 'teams'
                        ? teamsResponse?.total_count ?? teams.length
                        : ''
                  return (
                    <button
                      key={tab.id}
                      onClick={() => setActiveTab(tab.id)}
                      className={`nav-tab${activeTab === tab.id ? ' active' : ''}`}
                    >
                      <tab.icon size={14} />
                      {t[tab.labelKey]}
                      {count !== '' && <span className="nav-tab-count">{count}</span>}
                    </button>
                  )
                })}
              </div>
            </div>

            <div>
              <div className="community-summary">
                <div className="community-summary-card">
                  <span className="community-summary-label">{t.users}</span>
                  <span className="community-summary-value">{usersResponse?.total_count ?? users.length}</span>
                </div>
                <div className="community-summary-card">
                  <span className="community-summary-label">{t.clubs}</span>
                  <span className="community-summary-value">{clubsResponse?.total_count ?? clubs.length}</span>
                </div>
                <div className="community-summary-card">
                  <span className="community-summary-label">{t.teams}</span>
                  <span className="community-summary-value">{teamsResponse?.total_count ?? teams.length}</span>
                </div>
              </div>

              {/* Content */}
              <div className="content-area">
            {/* Users Tab */}
            {activeTab === 'users' && (
              <>
                <div className="search-section">
                  <FiSearch className="search-icon" size={16} />
                  <input
                    type="text"
                    placeholder={t.searchPlaceholder}
                    value={searchQuery}
                    onChange={(e) => {
                      setSearchQuery(e.target.value)
                      setUsersPage(1)
                    }}
                    className="search-input"
                  />
                </div>

                {isLoadingUsers ? (
                  <div className="loading-state">
                    <div className="loading-spinner" />
                    {t.loading}
                  </div>
                ) : (
                  <div className="entity-grid">
                    {users.map((user: AuthUser) => (
                      <div key={user.id} className="entity-card user-card">
                        <div className="entity-header">
                          <div className="entity-avatar user">
                            {user.avatar
                              ? <img src={user.avatar} alt="" />
                              : user.nickname?.charAt(0).toUpperCase() || '?'}
                          </div>
                          <div className="entity-info">
                            <div className="entity-name">{user.nickname}</div>
                            <div className="entity-meta">{user.email}</div>
                          </div>
                        </div>
                        {user.bio && <div className="entity-bio">{user.bio}</div>}
                        <div className="entity-footer">
                          <button className="btn" onClick={() => setPreviewUser(user)}>
                            <FiUser size={12} />
                            {t.preview}
                          </button>
                          {isAuthenticated && currentUser?.id !== user.id ? (
                            <button
                              className="btn btn-secondary"
                              disabled={sendFriendMutation.isPending || friendSentIds.has(user.id)}
                              onClick={() => handleSendFriendRequest(user)}
                            >
                              <FiUserPlus size={12} />
                              {friendSentIds.has(user.id) ? t.friendRequestSent : t.addFriend}
                            </button>
                          ) : (
                            <span className="entity-meta">{isAuthenticated ? '' : t.loginRequired}</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {users.length === 0 && !isLoadingUsers && (
                  <div className="empty-state">{t.noResults}</div>
                )}

                {!isLoadingUsers && users.length > 0 && (
                  <PaginationControls
                    page={usersPage}
                    hasNext={usersResponse?.has_next}
                    totalCount={usersResponse?.total_count}
                    isFetching={isFetchingUsers}
                    labels={t}
                    onPageChange={setUsersPage}
                  />
                )}
              </>
            )}

            {/* Clubs Tab */}
            {activeTab === 'clubs' && (
              <>
                {isLoadingClubs ? (
                  <div className="loading-state">
                    <div className="loading-spinner" />
                    {t.loading}
                  </div>
                ) : (
                  <div className="entity-grid">
                    {clubs.map((club: ClubResponse) => (
                      <div key={club.id} className="entity-card">
                        <div className="entity-header">
                          <div className="entity-avatar club">
                            {club.name.charAt(0).toUpperCase()}
                          </div>
                          <div className="entity-info">
                            <div className="entity-name">{club.name}</div>
                            <div className="entity-meta">{club.members.length} {t.members}</div>
                          </div>
                        </div>
                        {club.description && <div className="entity-bio">{club.description}</div>}
                        <div className="entity-footer">
                          <div /> {/* Spacer */}
                          {isAuthenticated ? (
                            <button
                              onClick={() => handleJoinClub(club.id)}
                              disabled={joinClubMutation.isPending}
                              className="btn btn-secondary"
                            >
                              <FiUsers size={12} />
                              {joinClubMutation.isPending ? t.creating : t.joinClub}
                            </button>
                          ) : (
                            <span className="entity-meta">{t.loginRequired}</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {clubs.length === 0 && !isLoadingClubs && (
                  <div className="empty-state">{t.noResults}</div>
                )}

                {!isLoadingClubs && clubs.length > 0 && (
                  <PaginationControls
                    page={clubsPage}
                    hasNext={clubsResponse?.has_next}
                    totalCount={clubsResponse?.total_count}
                    isFetching={isFetchingClubs}
                    labels={t}
                    onPageChange={setClubsPage}
                  />
                )}
              </>
            )}

            {/* Teams Tab */}
            {activeTab === 'teams' && (
              <>
                {isLoadingTeams ? (
                  <div className="loading-state">
                    <div className="loading-spinner" />
                    {t.loading}
                  </div>
                ) : (
                  <div className="entity-grid">
                    {teams.map((team: TeamResponse) => (
                      <div key={team.id} className="entity-card">
                        <div className="entity-header">
                          <div className="entity-avatar team">
                            {team.tag.toUpperCase()}
                          </div>
                          <div className="entity-info">
                            <div className="entity-name">{team.name}</div>
                            <div className="entity-meta">{team.members.length} {t.members}</div>
                          </div>
                        </div>
                        <div className="entity-footer">
                          <div className="entity-tag">
                            <FiTag size={10} style={{ marginRight: 4 }} />
                            {team.tag}
                          </div>
                          {isAuthenticated ? (
                            <button className="btn btn-danger">
                              <FiUsers size={12} />
                              {t.applyTeam}
                            </button>
                          ) : (
                            <span className="entity-meta">{t.loginRequired}</span>
                          )}
                        </div>
                      </div>
                    ))}
                  </div>
                )}

                {teams.length === 0 && !isLoadingTeams && (
                  <div className="empty-state">{t.noResults}</div>
                )}

                {!isLoadingTeams && teams.length > 0 && (
                  <PaginationControls
                    page={teamsPage}
                    hasNext={teamsResponse?.has_next}
                    totalCount={teamsResponse?.total_count}
                    isFetching={isFetchingTeams}
                    labels={t}
                    onPageChange={setTeamsPage}
                  />
                )}
              </>
            )}

            {/* Create Tab */}
            {activeTab === 'create' && (
              <div className="create-section">
                {!isAuthenticated ? (
                  <div className="auth-notice">{t.loginToCreate}</div>
                ) : (
                  <>
                    <div className="type-selector">
                      <button
                        onClick={() => setCreateType('club')}
                        className={`type-btn${createType === 'club' ? ' active club' : ''}`}
                      >
                        <FiShield size={14} />
                        {t.clubs}
                      </button>
                      <button
                        onClick={() => setCreateType('team')}
                        className={`type-btn${createType === 'team' ? ' active team' : ''}`}
                      >
                        <FiUsers size={14} />
                        {t.teams}
                      </button>
                    </div>

                    <div className="create-form">
                      <div className="form-group">
                        <label className="form-label">
                          {createType === 'club' ? t.clubName : t.teamName}
                        </label>
                        <input
                          type="text"
                          value={createName}
                          onChange={(e) => setCreateName(e.target.value)}
                          placeholder={createType === 'club' ? t.clubName : t.teamName}
                          className="form-input"
                        />
                      </div>

                      {createType === 'team' && (
                        <div className="form-group">
                          <label className="form-label">{t.teamTag}</label>
                          <input
                            type="text"
                            value={createTag}
                            onChange={(e) => setCreateTag(e.target.value.slice(0, 5).toUpperCase())}
                            placeholder={t.tagPlaceholder}
                            className="form-input"
                            maxLength={5}
                          />
                          <div className="form-hint">{t.maxChars}</div>
                        </div>
                      )}

                      <button
                        onClick={handleCreateSubmit}
                        disabled={
                          !createName.trim() ||
                          (createType === 'team' && !createTag.trim()) ||
                          createClubMutation.isPending ||
                          createTeamMutation.isPending
                        }
                        className="btn btn-primary"
                        style={{ width: '100%', justifyContent: 'center', marginTop: 8 }}
                      >
                        <FiPlus size={12} />
                        {createClubMutation.isPending || createTeamMutation.isPending
                          ? t.creating
                          : createType === 'club' ? t.createClub : t.createTeam
                        }
                      </button>
                    </div>
                  </>
                )}
              </div>
            )}
              </div>
            </div>
          </div>
        </div>

        {previewUser && (
          <div className="preview-backdrop" onClick={() => setPreviewUser(null)}>
            <div className="user-preview" onClick={(event) => event.stopPropagation()}>
              <div className="user-preview-head">
                <div className="entity-avatar user">
                  {previewUser.avatar
                    ? <img src={previewUser.avatar} alt="" />
                    : previewUser.nickname?.charAt(0).toUpperCase() || '?'}
                </div>
                <div>
                  <h2 className="user-preview-name">{previewUser.nickname}</h2>
                  <div className="user-preview-email">{previewUser.email}</div>
                </div>
                <button className="user-preview-close" onClick={() => setPreviewUser(null)} aria-label="Close">
                  <FiX size={16} />
                </button>
              </div>
              <div className="entity-meta">{previewUser.user_type}</div>
              <p className="user-preview-bio">{previewUser.bio || t.noResults}</p>
              <div className="user-preview-actions">
                {isAuthenticated && currentUser?.id !== previewUser.id && (
                  <button
                    className="btn btn-secondary"
                    disabled={sendFriendMutation.isPending || friendSentIds.has(previewUser.id)}
                    onClick={() => handleSendFriendRequest(previewUser)}
                  >
                    <FiUserPlus size={12} />
                    {friendSentIds.has(previewUser.id) ? t.friendRequestSent : t.addFriend}
                  </button>
                )}
                <a className="btn btn-primary" href={`/users/${previewUser.id}`}>
                  <FiExternalLink size={12} />
                  {t.openProfile}
                </a>
              </div>
            </div>
          </div>
        )}
      </PageShell>
    </>
  )
}
