# =========================
# 1. Build Stage
# =========================
FROM node:22-alpine AS builder

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build


# =========================
# 2. Run Stage (NO NGINX)
# =========================
FROM node:22-alpine

WORKDIR /app

# install static server
RUN npm install -g serve

# copy build output
COPY --from=builder /app/dist ./dist

EXPOSE 3000

CMD ["serve", "-s", "dist", "-l", "3000"]