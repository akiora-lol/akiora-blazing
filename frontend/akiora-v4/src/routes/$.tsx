import { createFileRoute } from '@tanstack/react-router'
import { NotFoundPage } from '../components/ErrorPages'

export const Route = createFileRoute('/$')({
    component: NotFoundPage,
})
