FROM nginx:alpine

WORKDIR /usr/share/nginx/html
RUN rm -rf /usr/share/nginx/html/*

COPY . .

# Переопределяем конфиг nginx
RUN echo 'server { \
    listen 80; \
    root /usr/share/nginx/html; \
    index main.html; \
    location / { try_files $uri /main.html; } \
}' > /etc/nginx/conf.d/default.conf

EXPOSE 80
