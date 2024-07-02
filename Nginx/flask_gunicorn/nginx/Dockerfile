# nginx/Dockerfile

# Use the official nginx image from the Docker Hub
FROM nginx:alpine

# Copy custom nginx config
COPY nginx_proxy.conf /etc/nginx/nginx.conf

# Expose port 80
EXPOSE 80

# Command to run nginx
CMD ["nginx", "-g", "daemon off;"]
