# Use the official Nginx image from the Docker Hub
FROM nginx:latest

# Copy the custom Nginx configuration file into the container
COPY nginx_proxy.conf /etc/nginx/nginx.conf

# Expose the port Nginx will run on
EXPOSE 80

EXPOSE 443