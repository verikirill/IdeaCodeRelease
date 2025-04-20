FROM node:21-alpine AS builder

# Добавляем аргументы для прокси и npm registry
ARG HTTP_PROXY
ARG HTTPS_PROXY
ARG NPM_REGISTRY

# Настраиваем proxy и registry если они заданы
RUN if [ -n "$HTTP_PROXY" ]; then \
      npm config set proxy $HTTP_PROXY; \
    fi && \
    if [ -n "$HTTPS_PROXY" ]; then \
      npm config set https-proxy $HTTPS_PROXY; \
    fi && \
    if [ -n "$NPM_REGISTRY" ]; then \
      npm config set registry $NPM_REGISTRY; \
    fi

WORKDIR /app
COPY package.json .
COPY package-lock.json .
RUN npm config set fetch-retry-maxtimeout 120000 && \
    npm config set fetch-retry-mintimeout 30000 && \
    npm config set fetch-retries 5 && \
    npm install
COPY . .
RUN npm run build

FROM node:21-alpine AS production

WORKDIR /app
COPY --from=builder /app/build ./build
COPY --from=builder /app/node_modules ./node_modules
COPY package.json .

# Expose port
EXPOSE 3000

# Start the server
CMD ["node", "./build"]
