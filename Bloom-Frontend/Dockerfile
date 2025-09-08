FROM node:20 AS build
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build  # Vite builds to /app/dist by default

FROM nginx:1.27-alpine
COPY --from=build /app/dist/ /usr/share/nginx/html/
