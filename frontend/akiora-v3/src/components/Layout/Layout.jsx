import { Link, useLocation } from 'react-router-dom'
import { useTranslation } from 'react-i18next'
import { LanguageSwitcher } from '../ui/LanguageSwitcher'
import { Button } from '../ui/Button'
import { cn } from '../../lib/utils'

export function Layout({ children }) {
  const location = useLocation()
  const { t } = useTranslation()

  const navItems = [
    { path: '/', label: t('nav.home') },
    { path: '/champions', label: t('nav.champions') },
    { path: '/items', label: t('nav.items') },
    { path: '/builds', label: t('nav.builds') }
  ]

  return (
    <div className="min-h-screen bg-background flex flex-col">
      {/* Navigation */}
      <header className="sticky top-0 z-50 w-full border-b border-white/10 bg-background/80 backdrop-blur-xl">
        <div className="container mx-auto px-4 h-16 flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center gap-3 group">
            <div className="relative w-10 h-10">
              <img
                src="/red-yang.svg"
                alt="Logo"
                className="w-full h-full object-contain drop-shadow-[0_0_10px_rgba(255,0,42,0.5)] group-hover:drop-shadow-[0_0_20px_rgba(255,0,42,0.8)] transition-all duration-300"
              />
            </div>
            <span className="text-xl font-bold text-glow-red">AKIORA</span>
          </Link>

          {/* Navigation Links */}
          <nav className="hidden md:flex items-center gap-1">
            {navItems.map((item) => (
              <Link
                key={item.path}
                to={item.path}
                className={cn(
                  'px-4 py-2 rounded-md text-sm font-medium transition-all duration-300',
                  location.pathname === item.path
                    ? 'text-primary bg-primary/10 glow-red'
                    : 'text-text-muted hover:text-white hover:bg-white/5'
                )}
              >
                {item.label}
              </Link>
            ))}
          </nav>

          {/* Right Side */}
          <div className="flex items-center gap-4">
            <LanguageSwitcher />
            <Button variant="accent" size="sm" className="hidden sm:flex">
              Sign In
            </Button>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1">{children}</main>

      {/* Footer */}
      <footer className="border-t border-white/10 bg-surface">
        <div className="container mx-auto px-4 py-8">
          <div className="flex flex-col md:flex-row items-center justify-between gap-4">
            <div className="flex items-center gap-3">
              <img
                src="/blue-yang.svg"
                alt="Logo"
                className="w-8 h-8 object-contain"
              />
              <span className="text-sm text-text-muted">
                © 2026 Akiora. All rights reserved.
              </span>
            </div>
            <div className="flex items-center gap-6">
              <a
                href="#"
                className="text-text-muted hover:text-accent transition-colors"
              >
                Privacy
              </a>
              <a
                href="#"
                className="text-text-muted hover:text-accent transition-colors"
              >
                Terms
              </a>
              <a
                href="#"
                className="text-text-muted hover:text-accent transition-colors"
              >
                Contact
              </a>
            </div>
          </div>
        </div>
      </footer>
    </div>
  )
}
