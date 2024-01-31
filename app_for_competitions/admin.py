from django.contrib import admin
from .models import Competition


# Register your models here.

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'name', 'active', 'date']
    ordering = ['date']
    list_filter = ['fullname', 'date']
    search_fields = ['fullname', 'name']
    search_help_text = "Поиск по полю Название конкурса"


admin.site.register(Competition, CompetitionAdmin)
