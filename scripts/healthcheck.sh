#!/bin/bash
# Healthcheck script
curl -f http://localhost:8000/system/info || exit 1
