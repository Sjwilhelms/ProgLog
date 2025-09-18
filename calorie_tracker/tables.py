from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
from .models import FoodLog, CardioLog

MEAL_TYPES = [
    FoodLog.BREAKFAST,
    FoodLog.LUNCH,
    FoodLog.DINNER,
    FoodLog.SNACK
]


def get_week_summary(user, start_date, days_count=7, reverse_order=False):
    """
    Generate summary data for a sequence of days starting from start_date.


    :param user: User object
    :param start_date: First day in the period (date object)
    :param days_count: Number of days (default 7)
    :param reverse_order: If True, reverse the order of days
    :return:
    dict containing
    days,
    table_data,
    food_totals,
    exercise_totals,
    net_calories
    """
    days = [start_date + timedelta(days=i) for i in range(days_count)]
    day_names = [day.strftime("%a") for day in days]

    table_data = {meal: [] for meal in MEAL_TYPES}
    food_totals, exercise_totals, net_calories = [], [], []

    for day in days:
        for meal in MEAL_TYPES:
            total = (
                FoodLog.objects.filter(
                    user=user, meal_type=meal, timestamp__date=day
                ).aggregate(Sum('calories_in'))['calories_in__sum'] or 0
            )
            table_data[meal].append(total)

        food_total = FoodLog.total_food_day(user, date=day)
        exercise_total = CardioLog.total_burn_day(user, date=day)
        net = food_total - exercise_total

        food_totals.append(food_total)
        exercise_totals.append(exercise_total)
        net_calories.append(net)

    if reverse_order:
        days.reverse()
        day_names.reverse()
        food_totals.reverse()
        exercise_totals.reverse()
        net_calories.reverse()
        for meal in MEAL_TYPES:
            table_data[meal].reverse()

    meal_totals = {meal: sum(table_data[meal]) for meal in MEAL_TYPES}

    meal_rows = []
    for meal in MEAL_TYPES:
        meal_rows.append({
            "meal": meal,
            "values": table_data[meal],
            "total": sum(table_data[meal])
        })

    return {
        "days": day_names,
        "table_data": table_data,
        "food_totals": food_totals,
        "exercise_totals": exercise_totals,
        "net_calories": net_calories,
        "meal_totals": meal_totals,
    }


def get_year_summary(user, year=None):
    """
    Generate summary data for all 12 months in a year
    """
    year = year or timezone.now().date().year
    months = [
        'Jan',
        'Feb',
        'Mar',
        'Apr',
        'May',
        'Jun',
        'Jul',
        'Aug',
        'Sep',
        'Oct',
        'Nov',
        'Dec'
    ]

    food_monthly = []
    cardio_monthly = []
    net_monthly = []

    for month in range(1, 13):
        food_total = FoodLog.total_food_month(user, year, month)
        cardio_total = CardioLog.total_burn_month(user, year, month)
        net_total = food_total - cardio_total

        food_monthly.append(food_total)
        cardio_monthly.append(cardio_total)
        net_monthly.append(net_total)

    return {
        "months": months,
        "food_totals": food_monthly,
        "exercise_totals": cardio_monthly,
        "net_calories": net_monthly,
        "yearly_totals": {
            'food_year': sum(food_monthly),
            'cardio_year': sum(cardio_monthly),
            'net_year': sum(net_monthly),
        }
    }


def get_calendar_week_summary(user, reference_date=None):
    today = reference_date or timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())  # Monday
    return get_week_summary(user, start_of_week)


def get_rolling_week_summary(user, reference_date=None):
    today = reference_date or timezone.now().date()
    start_of_rolling = today - timedelta(days=6)  # Last 7 days including today
    return get_week_summary(user, start_of_rolling, reverse_order=False)
