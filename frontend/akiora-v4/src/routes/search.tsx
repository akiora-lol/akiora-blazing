import { createFileRoute, useNavigate } from '@tanstack/react-router'
import type { CSSProperties } from 'react'
import { useMemo, useState } from 'react'
import {
    FiChevronLeft,
    FiFilter,
    FiHeart,
    FiMessageSquare,
    FiPlus,
    FiRefreshCcw,
    FiSearch,
    FiSend,
    FiSlash,
    FiX,
    FiZap,
} from 'react-icons/fi'
import { PageShell } from '../components/PageShell'
import { useAuthContext } from '../contexts/AuthContext'
import {
    type ColdFormResponse,
    type CreateSearchFormRequest,
    type HotFormResponse,
    type SearchRankName,
    type SearchRole,
    type SearchServer,
    useColdDeck,
    useCreateColdSearchFormMutation,
    useCreateHotSearchFormMutation,
    useHotForms,
    useSwipeColdSearchFormMutation,
    useSwipeHotSearchFormMutation,
} from '../lib/api'

export const Route = createFileRoute('/search')({ component: SearchPage })

type FormMode = 'cold' | 'hot'
type Lang = 'ru' | 'en'

const ROLE_LABELS: Record<SearchRole, string> = {
    top: 'Top',
    jg: 'Jungle',
    mid: 'Mid',
    adc: 'ADC',
    sup: 'Support',
}

const SERVER_LABELS: Record<SearchServer, string> = {
    euw: 'EUW',
    ru: 'RU',
    eune: 'EUNE',
    na: 'NA',
    tr: 'TR',
}

const RANK_LABELS: Record<SearchRankName, string> = {
    iron: 'Iron',
    bronze: 'Bronze',
    silver: 'Silver',
    gold: 'Gold',
    platinum: 'Platinum',
    emerald: 'Emerald',
    diamond: 'Diamond',
    master: 'Master',
    grandmaster: 'GM',
    challenger: 'Challenger',
}

const RANK_COLORS: Record<SearchRankName, string> = {
    iron: '#858585',
    bronze: '#b87746',
    silver: '#c7d2fe',
    gold: '#f5b642',
    platinum: '#2dd4bf',
    emerald: '#34d399',
    diamond: '#60a5fa',
    master: '#c084fc',
    grandmaster: '#fb7185',
    challenger: '#facc15',
}

const ROLES: SearchRole[] = ['top', 'jg', 'mid', 'adc', 'sup']
const SERVERS: SearchServer[] = ['euw', 'ru', 'eune', 'na', 'tr']
const RANKS: SearchRankName[] = [
    'iron',
    'bronze',
    'silver',
    'gold',
    'platinum',
    'emerald',
    'diamond',
    'master',
    'grandmaster',
    'challenger',
]

const TEXT = {
    ru: {
        title: 'Поиск напарника',
        subtitle: 'Холодные анкеты листаются карточками, горячие заявки живут в быстром списке.',
        cold: 'Холодные',
        hot: 'Горячие',
        filters: 'Фильтры',
        create: 'Создать',
        lookingFor: 'Ищет',
        myRoles: 'Играет',
        server: 'Сервер',
        rank: 'Ранг',
        minRank: 'Мин. ранг',
        maxRank: 'Макс. ранг',
        description: 'Описание',
        publish: 'Опубликовать',
        emptyCold: 'Карточки закончились',
        emptyHot: 'Горячих заявок пока нет',
        login: 'Войдите, чтобы свайпать и создавать анкеты',
        refresh: 'Обновить',
        searchPlaceholder: 'Поиск по описанию',
        allRoles: 'Все роли',
        allServers: 'Все сервера',
        page: 'Страница',
        next: 'Дальше',
        previous: 'Назад',
    },
    en: {
        title: 'Partner Search',
        subtitle: 'Cold profiles are swipe cards, hot requests stay in a fast filtered list.',
        cold: 'Cold',
        hot: 'Hot',
        filters: 'Filters',
        create: 'Create',
        lookingFor: 'Looking for',
        myRoles: 'Plays',
        server: 'Server',
        rank: 'Rank',
        minRank: 'Min rank',
        maxRank: 'Max rank',
        description: 'Description',
        publish: 'Publish',
        emptyCold: 'No more cards',
        emptyHot: 'No hot requests yet',
        login: 'Sign in to swipe and create forms',
        refresh: 'Refresh',
        searchPlaceholder: 'Search description',
        allRoles: 'All roles',
        allServers: 'All servers',
        page: 'Page',
        next: 'Next',
        previous: 'Previous',
    },
}

interface Filters {
    roles: SearchRole[]
    servers: SearchServer[]
    query: string
}

const defaultForm = {
    server: 'euw' as SearchServer,
    minRank: 'gold' as SearchRankName,
    minDivision: 4,
    maxRank: 'diamond' as SearchRankName,
    maxDivision: 1,
    myRoles: [] as SearchRole[],
    lookingForRoles: [] as SearchRole[],
    description: '',
}

function displayName(form: ColdFormResponse | HotFormResponse) {
    return form.owner?.username || form.owner?.riot_game_name || `Player ${form.owner_id.slice(0, 8)}`
}

function rankRange(form: ColdFormResponse | HotFormResponse) {
    const first = form.rank_range[0]
    if (!first) return 'Any rank'
    const min = `${RANK_LABELS[first.min_rank.rank]} ${first.min_rank.division}`
    const max = `${RANK_LABELS[first.max_rank.rank]} ${first.max_rank.division}`
    return `${SERVER_LABELS[first.server]} · ${min} - ${max}`
}

function formAccent(form: ColdFormResponse | HotFormResponse) {
    const rank = form.rank_range[0]?.max_rank.rank ?? 'gold'
    return RANK_COLORS[rank]
}

function timeAgo(value: string) {
    const then = new Date(value).getTime()
    if (Number.isNaN(then)) return value
    const diff = Math.max(0, Date.now() - then)
    const minutes = Math.floor(diff / 60000)
    if (minutes < 1) return 'now'
    if (minutes < 60) return `${minutes}m`
    const hours = Math.floor(minutes / 60)
    if (hours < 24) return `${hours}h`
    return `${Math.floor(hours / 24)}d`
}

function Avatar({ form, size = 56 }: { form: ColdFormResponse | HotFormResponse; size?: number }) {
    const name = displayName(form)
    const image = form.owner?.profile_image_url || form.owner?.avatar_url
    const accent = formAccent(form)
    return (
        <div className="ps-avatar" style={{ width: size, height: size, borderColor: `${accent}66` }}>
            {image ? <img src={image} alt="" /> : <span>{name.slice(0, 2).toUpperCase()}</span>}
        </div>
    )
}

function RolePills({ roles }: { roles: SearchRole[] }) {
    return (
        <div className="ps-pills">
            {roles.map((role) => (
                <span key={role} className="ps-pill">
                    {ROLE_LABELS[role]}
                </span>
            ))}
        </div>
    )
}

function FilterBar({
    filters,
    labels,
    onChange,
}: {
    filters: Filters
    labels: typeof TEXT[Lang]
    onChange: (filters: Filters) => void
}) {
    const toggleRole = (role: SearchRole) => {
        onChange({
            ...filters,
            roles: filters.roles.includes(role)
                ? filters.roles.filter((item) => item !== role)
                : [...filters.roles, role],
        })
    }
    const toggleServer = (server: SearchServer) => {
        onChange({
            ...filters,
            servers: filters.servers.includes(server)
                ? filters.servers.filter((item) => item !== server)
                : [...filters.servers, server],
        })
    }

    return (
        <div className="ps-filterbar">
            <label className="ps-searchbox">
                <FiSearch size={16} />
                <input
                    value={filters.query}
                    onChange={(event) => onChange({ ...filters, query: event.target.value })}
                    placeholder={labels.searchPlaceholder}
                />
            </label>
            <div className="ps-filter-row">
                <span><FiFilter size={14} /> {labels.allRoles}</span>
                {ROLES.map((role) => (
                    <button
                        key={role}
                        type="button"
                        className={`ps-chip ${filters.roles.includes(role) ? 'active' : ''}`}
                        onClick={() => toggleRole(role)}
                    >
                        {ROLE_LABELS[role]}
                    </button>
                ))}
            </div>
            <div className="ps-filter-row">
                <span>{labels.allServers}</span>
                {SERVERS.map((server) => (
                    <button
                        key={server}
                        type="button"
                        className={`ps-chip ${filters.servers.includes(server) ? 'active' : ''}`}
                        onClick={() => toggleServer(server)}
                    >
                        {SERVER_LABELS[server]}
                    </button>
                ))}
            </div>
        </div>
    )
}

function ColdCard({
    form,
    labels,
    dragX,
    onDrag,
    onRelease,
    onLike,
    onDislike,
    onBlock,
}: {
    form: ColdFormResponse
    labels: typeof TEXT[Lang]
    dragX: number
    onDrag: (value: number) => void
    onRelease: () => void
    onLike: () => void
    onDislike: () => void
    onBlock: () => void
}) {
    const accent = formAccent(form)
    const [startX, setStartX] = useState<number | null>(null)

    return (
        <article
            className="ps-cold-card"
            style={{
                '--accent': accent,
                transform: `translateX(${dragX}px) rotate(${dragX / 20}deg)`,
            } as CSSProperties}
            onPointerDown={(event) => {
                event.currentTarget.setPointerCapture(event.pointerId)
                setStartX(event.clientX)
            }}
            onPointerMove={(event) => {
                if (startX !== null) onDrag(event.clientX - startX)
            }}
            onPointerUp={() => {
                setStartX(null)
                onRelease()
            }}
        >
            <div className="ps-card-topline">
                <span>{rankRange(form)}</span>
                <span>{timeAgo(form.created_at)}</span>
            </div>
            <div className="ps-card-hero">
                <Avatar form={form} size={88} />
                <div>
                    <h2>{displayName(form)}</h2>
                    <p>{form.owner?.riot_tagline ? `#${form.owner.riot_tagline}` : form.owner_id.slice(0, 8)}</p>
                </div>
            </div>
            <div className="ps-role-grid">
                <section>
                    <span>{labels.myRoles}</span>
                    <RolePills roles={form.my_roles} />
                </section>
                <section>
                    <span>{labels.lookingFor}</span>
                    <RolePills roles={form.looking_for_roles} />
                </section>
            </div>
            <p className="ps-card-description">{form.description}</p>
            <div className="ps-card-actions">
                <button className="ps-action danger" type="button" onClick={onDislike} title="Skip">
                    <FiX size={24} />
                </button>
                <button className="ps-action muted" type="button" onClick={onBlock} title="Block">
                    <FiSlash size={19} />
                </button>
                <button className="ps-action good" type="button" onClick={onLike} title="Like">
                    <FiHeart size={24} />
                </button>
            </div>
            <div className={`ps-swipe-mark like ${dragX > 70 ? 'visible' : ''}`}>LIKE</div>
            <div className={`ps-swipe-mark nope ${dragX < -70 ? 'visible' : ''}`}>SKIP</div>
        </article>
    )
}

function HotRow({
    form,
    labels,
    onLike,
}: {
    form: HotFormResponse
    labels: typeof TEXT[Lang]
    onLike: () => void
}) {
    const accent = formAccent(form)
    return (
        <article className="ps-hot-row" style={{ '--accent': accent } as CSSProperties}>
            <Avatar form={form} />
            <div className="ps-hot-main">
                <div className="ps-hot-title">
                    <h3>{displayName(form)}</h3>
                    <span>{rankRange(form)}</span>
                </div>
                <p>{form.description}</p>
                <div className="ps-hot-meta">
                    <span>{labels.myRoles}</span>
                    <RolePills roles={form.my_roles} />
                    <span>{labels.lookingFor}</span>
                    <RolePills roles={form.looking_for_roles} />
                </div>
            </div>
            <div className="ps-hot-actions">
                <span>{timeAgo(form.created_at)}</span>
                <button type="button" className="ps-icon-btn good" onClick={onLike} title="Like">
                    <FiHeart size={18} />
                </button>
                <button type="button" className="ps-icon-btn" title="Message">
                    <FiMessageSquare size={18} />
                </button>
            </div>
        </article>
    )
}

function CreatePanel({
    mode,
    labels,
    disabled,
    onSubmit,
}: {
    mode: FormMode
    labels: typeof TEXT[Lang]
    disabled: boolean
    onSubmit: (data: Omit<CreateSearchFormRequest, 'owner_id'>) => void
}) {
    const [form, setForm] = useState(defaultForm)

    const toggle = (field: 'myRoles' | 'lookingForRoles', role: SearchRole) => {
        setForm((current) => ({
            ...current,
            [field]: current[field].includes(role)
                ? current[field].filter((item) => item !== role)
                : [...current[field], role],
        }))
    }

    const submit = () => {
        if (!form.description.trim() || form.myRoles.length === 0 || form.lookingForRoles.length === 0) return
        onSubmit({
            rank_range: [
                {
                    server: form.server,
                    min_rank: { rank: form.minRank, division: form.minDivision },
                    max_rank: { rank: form.maxRank, division: form.maxDivision },
                },
            ],
            my_roles: form.myRoles,
            looking_for_roles: form.lookingForRoles,
            description: form.description.trim(),
            status: mode === 'cold' ? 'active' : undefined,
        })
        setForm(defaultForm)
    }

    return (
        <aside className="ps-create-panel">
            <div className="ps-create-head">
                <FiPlus size={18} />
                <span>{labels.create} · {mode === 'cold' ? labels.cold : labels.hot}</span>
            </div>
            <div className="ps-form-grid">
                <label>
                    {labels.server}
                    <select value={form.server} onChange={(event) => setForm({ ...form, server: event.target.value as SearchServer })}>
                        {SERVERS.map((server) => <option key={server} value={server}>{SERVER_LABELS[server]}</option>)}
                    </select>
                </label>
                <label>
                    {labels.minRank}
                    <select value={form.minRank} onChange={(event) => setForm({ ...form, minRank: event.target.value as SearchRankName })}>
                        {RANKS.map((rank) => <option key={rank} value={rank}>{RANK_LABELS[rank]}</option>)}
                    </select>
                </label>
                <label>
                    {labels.maxRank}
                    <select value={form.maxRank} onChange={(event) => setForm({ ...form, maxRank: event.target.value as SearchRankName })}>
                        {RANKS.map((rank) => <option key={rank} value={rank}>{RANK_LABELS[rank]}</option>)}
                    </select>
                </label>
            </div>
            <div className="ps-form-section">
                <span>{labels.myRoles}</span>
                <div className="ps-filter-row compact">
                    {ROLES.map((role) => (
                        <button key={role} type="button" className={`ps-chip ${form.myRoles.includes(role) ? 'active' : ''}`} onClick={() => toggle('myRoles', role)}>
                            {ROLE_LABELS[role]}
                        </button>
                    ))}
                </div>
            </div>
            <div className="ps-form-section">
                <span>{labels.lookingFor}</span>
                <div className="ps-filter-row compact">
                    {ROLES.map((role) => (
                        <button key={role} type="button" className={`ps-chip ${form.lookingForRoles.includes(role) ? 'active' : ''}`} onClick={() => toggle('lookingForRoles', role)}>
                            {ROLE_LABELS[role]}
                        </button>
                    ))}
                </div>
            </div>
            <label className="ps-textarea-label">
                {labels.description}
                <textarea value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} maxLength={1000} />
            </label>
            <button type="button" className="ps-primary-btn" disabled={disabled} onClick={submit}>
                <FiSend size={16} /> {labels.publish}
            </button>
        </aside>
    )
}

function SearchPage() {
    const [lang, setLang] = useState<Lang>('ru')
    const [mode, setMode] = useState<FormMode>('cold')
    const [filters, setFilters] = useState<Filters>({ roles: [], servers: [], query: '' })
    const [page, setPage] = useState(1)
    const [dragX, setDragX] = useState(0)
    const [localHidden, setLocalHidden] = useState<Set<string>>(new Set())
    const { user, isAuthenticated } = useAuthContext()
    const navigate = useNavigate()
    const labels = TEXT[lang]

    const apiFilter = useMemo(() => ({
        looking_for_roles: filters.roles,
        servers: filters.servers,
        exclude_owner_id: user?.id,
        exclude_blocked_by: user?.id,
        status: 'active' as const,
        query: filters.query || null,
    }), [filters, user?.id])

    const coldDeck = useColdDeck(user?.id, apiFilter, 24)
    const hotForms = useHotForms(
        { ...apiFilter, status: null },
        { page, page_size: 30 },
    )
    const createCold = useCreateColdSearchFormMutation()
    const createHot = useCreateHotSearchFormMutation()
    const swipeCold = useSwipeColdSearchFormMutation()
    const swipeHot = useSwipeHotSearchFormMutation()

    const coldForms = (coldDeck.data?.forms ?? []).filter((form) => !localHidden.has(form.id))
    const hotList = (hotForms.data?.forms ?? []).filter((form) => {
        if (!filters.query.trim()) return true
        return form.description.toLowerCase().includes(filters.query.trim().toLowerCase())
    })
    const activeCold = coldForms[0]

    const swipe = (form: ColdFormResponse, action: 'like' | 'dislike' | 'block') => {
        if (!user) return
        setLocalHidden((current) => new Set(current).add(form.id))
        setDragX(0)
        swipeCold.mutate({ formId: form.id, userId: user.id, action })
    }

    const releaseDrag = () => {
        if (!activeCold) {
            setDragX(0)
            return
        }
        if (dragX > 90) swipe(activeCold, 'like')
        else if (dragX < -90) swipe(activeCold, 'dislike')
        else setDragX(0)
    }

    const submitForm = (data: Omit<CreateSearchFormRequest, 'owner_id'>) => {
        if (!user) {
            navigate({ to: '/login' })
            return
        }
        const payload = { ...data, owner_id: user.id }
        if (mode === 'cold') createCold.mutate(payload)
        else createHot.mutate(payload)
    }

    return (
        <PageShell lang={lang} onLangChange={setLang}>
            <style>{`
                .ps-page { min-height: 100vh; padding: 88px 24px 48px; color: #fff; position: relative; z-index: 1; }
                .ps-shell { max-width: 1180px; margin: 0 auto; display: grid; grid-template-columns: minmax(0, 1fr) 340px; gap: 24px; align-items: start; }
                .ps-hero { max-width: 1180px; margin: 0 auto 24px; display: flex; align-items: flex-end; justify-content: space-between; gap: 20px; }
                .ps-title h1 { font-family: 'Russo One', sans-serif; font-size: clamp(2rem, 5vw, 4rem); margin: 0 0 10px; letter-spacing: 0; }
                .ps-title p { margin: 0; max-width: 620px; color: rgba(255,255,255,.58); line-height: 1.6; font-size: 14px; }
                .ps-tabs { display: flex; gap: 8px; padding: 6px; border: 1px solid rgba(255,255,255,.1); background: rgba(6,8,18,.72); border-radius: 8px; backdrop-filter: blur(18px); }
                .ps-tab { height: 40px; padding: 0 16px; border: 0; border-radius: 6px; display: inline-flex; align-items: center; gap: 8px; background: transparent; color: rgba(255,255,255,.58); cursor: pointer; font: 700 12px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-tab.active { color: #fff; background: linear-gradient(135deg, rgba(45,212,191,.2), rgba(192,132,252,.22)); box-shadow: inset 0 0 0 1px rgba(255,255,255,.12); }
                .ps-main { min-width: 0; }
                .ps-panel { border: 1px solid rgba(255,255,255,.1); background: rgba(5,8,18,.76); border-radius: 8px; backdrop-filter: blur(18px); box-shadow: 0 18px 60px rgba(0,0,0,.28); }
                .ps-filterbar { padding: 16px; margin-bottom: 18px; display: grid; gap: 12px; }
                .ps-searchbox { height: 44px; display: flex; align-items: center; gap: 10px; padding: 0 14px; border-radius: 6px; background: rgba(255,255,255,.055); border: 1px solid rgba(255,255,255,.1); color: rgba(255,255,255,.45); }
                .ps-searchbox input { flex: 1; min-width: 0; border: 0; outline: 0; background: transparent; color: #fff; font: 500 13px 'Chakra Petch', monospace; }
                .ps-filter-row { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
                .ps-filter-row > span { display: inline-flex; align-items: center; gap: 6px; min-width: 102px; color: rgba(255,255,255,.46); font: 700 11px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-filter-row.compact > span { min-width: 0; }
                .ps-chip { height: 30px; padding: 0 10px; border: 1px solid rgba(255,255,255,.1); border-radius: 6px; background: rgba(255,255,255,.04); color: rgba(255,255,255,.64); cursor: pointer; font: 700 11px 'Chakra Petch', monospace; }
                .ps-chip.active { color: #fff; border-color: rgba(45,212,191,.5); background: rgba(45,212,191,.14); }
                .ps-deck { min-height: 620px; display: grid; place-items: center; padding: 26px; overflow: hidden; }
                .ps-cold-card { --accent: #2dd4bf; width: min(100%, 520px); min-height: 560px; border-radius: 8px; border: 1px solid color-mix(in srgb, var(--accent) 42%, rgba(255,255,255,.08)); background: radial-gradient(circle at 50% 0, color-mix(in srgb, var(--accent) 24%, transparent), transparent 34%), rgba(8,12,24,.94); box-shadow: 0 24px 80px rgba(0,0,0,.38); padding: 22px; touch-action: none; user-select: none; position: relative; transition: transform 160ms ease; }
                .ps-card-topline { display: flex; justify-content: space-between; color: rgba(255,255,255,.54); font: 700 11px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-card-hero { display: flex; align-items: center; gap: 18px; margin: 34px 0 28px; }
                .ps-card-hero h2 { font-family: 'Russo One', sans-serif; margin: 0 0 6px; font-size: 30px; letter-spacing: 0; }
                .ps-card-hero p { margin: 0; color: rgba(255,255,255,.5); }
                .ps-avatar { flex: 0 0 auto; border: 2px solid rgba(255,255,255,.16); border-radius: 50%; display: grid; place-items: center; overflow: hidden; background: rgba(255,255,255,.06); }
                .ps-avatar img { width: 100%; height: 100%; object-fit: cover; }
                .ps-avatar span { font-family: 'Russo One', sans-serif; color: #fff; }
                .ps-role-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 12px; }
                .ps-role-grid section { padding: 14px; border-radius: 8px; background: rgba(255,255,255,.045); border: 1px solid rgba(255,255,255,.08); }
                .ps-role-grid section > span, .ps-form-section > span { display: block; margin-bottom: 10px; color: rgba(255,255,255,.45); font: 700 11px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-pills { display: flex; flex-wrap: wrap; gap: 6px; }
                .ps-pill { border-radius: 6px; padding: 5px 8px; background: rgba(255,255,255,.08); color: rgba(255,255,255,.82); font: 700 11px 'Chakra Petch', monospace; }
                .ps-card-description { min-height: 112px; margin: 22px 0; color: rgba(255,255,255,.72); line-height: 1.65; font-size: 14px; }
                .ps-card-actions { display: flex; justify-content: center; gap: 14px; }
                .ps-action, .ps-icon-btn { border: 1px solid rgba(255,255,255,.12); color: #fff; background: rgba(255,255,255,.06); cursor: pointer; display: inline-grid; place-items: center; }
                .ps-action { width: 58px; height: 58px; border-radius: 50%; }
                .ps-icon-btn { width: 38px; height: 38px; border-radius: 50%; }
                .ps-action.good, .ps-icon-btn.good { color: #34d399; border-color: rgba(52,211,153,.36); background: rgba(52,211,153,.1); }
                .ps-action.danger { color: #fb7185; border-color: rgba(251,113,133,.36); background: rgba(251,113,133,.1); }
                .ps-action.muted { color: #facc15; border-color: rgba(250,204,21,.3); background: rgba(250,204,21,.09); }
                .ps-swipe-mark { position: absolute; top: 86px; padding: 8px 12px; border: 2px solid currentColor; border-radius: 6px; font: 900 24px 'Russo One', sans-serif; opacity: 0; transform: rotate(-12deg); }
                .ps-swipe-mark.like { left: 28px; color: #34d399; }
                .ps-swipe-mark.nope { right: 28px; color: #fb7185; transform: rotate(12deg); }
                .ps-swipe-mark.visible { opacity: .9; }
                .ps-hot-list { display: grid; gap: 12px; }
                .ps-hot-row { --accent: #2dd4bf; display: grid; grid-template-columns: auto minmax(0,1fr) auto; gap: 14px; align-items: center; padding: 16px; border: 1px solid rgba(255,255,255,.1); background: linear-gradient(90deg, color-mix(in srgb, var(--accent) 10%, transparent), transparent 48%), rgba(6,9,18,.72); border-radius: 8px; }
                .ps-hot-title { display: flex; align-items: baseline; gap: 10px; flex-wrap: wrap; }
                .ps-hot-title h3 { margin: 0; font-family: 'Russo One', sans-serif; letter-spacing: 0; }
                .ps-hot-title span, .ps-hot-actions span { color: rgba(255,255,255,.48); font: 700 11px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-hot-main p { margin: 8px 0 12px; color: rgba(255,255,255,.66); line-height: 1.5; }
                .ps-hot-meta { display: flex; align-items: center; gap: 8px; flex-wrap: wrap; }
                .ps-hot-meta > span { color: rgba(255,255,255,.4); font: 700 10px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-hot-actions { display: flex; align-items: center; gap: 8px; }
                .ps-create-panel { position: sticky; top: 88px; border: 1px solid rgba(255,255,255,.1); background: rgba(6,8,18,.76); border-radius: 8px; padding: 16px; backdrop-filter: blur(18px); }
                .ps-create-head { display: flex; align-items: center; gap: 8px; margin-bottom: 16px; font: 800 12px 'Chakra Petch', monospace; text-transform: uppercase; color: #fff; }
                .ps-form-grid { display: grid; grid-template-columns: 1fr; gap: 10px; }
                .ps-form-grid label, .ps-textarea-label { display: grid; gap: 6px; color: rgba(255,255,255,.48); font: 700 10px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-form-grid select, .ps-textarea-label textarea { width: 100%; border: 1px solid rgba(255,255,255,.1); border-radius: 6px; background: rgba(255,255,255,.055); color: #fff; outline: none; box-sizing: border-box; }
                .ps-form-grid select { height: 38px; padding: 0 10px; }
                .ps-textarea-label textarea { min-height: 118px; resize: vertical; padding: 10px; font: 500 13px 'Chakra Petch', monospace; text-transform: none; }
                .ps-form-section { margin: 14px 0; }
                .ps-primary-btn { width: 100%; height: 42px; border-radius: 6px; border: 1px solid rgba(45,212,191,.4); background: linear-gradient(135deg, rgba(45,212,191,.22), rgba(96,165,250,.18)); color: #fff; display: inline-flex; align-items: center; justify-content: center; gap: 8px; cursor: pointer; font: 800 12px 'Chakra Petch', monospace; text-transform: uppercase; }
                .ps-primary-btn:disabled { opacity: .45; cursor: not-allowed; }
                .ps-empty { min-height: 360px; display: grid; place-items: center; text-align: center; color: rgba(255,255,255,.5); }
                .ps-empty svg { margin-bottom: 12px; color: #2dd4bf; }
                .ps-pager { display: flex; align-items: center; justify-content: center; gap: 10px; margin-top: 16px; }
                .ps-pager button { height: 34px; padding: 0 12px; border-radius: 6px; border: 1px solid rgba(255,255,255,.1); background: rgba(255,255,255,.05); color: #fff; cursor: pointer; }
                .ps-auth { max-width: 1180px; margin: 0 auto 16px; padding: 12px 14px; border-radius: 8px; border: 1px solid rgba(250,204,21,.28); background: rgba(250,204,21,.08); color: rgba(255,255,255,.72); }
                @media (max-width: 980px) { .ps-shell { grid-template-columns: 1fr; } .ps-create-panel { position: static; } .ps-hero { align-items: stretch; flex-direction: column; } }
                @media (max-width: 640px) { .ps-page { padding: 78px 14px 32px; } .ps-tabs { width: 100%; } .ps-tab { flex: 1; justify-content: center; } .ps-role-grid, .ps-hot-row { grid-template-columns: 1fr; } .ps-hot-actions { justify-content: flex-start; } .ps-deck { padding: 14px; min-height: 560px; } .ps-cold-card { min-height: 520px; padding: 18px; } .ps-card-hero h2 { font-size: 24px; } }
            `}</style>

            <main className="ps-page">
                <header className="ps-hero">
                    <div className="ps-title">
                        <h1>{labels.title}</h1>
                        <p>{labels.subtitle}</p>
                    </div>
                    <div className="ps-tabs">
                        <button className={`ps-tab ${mode === 'cold' ? 'active' : ''}`} type="button" onClick={() => setMode('cold')}>
                            <FiHeart size={16} /> {labels.cold}
                        </button>
                        <button className={`ps-tab ${mode === 'hot' ? 'active' : ''}`} type="button" onClick={() => setMode('hot')}>
                            <FiZap size={16} /> {labels.hot}
                        </button>
                    </div>
                </header>

                {!isAuthenticated && <div className="ps-auth">{labels.login}</div>}

                <section className="ps-shell">
                    <div className="ps-main">
                        <FilterBar filters={filters} labels={labels} onChange={(next) => { setFilters(next); setPage(1) }} />

                        {mode === 'cold' ? (
                            <div className="ps-panel ps-deck">
                                {coldDeck.isLoading ? (
                                    <div className="ps-empty"><FiRefreshCcw size={28} /> Loading...</div>
                                ) : activeCold ? (
                                    <ColdCard
                                        form={activeCold}
                                        labels={labels}
                                        dragX={dragX}
                                        onDrag={setDragX}
                                        onRelease={releaseDrag}
                                        onLike={() => swipe(activeCold, 'like')}
                                        onDislike={() => swipe(activeCold, 'dislike')}
                                        onBlock={() => swipe(activeCold, 'block')}
                                    />
                                ) : (
                                    <div className="ps-empty">
                                        <div>
                                            <FiRefreshCcw size={30} />
                                            <p>{labels.emptyCold}</p>
                                            <button className="ps-primary-btn" type="button" onClick={() => { setLocalHidden(new Set()); coldDeck.refetch() }}>
                                                {labels.refresh}
                                            </button>
                                        </div>
                                    </div>
                                )}
                            </div>
                        ) : (
                            <>
                                <div className="ps-hot-list">
                                    {hotForms.isLoading ? (
                                        <div className="ps-panel ps-empty"><FiRefreshCcw size={28} /> Loading...</div>
                                    ) : hotList.length > 0 ? hotList.map((form) => (
                                        <HotRow
                                            key={form.id}
                                            form={form}
                                            labels={labels}
                                            onLike={() => user && swipeHot.mutate({ formId: form.id, userId: user.id, action: 'like' })}
                                        />
                                    )) : (
                                        <div className="ps-panel ps-empty"><FiZap size={30} /><p>{labels.emptyHot}</p></div>
                                    )}
                                </div>
                                <div className="ps-pager">
                                    <button type="button" disabled={page <= 1} onClick={() => setPage((current) => Math.max(1, current - 1))}>
                                        <FiChevronLeft size={14} /> {labels.previous}
                                    </button>
                                    <span>{labels.page} {page}</span>
                                    <button type="button" disabled={!hotForms.data?.has_next} onClick={() => setPage((current) => current + 1)}>
                                        {labels.next}
                                    </button>
                                </div>
                            </>
                        )}
                    </div>

                    <CreatePanel
                        mode={mode}
                        labels={labels}
                        disabled={!user || createCold.isPending || createHot.isPending}
                        onSubmit={submitForm}
                    />
                </section>
            </main>
        </PageShell>
    )
}
