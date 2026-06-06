import { createFileRoute, Outlet } from '@tanstack/react-router'

export const Route = createFileRoute('/gameseries/$id')({ component: () => <Outlet /> })
