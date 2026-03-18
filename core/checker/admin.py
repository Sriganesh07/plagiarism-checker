from django.contrib import admin
from .models import ProjectAbstract

# This tells the Admin panel to show our ProjectAbstract table
admin.site.register(ProjectAbstract)
