from .models import FoodLog, CardioLog
from django.utils import timezone

# methods for getting net calories


def net_calorie_day(user, date=None):
    date = date or timezone.now().date()
    calories_in = FoodLog.total_food_day(user, date)
    calories_out = CardioLog.total_burn_day(user, date)
    net_day = calories_in - calories_out
    return net_day


def net_calorie_rolling_week(user, date=None):
    date = date or timezone.now().date()
    calories_in = FoodLog.total_food_rolling_week(user, date)
    calories_out = CardioLog.total_burn_rolling_week(user, date)
    net_rolling_week = calories_in - calories_out
    return net_rolling_week


def net_calorie_calendar_week(user, date=None):
    date = date or timezone.now().date()
    calories_in = FoodLog.total_food_calendar_week(user, date)
    calories_out = CardioLog.total_burn_calendar_week(user, date)
    net_calendar_week = calories_in - calories_out
    return net_calendar_week


def net_calorie_month(user, year=None, month=None):
    year = year or timezone.now().date().year
    month = month or timezone.now().date().month
    calories_in = FoodLog.total_food_month(user, year, month)
    calories_out = CardioLog.total_burn_month(user, year, month)
    net_month = calories_in - calories_out
    return net_month


def net_calorie_year(user, year=None):
    year = year or timezone.now().date().year
    calories_in = FoodLog.total_food_year(user, year)
    calories_out = CardioLog.total_burn_year(user, year)
    net_year = calories_in - calories_out
    return net_year
