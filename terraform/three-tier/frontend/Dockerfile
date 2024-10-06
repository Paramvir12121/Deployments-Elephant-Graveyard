# Stage 1: Build the application
FROM node:16-alpine as build

WORKDIR /usr/src/app

COPY package.json package-lock.json ./
RUN npm install

COPY . .

# EXPOSE 5173

# Ensure Vite binds to 0.0.0.0 instead of localhost
CMD ["npm", "run", "dev", "--", "--host"]

# Stage 2: Serve the application
# Use the official Nginx image from the Docker Hub
FROM nginx:1.21-alpine

# Copy the build output from the build stage to the Nginx server
COPY --from=build /usr/src/app/dist /usr/share/nginx/html

# Expose the port the app runs on
EXPOSE 80

# use nignx.conf from the local directory
COPY nginx.conf /etc/nginx/nginx.conf

# Start Nginx and keep it running in the background
CMD ["nginx", "-g", "daemon off;"]
