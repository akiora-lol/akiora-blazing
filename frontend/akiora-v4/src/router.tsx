import { createRouter as createTanStackRouter } from '@tanstack/react-router'
import { routeTree } from './routeTree.gen'

import { QueryClient } from '@tanstack/react-query'
import { setupRouterSsrQueryIntegration } from '@tanstack/react-router-ssr-query'
import TanstackQueryProvider, {
    getContext,
} from './integrations/tanstack-query/root-provider'
import { ServerErrorPage } from './components/ErrorPages'

export function getRouter() {
    const context = getContext()

    const router = createTanStackRouter({
        routeTree,
        context,
        scrollRestoration: true,
        defaultPreload: 'intent',
        defaultPreloadStaleTime: 0,
        defaultErrorComponent: ({ error, reset }) => (
            <ServerErrorPage
                error={error instanceof Error ? error : new Error(String(error))}
                onRetry={reset}
            />
        ),
    })

    setupRouterSsrQueryIntegration({ router, queryClient: context.queryClient })

    return router
}

declare module '@tanstack/react-router' {
    interface Register {
        router: ReturnType<typeof getRouter>
    }
}
