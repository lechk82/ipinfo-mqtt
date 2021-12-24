# ipinfo-mqtt
ipinfo mqtt client

### Using Docker
Supported platforms: linux/amd64, linux/arm/v7, linux/arm64

Docker example to run this script every 5 minutes and providing a config file:

```lang=bash
cd /opt
git clone https://github.com/lechk82/ipinfo-mqtt
cd ipinfo-mqtt
mv config.sample.json config.json # setup your config
sudo docker run --name ipinfo-mqtt -d --restart unless-stopped -v /opt/ipinfo-mqtt:/opt/app-root/src ghcr.io/lechk82/ipinfo-mqtt:latest
```
### Using docker-compose

This `docker-compose.yml` example can be used with docker-compose or podman-compose

```lang=yaml
version: '3'

services:
  ipinfo-mqtt:
    image: ghcr.io/lechk82/ipinfo-mqtt:latest
    container_name: "ipinfo-mqtt"
    environment:
    - TZ=Europe/Berlin
    volumes:
      - /opt/ipinfo-mqtt:/opt/app-root/src
    restart: unless-stopped
```

### Using Python

Run `pip install paho_mqtt ` and start `python3 run.py`.
