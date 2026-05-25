# 🐳 Deployment Guide

## Docker Deployment

### Build and Run

```bash
# Navigate to project directory
cd vehicle-telematics-python-web

# Build and start the application
docker compose up --build

# Application will be available at http://localhost:8080
```

### Using Docker Compose (Recommended)

The `docker-compose.yml` file provides:
- Automated image building
- Port mapping (8080:8080)
- Volume mounts for data and models
- Container restart policy

```bash
# Start in background
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down
```

### Docker Environment Variables

Add to `docker-compose.yml` or `.env`:

```yaml
environment:
  - PYTHONUNBUFFERED=1
  - HOST=0.0.0.0
  - PORT=8080
```

---

## Production Deployment

### 1. AWS ECS

```bash
# Build image
docker build -t telematics-app:latest .

# Tag for ECR
docker tag telematics-app:latest AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/telematics-app:latest

# Push to ECR
aws ecr get-login-password --region REGION | docker login --username AWS --password-stdin AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com
docker push AWS_ACCOUNT_ID.dkr.ecr.REGION.amazonaws.com/telematics-app:latest

# Create ECS task definition and service
# (Use AWS Console or CLI)
```

### 2. Kubernetes

```yaml
# deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: telematics-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: telematics
  template:
    metadata:
      labels:
        app: telematics
    spec:
      containers:
      - name: telematics
        image: telematics-app:latest
        ports:
        - containerPort: 8080
        volumeMounts:
        - name: data
          mountPath: /app/data
        - name: models
          mountPath: /app/models
      volumes:
      - name: data
        persistentVolumeClaim:
          claimName: data-pvc
      - name: models
        persistentVolumeClaim:
          claimName: models-pvc
---
apiVersion: v1
kind: Service
metadata:
  name: telematics-service
spec:
  selector:
    app: telematics
  ports:
  - protocol: TCP
    port: 80
    targetPort: 8080
  type: LoadBalancer
```

```bash
kubectl apply -f deployment.yaml
kubectl get service telematics-service
```

### 3. Docker Swarm

```bash
# Initialize swarm
docker swarm init

# Build image
docker build -t telematics-app:latest .

# Create service
docker service create \
  --name telematics \
  --publish 8080:8080 \
  --mount type=bind,source=/data,target=/app/data \
  --mount type=bind,source=/models,target=/app/models \
  telematics-app:latest

# Scale up
docker service scale telematics=3
```

---

## Nginx Reverse Proxy

### Configuration

```nginx
# /etc/nginx/sites-available/telematics.conf

upstream telematics_backend {
    server localhost:8080;
    server localhost:8081;
    server localhost:8082;
    # Add more if using multiple instances
}

server {
    listen 80;
    server_name telematics.example.com;

    # Redirect to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name telematics.example.com;

    ssl_certificate /etc/letsencrypt/live/telematics.example.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/telematics.example.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    location / {
        proxy_pass http://telematics_backend;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 60s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/telematics.conf /etc/nginx/sites-enabled/

# Test config
sudo nginx -t

# Restart nginx
sudo systemctl restart nginx
```

---

## Load Balancing

### Multiple Instances

```bash
# Start multiple instances on different ports
docker run -d -p 8080:8080 --name telematics-1 telematics-app
docker run -d -p 8081:8080 --name telematics-2 telematics-app
docker run -d -p 8082:8080 --name telematics-3 telematics-app
```

### HAProxy Configuration

```
global
    log stdout local0
    log stdout local1 notice
    chroot /var/lib/haproxy
    stats socket /run/haproxy/admin.sock mode 660 level admin
    stats timeout 30s

defaults
    log     global
    mode    http
    option  httplog
    option  dontlognull
    timeout connect 5000
    timeout client  50000
    timeout server  50000

listen telematics
    bind *:80
    stats enable
    stats uri /stats
    balance roundrobin
    server app1 localhost:8080 check
    server app2 localhost:8081 check
    server app3 localhost:8082 check
```

---

## Data & Model Management

### Volume Mounting

```bash
# Create named volumes
docker volume create telematics-data
docker volume create telematics-models

# Use in docker-compose.yml
volumes:
  - telematics-data:/app/data
  - telematics-models:/app/models
```

### Backup Data

```bash
# Backup data volume
docker run --rm -v telematics-data:/app/data -v $(pwd):/backup \
  alpine tar czf /backup/data-backup.tar.gz -C /app/data .

# Restore data volume
docker run --rm -v telematics-data:/app/data -v $(pwd):/backup \
  alpine tar xzf /backup/data-backup.tar.gz -C /app/data
```

### CSV File Sync

```bash
# Copy data from host to container
docker cp ./data/df_clean.csv telematics-app-1:/app/data/

# Copy from container to host
docker cp telematics-app-1:/app/data/vehicle_risk.csv ./data/
```

---

## Monitoring & Logging

### Docker Logs

```bash
# View container logs
docker logs telematics-app-1

# Follow logs
docker logs -f telematics-app-1

# Last 100 lines
docker logs --tail 100 telematics-app-1
```

### Health Check

Add to `docker-compose.yml`:

```yaml
healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8080"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s
```

### Prometheus Monitoring

```yaml
# prometheus.yml
global:
  scrape_interval: 15s

scrape_configs:
  - job_name: 'telematics'
    static_configs:
      - targets: ['localhost:8080']
```

---

## Performance Tuning

### Python Settings

```bash
# Set environment variables
export PYTHONUNBUFFERED=1
export PYTHONOPTIMIZE=2
```

### Container Resources

```yaml
# docker-compose.yml
services:
  telematics-app:
    resources:
      limits:
        cpus: '2'
        memory: 4G
      reservations:
        cpus: '1'
        memory: 2G
```

### Data Caching

Services include built-in caching:
- Data frames cached after first load
- Models cached in memory
- Predictions cached per session

---

## Troubleshooting

### Port Already in Use

```bash
# Find process using port 8080
lsof -i :8080

# Kill process
kill -9 <PID>

# Or use different port in docker-compose.yml
ports:
  - "8081:8080"
```

### Memory Issues

```bash
# Increase Docker memory
docker run -m 4g telematics-app

# Monitor memory usage
docker stats telematics-app-1
```

### Data Not Persisting

```bash
# Check volume mounts
docker inspect telematics-app-1 | grep -A 10 Mounts

# Verify permissions
docker exec telematics-app-1 ls -la /app/data
```

---

## Security Checklist

- [ ] Use HTTPS with valid certificates
- [ ] Enable authentication (add in future)
- [ ] Restrict API access via firewall
- [ ] Use read-only file systems where possible
- [ ] Run container as non-root user
- [ ] Keep base image updated
- [ ] Scan for vulnerabilities: `trivy image telematics-app`
- [ ] Use secrets management for credentials
- [ ] Enable audit logging

---

## Scaling Considerations

### Horizontal Scaling
- Add more container instances
- Use load balancer (Nginx, HAProxy, AWS ELB)
- Share data volumes across instances

### Vertical Scaling
- Increase CPU/memory per container
- Optimize data loading (streaming)
- Add caching layer (Redis)

### Database Migration
- Replace CSV with PostgreSQL
- Use connection pooling
- Enable query optimization
- Add indexes on frequently queried columns

---

## Continuous Deployment

### GitHub Actions Example

```yaml
name: Deploy Telematics App

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Build image
        run: docker build -t telematics-app:latest .
      - name: Push to registry
        run: |
          echo ${{ secrets.DOCKER_PASSWORD }} | docker login -u ${{ secrets.DOCKER_USERNAME }} --password-stdin
          docker tag telematics-app:latest username/telematics-app:latest
          docker push username/telematics-app:latest
      - name: Deploy to server
        run: |
          ssh user@server 'cd /app && docker-compose pull && docker-compose up -d'
```

---

## Support & Maintenance

- Monitor application logs regularly
- Update dependencies monthly
- Backup data weekly
- Test disaster recovery procedures
- Document any customizations
- Keep deployment documentation updated

---

**For production use, always test thoroughly in a staging environment first.**
