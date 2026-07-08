#!/bin/bash
# Backup InfluxDB
influx backup /backups/$(date +%Y%m%d%H%M)
