# Stage 1: Build the application
FROM node:16-alpine as build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

EXPOSE 5173

# Ensure Vite binds to 0.0.0.0 instead of localhost
CMD ["npm", "run", "dev", "--", "--host"]
