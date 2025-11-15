# Production Deployment Guide

## Pre-Deployment Checklist

### ✅ Code Quality
- [x] All tests passing (13/13)
- [x] Error handling implemented
- [x] Logging system configured
- [x] Input validation added
- [x] Security headers configured

### ✅ Configuration
- [x] Environment variables documented (.env.example)
- [x] .gitignore configured
- [x] Database schema finalized
- [x] CORS origins configurable

### ⚠️ Production Requirements
- [ ] SSL/TLS certificates obtained
- [ ] Production database setup (PostgreSQL recommended)
- [ ] Backup strategy defined
- [ ] Monitoring solution chosen
- [ ] Reverse proxy configured (nginx/Apache)

---

## Production Environment Setup

### 1. Server Requirements

**Minimum:**
- CPU: 2 cores
- RAM: 4GB
- Storage: 20GB
- Python: 3.12+
- OS: Ubuntu 20.04+ / Windows Server 2019+

**Recommended:**
- CPU: 4 cores
- RAM: 8GB
- Storage: 50GB (more if storing many images)
- GPU: Optional (for faster inference)

### 2. Install Dependencies

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install Python 3.12
sudo apt install python3.12 python3.12-venv python3-pip

# Install system dependencies
sudo apt install nginx postgresql libpq-dev

# Clone repository
cd /opt
git clone <your-repo-url> skin_ai_assistant
cd skin_ai_assistant/skin_ai_assistant

# Create virtual environment
python3.12 -m venv .venv
source .venv/bin/activate

# Install Python packages
pip install --upgrade pip
pip install -r requirements.txt
```

### 3. Configure Database

**PostgreSQL (Recommended for Production):**

```bash
# Create database and user
sudo -u postgres psql
```

```sql
CREATE DATABASE skinai_db;
CREATE USER skinai_user WITH PASSWORD 'your_secure_password';
GRANT ALL PRIVILEGES ON DATABASE skinai_db TO skinai_user;
\q
```

**Configure .env:**

```bash
cd /opt/skin_ai_assistant/skin_ai_assistant
cp .env.example .env
nano .env
```

Update:
```env
SKINAI_DB_URL=postgresql://skinai_user:your_secure_password@localhost/skinai_db
BACKEND_PORT=8000
LOG_LEVEL=INFO
ENVIRONMENT=production
```

### 4. Configure Nginx Reverse Proxy

Create `/etc/nginx/sites-available/skinai`:

```nginx
# Backend API
server {
    listen 80;
    server_name api.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # Increase timeout for ML inference
        proxy_read_timeout 300;
        proxy_connect_timeout 300;
        proxy_send_timeout 300;
    }
}

# User UI
server {
    listen 80;
    server_name app.yourdomain.com;

    location / {
        proxy_pass http://127.0.0.1:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}

# Admin Dashboard
server {
    listen 80;
    server_name admin.yourdomain.com;

    # Optional: Add basic auth
    # auth_basic "Admin Area";
    # auth_basic_user_file /etc/nginx/.htpasswd;

    location / {
        proxy_pass http://127.0.0.1:8601;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    }
}
```

Enable the site:
```bash
sudo ln -s /etc/nginx/sites-available/skinai /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### 5. Configure SSL with Let's Encrypt

```bash
sudo apt install certbot python3-certbot-nginx
sudo certbot --nginx -d api.yourdomain.com -d app.yourdomain.com -d admin.yourdomain.com
```

### 6. Create Systemd Services

**Backend Service** (`/etc/systemd/system/skinai-backend.service`):

```ini
[Unit]
Description=Skin AI Assistant Backend
After=network.target postgresql.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/skin_ai_assistant/skin_ai_assistant
Environment="PATH=/opt/skin_ai_assistant/skin_ai_assistant/.venv/bin"
ExecStart=/opt/skin_ai_assistant/skin_ai_assistant/.venv/bin/python run_backend.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**UI Service** (`/etc/systemd/system/skinai-ui.service`):

```ini
[Unit]
Description=Skin AI Assistant UI
After=network.target skinai-backend.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/skin_ai_assistant/skin_ai_assistant
Environment="PATH=/opt/skin_ai_assistant/skin_ai_assistant/.venv/bin"
Environment="SKINAI_API_URL=http://127.0.0.1:8000"
ExecStart=/opt/skin_ai_assistant/skin_ai_assistant/.venv/bin/python run_ui.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Admin Service** (`/etc/systemd/system/skinai-admin.service`):

```ini
[Unit]
Description=Skin AI Assistant Admin
After=network.target skinai-backend.service

[Service]
Type=simple
User=www-data
WorkingDirectory=/opt/skin_ai_assistant/skin_ai_assistant
Environment="PATH=/opt/skin_ai_assistant/skin_ai_assistant/.venv/bin"
Environment="SKINAI_API_URL=http://127.0.0.1:8000"
ExecStart=/opt/skin_ai_assistant/skin_ai_assistant/.venv/bin/python run_admin.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Enable and start services:**

```bash
sudo systemctl daemon-reload
sudo systemctl enable skinai-backend skinai-ui skinai-admin
sudo systemctl start skinai-backend skinai-ui skinai-admin

# Check status
sudo systemctl status skinai-backend
sudo systemctl status skinai-ui
sudo systemctl status skinai-admin
```

---

## Backup Strategy

### Database Backups

Create `/opt/skin_ai_assistant/backup.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/opt/skin_ai_assistant/backups"
DATE=$(date +%Y%m%d_%H%M%S)
mkdir -p $BACKUP_DIR

# Backup database
pg_dump skinai_db > "$BACKUP_DIR/db_backup_$DATE.sql"

# Backup uploaded images
tar -czf "$BACKUP_DIR/images_backup_$DATE.tar.gz" /opt/skin_ai_assistant/skin_ai_assistant/uploaded_images/

# Keep only last 7 days of backups
find $BACKUP_DIR -type f -mtime +7 -delete

echo "Backup completed: $DATE"
```

Add to crontab:
```bash
sudo crontab -e
# Add line:
0 2 * * * /opt/skin_ai_assistant/backup.sh
```

---

## Monitoring

### 1. Log Monitoring

Logs are written to:
- Application: `/opt/skin_ai_assistant/skin_ai_assistant/skin_ai.log`
- Systemd: `sudo journalctl -u skinai-backend -f`

### 2. Health Check Monitoring

Use a monitoring service (UptimeRobot, Pingdom, etc.) to check:
- `https://api.yourdomain.com/health` (every 5 minutes)

### 3. Disk Space Monitoring

```bash
# Check disk usage
df -h

# Monitor uploaded images directory
du -sh /opt/skin_ai_assistant/skin_ai_assistant/uploaded_images/
```

---

## Security Hardening

### 1. Firewall Configuration

```bash
sudo ufw allow 22/tcp   # SSH
sudo ufw allow 80/tcp   # HTTP
sudo ufw allow 443/tcp  # HTTPS
sudo ufw enable
```

### 2. File Permissions

```bash
cd /opt/skin_ai_assistant
sudo chown -R www-data:www-data skin_ai_assistant/
sudo chmod -R 750 skin_ai_assistant/
sudo chmod 640 skin_ai_assistant/.env
```

### 3. Rate Limiting (Nginx)

Add to nginx server blocks:

```nginx
limit_req_zone $binary_remote_addr zone=skinai:10m rate=10r/m;

location /analyze {
    limit_req zone=skinai burst=5;
    # ... rest of proxy config
}
```

### 4. Database Connection Limits

In .env:
```env
# Set reasonable pool sizes
SQLALCHEMY_POOL_SIZE=10
SQLALCHEMY_MAX_OVERFLOW=20
```

---

## Performance Optimization

### 1. Enable Database Connection Pooling

Already configured in SQLAlchemy setup.

### 2. Image Storage

For production with many images, consider:
- AWS S3
- Azure Blob Storage
- Google Cloud Storage

### 3. Caching

Consider adding Redis for:
- API response caching
- Session management

---

## Troubleshooting Production Issues

### Service Won't Start

```bash
# Check logs
sudo journalctl -u skinai-backend -n 50
sudo journalctl -u skinai-ui -n 50
sudo journalctl -u skinai-admin -n 50

# Check if ports are available
sudo netstat -tulpn | grep :8000
sudo netstat -tulpn | grep :8501
sudo netstat -tulpn | grep :8601
```

### Database Connection Issues

```bash
# Test database connection
psql -h localhost -U skinai_user -d skinai_db

# Check PostgreSQL status
sudo systemctl status postgresql
```

### High Memory Usage

```bash
# Check memory
free -h

# Restart services
sudo systemctl restart skinai-backend
sudo systemctl restart skinai-ui
sudo systemctl restart skinai-admin
```

---

## Scaling Considerations

### Horizontal Scaling

1. **Load Balancer:** Use nginx or HAProxy
2. **Multiple Backend Instances:** Run on different ports
3. **Shared Database:** All instances connect to same PostgreSQL
4. **Shared Storage:** Use network storage for images

### Vertical Scaling

1. **Increase RAM:** For larger models
2. **Add GPU:** For faster inference
3. **SSD Storage:** For faster I/O

---

## Maintenance

### Regular Tasks

**Daily:**
- Check service status
- Monitor disk space
- Review error logs

**Weekly:**
- Review analytics
- Check backup integrity
- Update security patches

**Monthly:**
- Database maintenance (VACUUM, ANALYZE)
- Review and archive old data
- Performance optimization

### Updating the Application

```bash
cd /opt/skin_ai_assistant
git pull origin main
cd skin_ai_assistant
source .venv/bin/activate
pip install -r requirements.txt --upgrade

# Restart services
sudo systemctl restart skinai-backend
sudo systemctl restart skinai-ui
sudo systemctl restart skinai-admin
```

---

## Emergency Procedures

### Complete System Failure

1. Check systemd services
2. Check database connectivity
3. Check disk space
4. Review recent logs
5. Restore from backup if needed

### Restore from Backup

```bash
# Stop services
sudo systemctl stop skinai-backend skinai-ui skinai-admin

# Restore database
psql -U skinai_user -d skinai_db < /opt/skin_ai_assistant/backups/db_backup_YYYYMMDD_HHMMSS.sql

# Restore images
tar -xzf /opt/skin_ai_assistant/backups/images_backup_YYYYMMDD_HHMMSS.tar.gz -C /

# Start services
sudo systemctl start skinai-backend skinai-ui skinai-admin
```

---

## Production Checklist

Before going live:

- [ ] SSL certificates installed and auto-renewal configured
- [ ] Database backups automated
- [ ] Monitoring alerts configured
- [ ] Error logging configured
- [ ] Rate limiting enabled
- [ ] Firewall rules configured
- [ ] File permissions secured
- [ ] Admin dashboard protected (basic auth or VPN)
- [ ] All services start on boot
- [ ] Load testing completed
- [ ] Security audit performed
- [ ] Documentation updated
- [ ] Team trained on operations

---

## Support

For production issues:
1. Check application logs: `tail -f /opt/skin_ai_assistant/skin_ai_assistant/skin_ai.log`
2. Check systemd logs: `sudo journalctl -u skinai-backend -f`
3. Check nginx logs: `sudo tail -f /var/log/nginx/error.log`
4. Review this deployment guide

---

**Status:** Production Ready ✅
**Last Updated:** 2025-11-14
