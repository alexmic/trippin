"""
Settings loader. To load environment specific settings,
set TRIPPIN_ENV to either 'development' or 'production'. This will
load settings_development.py or settings_production.py respectively.

If the environment variable is not set, it defaults to 'production'.
"""

import os

# Common settings
# 
INDEXING_ENGINE = 'trippin.store.trie.Trie'
SCORE_FUNCTION = 'trippin.scorers.match_length'

# Environment-specific settings
#
environment = os.environ.get('TRIPPIN_ENV', 'production')
if environment == 'production':
    from local_settings.settings_production import *
elif environment == 'development':
    from local_settings.settings_development import *