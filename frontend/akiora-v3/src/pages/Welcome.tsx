import { useTranslation } from 'react-i18next'
import { Button } from '@/components/ui/button.js'
import { Card, CardContent } from '@/components/ui/card.js'

export function Welcome() {
    const { t } = useTranslation()

    return (
        <div className="relative min-h-[calc(100vh-4rem)] overflow-hidden">
            {/* Background Effects */}
            <div className="absolute inset-0 bg-gradient-to-b from-primary/5 via-transparent to-accent/5" />
            <div className="absolute top-1/4 left-1/4 w-96 h-96 bg-primary/20 rounded-full blur-[128px]" />
            <div className="absolute bottom-1/4 right-1/4 w-96 h-96 bg-accent/20 rounded-full blur-[128px]" />

            {/* Grid Pattern */}
            <div
                className="absolute inset-0 opacity-[0.03]"
                style={{
                    backgroundImage: `linear-gradient(white 1px, transparent 1px), linear-gradient(90deg, white 1px, transparent 1px)`,
                    backgroundSize: '64px 64px'
                }}
            />

            {/* Hero Content */}
            <div className="container mx-auto px-4 py-20 relative z-10">
                <div className="flex flex-col lg:flex-row items-center gap-12 min-h-[70vh]">
                    {/* Left Side - Content */}
                    <div className="flex-1 text-center lg:text-left">
                        {/* Badge */}
                        <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-primary/10 border border-primary/20 mb-6 animate-pulse-glow">
                            <span className="w-2 h-2 rounded-full bg-primary" />
                            <span className="text-sm text-primary font-medium">Season 2026</span>
                        </div>

                        {/* Title */}
                        <h1 className="text-5xl md:text-7xl font-black mb-4">
                            <span className="bg-gradient-to-r from-primary via-red-400 to-accent bg-clip-text text-transparent text-glow-red">
                                {t('welcome.title')}
                            </span>
                        </h1>

                        {/* Subtitle */}
                        <p className="text-2xl md:text-3xl text-text-muted mb-6 font-light">
                            {t('welcome.subtitle')}
                        </p>

                        {/* Description */}
                        <p className="text-lg text-text-muted/80 mb-8 max-w-xl mx-auto lg:mx-0">
                            {t('welcome.description')}
                        </p>

                        {/* CTA Buttons */}
                        <div className="flex flex-col sm:flex-row items-center gap-4 justify-center lg:justify-start">
                            <Button variant="default" size="lg" className="w-full sm:w-auto px-8">
                                {t('welcome.getStarted')}
                            </Button>
                            <Button variant="accent" size="lg" className="w-full sm:w-auto px-8">
                                {t('welcome.learnMore')}
                            </Button>
                        </div>

                        {/* Stats */}
                        <div className="grid grid-cols-3 gap-8 mt-12 pt-8 border-t border-white/10">
                            <div>
                                <div className="text-3xl font-bold text-primary text-glow-red">160+</div>
                                <div className="text-sm text-text-muted">Champions</div>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-accent text-glow-cyan">200+</div>
                                <div className="text-sm text-text-muted">Items</div>
                            </div>
                            <div>
                                <div className="text-3xl font-bold text-primary text-glow-red">1M+</div>
                                <div className="text-sm text-text-muted">Builds</div>
                            </div>
                        </div>
                    </div>

                    {/* Right Side - Visual */}
                    <div className="flex-1 relative">
                        <div className="relative w-full max-w-lg mx-auto">
                            {/* Animated Rings */}
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="w-[400px] h-[400px] border border-primary/20 rounded-full animate-[spin_20s_linear_infinite]" />
                            </div>
                            <div className="absolute inset-0 flex items-center justify-center">
                                <div className="w-[300px] h-[300px] border border-accent/20 rounded-full animate-[spin_15s_linear_infinite_reverse]" />
                            </div>

                            {/* Main Logo */}
                            <div className="relative z-10 animate-float">
                                <Card className="bg-surface/50 backdrop-blur-xl border-primary/20 glow-red overflow-hidden">
                                    <CardContent className="p-8">
                                        <div className="flex items-center justify-center gap-6">
                                            <img
                                                src="/red-yang.svg"
                                                alt="Red Yang"
                                                className="w-32 h-32 object-contain drop-shadow-[0_0_30px_rgba(255,0,42,0.6)]"
                                            />
                                            <img
                                                src="/blue-yang.svg"
                                                alt="Blue Yang"
                                                className="w-32 h-32 object-contain drop-shadow-[0_0_30px_rgba(6,182,212,0.6)]"
                                            />
                                        </div>
                                    </CardContent>
                                </Card>
                            </div>

                            {/* Floating Elements */}
                            <div className="absolute -top-4 -right-4 w-20 h-20 bg-primary/30 rounded-full blur-2xl animate-pulse" />
                            <div className="absolute -bottom-4 -left-4 w-20 h-20 bg-accent/30 rounded-full blur-2xl animate-pulse" style={{ animationDelay: '1s' }} />
                        </div>
                    </div>
                </div>

                {/* Feature Cards */}
                <div className="grid md:grid-cols-3 gap-6 mt-20">
                    <Card className="bg-surface/50 backdrop-blur-xl border-white/10 hover:border-primary/50 transition-all duration-300 group">
                        <CardContent className="p-6">
                            <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center mb-4 group-hover:glow-red transition-all duration-300">
                                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M13 10V3L4 14h7v7l9-11h-7z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold mb-2 text-glow-red">Champion Guides</h3>
                            <p className="text-text-muted">Master every champion with detailed guides, combos, and matchup analysis.</p>
                        </CardContent>
                    </Card>

                    <Card className="bg-surface/50 backdrop-blur-xl border-white/10 hover:border-accent/50 transition-all duration-300 group">
                        <CardContent className="p-6">
                            <div className="w-12 h-12 rounded-lg bg-accent/20 flex items-center justify-center mb-4 group-hover:glow-cyan transition-all duration-300">
                                <svg className="w-6 h-6 text-accent" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold mb-2 text-glow-cyan">Build Analytics</h3>
                            <p className="text-text-muted">Discover optimal builds with data-driven item recommendations and win rates.</p>
                        </CardContent>
                    </Card>

                    <Card className="bg-surface/50 backdrop-blur-xl border-white/10 hover:border-primary/50 transition-all duration-300 group">
                        <CardContent className="p-6">
                            <div className="w-12 h-12 rounded-lg bg-primary/20 flex items-center justify-center mb-4 group-hover:glow-red transition-all duration-300">
                                <svg className="w-6 h-6 text-primary" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0112 2.944a11.955 11.955 0 01-8.618 3.04A12.02 12.02 0 003 9c0 5.591 3.824 10.29 9 11.622 5.176-1.332 9-6.03 9-11.622 0-1.042-.133-2.052-.382-3.016z" />
                                </svg>
                            </div>
                            <h3 className="text-xl font-semibold mb-2 text-glow-red">Rank Tracking</h3>
                            <p className="text-text-muted">Track your progress and climb the ladder with personalized insights.</p>
                        </CardContent>
                    </Card>
                </div>
            </div>
        </div>
    )
}
