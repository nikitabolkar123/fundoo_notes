from django.contrib import admin
from notes.models import Note
from notes.models import Labels
# Register your models here.z
admin.site.register(Note)
admin.site.register(Labels)
class NoteAdmin(admin.ModelAdmin):
    list_display =('flower')