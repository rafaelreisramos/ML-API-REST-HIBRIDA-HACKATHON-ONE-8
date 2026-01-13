# ============================================================================
# Multi-stage build para Frontend React/Vite
# ============================================================================

FROM node:20-alpine AS build

WORKDIR /app

# Copiar package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copiar código fonte
COPY . .

# Build da aplicação
RUN npm run build

# ============================================================================
# Runtime stage com Nginx
# ============================================================================

FROM nginx:alpine

# Copiar build do stage anterior
COPY --from=build /app/dist /usr/share/nginx/html

# Copiar configuração customizada do Nginx
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Expor porta
EXPOSE 80

# Health check
HEALTHCHECK --interval=30s --timeout=3s --start-period=5s --retries=3 \
    CMD wget --no-verbose --tries=1 --spider http://localhost/ || exit 1

# Nginx roda como daemon off por padrão na imagem oficial
CMD ["nginx", "-g", "daemon off;"]
