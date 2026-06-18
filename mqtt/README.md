# MQTT

Mosquitto MQTT broker configuration for PowerGuard IoT.

## Topic Structure

```
home/energy/{device_id}/{channel}   — Sensor readings per channel
home/energy/alerts                  — Anomaly alert notifications
home/energy/status                  — Device online/offline status
```
