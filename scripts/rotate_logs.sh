#!/usr/bin/env bash
# ==============================================================================
# PowerGuard IoT — Automated Log Rotation & Compression Utility
#
# Rotates, archives, and prunes backend, broker, and database logs to maintain
# disk space integrity on edge gateways and cloud deployment servers.
# ==============================================================================

set -euo pipefail

LOG_DIR="${1:-/var/log/powerguard}"
RETENTION_DAYS="${RETENTION_DAYS:-14}"
MAX_SIZE_MB="${MAX_SIZE_MB:-50}"
DRY_RUN="${DRY_RUN:-false}"

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Starting PowerGuard Log Rotation"
echo "Target directory: ${LOG_DIR}"
echo "Retention policy: ${RETENTION_DAYS} days"
echo "Max uncompressed size: ${MAX_SIZE_MB}MB"

if [ ! -d "${LOG_DIR}" ]; then
    echo "Notice: Log directory ${LOG_DIR} does not exist. Creating..."
    if [ "${DRY_RUN}" = "false" ]; then
        mkdir -p "${LOG_DIR}"
    fi
fi

# 1. Compress logs exceeding size threshold or modified > 24h
echo "Scanning for uncompressed active log files..."
find "${LOG_DIR}" -type f -name "*.log" -size +"${MAX_SIZE_MB}"M | while read -r logfile; do
    echo "Compressing: ${logfile}"
    if [ "${DRY_RUN}" = "false" ]; then
        timestamp=$(date -u +'%Y%m%d_%H%M%S')
        mv "${logfile}" "${logfile}.${timestamp}"
        gzip -9 "${logfile}.${timestamp}"
        touch "${logfile}"
    fi
done

# 2. Prune archives older than retention threshold
echo "Pruning compressed archives older than ${RETENTION_DAYS} days..."
find "${LOG_DIR}" -type f -name "*.gz" -mtime +"${RETENTION_DAYS}" | while read -r old_archive; do
    echo "Removing expired log: ${old_archive}"
    if [ "${DRY_RUN}" = "false" ]; then
        rm -f "${old_archive}"
    fi
done

echo "[$(date -u +'%Y-%m-%dT%H:%M:%SZ')] Log rotation completed successfully."
exit 0