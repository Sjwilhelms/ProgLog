"""
Settings loader based on environment.
"""

import os

# Set the environment variable DJANGO_SETTINGS_MODULE to:
# - config.settings.dev (for development)
# - config.settings.prod (for production)
environment = os.environ.get('DJANGO_ENVIRONMENT', 'development')

if environment == 'production':
    from .prod import *
else:
    from .dev import *