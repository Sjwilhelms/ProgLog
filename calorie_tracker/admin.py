from django.contrib import admin
from .models import FoodLog, CardioLog

# Register your models here.


@admin.register(FoodLog)
class FoodLogAdmin(admin.ModelAdmin):
    list_display = [
        'user', 'timestamp', 'meal_name', 'meal_type', 'calories_in'
    ]
    list_filter = ['meal_type', 'timestamp', 'user']
    search_fields = ['meal_name', 'user__username', 'cardio_desc']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'timestamp', 'meal_name', 'meal_type')
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
        'user', 'timestamp', 'cardio_name', 'duration', 'calories_out'
    ]
    list_filter = ['timestamp', 'user']
    search_fields = ['cardio_name', 'user__username', 'cardio_desc']
    readonly_fields = ['timestamp']
    ordering = ['-timestamp']
    date_hierarchy = 'timestamp'

    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'timestamp', 'cardio_name')
        }),
        ('Workout Details', {
            'fields': ('cardio_desc', 'duration', 'calories_out',),
            'classes': ('collapse',)
        }),
    )

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('user')
