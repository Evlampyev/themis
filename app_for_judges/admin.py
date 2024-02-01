from django.contrib import admin
from .models import Judge


@admin.action(description='Сбросить статус до наблюдателя')
def reset_status(modeladmin, request, queryset):
    queryset.update(status='O')


# Register your models here.
# class JudgeAdmin(admin.ModelAdmin):
#     list_display = ['last_name', 'name', 'patronymic', 'status', 'is_active']
#     ordering = ['last_name', 'name']
#     list_filter = ['last_name', 'status', 'organization']
#     search_fields = ['last_name']
#     search_help_text = "Поиск по полю Фамилия пользователя"
#     actions = [reset_status]
#     # readonly_fields = ['organization']
#
#     fieldsets = [
#         (
#             None,
#             {
#                 'classes': ['wide'],
#                 'fields' : ['status', 'last_name', 'name', 'patronymic', 'is_active']
#
#             },
#         ),
#         (
#             'Подробности',
#             {
#                 'classes'    : ['collapse'],
#                 'description': 'Место работы, должность и регалии',
#                 'fields'     : ['organization', 'post', 'regalia']
#             }
#         ),
#         ('Конкурсы и этапы',
#          {
#              'fields': ['competitions']
#          }
#          )
#     ]
#
#
# admin.site.register(Judge, JudgeAdmin)
