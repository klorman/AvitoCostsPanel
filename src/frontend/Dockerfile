# Используем node:18-alpine для сборки проекта
FROM node:18-alpine as builder

WORKDIR /react-ui

# Копируем файлы проекта
COPY package.json package-lock.json ./

# Устанавливаем зависимости
RUN npm cache clean --force && npm install

# Копируем оставшиеся файлы проекта
COPY . .

# Запускаем сборку проекта
RUN npm run build

# Выводим содержимое директории dist для проверки
RUN ls /react-ui/dist

# Используем nginx:alpine для раздачи собранных файлов
FROM nginx:alpine as production

# Конфигурация Nginx
COPY ./.nginx/nginx.conf /etc/nginx/nginx.conf

# Удаляем стандартные файлы nginx
RUN rm -rf /usr/share/nginx/html/*

# Копируем собранные файлы из контейнера builder в директорию dist
COPY --from=builder /react-ui/dist /usr/share/nginx/html

# Открываем порт 80
EXPOSE 80

# Запускаем Nginx
ENTRYPOINT ["nginx", "-g", "daemon off;"]
