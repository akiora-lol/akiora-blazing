import { createFileRoute, Link } from '@tanstack/react-router'
import { useMemo, useState } from 'react'
import { useAuthContext } from '../contexts/AuthContext'
import {
    type Actor,
    type MatchResponse,
    type TeamResponse,
    useTeams,
    useTournament,
} from '../lib/api'

export const Route = createFileRoute('/tournaments/$id/results')({
    component: TournamentResultsPage,
})

/**
 * Host-only screen for reporting per-game winners.
 *
 * Server-side is intentionally NOT wired here yet — the gateway lacks a
 * read-side endpoint for series games and there's no "next game" RPC, so any
 * mutation we'd fire would either need a fake `game_id` or a new proto+RPC.
 * Per current product spec, this page is a local-only scratchpad: clicking
 * "winner"/"loser" pushes into an in-memory log per match. The display labels
 * use team tags (not id prefixes) so the host can actually tell teams apart.
 */
function TournamentResultsPage() {
    const { id } = Route.useParams()
    const { user } = useAuthContext()
    const { data: tournament, isLoading, error } = useTournament(id)
    const { data: allTeams } = useTeams()

    // Team-id → tag map, computed once. Falls back to a short id slice for
    // non-team actors (users in 1v1, or teams missing from the list).
    const teamsById = useMemo(() => {
        const m = new Map<string, TeamResponse>()
        for (const t of allTeams ?? []) m.set(t.id, t)
        return m
    }, [allTeams])

    const actorLabel = (a: Actor | null): string => {
        if (!a) return '—'
        if (a.type === 'team') {
            const t = teamsById.get(a.id)
            if (t?.tag) return t.tag
            if (t?.name) return t.name
        }
        return `${a.type}:${a.id.slice(0, 8)}`
    }

    // Local-only per-match game log: matchKey → ordered list of winners.
    // Each entry is which slot won that game. Nothing is sent to the server.
    type Slot = 'team1' | 'team2'
    const [localResults, setLocalResults] = useState<Record<string, Slot[]>>({})

    const matches: MatchResponse[] = useMemo(
        () => tournament?.bracket?.rounds.flat() ?? [],
        [tournament?.bracket],
    )

    // Shell styles applied to EVERY branch so the page is never invisible:
    // - paddingTop clears the 52px fixed TopDock
    // - explicit color overrides parent dark-mode resets
    // - position/zIndex keeps it above the global background canvas
    const shellStyle: React.CSSProperties = {
        position: 'relative',
        zIndex: 1,
        minHeight: 'calc(100vh - 52px)',
        padding: '76px 24px 32px',
        maxWidth: 960,
        margin: '0 auto',
        color: 'rgba(255,255,255,0.88)',
        fontFamily: "'Chakra Petch', monospace",
    }
    const headerStyle: React.CSSProperties = {
        margin: 0,
        fontFamily: "'Russo One', sans-serif",
        fontSize: 22,
        letterSpacing: '0.04em',
        color: '#fff',
    }

    const Banner = () => (
        <div
            style={{
                background: 'rgba(166,0,255,0.18)',
                border: '1px solid rgba(166,0,255,0.45)',
                color: '#fff',
                padding: '6px 10px',
                borderRadius: 6,
                fontSize: 11,
                marginBottom: 16,
                letterSpacing: '0.06em',
            }}
        >
            RESULTS PAGE MOUNTED · tournamentId={id} · local-only mode
        </div>
    )

    if (isLoading) {
        return (
            <div style={shellStyle}>
                <Banner />
                <h2 style={headerStyle}>Match results</h2>
                <p style={{ color: 'rgba(255,255,255,0.5)' }}>Loading tournament…</p>
            </div>
        )
    }
    if (error) {
        return (
            <div style={shellStyle}>
                <Banner />
                <h2 style={headerStyle}>Match results</h2>
                <p style={{ color: '#ff7f7f' }}>
                    Failed to load tournament: {error instanceof Error ? error.message : String(error)}
                </p>
                <Link to="/tournaments/$id" params={{ id }} style={{ color: '#c77dff' }}>
                    ← Back to tournament
                </Link>
            </div>
        )
    }
    if (!tournament) {
        return (
            <div style={shellStyle}>
                <Banner />
                <h2 style={headerStyle}>Match results</h2>
                <p>Tournament not found.</p>
                <Link to="/tournaments/$id" params={{ id }} style={{ color: '#c77dff' }}>
                    ← Back to tournament
                </Link>
            </div>
        )
    }

    const isHost = !!user && user.id === tournament.host.id
    if (!isHost) {
        return (
            <div style={shellStyle}>
                <Banner />
                <h2 style={headerStyle}>Match results</h2>
                <p>Only the tournament host can set match results.</p>
                <Link to="/tournaments/$id" params={{ id }} style={{ color: '#c77dff' }}>
                    ← Back to tournament
                </Link>
            </div>
        )
    }

    if (!tournament.bracket || matches.length === 0) {
        return (
            <div style={shellStyle}>
                <Banner />
                <h2 style={headerStyle}>Match results — {tournament.name}</h2>
                <p style={{ color: 'rgba(255,255,255,0.5)' }}>
                    Bracket is not built yet. Build it from the tournament page first.
                </p>
                <Link to="/tournaments/$id" params={{ id }} style={{ color: '#c77dff' }}>
                    ← Back to tournament
                </Link>
            </div>
        )
    }

    const pushResult = (matchKey: string, slot: Slot) => {
        setLocalResults(prev => {
            const list = prev[matchKey] ?? []
            return { ...prev, [matchKey]: [...list, slot] }
        })
    }

    const popResult = (matchKey: string) => {
        setLocalResults(prev => {
            const list = prev[matchKey] ?? []
            if (!list.length) return prev
            return { ...prev, [matchKey]: list.slice(0, -1) }
        })
    }

    return (
        <div style={shellStyle}>
            <Banner />
            <div
                style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    marginBottom: 16,
                }}
            >
                <h2 style={headerStyle}>Match results — {tournament.name}</h2>
                <Link to="/tournaments/$id" params={{ id }} style={{ color: '#c77dff' }}>
                    ← Back
                </Link>
            </div>
            <p style={{ color: 'rgba(255,255,255,0.5)', marginTop: 0 }}>
                Local-only: clicks update an in-memory log per match — nothing is sent
                to the server. Backend wiring lands once the read-side endpoint exists.
            </p>
            {tournament.bracket.rounds.map((round, ri) => (
                <section key={ri} style={{ marginTop: 24 }}>
                    <h3
                        style={{
                            borderBottom: '1px solid rgba(166,0,255,0.25)',
                            paddingBottom: 6,
                            color: 'rgba(255,255,255,0.78)',
                            fontFamily: "'Russo One', sans-serif",
                            fontSize: 14,
                            letterSpacing: '0.08em',
                            textTransform: 'uppercase',
                        }}
                    >
                        Round {ri + 1}
                        {tournament.bracket?.round_settings.find(s => s.round === ri)?.label
                            ? ` — ${tournament.bracket?.round_settings.find(s => s.round === ri)?.label}`
                            : null}
                    </h3>
                    {round.map(match => {
                        const matchKey = `${ri}:${match.match_number}`
                        return (
                            <MatchCard
                                key={matchKey}
                                match={match}
                                actorLabel={actorLabel}
                                results={localResults[matchKey] ?? []}
                                onWinner={slot => pushResult(matchKey, slot)}
                                onUndo={() => popResult(matchKey)}
                            />
                        )
                    })}
                </section>
            ))}
        </div>
    )
}

function MatchCard({
    match,
    actorLabel,
    results,
    onWinner,
    onUndo,
}: {
    match: MatchResponse
    actorLabel: (a: Actor | null) => string
    results: Array<'team1' | 'team2'>
    onWinner: (slot: 'team1' | 'team2') => void
    onUndo: () => void
}) {
    const teamsAssigned = !!(match.team1 && match.team2)
    const team1Wins = results.filter(r => r === 'team1').length
    const team2Wins = results.filter(r => r === 'team2').length
    const needed = Math.floor((match.best_of || 1) / 2) + 1
    const localSeriesWinner: 'team1' | 'team2' | null =
        team1Wins >= needed ? 'team1' : team2Wins >= needed ? 'team2' : null
    const serverWinnerLabel = match.winner ? actorLabel(match.winner) : null

    const btnBase: React.CSSProperties = {
        color: '#fff',
        border: '1px solid rgba(166,0,255,0.35)',
        padding: '6px 14px',
        borderRadius: 6,
        cursor: teamsAssigned ? 'pointer' : 'not-allowed',
        background: 'rgba(166,0,255,0.14)',
        fontFamily: "'Chakra Petch', monospace",
        fontSize: 11,
        letterSpacing: '0.05em',
        opacity: teamsAssigned ? 1 : 0.4,
    }
    const winnerBtnStyle = (slot: 'team1' | 'team2'): React.CSSProperties => ({
        ...btnBase,
        background: localSeriesWinner === slot
            ? 'rgba(16,185,129,0.35)'
            : 'rgba(166,0,255,0.14)',
        borderColor: localSeriesWinner === slot
            ? 'rgba(16,185,129,0.55)'
            : 'rgba(166,0,255,0.35)',
    })
    const loserBtnStyle = (slot: 'team1' | 'team2'): React.CSSProperties => ({
        ...btnBase,
        background: 'rgba(255,0,42,0.10)',
        borderColor: 'rgba(255,0,42,0.35)',
        // Clicking "team1 loses" is recorded as "team2 wins" — same as below.
        opacity: teamsAssigned ? 0.85 : 0.4,
    })

    return (
        <div
            style={{
                border: '1px solid rgba(166,0,255,0.18)',
                borderRadius: 10,
                padding: 14,
                marginBottom: 12,
                background: 'rgba(20,12,30,0.65)',
            }}
        >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <strong style={{ color: 'rgba(255,255,255,0.92)' }}>
                    Match #{match.match_number} (BO{match.best_of}) — {actorLabel(match.team1)} vs {actorLabel(match.team2)}
                </strong>
                <span style={{ display: 'flex', gap: 12, fontSize: 11 }}>
                    <span style={{ color: 'rgba(255,255,255,0.6)' }}>
                        local: {team1Wins}–{team2Wins}
                    </span>
                    {serverWinnerLabel && (
                        <span style={{ color: '#7fff7f' }}>server: {serverWinnerLabel}</span>
                    )}
                    {localSeriesWinner && (
                        <span style={{ color: '#7fff7f' }}>
                            clinched: {actorLabel(localSeriesWinner === 'team1' ? match.team1 : match.team2)}
                        </span>
                    )}
                </span>
            </div>

            {!teamsAssigned ? (
                <div style={{ marginTop: 8, color: 'rgba(255,255,255,0.4)', fontSize: 11 }}>
                    Waiting on earlier matches to determine participants.
                </div>
            ) : (
                <>
                    {/* Two pairs of buttons per side: explicit winner OR explicit loser. */}
                    <div style={{ marginTop: 10, display: 'flex', gap: 16, flexWrap: 'wrap' }}>
                        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                            <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: 11, marginRight: 4 }}>
                                {actorLabel(match.team1)}:
                            </span>
                            <button
                                disabled={!teamsAssigned}
                                onClick={() => onWinner('team1')}
                                style={winnerBtnStyle('team1')}
                            >
                                Set winner
                            </button>
                            <button
                                disabled={!teamsAssigned}
                                onClick={() => onWinner('team2')}
                                style={loserBtnStyle('team1')}
                                title="Recorded as the other team winning this game"
                            >
                                Set loser
                            </button>
                        </div>
                        <div style={{ display: 'flex', gap: 6, alignItems: 'center' }}>
                            <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: 11, marginRight: 4 }}>
                                {actorLabel(match.team2)}:
                            </span>
                            <button
                                disabled={!teamsAssigned}
                                onClick={() => onWinner('team2')}
                                style={winnerBtnStyle('team2')}
                            >
                                Set winner
                            </button>
                            <button
                                disabled={!teamsAssigned}
                                onClick={() => onWinner('team1')}
                                style={loserBtnStyle('team2')}
                                title="Recorded as the other team winning this game"
                            >
                                Set loser
                            </button>
                        </div>
                        <button
                            disabled={!results.length}
                            onClick={onUndo}
                            style={{
                                ...btnBase,
                                background: 'rgba(255,255,255,0.05)',
                                borderColor: 'rgba(255,255,255,0.2)',
                                opacity: results.length ? 1 : 0.4,
                            }}
                        >
                            Undo last
                        </button>
                    </div>

                    {/* Game-by-game history, so the host can see what they pressed. */}
                    {results.length > 0 && (
                        <div style={{ marginTop: 10, display: 'flex', gap: 6, flexWrap: 'wrap' }}>
                            {results.map((slot, i) => (
                                <span
                                    key={i}
                                    style={{
                                        fontSize: 10,
                                        color: 'rgba(255,255,255,0.7)',
                                        background: 'rgba(166,0,255,0.10)',
                                        border: '1px solid rgba(166,0,255,0.25)',
                                        padding: '2px 8px',
                                        borderRadius: 4,
                                    }}
                                >
                                    Game {i + 1}: {actorLabel(slot === 'team1' ? match.team1 : match.team2)}
                                </span>
                            ))}
                        </div>
                    )}
                </>
            )}
        </div>
    )
}
