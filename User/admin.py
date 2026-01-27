from django.contrib import admin

# Note: User is a MongoEngine Document, not a Django ORM model,
# so we do NOT register it with the Django admin site to avoid errors.
# If you later add Django ORM models, register them here with admin.site.register().
