from django.contrib import admin
from .models import ProblemsModel

@admin.register(ProblemsModel)
class ProblemAdmin(admin.ModelAdmin):
    list_display = ('id', 'problemTitle', 'problemAuthor', 'problemTime')