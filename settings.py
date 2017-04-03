import os

# Cluster info
CLUSTER_NAME = os.environ.get('CLUSTER_NAME', '')

# Notifications
SLACK_TOKEN = os.environ.get('SLACK_TOKEN', '')
SLACK_CHANNEL = os.environ.get('SLACK_CHANNEL', '#alerts')

# Monitoring
UPDATE_INTERVAL = int(os.environ.get('UPDATE_INTERVAL', 60))

CONF_PATH = os.environ.get('CONF_PATH', '/usr/src/app/conf/config.yaml')

try:
    from local_settings import *
except ImportError:
    pass
