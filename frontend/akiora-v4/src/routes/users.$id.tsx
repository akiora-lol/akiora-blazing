import { createFileRoute, Link } from '@tanstack/react-router'
import { FiArrowLeft, FiShield, FiUserPlus } from 'react-icons/fi'
import { PageShell } from '../components/PageShell'
import { useAuthContext } from '../contexts/AuthContext'
import { useSendFriendRequestMutation, useUserProfile } from '../lib/api'

export const Route = createFileRoute('/users/$id')({
    component: UserProfilePage,
})

function UserProfilePage() {
    const { id } = Route.useParams()
    const { user: currentUser } = useAuthContext()
    const { data: user, isLoading } = useUserProfile(id)
    const sendFriend = useSendFriendRequestMutation()

    return (
        <PageShell lang="ru" onLangChange={() => undefined}>
            <style>{`
                .public-profile-page {
                    position: relative;
                    z-index: 10;
                    min-height: 100vh;
                    padding: 92px 24px 48px;
                    color: #fff;
                    display: grid;
                    place-items: center;
                }
                .public-profile {
                    width: min(720px, calc(100vw - 32px));
                    border: 1px solid rgba(255,255,255,0.1);
                    border-radius: 8px;
                    background:
                        linear-gradient(135deg, rgba(45,212,191,0.1), rgba(166,0,255,0.08)),
                        rgba(5,8,18,0.9);
                    backdrop-filter: blur(18px);
                    padding: 22px;
                    box-shadow: 0 24px 90px rgba(0,0,0,0.46);
                }
                .public-profile-top {
                    display: flex;
                    align-items: center;
                    gap: 16px;
                    margin-bottom: 18px;
                }
                .public-avatar {
                    width: 82px;
                    height: 82px;
                    border-radius: 50%;
                    border: 2px solid rgba(45,212,191,0.42);
                    background: rgba(255,255,255,0.06);
                    display: grid;
                    place-items: center;
                    overflow: hidden;
                    font-family: 'Russo One', sans-serif;
                    font-size: 24px;
                }
                .public-avatar img { width: 100%; height: 100%; object-fit: cover; }
                .public-name {
                    margin: 0 0 6px;
                    font-family: 'Russo One', sans-serif;
                    font-size: 28px;
                    letter-spacing: 0;
                }
                .public-email {
                    color: rgba(255,255,255,0.42);
                    font-size: 12px;
                    overflow-wrap: anywhere;
                }
                .public-bio {
                    color: rgba(255,255,255,0.72);
                    line-height: 1.65;
                    margin: 18px 0;
                }
                .public-meta {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                    margin-bottom: 18px;
                }
                .public-pill {
                    display: inline-flex;
                    align-items: center;
                    gap: 6px;
                    height: 30px;
                    padding: 0 10px;
                    border-radius: 999px;
                    border: 1px solid rgba(255,255,255,0.1);
                    color: rgba(255,255,255,0.72);
                    background: rgba(255,255,255,0.05);
                    font: 700 11px 'Chakra Petch', monospace;
                    text-transform: uppercase;
                }
                .public-actions {
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }
                .public-btn {
                    height: 38px;
                    padding: 0 14px;
                    border-radius: 6px;
                    border: 1px solid rgba(255,255,255,0.12);
                    background: rgba(255,255,255,0.06);
                    color: #fff;
                    display: inline-flex;
                    align-items: center;
                    gap: 8px;
                    text-decoration: none;
                    cursor: pointer;
                    font: 800 12px 'Chakra Petch', monospace;
                    text-transform: uppercase;
                }
                .public-btn.primary {
                    border-color: rgba(45,212,191,0.42);
                    background: rgba(45,212,191,0.12);
                }
                .public-btn:disabled { opacity: .5; cursor: not-allowed; }
            `}</style>
            <main className="public-profile-page">
                <section className="public-profile">
                    {isLoading || !user ? (
                        <div className="public-bio">Loading...</div>
                    ) : (
                        <>
                            <div className="public-profile-top">
                                <div className="public-avatar">
                                    {user.avatar ? <img src={user.avatar} alt="" /> : user.nickname.slice(0, 2).toUpperCase()}
                                </div>
                                <div>
                                    <h1 className="public-name">{user.nickname}</h1>
                                    <div className="public-email">{user.email}</div>
                                </div>
                            </div>
                            <div className="public-meta">
                                <span className="public-pill"><FiShield size={13} /> {user.user_type}</span>
                                <span className="public-pill">{user.league_accounts?.length ?? 0} League</span>
                            </div>
                            <p className="public-bio">{user.bio || 'Пользователь пока не добавил описание.'}</p>
                            <div className="public-actions">
                                <Link className="public-btn" to="/community">
                                    <FiArrowLeft size={14} />
                                    Community
                                </Link>
                                {currentUser && currentUser.id !== user.id && (
                                    <button
                                        className="public-btn primary"
                                        disabled={sendFriend.isPending}
                                        onClick={() => sendFriend.mutate({ senderId: currentUser.id, receiverId: user.id })}
                                    >
                                        <FiUserPlus size={14} />
                                        Добавить в друзья
                                    </button>
                                )}
                            </div>
                        </>
                    )}
                </section>
            </main>
        </PageShell>
    )
}
