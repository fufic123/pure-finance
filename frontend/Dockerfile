FROM node:20-alpine

WORKDIR /app

RUN corepack enable && corepack prepare pnpm@9.15.0 --activate

# Copy manifests first for better layer caching. The lockfile glob
# tolerates its absence on the very first build — pnpm will generate
# one inside the container.
COPY package.json ./
COPY pnpm-lock.yaml* ./

RUN pnpm install

COPY . .

EXPOSE 3000

CMD ["pnpm", "dev", "--hostname", "0.0.0.0"]
