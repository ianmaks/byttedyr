from django.apps import AppConfig
from pillow_heif import register_heif_opener

class MarketplaceConfig(AppConfig):
    name = 'marketplace'
    def ready(self):
        register_heif_opener()
