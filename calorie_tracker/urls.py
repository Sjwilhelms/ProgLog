from django.urls import path
from . import views
from .views import (
    DashboardView,
    FoodDetailView,
    FoodDayView,
    FoodCalendarWeekView,
    FoodRollingWeekView,
    FoodCreateView,
    CardioDetailView,
    CardioDayView,
    CardioCalendarWeekView,
    CardioRollingWeekView,
    CardioCreateView
)

app_name = 'calorie_tracker'

urlpatterns = [
    # Overview URLS

    path('', DashboardView.as_view(), name='home'),
    path('weekly-summary/', views.weekly_summary, name='weekly_summary'),

    # Food URLS

    path('food/', FoodDayView.as_view(), name='food_day'),
    path('food/add/', FoodCreateView.as_view(), name='add_food'),
    path('food/<int:pk>/', FoodDetailView.as_view(), name='food_detail'),
    path(
        'food/week/calendar/',
        FoodCalendarWeekView.as_view(),
        name='food_calendar_week'),
    path(
        'food/week/rolling/',
        FoodRollingWeekView.as_view(),
        name='food_rolling_week'),

    # Cardio URLS

    path('cardio/', CardioDayView.as_view(), name='cardio_day'),
    path('cardio/add/', CardioCreateView.as_view(), name='add_cardio'),
    path(
        'cardio/<int:pk>/',
        CardioDetailView.as_view(),
        name='cardio_detail'),
    path(
        'cardio/week/calendar/',
        CardioCalendarWeekView.as_view(),
        name='cardio_calendar_week'),
    path(
        'cardio/week/rolling/',
        CardioRollingWeekView.as_view(),
        name='cardio_rolling_week'),
]
