from django.contrib import admin
from .models import FoodLog, CardioLog

# Register your models here.


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'time_stamp', 'meal_name', 'meal_type', 'calories_in'
    ]
    list_filter = ['meal_type', 'time_stamp', 'user']
    search_fields = ['meal_name', 'user__username', 'cardio_desc']
    readonly_fields = ['time_stamp']
    ordering = ['-time_stamp']
    date_hierarchy = 'time_stamp'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'time_stamp', 'meal_name', 'meal_type')
        }),
        ('Workout Details', {
            'fields': ('meal_desc', 'calories_in',),
            'classes': ('collapse',)
        })
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')


@admin.register(CardioLog)
class CardioLogAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'time_stamp', 'cardio_name', 'duration', 'calories_out'
    ]
    list_filter = ['time_stamp', 'user']
    search_fields = ['cardio_name', 'user__username', 'cardio_desc']
    readonly_fields = ['time_stamp']
    ordering = ['-time_stamp']
    date_hierarchy = 'time_stamp'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'time_stamp', 'cardio_name')
        }),
        ('Workout Details', {
            'fields': ('cardio_desc', 'duration', 'calories_out',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
