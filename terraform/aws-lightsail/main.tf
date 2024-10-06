provider "aws" {
  region = var.aws_region
}

# Create a Lightsail instance for your app
resource "aws_lightsail_instance" "app" {
  name              = "test-app-instance"
  availability_zone = "${var.aws_region}a"
  blueprint_id      = "amazon_linux_2"
  bundle_id         = "nano_2_0"
  key_pair_name     = aws_key_pair.lightsail-key.key_name

  # Provision script to install Docker and run the containers
  user_data = <<-EOF
              #!/bin/bash
              sudo yum update -y
              sudo amazon-linux-extras install docker -y
              sudo service docker start
              sudo usermod -a -G docker ec2-user
              
              # Pull the Docker images (replace with your actual Docker images or build steps)
              docker run -d -p 5000:5000 backend-image
              docker run -d -p 5173:5173 frontend-image
              
              # Install PostgreSQL and set up the database
              docker run -d -e POSTGRES_USER=user -e POSTGRES_PASSWORD=password -e POSTGRES_DB=mydatabase -p 5432:5432 postgres:latest
              EOF

  tags = {
    Name = "TestApp"
  }
}

# Define a security group to allow HTTP, HTTPS, and database connections
resource "aws_security_group" "lightsail_sg" {
  name        = "lightsail-sg"
  description = "Allow HTTP, HTTPS, and database connections"

  # Allow HTTP, HTTPS, PostgreSQL, and Vite dev server access
  ingress {
    from_port   = 80
    to_port     = 80
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 443
    to_port     = 443
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5173
    to_port     = 5173
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5000
    to_port     = 5000
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  ingress {
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Associate the security group with the Lightsail instance
resource "aws_lightsail_instance_public_ports" "instance_ports" {
  instance_name = aws_lightsail_instance.app.name

  port_info {
    from_port = 80
    to_port   = 80
    protocol  = "tcp"
  }

  port_info {
    from_port = 443
    to_port   = 443
    protocol  = "tcp"
  }

  port_info {
    from_port = 5000
    to_port   = 5000
    protocol  = "tcp"
  }

  port_info {
    from_port = 5173
    to_port   = 5173
    protocol  = "tcp"
  }

  port_info {
    from_port = 5432
    to_port   = 5432
    protocol  = "tcp"
  }
}

# Define the SSH key pair for connecting to the instance
resource "aws_key_pair" "lightsail-key" {
  key_name   = "lightsail-key"
  public_key = file(var.ssh_public_key)
}

output "public_ip" {
  value = aws_lightsail_instance.app.public_ip_address
}
