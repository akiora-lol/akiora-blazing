# --- build stage ---
FROM node:22-alpine AS build

WORKDIR /app

# Build-time API URL is baked into the bundle. Provided via compose `args`.
# ARG VITE_API_URL
# ENV VITE_API_URL=$VITE_API_URL

COPY package*.json ./
RUN npm install

COPY . .
RUN npm run dev

