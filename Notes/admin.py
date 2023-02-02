from django.contrib import admin

from Notes.models import Note
from Notes.models import Labels
# Register your models here.z
admin.site.register(Note)
admin.site.register(Labels)
