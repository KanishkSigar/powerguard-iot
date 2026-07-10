# Production Deployment Guide

This document describes how to deploy the PowerGuard IoT stack in a production environment using Docker Compose overrides, security hardening, and volume backups.

---

## 1. Production Architecture (`docker-compose.yml`)

For production environments, the services run inside isolated Docker containers managed by `docker-compose.yml`.

### Key Differences from Development
- **No Hot Reloading**: FastAPI runs under standard Gunicorn/Uvicorn workers without `--reload` mode.
- **Port Exposure**: InfluxDB and Mosquitto ports are NOT exposed to the public internet. Only the FastAPI backend and reverse proxy (e.g. Nginx) are exposed.
- **Persistent Volumes**: All InfluxDB data is stored on persistent host volumes under `/var/lib/influxdb2`.

---

## 2. Hardening Checklist

### MQTT Security
1. **Enable Authentication**: Configure password files for Mosquitto in `mosquitto.conf`.
2. **Enable TLS**: Encrypt traffic from the ESP32 devices to the broker using Port `8883` and self-signed certificates or Let's Encrypt certificates.

### Database Hardening
1. **Disable Default Tokens**: Change `INFLUXDB_TOKEN` in your `.env` to a strong cryptographically generated token.
2. **Restrict Access**: Ensure InfluxDB is only accessible on the internal Docker bridge network.

### Backend Security
1. **Secure CORS**: Restrict `CORS_ORIGINS` to the exact host domain of your dashboard instead of wildcard (`*`).
2. **Production Secrets**: Fill in active `EMAIL_PASSWORD` and `TELEGRAM_BOT_TOKEN` for alerting.

---

## 3. Deployment Command Execution

Run the complete multi-container production stack:
```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d --build
```

---

## 4. Backups and Database Maintenance

### Database Backup Script
To backup your InfluxDB bucket to a backup directory:
```bash
docker-compose exec influxdb influx backup /etc/influxdb2/backups/pg_backup_$(date +%F) --token <admin-token>
```

### Database Restore Script
To restore a backup directory:
```bash
docker-compose exec influxdb influx restore /etc/influxdb2/backups/pg_backup_YYYY-MM-DD --token <admin-token>
```
