# Docker Deployment Guide

## Quick Start (Easiest Way!)

### Option 1: Using MongoDB Atlas (Recommended for Production)

1. **Get MongoDB Atlas Connection String**
   - Go to [MongoDB Atlas](https://www.mongodb.com/cloud/atlas)
   - Create free cluster
   - Get connection string
   - Update `.env` file

2. **Run with Docker Compose**
```bash
# Build and start
docker-compose -f docker-compose.prod.yml up -d

# View logs
docker-compose -f docker-compose.prod.yml logs -f

# Stop
docker-compose -f docker-compose.prod.yml down
```

3. **Access the app**
   - Open: http://localhost

### Option 2: Using Local MongoDB (For Development)

1. **Run everything with one command**
```bash
# Build and start (includes local MongoDB)
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

2. **Update .env for local MongoDB**
```env
MONGODB_URL=mongodb://admin:password123@mongodb:27017/socialtab?authSource=admin
SECRET_KEY=your-secret-key-here
```

3. **Access the app**
   - App: http://localhost:8000
   - MongoDB: localhost:27017

## Prerequisites

- Docker installed ([Get Docker](https://docs.docker.com/get-docker/))
- Docker Compose installed (included with Docker Desktop)

## Installation

### Install Docker

**Linux:**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER
```

**Mac/Windows:**
- Download [Docker Desktop](https://www.docker.com/products/docker-desktop)
- Install and start Docker Desktop

### Verify Installation
```bash
docker --version
docker-compose --version
```

## Configuration

### 1. Create .env file

```bash
cp .env.example .env
```

### 2. Edit .env file

**For MongoDB Atlas:**
```env
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/socialtab?retryWrites=true&w=majority
SECRET_KEY=generate-a-random-32-character-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

**For Local MongoDB:**
```env
MONGODB_URL=mongodb://admin:password123@mongodb:27017/socialtab?authSource=admin
SECRET_KEY=generate-a-random-32-character-string
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=10080
```

### 3. Generate SECRET_KEY

```bash
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

## Docker Commands

### Build Image
```bash
# Build the image
docker build -t socialtab:latest .

# Build with no cache
docker build --no-cache -t socialtab:latest .
```

### Run Container (Single Container)
```bash
# Run in foreground
docker run -p 8000:8000 --env-file .env socialtab:latest

# Run in background
docker run -d -p 8000:8000 --env-file .env --name socialtab socialtab:latest

# Run with custom port
docker run -d -p 3000:8000 --env-file .env --name socialtab socialtab:latest
```

### Docker Compose Commands

**Development (with local MongoDB):**
```bash
# Start services
docker-compose up -d

# Start and rebuild
docker-compose up -d --build

# View logs
docker-compose logs -f

# View logs for specific service
docker-compose logs -f web

# Stop services
docker-compose down

# Stop and remove volumes
docker-compose down -v

# Restart services
docker-compose restart

# Check status
docker-compose ps
```

**Production (MongoDB Atlas only):**
```bash
# Start
docker-compose -f docker-compose.prod.yml up -d

# Stop
docker-compose -f docker-compose.prod.yml down

# Logs
docker-compose -f docker-compose.prod.yml logs -f
```

### Container Management

```bash
# List running containers
docker ps

# List all containers
docker ps -a

# Stop container
docker stop socialtab

# Start container
docker start socialtab

# Restart container
docker restart socialtab

# Remove container
docker rm socialtab

# Remove container (force)
docker rm -f socialtab

# View container logs
docker logs socialtab

# Follow logs
docker logs -f socialtab

# Execute command in container
docker exec -it socialtab bash

# View container stats
docker stats socialtab
```

### Image Management

```bash
# List images
docker images

# Remove image
docker rmi socialtab:latest

# Remove unused images
docker image prune

# Remove all unused images
docker image prune -a
```

### System Cleanup

```bash
# Remove stopped containers
docker container prune

# Remove unused images
docker image prune

# Remove unused volumes
docker volume prune

# Remove unused networks
docker network prune

# Remove everything unused
docker system prune

# Remove everything (including volumes)
docker system prune -a --volumes
```

## Deployment Scenarios

### Scenario 1: Local Development

```bash
# Use local MongoDB
docker-compose up -d

# Access app at http://localhost:8000
# MongoDB at localhost:27017
```

### Scenario 2: Production with MongoDB Atlas

```bash
# Update .env with MongoDB Atlas URL
# Use production compose file
docker-compose -f docker-compose.prod.yml up -d

# Access app at http://localhost
```

### Scenario 3: Deploy to VPS (DigitalOcean, AWS, etc.)

1. **SSH into your server**
```bash
ssh user@your-server-ip
```

2. **Install Docker**
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```

3. **Clone your repository**
```bash
git clone https://github.com/yourusername/socialtab.git
cd socialtab
```

4. **Create .env file**
```bash
nano .env
# Add your environment variables
```

5. **Run with Docker Compose**
```bash
docker-compose -f docker-compose.prod.yml up -d
```

6. **Setup Nginx (Optional)**
```bash
sudo apt install nginx
sudo nano /etc/nginx/sites-available/socialtab
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

```bash
sudo ln -s /etc/nginx/sites-available/socialtab /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

7. **Setup SSL with Let's Encrypt**
```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d your-domain.com
```

### Scenario 4: Deploy to Render with Docker

1. **Create render.yaml**
```yaml
services:
  - type: web
    name: socialtab
    env: docker
    dockerfilePath: ./Dockerfile
    envVars:
      - key: MONGODB_URL
        sync: false
      - key: SECRET_KEY
        generateValue: true
```

2. **Push to GitHub and connect to Render**

## Troubleshooting

### Container Won't Start

**Check logs:**
```bash
docker logs socialtab
# or
docker-compose logs web
```

**Common issues:**
- Missing .env file
- Invalid MongoDB URL
- Port already in use

**Solutions:**
```bash
# Check if port is in use
sudo lsof -i :8000

# Use different port
docker run -p 3000:8000 --env-file .env socialtab:latest
```

### MongoDB Connection Failed

**Check MongoDB container:**
```bash
docker-compose logs mongodb
```

**Test connection:**
```bash
docker exec -it socialtab-mongodb mongosh -u admin -p password123
```

**Verify .env:**
- Check MONGODB_URL is correct
- For local: `mongodb://admin:password123@mongodb:27017/socialtab?authSource=admin`
- For Atlas: Use connection string from Atlas dashboard

### Permission Denied

**Linux users:**
```bash
# Add user to docker group
sudo usermod -aG docker $USER

# Logout and login again
```

### Out of Disk Space

**Clean up Docker:**
```bash
# Remove unused containers, images, volumes
docker system prune -a --volumes

# Check disk usage
docker system df
```

### Container Keeps Restarting

**Check health:**
```bash
docker inspect socialtab | grep -A 10 Health
```

**Disable health check temporarily:**
Edit Dockerfile and comment out HEALTHCHECK line

### Can't Access App

**Check container is running:**
```bash
docker ps
```

**Check port mapping:**
```bash
docker port socialtab
```

**Test from inside container:**
```bash
docker exec -it socialtab curl http://localhost:8000/health
```

**Check firewall:**
```bash
# Linux
sudo ufw allow 8000

# Check if port is accessible
curl http://localhost:8000
```

## Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `MONGODB_URL` | MongoDB connection string | - | Yes |
| `SECRET_KEY` | JWT secret key | - | Yes |
| `ALGORITHM` | JWT algorithm | HS256 | No |
| `ACCESS_TOKEN_EXPIRE_MINUTES` | Token expiry time | 10080 | No |
| `PORT` | Application port | 8000 | No |

## Performance Optimization

### 1. Multi-stage Build (Advanced)

Create `Dockerfile.optimized`:
```dockerfile
# Build stage
FROM python:3.11-slim as builder
WORKDIR /app
COPY requirements.txt .
RUN pip install --user --no-cache-dir -r requirements.txt

# Runtime stage
FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY . .
ENV PATH=/root/.local/bin:$PATH
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### 2. Resource Limits

```yaml
# In docker-compose.yml
services:
  web:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 512M
```

### 3. Use Docker BuildKit

```bash
DOCKER_BUILDKIT=1 docker build -t socialtab:latest .
```

## Monitoring

### View Resource Usage

```bash
# Real-time stats
docker stats

# Specific container
docker stats socialtab
```

### View Logs

```bash
# Last 100 lines
docker logs --tail 100 socialtab

# Follow logs
docker logs -f socialtab

# With timestamps
docker logs -t socialtab
```

### Health Checks

```bash
# Check health status
docker inspect socialtab | grep -A 10 Health

# Manual health check
curl http://localhost:8000/health
```

## Backup and Restore

### Backup MongoDB Data

```bash
# Backup local MongoDB
docker exec socialtab-mongodb mongodump --out /data/backup

# Copy backup to host
docker cp socialtab-mongodb:/data/backup ./mongodb-backup
```

### Restore MongoDB Data

```bash
# Copy backup to container
docker cp ./mongodb-backup socialtab-mongodb:/data/backup

# Restore
docker exec socialtab-mongodb mongorestore /data/backup
```

## CI/CD Integration

### GitHub Actions Example

Create `.github/workflows/docker.yml`:
```yaml
name: Docker Build and Push

on:
  push:
    branches: [ main ]

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      
      - name: Build Docker image
        run: docker build -t socialtab:latest .
      
      - name: Run tests
        run: docker run socialtab:latest python -m pytest
```

## Security Best Practices

1. ✅ Use non-root user in container
2. ✅ Don't include .env in image
3. ✅ Use secrets for sensitive data
4. ✅ Keep base image updated
5. ✅ Scan for vulnerabilities
6. ✅ Use specific image versions

```bash
# Scan for vulnerabilities
docker scan socialtab:latest
```

## Quick Reference

```bash
# Start everything
docker-compose up -d

# Stop everything
docker-compose down

# View logs
docker-compose logs -f

# Rebuild and restart
docker-compose up -d --build

# Clean everything
docker-compose down -v && docker system prune -a
```

## Support

- Docker Docs: https://docs.docker.com
- Docker Compose Docs: https://docs.docker.com/compose
- MongoDB Docker: https://hub.docker.com/_/mongo

---

**Happy Dockerizing! 🐳💚**
