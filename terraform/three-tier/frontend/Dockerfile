# Stage 1: Build the application
FROM node:16-alpine as build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm install

COPY . .
# RUN npm run build

EXPOSE 5173
# run the vite react app
CMD ["npm", "run", "dev"]

# Stage 2: Serve the application with nginx
# FROM nginx:alpine

# COPY --from=build /usr/src/app/dist /usr/share/nginx/html

# COPY --from=build . /usr/share/nginx/html

# EXPOSE 80

# CMD ["nginx", "-g", "daemon off;"]