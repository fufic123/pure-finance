# Pure Finance — frontend-mock

Standalone Next.js 15 + Tailwind + Framer Motion design-preview app. Pure mock
data — **no backend, no auth, no API calls**. Used to preview screen designs and
animations in isolation from the real app.

## Run

Runs on **port 3001** via the root `docker-compose.yml`:

```bash
docker compose up frontend-mock
```

Open http://localhost:3001.

## Structure

Mirrors the real `frontend/` scaffold but strips out the API client, auth, and
TanStack Query. Every page is wrapped in `<PageTransition>` for an iOS-feeling
opacity + translateY fade on mount; list screens use `<StaggerList>` to stagger
their children.

Mock data lives in `src/lib/mock.ts` (ported from
`backend/docs/frontend/pf_components.jsx`).
