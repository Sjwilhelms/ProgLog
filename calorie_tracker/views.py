from django.db.models import Sum
from django.contrib import messages
from django.shortcuts import render
from django.views.generic import (
    CreateView,
    ListView,
    DetailView,
    TemplateView)
from django.urls import reverse_lazy
from django.utils import timezone
from datetime import timedelta
from .models import FoodLog, CardioLog
from .forms import FoodForm, CardioForm
from .services import (
    net_calorie_day,
    net_calorie_rolling_week,
    net_calorie_calendar_week
)

# dashboard view


class DashboardView(TemplateView):

    template_name = 'overview/dashboard.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['food_logs_day'] = FoodLog.logs_for_day(
            self.request.user)
        context['food_logs_rolling_week'] = FoodLog.logs_for_rolling_week(
            self.request.user)
        context['food_logs_calendar_week'] = FoodLog.logs_for_calendar_week(
            self.request.user)
        context['cardio_logs_day'] = CardioLog.logs_for_day(
            self.request.user)
        context['cardio_logs_rolling_week'] = CardioLog.logs_for_rolling_week(
            self.request.user)
        context['cardio_logs_calendar_week'] = CardioLog.logs_for_calendar_week(
            self.request.user)
        context['net_calorie_day'] = net_calorie_day(
            self.request.user)
        context['net_calorie_rolling_week'] = net_calorie_rolling_week(
            self.request.user)
        context['net_calorie_calendar_week'] = net_calorie_calendar_week(
            self.request.user)

        return context


# fucntional view for viewing a weekly summary table

def weekly_summary(request):
    user = request.user
    today = timezone.now().date()

    # Get start and end of current week (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    days = [start_of_week + timedelta(days=i) for i in range(7)]
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    meal_types = [FoodLog.BREAKFAST, FoodLog.LUNCH, FoodLog.DINNER, FoodLog.SNACK]

    # Prepare data structure
    table_data = {meal: [] for meal in meal_types}
    food_totals = []
    exercise_totals = []
    net_calories = []

    for day in days:
        # For each meal type
        for meal in meal_types:
            total = (
                FoodLog.objects.filter(user=user, meal_type=meal, timestamp__date=day)
                .aggregate(Sum('calories_in'))['calories_in__sum'] or 0
            )
            table_data[meal].append(total)

        # Daily totals
        food_total = FoodLog.total_food_day(user, date=day)
        exercise_total = CardioLog.total_burn_day(user, date=day)
        net = food_total - exercise_total

        food_totals.append(food_total)
        exercise_totals.append(exercise_total)
        net_calories.append(net)

    context = {
        "days": day_names,
        "table_data": table_data,
        "food_totals": food_totals,
        "exercise_totals": exercise_totals,
        "net_calories": net_calories,
    }

    return render(request, "overview/weekly_summary.html", context)

# List Views for viewing food logs


class FoodDetailView(DetailView):
    model = FoodLog
    template_name = 'food/food_detail.html'
    context_object_name = 'food_logs'

    def get_queryset(self):
        return FoodLog.objects.filter(user=self.request.user)


class FoodDayView(ListView):
    model = FoodLog
    template_name = 'food/food_day.html'
    context_object_name = 'food_logs'

    def get_queryset(self):
        return FoodLog.logs_for_day(self.request.user)


class FoodCalendarWeekView(ListView):
    model = FoodLog
    template_name = 'food/food_calendar_week.html'
    context_object_name = 'food_logs'

    def get_queryset(self):
        return FoodLog.logs_for_calendar_week(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_calories'] = FoodLog.total_food_calendar_week(
            self.request.user)
        return context


class FoodRollingWeekView(ListView):
    model = FoodLog
    template_name = 'food/food_rolling_week.html'
    context_object_name = 'food_logs'

    def get_queryset(self):
        return FoodLog.logs_for_rolling_week(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_calories'] = FoodLog.total_food_rolling_week(
            self.request.user)
        return context

# List Views for viewing cardio logs


class CardioDetailView(DetailView):
    model = CardioLog
    template_name = 'cardio/cardio_detail.html'
    context_object_name = 'cardio_logs'

    def get_queryset(self):
        return CardioLog.objects.filter(user=self.request.user)


class CardioDayView(ListView):
    model = CardioLog
    template_name = 'cardio/cardio_day.html'
    context_object_name = 'cardio_logs'

    def get_queryset(self):
        return CardioLog.logs_for_day(self.request.user)


class CardioCalendarWeekView(ListView):
    model = CardioLog
    template_name = 'cardio/cardio_calendar_week.html'
    context_object_name = 'cardio_logs'

    def get_queryset(self):
        return CardioLog.logs_for_calendar_week(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_calories'] = CardioLog.total_burn_calendar_week(
            self.request.user)
        return context


class CardioRollingWeekView(ListView):
    model = CardioLog
    template_name = 'cardio/cardio_rolling_week.html'
    context_object_name = 'cardio_logs'

    def get_queryset(self):
        return CardioLog.logs_for_rolling_week(self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_calories'] = CardioLog.total_burn_rolling_week(
            self.request.user)
        return context

# Create Views for adding logs with forms


class FoodCreateView(CreateView):
    model = FoodLog
    form_class = FoodForm
    template_name = 'food/add_food.html'
    success_url = reverse_lazy('calorie_tracker:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Food Log added successfully!")
        return super().form_valid(form)


class CardioCreateView(CreateView):
    model = CardioLog
    form_class = CardioForm
    template_name = 'cardio/add_cardio.html'
    success_url = reverse_lazy('calorie_tracker:home')

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Cardio Log added successfully!")
        return super().form_valid(form)
