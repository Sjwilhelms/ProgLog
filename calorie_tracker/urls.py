from django.urls import path
from . import views
from .views import (
    DashboardView,
    ProfileDetailView,
    ProfileUpdateView,
    FoodDetailView,
    FoodDayView,
    FoodCalendarWeekView,
    FoodRollingWeekView,
    FoodCreateView,
    FoodUpdateView,
    FoodDeleteView,
    CardioDetailView,
    CardioDayView,
    CardioCalendarWeekView,
    CardioRollingWeekView,
    CardioCreateView,
    CardioUpdateView,
    CardioDeleteView,
)

app_name = 'calorie_tracker'

urlpatterns = [
    # Overview URLS

    path('', DashboardView.as_view(), name='home'),
    path(
        'calendar-week-summary/', views.calendar_week_summary,
        name='calendar_week_summary'),
    path(
        'rolling-week-summary/',
        views.rolling_week_summary,
        name='rolling_week_summary'),

    # User profile URLS

    path('profile/', ProfileDetailView.as_view(), name='profile_detail'),
    path('profile/update', ProfileUpdateView.as_view(), name='profile_update'),

    # Food URLS

    path('food/', FoodDayView.as_view(), name='food_day'),
    path('food/add/', FoodCreateView.as_view(), name='add_food'),

    path('food/<int:pk>/', FoodDetailView.as_view(), name='food_detail'),
    path(
        'food/<int:pk>/update/',
        FoodUpdateView.as_view(),
        name="update_food"),
    path(
        'food/<int:pk>/delete/',
        FoodDeleteView.as_view(),
        name="delete_food"),
    path(
        'food/week/calendar/',
        FoodCalendarWeekView.as_view(),
        name='food_calendar_week'),
    path(
        'food/week/rolling/',
        FoodRollingWeekView.as_view(),
        name='food_rolling_week'),

    # Cardio URLS

    path(
        'cardio/', CardioDayView.as_view(), name='cardio_day'),
    path(
        'cardio/add/', CardioCreateView.as_view(), name='add_cardio'),

    path(
        'cardio/<int:pk>/',
        CardioDetailView.as_view(),
        name='cardio_detail'),
    path(
        'cardio/<int:pk>/update/',
        CardioUpdateView.as_view(),
        name="update_cardio"),
    path(
        'cardio/<int:pk>/delete/',
        CardioDeleteView.as_view(),
        name="delete_cardio"),
    path(
        'cardio/week/calendar/',
        CardioCalendarWeekView.as_view(),
        name='cardio_calendar_week'),
    path(
        'cardio/week/rolling/',
        CardioRollingWeekView.as_view(),
        name='cardio_rolling_week'),
]
