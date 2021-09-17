import os

import class_settings

def set_settings():
    """
    Set local/production settings according to usage
    """
    if(os.path.exists("poker/settings/local.py")):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poker.settings.local")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "poker.settings.base")
    os.environ.setdefault('DJANGO_SETTINGS_CLASS', 'Setting')

set_settings()
class_settings.setup()
