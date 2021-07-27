# VEEAM AHV Proxy Backup

This script creates veeam ahv proxy configuration backups and save them to
local filesystem

Requirements:

* Python: >3.8
* Modules: request, re, json, argparse, time

Usage:

```bash
usage: backup.py [-h] --proxy-hostname PROXY_HOSTNAME [--proxy-username PROXY_USERNAME] [--proxy-password PROXY_PASSWORD] --backup-password BACKUP_PASSWORD [--backup-common | --no-backup-common]
            [--backup-events | --no-backup-events] [--out-dir OUT_DIR]

Create and Download AHV Config Backup

optional arguments:
  -h, --help            show this help message and exit
  --proxy-hostname PROXY_HOSTNAME
                        AHV Proxy Host
  --proxy-username PROXY_USERNAME
                        Proxy Username (default: veeam)
  --proxy-password PROXY_PASSWORD
                        Proxy Password (default: veeam)
  --backup-password BACKUP_PASSWORD
                        Backup Password
  --backup-common, --no-backup-common
                        Include Common Data (default: True)
  --backup-events, --no-backup-events
                        Include Events Data (default: False)
  --out-dir OUT_DIR     Output directory (default: ./)
```

Example:

    ./backup.py --proxy-hostname myproxy.company.net --backup-password 'Hello-World!'


Docker:

```bash
usage: docker run claranet/veeam-ahv-proxy-config-backup [-h] --proxy-hostname PROXY_HOSTNAME [--proxy-username PROXY_USERNAME] [--proxy-password PROXY_PASSWORD] --backup-password BACKUP_PASSWORD [--backup-common | --no-backup-common]
            [--backup-events | --no-backup-events] [--out-dir OUT_DIR]
```

docker-compose:

```yaml
---
version: "3"
services:
  backup:
    image: claranet/veeam-ahv-proxy-config-backup
    command: --no-backup-common
    environment:
      - PROXY_HOSTNAME
      - PROXY_PASSWORD
      - PROXY_USERNAME
      - BACKUP_PASSWORD
    volumes:
      - ./backup:/backup
```
