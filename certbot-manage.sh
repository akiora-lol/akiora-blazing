#!/bin/bash

set -e

DOMAIN=${DOMAIN:-akiora.webhop.me}
EMAIL=${EMAIL:-admin@${DOMAIN}}

echo "=== Фикс SSL сертификатов ==="

# 1. Останавливаем все
echo "Останавливаем контейнеры..."
docker compose down

# 2. Создаем HTTP-only конфиг
echo "Создаем временную HTTP-конфигурацию..."
mkdir -p ./nginx/templates

cat > ./nginx/templates/default.conf.template << 'EOF'
server {
    listen 80;
    server_name akiora.webhop.me www.akiora.webhop.me;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type text/plain;
    }
    
    location / {
        proxy_pass http://front:3000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
    
    
    
    
}
EOF

# 3. Запускаем все контейнеры
echo "Запускаем контейнеры..."
docker compose up -d

# 4. Ждем запуска Nginx
echo "Ожидаем запуска Nginx..."
sleep 10

# 5. Проверяем доступность
echo "Проверяем доступность..."
curl -I http://${DOMAIN}/.well-known/acme-challenge/ || echo "⚠️ Проверка не удалась, но продолжаем..."

# 6. Останавливаем Nginx для standalone режима
echo "Останавливаем Nginx для получения сертификата..."
docker compose stop nginx

# 7. Получаем сертификат
echo "Получаем сертификат..."
docker run --rm -p 80:80 -p 443:443 \
  -v hotel_letsencrypt_certs:/etc/letsencrypt \
  certbot/certbot \
  certonly --standalone \
  -d ${DOMAIN} \
  --email ${EMAIL} \
  --agree-tos \
  --no-eff-email \
  --keep-until-expiring

# 8. Проверяем сертификат
echo "Проверяем сертификат..."
docker run --rm -v hotel_letsencrypt_certs:/etc/letsencrypt alpine ls -la /etc/letsencrypt/live/${DOMAIN}/

# 9. Восстанавливаем полную конфигурацию с SSL
echo "Восстанавливаем конфигурацию с SSL..."

cat > ./nginx/templates/default.conf.template << 'EOF'
server {
    listen 80;
    server_name akiora.webhop.me www.akiora.webhop.me;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type text/plain;
    }
    
    location / {
        return 301 https://${DOMAIN}$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name ${DOMAIN};
    
    ssl_certificate /etc/letsencrypt/live/${DOMAIN}/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/${DOMAIN}/privkey.pem;
    
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    
    location /.well-known/acme-challenge/ {
        root /var/www/certbot;
        default_type text/plain;
    }
    
    location / {
            proxy_pass http://front:3000;
            proxy_set_header Host $host;
            proxy_set_header X-Real-IP $remote_addr;
            proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
            proxy_set_header X-Forwarded-Proto $scheme;
        }
}
EOF

# 10. Запускаем Nginx
echo "Запускаем Nginx с SSL..."
docker compose up -d nginx

# 11. Проверяем
echo "Проверяем логи..."
sleep 5
docker compose logs nginx --tail 20

echo "✅ Готово! Проверьте: https://${DOMAIN}"
