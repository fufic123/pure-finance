# Pure Finance — frontend

Next.js 15 + TypeScript + Tailwind PWA shell. Consumes the backend at `NEXT_PUBLIC_API_BASE_URL` (see `.env.example`).

## Setup

```bash
# First-time: install Node (if missing) and pnpm.
brew install node pnpm

# Install deps.
pnpm install

# Configure environment.
cp .env.example .env.local

# Run.
pnpm dev
```

Open http://localhost:3000.

## Structure

```
src/
├── app/
│   ├── layout.tsx          # iOS PWA metadata, providers, global CSS
│   ├── page.tsx            # landing placeholder (real login comes in the auth task)
│   ├── globals.css         # Tailwind + PF design tokens as CSS vars
│   └── providers.tsx       # TanStack Query client
└── lib/
    ├── tokens.ts           # PF color map + gold gradients (TS-side)
    ├── api/
    │   ├── client.ts       # fetch wrapper + Bearer + silent refresh on 401
    │   ├── auth.ts         # startGoogleAuth / completeGoogleAuth / logout / getCurrentUser
    │   └── types.ts        # TS mirrors of backend DTOs
    └── auth/
        └── storage.ts      # access in memory, refresh in localStorage
```

## Icons

`public/icon-192.png`, `public/icon-512.png`, and an `apple-touch-icon.png` are referenced by the manifest and iOS meta tags but are not yet in the repo. Generate them from the logo mark once the design is final.

## Scripts

- `pnpm dev` — dev server, hot reload.
- `pnpm build` — production build.
- `pnpm start` — run production build.
- `pnpm lint` — Next.js ESLint config.
- `pnpm typecheck` — strict TS check (no emit).
