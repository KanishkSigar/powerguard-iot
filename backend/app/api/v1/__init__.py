"""
PowerGuard IoT — API v1 Router Aggregator
Mounts all 32 REST endpoint subrouters onto the unified v1 API router.
"""
from fastapi import APIRouter
from app.api.v1.endpoints import (
    devices, readings, alerts, anomalies, dashboard,
    tariffs, billing, reports, export, firmware,
    schedules, health, metrics, logs, audit,
    auth, users, roles, permissions, notifications,
    webhooks, integrations, settings, rules,
    groups, keys, mfa, oauth, preferences, sessions, status, tokens
)

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(devices.router)
v1_router.include_router(readings.router)
v1_router.include_router(alerts.router)
v1_router.include_router(anomalies.router)
v1_router.include_router(dashboard.router)
v1_router.include_router(tariffs.router)
v1_router.include_router(billing.router)
v1_router.include_router(reports.router)
v1_router.include_router(export.router)
v1_router.include_router(firmware.router)
v1_router.include_router(schedules.router)
v1_router.include_router(health.router)
v1_router.include_router(metrics.router)
v1_router.include_router(logs.router)
v1_router.include_router(audit.router)
v1_router.include_router(auth.router)
v1_router.include_router(users.router)
v1_router.include_router(roles.router)
v1_router.include_router(permissions.router)
v1_router.include_router(notifications.router)
v1_router.include_router(webhooks.router)
v1_router.include_router(integrations.router)
v1_router.include_router(settings.router)
v1_router.include_router(rules.router)
v1_router.include_router(groups.router)
v1_router.include_router(keys.router)
v1_router.include_router(mfa.router)
v1_router.include_router(oauth.router)
v1_router.include_router(preferences.router)
v1_router.include_router(sessions.router)
v1_router.include_router(status.router)
v1_router.include_router(tokens.router)

__all__ = ["v1_router"]