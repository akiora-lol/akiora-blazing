import { createFileRoute, Link } from '@tanstack/react-router'
import { useMemo, useState } from 'react'
import { useAuthContext } from '../contexts/AuthContext'
import {
    type Actor,
    type MatchResponse,
    type TeamResponse,
    useSeriesView,
    useSetGameWinnerMutation,
    useTeams,
    useTournament,
} from '../lib/api'

export const Route = createFileRoute('/tournaments/$id/results')({
    component: TournamentResultsPage,
})

/**
 * Host-only screen for reporting per-game winners.
 *
 * Server-wired: each Match in the bracket loads its own SeriesView via
 * `GET /v1/game-series/{id}` to learn the real `game_id`s, then submits per
 * game with `POST /v1/game-series/{sid}/games/{gid}/winner`. The backend
 * re-tallies wins, closes the series on clinch, propagates the winner into
 * the next bracket match (SE), and auto-finishes the tournament on the
 * final. We just invalidate and re-render.
 */
function TournamentResultsPage() {
    const { id } = Route.useParams()
    const { user } = useAuthContext()
    const { data: tournament, isLoading, error } = useTournament(id)
    const { data: allTeams } = useTeams()

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

    const matches: MatchResponse[] = useMemo(
        () => tournament?.bracket?.rounds.flat() ?? [],
        [tournament?.bracket],
    )

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

    if (isLoading) {
        return (
            <div style={shellStyle}>
                <h2 style={headerStyle}>Match results</h2>
                <p style={{ color: 'rgba(255,255,255,0.5)' }}>Loading tournament…</p>
            </div>
        )
    }
    if (error) {
        return (
            <div style={shellStyle}>
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

    return (
        <div style={shellStyle}>
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
                Set winner per game. Each click hits the server; the bracket advances
                automatically when a series clinches.
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
                    {round.map(match => (
                        <MatchCard
                            key={`${ri}:${match.match_number}`}
                            tournamentId={id}
                            match={match}
                            actorId={user.id}
                            actorLabel={actorLabel}
                        />
                    ))}
                </section>
            ))}
        </div>
    )
}

function MatchCard({
    tournamentId,
    match,
    actorId,
    actorLabel,
}: {
    tournamentId: string
    match: MatchResponse
    actorId: string
    actorLabel: (a: Actor | null) => string
}) {
    const teamsAssigned = !!(match.team1 && match.team2)
    // Diagnostic: surface the series id and query state into the UI so we can
    // tell "endpoint never called" from "endpoint pending" from "endpoint failed".
    const seriesQuery = useSeriesView(
        teamsAssigned ? match.game_series_id : null,
    )
    const { data: series, isLoading: seriesLoading, isFetching: seriesFetching, error: seriesError, refetch } = seriesQuery
    const { mutateAsync, isPending } = useSetGameWinnerMutation(tournamentId)
    const [error, setError] = useState<string | null>(null)
    const [submitting, setSubmitting] = useState<string | null>(null) // game_id in flight

    const submitWinner = async (gameId: string, winner: Actor) => {
        setError(null)
        setSubmitting(gameId)
        try {
            await mutateAsync({
                seriesId: match.game_series_id,
                gameId,
                actorId,
                winner,
            })
            await refetch()
        } catch (e) {
            setError(e instanceof Error ? e.message : String(e))
        } finally {
            setSubmitting(null)
        }
    }

    const btnBase: React.CSSProperties = {
        color: '#fff',
        border: '1px solid rgba(166,0,255,0.35)',
        padding: '6px 12px',
        borderRadius: 6,
        cursor: 'pointer',
        background: 'rgba(166,0,255,0.14)',
        fontFamily: "'Chakra Petch', monospace",
        fontSize: 11,
        letterSpacing: '0.05em',
    }
    const winnerActiveStyle: React.CSSProperties = {
        background: 'rgba(16,185,129,0.35)',
        borderColor: 'rgba(16,185,129,0.55)',
    }
    const loserStyle: React.CSSProperties = {
        background: 'rgba(255,0,42,0.10)',
        borderColor: 'rgba(255,0,42,0.35)',
    }
    const disabledStyle: React.CSSProperties = {
        cursor: 'not-allowed',
        opacity: 0.5,
    }

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
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', gap: 12 }}>
                <strong style={{ color: 'rgba(255,255,255,0.92)' }}>
                    Match #{match.match_number} (BO{match.best_of}) — {actorLabel(match.team1)} vs {actorLabel(match.team2)}
                </strong>
                {match.winner && (
                    <span style={{ color: '#7fff7f', fontSize: 11 }}>
                        series winner: {actorLabel(match.winner)}
                    </span>
                )}
            </div>

            {!teamsAssigned ? (
                <div style={{ marginTop: 8, color: 'rgba(255,255,255,0.4)', fontSize: 11 }}>
                    Waiting on earlier matches to determine participants.
                </div>
            ) : seriesLoading ? (
                <div style={{ marginTop: 8, color: 'rgba(255,255,255,0.5)', fontSize: 11 }}>
                    Loading series {match.game_series_id.slice(0, 8)}… (fetching={String(seriesFetching)})
                </div>
            ) : seriesError ? (
                <div style={{ marginTop: 8, color: '#ff7f7f', fontSize: 11 }}>
                    Series load error: {seriesError instanceof Error ? seriesError.message : String(seriesError)}
                </div>
            ) : !series ? (
                <div style={{ marginTop: 8, color: '#ff7f7f', fontSize: 11 }}>
                    Failed to load series games (series_id={match.game_series_id}).
                </div>
            ) : (
                <div style={{ marginTop: 10, display: 'flex', flexDirection: 'column', gap: 8 }}>
                    {series.games.map((g, i) => {
                        const finished = g.status === 'finished'
                        const winnerSlot: 'team1' | 'team2' | null =
                            g.winner && match.team1 && g.winner.id === match.team1.id
                                ? 'team1'
                                : g.winner && match.team2 && g.winner.id === match.team2.id
                                    ? 'team2'
                                    : null
                        const inFlight = submitting === g.id
                        const locked = isPending && !inFlight
                        return (
                            <div key={g.id} style={{ display: 'flex', alignItems: 'center', gap: 8, flexWrap: 'wrap' }}>
                                <span style={{ color: 'rgba(255,255,255,0.55)', fontSize: 11, minWidth: 64 }}>
                                    Game {i + 1}
                                </span>
                                <span style={{
                                    color: finished ? '#7fff7f' : 'rgba(255,255,255,0.45)',
                                    fontSize: 10,
                                    minWidth: 70,
                                }}>
                                    {g.status}
                                </span>
                                <button
                                    disabled={inFlight || locked || !match.team1}
                                    onClick={() => match.team1 && submitWinner(g.id, match.team1)}
                                    style={{
                                        ...btnBase,
                                        ...(winnerSlot === 'team1' ? winnerActiveStyle : {}),
                                        ...(inFlight || locked ? disabledStyle : {}),
                                    }}
                                >
                                    {actorLabel(match.team1)} wins
                                </button>
                                <button
                                    disabled={inFlight || locked || !match.team2}
                                    onClick={() => match.team2 && submitWinner(g.id, match.team2)}
                                    style={{
                                        ...btnBase,
                                        ...(winnerSlot === 'team2' ? winnerActiveStyle : {}),
                                        ...(inFlight || locked ? disabledStyle : {}),
                                    }}
                                >
                                    {actorLabel(match.team2)} wins
                                </button>
                                <span style={{ color: 'rgba(255,255,255,0.3)', fontSize: 11 }}>·</span>
                                <button
                                    disabled={inFlight || locked || !match.team2}
                                    onClick={() => match.team2 && submitWinner(g.id, match.team2)}
                                    title="Equivalent to 'team2 wins' — recorded server-side as a win for the other team"
                                    style={{
                                        ...btnBase,
                                        ...loserStyle,
                                        ...(inFlight || locked ? disabledStyle : {}),
                                    }}
                                >
                                    {actorLabel(match.team1)} loses
                                </button>
                                <button
                                    disabled={inFlight || locked || !match.team1}
                                    onClick={() => match.team1 && submitWinner(g.id, match.team1)}
                                    title="Equivalent to 'team1 wins' — recorded server-side as a win for the other team"
                                    style={{
                                        ...btnBase,
                                        ...loserStyle,
                                        ...(inFlight || locked ? disabledStyle : {}),
                                    }}
                                >
                                    {actorLabel(match.team2)} loses
                                </button>
                                {inFlight && (
                                    <span style={{ color: 'rgba(255,255,255,0.5)', fontSize: 10 }}>submitting…</span>
                                )}
                            </div>
                        )
                    })}
                    {series.games.length === 0 && (
                        <div style={{ color: 'rgba(255,255,255,0.4)', fontSize: 11 }}>
                            No games scheduled in this series yet.
                        </div>
                    )}
                </div>
            )}
            {error && <div style={{ marginTop: 8, color: '#ff7f7f', fontSize: 11 }}>{error}</div>}
        </div>
    )
}
