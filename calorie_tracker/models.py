from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.core.validators import MinValueValidator
from django.db.models import Sum
from django.dispatch import receiver
from django.utils import timezone
from datetime import timedelta, date
from calendar import monthrange

# Create your models here.


class UserProfile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    height = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    weight = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    weight_goal = models.DecimalField(
        max_digits=5, decimal_places=2, null=True, blank=True)
    cardio_goal = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def bmi(self):
        if self.height and self.weight:
            height_m = float(self.height) / 100
            return round(float(self.weight) / (height_m ** 2), 1)

    @property
    def weight_difference(self):
        if self.weight and self.weight_goal:
            return float(self.weight) - float(self.weight_goal)


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        UserProfile.objects.get_or_create(user=instance)


class BaseLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        indexes = [
            models.Index(fields=['user', 'timestamp'])
        ]

    # class methods for totalling calories for day and weeks

    @classmethod
    def _total_for_day(cls, user, field_name, date=None):
        date = date or timezone.now().date()
        return (
            cls.objects
            .filter(user=user, timestamp__date=date)
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
                timestamp__date__range=(start_date, reference_date)
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
                timestamp__date__range=(start_of_week, end_of_week))
            .aggregate(total=Sum(field_name))['total']
            or 0
        )

    @classmethod
    def _total_for_month(cls, user, field_name, year=None, month=None):
        """
        Get total for a specific moonth and year
        """
        if year is None or month is None:
            today = timezone.now().date()
            year = year or today.year
            month = month or today.month

        # get first and last day of month
        start_date = date(year, month, 1)
        _, last_day = monthrange(year, month)
        end_date = date(year, month, last_day)

        return (
            cls.objects.filter(
                user=user,
                timestamp__date__range=(start_date, end_date)
            )
            .aggregate(total=Sum(field_name))['total']
            or 0
        )

    def _total_for_year(cls, user, field_name, year=None):
        """
        Get total for the year
        """

        year = year or timezone.now().date().year
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)

        return (
            cls.objects
            .filter(
                user=user,
                timestamp__date__range=(start_date, end_date)
            )
            .aggregate(total=Sum(field_name))['total']
            or 0
        )

    def _monthly_breakdown_for_year(cls, user, field_name, year=None):
        """
        Get monthly totals for each month in a year
        """

        year = year or timezone.now().date().year
        monthly_data = []

        for month in range(1, 13):
            total = cls._total_for_month(user, field_name, year, month)
            monthly_data.append({
                'month': month,
                'month_name': date(year, month, 1).strftime('%B'),
                'year': year,
                'total': total
            })

        return monthly_data

    # queryset methods for the views

    @classmethod
    def logs_for_day(cls, user, date=None):
        date = date or timezone.now().date()
        return cls.objects.filter(user=user, timestamp__date=date)

    @classmethod
    def logs_for_rolling_week(cls, user, reference_date=None):
        reference_date = reference_date or timezone.now().date()
        start_date = reference_date - timedelta(days=6)
        return cls.objects.filter(user=user, timestamp__date__range=(
            start_date, reference_date))

    @classmethod
    def logs_for_calendar_week(cls, user, reference_date=None):
        reference_date = reference_date or timezone.now().date()
        start_of_week = reference_date - timedelta(
            days=reference_date.weekday())
        end_of_week = start_of_week + timedelta(days=6)
        return cls.objects.filter(user=user, timestamp__date__range=(
            start_of_week, end_of_week))

    @classmethod
    def logs_for_months(cls, user, year=None, month=None):
        """
        Get all logs for a specific month
        """
        if year is None or month is None:
            today = timezone.now().date()
            year = year or today.year
            month = month or today.month

        start_date = date(year, month, 1)
        _, last_day = monthrange(year, month)
        end_date = date(year, month, last_day)

        return cls.objects.filter(
            user=user,
            timestamp__date__range=(start_date, end_date)
        )

    @classmethod
    def logs_for_year(cls, user, field_name, year=None):
        """
        Get all logs for a specific year
        """

        year = year or timezone.now().date().year
        start_date = date(year, 1, 1)
        end_date = date(year, 12, 31)

        return cls.objects.filter(
            user=user,
            timestamp__date__range=(start_date, end_date)
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
            f"{self.timestamp:%Y-%m-%d %H:%M} -"
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

    @classmethod
    def total_food_month(cls, user, year=None, month=None):
        return cls._total_for_month(user, 'calories_in', year, month)

    @classmethod
    def total_food_year(cls, user, year=None, month=None):
        return cls._total_for_year(user, 'calories_in', year)

    @classmethod
    def monthly_food_breakdown(cls, user, year=None):
        return cls._monthly_breakdown_for_year(user, 'calories_in', year)


class CardioLog(BaseLog):
    cardio_name = models.CharField(max_length=100)
    cardio_desc = models.TextField(blank=True, null=True)
    duration = models.PositiveIntegerField(
        help_text="Duration in Minutes", validators=[MinValueValidator(1)])
    calories_out = models.FloatField(validators=[MinValueValidator(0)])

    def __str__(self):
        return (
            f"{self.user} -"
            f"{self.timestamp:%Y-%m-%d %H:%M} -"
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

    @classmethod
    def total_burn_month(cls, user, year=None, month=None):
        return cls._total_for_month(user, 'calories_out', year, month)

    @classmethod
    def total_burn_year(cls, user, year=None, month=None):
        return cls._total_for_year(user, 'calories_out', year)

    @classmethod
    def monthly_burn_breakdown(cls, user, year=None):
        return cls._monthly_breakdown_for_year(user, 'calories_out', year)
