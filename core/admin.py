from django.contrib import admin
from .models import Person, Permission, Role, SavedSearch 

admin.site.register(Person)
admin.site.register(Permission)
admin.site.register(Role)
admin.site.register(SavedSearch)

