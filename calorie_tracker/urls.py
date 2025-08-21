from django.urls import path
from .views import (
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

url_patterns = [

    # Food URLS

    path('food/', FoodDayView.as_view(), name='food_list'),
    path('food/add', FoodCreateView.as_view(), name='add_food'),
    path('food/<int:pk>/', FoodDetailView.as_view(), name='food_detail'),
    path(
        'food/week/calendar',
        FoodCalendarWeekView.as_view(),
        name='food_calendar_week'),
    path(
        'food/week/rolling',
        FoodRollingWeekView.as_view(),
        name='food_rolling_week'),

    # Cardio URLS

    path('cardio/', CardioDayView.as_view(), name='cardio_list'),
    path('cardio/add', CardioCreateView.as_view(), name='add_cardio'),
    path(
        'cardio//<int:pk>/',
        CardioDetailView.as_view(),
        name='cardio_detail'),
    path(
        'cardio/week/calendar',
        CardioCalendarWeekView.as_view(),
        name='cardio_calendar_week'),
    path(
        'cardio/week/rolling',
        CardioRollingWeekView.as_view(),
        name='cardio_rolling_week'),
]
