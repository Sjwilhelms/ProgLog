from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta

# Create your models here.


class BaseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    time_stamp = models.DateTimeField()

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['user', 'time_stamp'])
        ]

    @classmethod
    def _total_for_day(cls, user, field_name, date=None):
        date = date or timezone.now().date()
        return (
            cls.objects
            .filter(user=user, time_stamp__date=date)
            .aggregate(total=Sum(field_name))['total']
            or 0
        )

    @classmethod
    def _total_for_rolling_week(cls, user, field_name, reference_date=None):
        reference_date = reference_date or timezone.now().date()
        start_date = reference_date - timedelta(days=6)
        return (
            cls.objects
            .filter(
                user=user,
                time_stamp__date__range=(start_date, reference_date)
                )
            .aggregate(total=Sum(field_name))['total']
            or 0
        )

    @classmethod
    def _total_for_calendar_week(cls, user, field_name, reference_date=None):
        reference_date = reference_date or timezone.now().date()
        start_of_week = (
            reference_date - timedelta(days=reference_date.weekday())
        )  # Monday
        end_of_week = start_of_week + timedelta(days=6)  # Sunday
        return (
            cls.objects
            .filter(
                user=user,
                time_stamp__date__range=(start_of_week, end_of_week))
            .aggregate(total=Sum(field_name))['total']
            or 0
        )


class FoodLog(BaseLog):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"

    MEAL_CHOICES = [
        (BREAKFAST, "Breakfast"),
        (LUNCH, "Lunch"),
        (DINNER, "Dinner"),
        (SNACK, "Snack"),
    ]

    meal_name = models.CharField(max_length=100)
    meal_desc = models.TextField(blank=True, null=True)
    meal_type = models.CharField(max_length=20, choices=MEAL_CHOICES)
    calories_in = models.FloatField(validators=[MinValueValidator(1)])

    def __str__(self):
        return (
            f"{self.user} -"
            f"{self.time_stamp:%Y-%m-%d %H:%M} -"
            f"{self.meal_name} -"
            f"{self.meal_type} -"
            f"{self.calories_in}"
        )

    @classmethod
    def total_food_day(cls, user, date=None):
        return cls._total_for_day(user, 'calories_in', date)

    @classmethod
    def total_food_rolling_week(cls, user, reference_date=None):
        return cls._total_for_rolling_week(user, 'calories_in', reference_date)

    @classmethod
    def total_food_calendar_week(cls, user, reference_date=None):
        return cls._total_for_calendar_week(
            user, 'calories_in', reference_date)


class CardioLog(BaseLog):
    cardio_name = models.CharField(max_length=100)
    cardio_desc = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(
        help_text="Duration in Minutes", validators=[MinValueValidator(1)])
    calories_out = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return (
            f"{self.user} -"
            f"{self.time_stamp:%Y-%m-%d %H:%M} -"
            f"{self.cardio_name} -"
            f"{self.calories_out}"
        )

    @classmethod
    def total_burn_day(cls, user, date=None):
        return cls._total_for_day(user, 'calories_out', date)

    @classmethod
    def total_burn_rolling_week(cls, user, reference_date=None):
        return (
            cls
            ._total_for_rolling_week(user, 'calories_out', reference_date)
            )

    @classmethod
    def total_burn_calendar_week(cls, user, reference_date=None):
        return (
            cls
            ._total_for_calendar_week(user, 'calories_out', reference_date)
            )
