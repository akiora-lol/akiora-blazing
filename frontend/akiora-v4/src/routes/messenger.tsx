import { createFileRoute } from '@tanstack/react-router'
import { useState, useRef, useEffect } from 'react'
import { FiSend, FiMessageSquare } from 'react-icons/fi'
import { AkioraBackground } from '../components/PageShell'
import { useAuthContext } from '../contexts/AuthContext'
import { useUserChats, useMessages, useSendMessage, type ChatResponse, type MessageResponse } from '../lib/api'

export const Route = createFileRoute('/messenger')({
    validateSearch: (search: Record<string, unknown>) => ({
        chat: typeof search.chat === 'string' ? search.chat : undefined,
    }),
    component: MessengerPage,
})

function formatTime(timestamp: number) {
    const date = new Date(timestamp * 1000)
    return date.toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' })
}

function formatDate(timestamp: number) {
    const date = new Date(timestamp * 1000)
    const today = new Date()
    const yesterday = new Date(today)
    yesterday.setDate(yesterday.getDate() - 1)

    if (date.toDateString() === today.toDateString()) return 'Today'
    if (date.toDateString() === yesterday.toDateString()) return 'Yesterday'
    return date.toLocaleDateString([], { day: 'numeric', month: 'short' })
}

function ChatListItem({ chat, isSelected, onClick }: { chat: ChatResponse; isSelected: boolean; onClick: () => void }) {
    const getChatName = () => {
        switch (chat.owner_type) {
            case 'CLUB': return 'Club Chat'
            case 'TOURNAMENT': return 'Tournament'
            case 'GAMESERIES': return 'Game Series'
            case 'SYSTEM': return 'System'
            default: return 'Private Chat'
        }
    }

    return (
        <button
            onClick={onClick}
            className={`chat-list-item ${isSelected ? 'selected' : ''}`}
            style={{
                width: '100%',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                padding: '14px 16px',
                background: isSelected ? 'rgba(166,0,255,0.08)' : 'transparent',
                border: 'none',
                borderBottom: '1px solid rgba(255,255,255,0.03)',
                cursor: 'pointer',
                textAlign: 'left',
                transition: 'background 150ms',
            }}
        >
            <div
                style={{
                    width: '38px',
                    height: '38px',
                    borderRadius: '10px',
                    background: 'rgba(166,0,255,0.1)',
                    border: '1px solid rgba(166,0,255,0.15)',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    flexShrink: 0,
                }}
            >
                <FiMessageSquare size={16} color="rgba(166,0,255,0.7)" />
            </div>
            <div style={{ flex: 1, minWidth: 0 }}>
                <p style={{
                    margin: 0,
                    fontSize: '13px',
                    fontWeight: 600,
                    color: '#fff',
                    fontFamily: "'Chakra Petch', monospace",
                    whiteSpace: 'nowrap',
                    overflow: 'hidden',
                    textOverflow: 'ellipsis',
                }}>
                    {getChatName()}
                </p>
                <p style={{
                    margin: '2px 0 0',
                    fontSize: '11px',
                    color: 'rgba(255,255,255,0.5)',
                    fontFamily: "'Chakra Petch', monospace",
                }}>
                    {chat.type === 'PUBLIC' ? 'Public' : 'Private'} • {formatDate(chat.timestamp)}
                </p>
            </div>
        </button>
    )
}

function MessageBubble({ message, isOwn, showDate }: { message: MessageResponse; isOwn: boolean; showDate: boolean }) {
    return (
        <div style={{ display: 'flex', flexDirection: 'column', alignItems: isOwn ? 'flex-end' : 'flex-start' }}>
            {showDate && (
                <p style={{
                    margin: '16px 0 8px',
                    fontSize: '10px',
                    color: 'rgba(255,255,255,0.25)',
                    fontFamily: "'Chakra Petch', monospace",
                    letterSpacing: '0.1em',
                    textTransform: 'uppercase',
                }}>
                    {formatDate(message.timestamp)}
                </p>
            )}
            <div
                style={{
                    maxWidth: '70%',
                    padding: '10px 14px',
                    borderRadius: isOwn ? '14px 14px 4px 14px' : '14px 14px 14px 4px',
                    background: isOwn
                        ? 'rgba(166,0,255,0.12)'
                        : 'rgba(255,255,255,0.04)',
                    border: isOwn ? '1px solid rgba(166,0,255,0.2)' : '1px solid rgba(255,255,255,0.04)',
                }}
            >
                <p style={{
                    margin: 0,
                    fontSize: '13px',
                    color: '#fff',
                    fontFamily: "'Chakra Petch', monospace",
                    lineHeight: 1.5,
                    wordBreak: 'break-word',
                }}>
                    {message.body}
                </p>
                <p style={{
                    margin: '4px 0 0',
                    fontSize: '9px',
                    color: isOwn ? 'rgba(255,255,255,0.4)' : 'rgba(255,255,255,0.25)',
                    fontFamily: "'Chakra Petch', monospace",
                    textAlign: 'right',
                }}>
                    {formatTime(message.timestamp)}
                </p>
            </div>
        </div>
    )
}

function MessengerPage() {
    const { user } = useAuthContext()
    const search = Route.useSearch()
    const [selectedChatId, setSelectedChatId] = useState<string | null>(null)
    const [messageText, setMessageText] = useState('')
    const messagesEndRef = useRef<HTMLDivElement>(null)

    const { data: chats, isLoading: chatsLoading } = useUserChats(user?.id || '')
    const { data: messages, isLoading: messagesLoading } = useMessages(selectedChatId || '', 50)
    const sendMessageMutation = useSendMessage()

    useEffect(() => {
        if (search.chat && selectedChatId !== search.chat) {
            setSelectedChatId(search.chat)
            return
        }
        if (chats && chats.length > 0 && !selectedChatId) {
            setSelectedChatId(chats[0].id)
        }
    }, [chats, selectedChatId, search.chat])

    useEffect(() => {
        messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' })
    }, [messages])

    const handleSendMessage = async () => {
        if (!messageText.trim() || !selectedChatId || !user) return
        await sendMessageMutation.mutateAsync({
            chat_id: selectedChatId,
            creator_id: user.id,
            body: messageText.trim(),
        })
        setMessageText('')
    }

    const handleKeyDown = (e: React.KeyboardEvent) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault()
            handleSendMessage()
        }
    }

    let lastDate = 0

    return (
        <>
            <style>{`
                .messenger-page {
                    position: relative;
                    z-index: 10;
                    display: flex;
                    height: calc(100vh - 52px);
                    margin-top: 52px;
                    background: transparent;
                }
                .chat-sidebar {
                    width: 280px;
                    flex-shrink: 0;
                    background: rgba(0,0,0,0.25);
                    border-right: 1px solid rgba(166,0,255,0.06);
                    display: flex;
                    flex-direction: column;
                    backdrop-filter: blur(20px);
                }
                .chat-sidebar-header {
                    padding: 18px 18px 14px;
                    border-bottom: 1px solid rgba(166,0,255,0.06);
                }
                .chat-sidebar-title {
                    font-family: 'Russo One', sans-serif;
                    font-size: 14px;
                    color: rgba(255,255,255,0.85);
                    margin: 0;
                    letter-spacing: 0.06em;
                    text-transform: uppercase;
                }
                .chat-list { flex: 1; overflow-y: auto; }
                .chat-list::-webkit-scrollbar { width: 2px; }
                .chat-list::-webkit-scrollbar-track { background: transparent; }
                .chat-list::-webkit-scrollbar-thumb { background: rgba(166,0,255,0.15); border-radius: 2px; }
                .chat-list-item { transition: background 150ms !important; }
                .chat-list-item:hover { background: rgba(166,0,255,0.06) !important; }
                .chat-list-item.selected { background: rgba(166,0,255,0.1) !important; border-left: 2px solid rgba(166,0,255,0.5); }
                .chat-main {
                    flex: 1;
                    display: flex;
                    flex-direction: column;
                    min-width: 0;
                    background: rgba(0,0,0,0.25);
                }
                .chat-header {
                    padding: 14px 24px;
                    border-bottom: 1px solid rgba(166,0,255,0.06);
                    display: flex;
                    align-items: center;
                    gap: 12px;
                    background: rgba(0,0,0,0.25);
                    backdrop-filter: blur(12px);
                }
                .chat-header-icon {
                    width: 34px; height: 34px; border-radius: 8px;
                    background: rgba(166,0,255,0.1);
                    border: 1px solid rgba(166,0,255,0.15);
                    display: flex; align-items: center; justify-content: center;
                }
                .chat-header-title {
                    font-family: 'Chakra Petch', monospace;
                    font-size: 13px; font-weight: 500; color: rgba(255,255,255,0.85);
                }
                .messages-container {
                    flex: 1; overflow-y: auto;
                    padding: 24px; display: flex; flex-direction: column; gap: 10px;
                }
                .messages-container::-webkit-scrollbar { width: 2px; }
                .messages-container::-webkit-scrollbar-thumb { background: rgba(166,0,255,0.1); border-radius: 2px; }
                .empty-chat {
                    flex: 1; display: flex; flex-direction: column; align-items: center; justify-content: center;
                    gap: 12px; color: rgba(255,255,255,0.15);
                    font-family: 'Chakra Petch', monospace; font-size: 13px;
                }
                .message-input-wrap {
                    padding: 14px 18px;
                    border-top: 1px solid rgba(166,0,255,0.06);
                    display: flex; gap: 10px;
                    background: rgba(0,0,0,0.25);
                }
                .message-input {
                    flex: 1; padding: 10px 14px; border-radius: 10px;
                    background: rgba(255,255,255,0.03);
                    border: 1px solid rgba(255,255,255,0.06);
                    color: #fff; font-family: 'Chakra Petch', monospace; font-size: 13px;
                    outline: none; transition: border-color 180ms;
                }
                .message-input:focus { border-color: rgba(166,0,255,0.5); box-shadow: 0 0 0 2px rgba(166,0,255,0.06); }
                .message-input::placeholder { color: rgba(255,255,255,0.15); }
                .send-btn {
                    padding: 10px 18px; border-radius: 10px;
                    background: rgba(166,0,255,0.12);
                    border: 1px solid rgba(166,0,255,0.2);
                    color: rgba(255,255,255,0.85); font-family: 'Chakra Petch', monospace;
                    font-size: 12px; font-weight: 500; letter-spacing: 0.05em;
                    cursor: pointer; display: flex; align-items: center; gap: 7px;
                    transition: all 180ms;
                }
                .send-btn:hover:not(:disabled) { background: rgba(166,0,255,0.2); border-color: rgba(166,0,255,0.5); box-shadow: 0 0 12px rgba(166,0,255,0.15); }
                .send-btn:disabled { opacity: 0.3; cursor: not-allowed; }
                .loading-text {
                    color: rgba(255,255,255,0.2);
                    font-family: 'Chakra Petch', monospace; font-size: 12px;
                }
            `}</style>

            <div className="messenger-page">
                <aside className="chat-sidebar">
                    <div className="chat-sidebar-header">
                        <h2 className="chat-sidebar-title">Messages</h2>
                    </div>
                    <div className="chat-list">
                        {chatsLoading ? (
                            <p className="loading-text" style={{ padding: '20px', textAlign: 'center' }}>Loading...</p>
                        ) : chats && chats.length > 0 ? (
                            chats.map((chat) => (
                                <ChatListItem
                                    key={chat.id}
                                    chat={chat}
                                    isSelected={selectedChatId === chat.id}
                                    onClick={() => setSelectedChatId(chat.id)}
                                />
                            ))
                        ) : (
                            <p className="loading-text" style={{ padding: '20px', textAlign: 'center' }}>No chats yet</p>
                        )}
                    </div>
                </aside>

                <main className="chat-main">
                    {selectedChatId ? (
                        <>
                            <div className="chat-header">
                                <div className="chat-header-icon">
                                    <FiMessageSquare size={16} color="#fff" />
                                </div>
                                <span className="chat-header-title">
                                    {chats?.find(c => c.id === selectedChatId)?.owner_type === 'CLUB' ? 'Club Chat' :
                                        chats?.find(c => c.id === selectedChatId)?.owner_type === 'TOURNAMENT' ? 'Tournament' : 'Chat'}
                                </span>
                            </div>

                            <div className="messages-container">
                                {messagesLoading ? (
                                    <p className="loading-text">Loading...</p>
                                ) : messages && messages.length > 0 ? (
                                    <>
                                        {messages.map((message, idx) => {
                                            const currentDate = new Date(message.timestamp * 1000).toDateString()
                                            const showDate = currentDate !== new Date(lastDate * 1000).toDateString()
                                            lastDate = message.timestamp
                                            return (
                                                <MessageBubble
                                                    key={message.id}
                                                    message={message}
                                                    isOwn={message.creator_id === user?.id}
                                                    showDate={showDate || idx === 0}
                                                />
                                            )
                                        })}
                                        <div ref={messagesEndRef} />
                                    </>
                                ) : (
                                    <p className="loading-text">No messages yet</p>
                                )}
                            </div>

                            <div className="message-input-wrap">
                                <input
                                    type="text"
                                    className="message-input"
                                    placeholder="Type a message..."
                                    value={messageText}
                                    onChange={(e) => setMessageText(e.target.value)}
                                    onKeyDown={handleKeyDown}
                                />
                                <button
                                    className="send-btn"
                                    onClick={handleSendMessage}
                                    disabled={!messageText.trim() || sendMessageMutation.isPending}
                                >
                                    <FiSend size={14} />
                                    Send
                                </button>
                            </div>
                        </>
                    ) : (
                        <div className="empty-chat">
                            <FiMessageSquare size={32} style={{ opacity: 0.3 }} />
                            Select a chat to start messaging
                        </div>
                    )}
                </main>
            </div>
        </>
    )
}
