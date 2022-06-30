from django.contrib import admin

from . import models

admin.site.register(models.Photo)
admin.site.register(models.Product)
admin.site.register(models.Asset)
admin.site.register(models.ValueAsset)
admin.site.register(models.Favorites)
admin.site.register(models.History)
admin.site.register(models.Category)
admin.site.register(models.AssetTemplate)

