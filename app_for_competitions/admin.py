from django.contrib import admin
from .models import Competition, CompetitionTask


# Register your models here.

class CompetitionAdmin(admin.ModelAdmin):
    list_display = ['fullname', 'name', 'active', 'date']
    ordering = ['date']
    list_filter = ['fullname', 'date']
    search_fields = ['fullname', 'name']
    search_help_text = "Поиск по полю Название конкурса"


class CompetitionTaskAdmin(admin.ModelAdmin):
    list_display = ['name', 'competition', 'judging']
    ordering = ['name', 'competition']
    search_fields = ['name']
    search_help_text = "Поиск по полю Название этапа'"

admin.site.register(Competition, CompetitionAdmin)
admin.site.register(CompetitionTask, CompetitionTaskAdmin)
