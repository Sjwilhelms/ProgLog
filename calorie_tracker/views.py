from django.db.models import Sum
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404
from django.views.generic import (
    CreateView,
    UpdateView,
    DeleteView,
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
    net_calorie_calendar_week,
    net_calorie_month,
    net_calorie_year
)
from .tables import (
    get_calendar_week_summary,
    get_rolling_week_summary,
    get_year_summary
)


# overview/dashboard view
# the Dashboard View


class DashboardView(LoginRequiredMixin, TemplateView):

    template_name = 'overview/dashboard.html'

    def get_context_data(self, **kwargs):
        if self.request.user.is_authenticated:
            context = super().get_context_data(**kwargs)

            # set page title
            context['page_title'] = 'Dashboard'

        # food logs
        context['food_logs_day'] = FoodLog.logs_for_day(
            self.request.user)
        context['food_logs_rolling_week'] = FoodLog.logs_for_rolling_week(
            self.request.user)
        context['food_logs_calendar_week'] = FoodLog.logs_for_calendar_week(
            self.request.user)

        # cardio logs
        context['cardio_logs_day'] = CardioLog.logs_for_day(
            self.request.user)
        context['cardio_logs_rolling_week'] = CardioLog.logs_for_rolling_week(
            self.request.user)
        context['cardio_logs_calendar_week'] = (
            CardioLog
            .logs_for_calendar_week(self.request.user))

        # net calories
        context['net_calorie_day'] = net_calorie_day(
            self.request.user)
        context['net_calorie_rolling_week'] = net_calorie_rolling_week(
            self.request.user)
        context['net_calorie_calendar_week'] = net_calorie_calendar_week(
            self.request.user)

        # Rolling week summary data
        rolling_data = get_rolling_week_summary(self.request.user)
        context.update({
            'rolling': {
                "rolling_days": rolling_data["days"],
                "rolling_table_data": rolling_data["table_data"],
                "rolling_food_totals": rolling_data["food_totals"],
                "rolling_exercise_totals": rolling_data["exercise_totals"],
                "rolling_net_calories": rolling_data["net_calories"],
            }
        })

        # Calendar week summary data
        calendar_data = get_calendar_week_summary(self.request.user)
        context.update({
            'calendar': {
                "days": calendar_data["days"],
                "table_data": calendar_data["table_data"],
                "food_totals": calendar_data["food_totals"],
                "exercise_totals": calendar_data["exercise_totals"],
                "net_calories": calendar_data["net_calories"],
            }
        })

        # month and year summary data
        year_data = get_year_summary(self.request.user)
        context.update({
            'year': {
                'table_data': {
                    'months': year_data['months'],
                    'food_monthly': year_data['food_totals'],
                    'exercise_monthly': year_data['exercise_totals'],
                    'net_monthly': year_data['net_calories'],
                },
                'summary_stats': {
                    'food_year': year_data['yearly_totals']['food_year'],
                    'cardio_year': year_data['yearly_totals']['cardio_year'],
                    'net_year': year_data['yearly_totals']['net_year'],
                }
            }
        })

        return context


# fucntional view for viewing calendar week summary table

def calendar_week_summary(request):
    user = request.user
    today = timezone.now().date()

    # Get start and end of current week (Monday to Sunday)
    start_of_week = today - timedelta(days=today.weekday())
    days = [start_of_week + timedelta(days=i) for i in range(7)]
    day_names = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]

    meal_types = [
        FoodLog.BREAKFAST,
        FoodLog.LUNCH,
        FoodLog.DINNER,
        FoodLog.SNACK
    ]

    # Prepare data structure
    table_data = {meal: [] for meal in meal_types}
    food_totals = []
    exercise_totals = []
    net_calories = []

    for day in days:
        # For each meal type
        for meal in meal_types:
            total = (
                FoodLog.objects.filter(
                    user=user, meal_type=meal, timestamp__date=day)
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
        "week_type": "Calendar Week",
        "days": day_names,
        "table_data": table_data,
        "food_totals": food_totals,
        "exercise_totals": exercise_totals,
        "net_calories": net_calories,
        "calendar_title": "Weekly Summary",
    }

    return render(request, "overview/calendar_week_summary.html", context)


def rolling_week_summary(request):
    user = request.user
    today = timezone.now().date()

    days = [today - timedelta(days=i) for i in range(7)]

    day_names = [day.strftime("%a") for day in days]

    meal_types = [
        FoodLog.BREAKFAST,
        FoodLog.LUNCH,
        FoodLog.DINNER,
        FoodLog.SNACK
    ]

    table_data = {meal: [] for meal in meal_types}
    food_totals = []
    exercise_totals = []
    net_calories = []

    for day in days:
        for meal in meal_types:
            total = (
                FoodLog.objects.filter(
                    user=user, meal_type=meal, timestamp__date=day)
                .aggregate(Sum('calories_in'))['calories_in__sum'] or 0
            )
            table_data[meal].append(total)

        food_total = FoodLog.total_food_day(user, date=day)
        exercise_total = CardioLog.total_burn_day(user, date=day)
        net = food_total - exercise_total

        food_totals.append(food_total)
        exercise_totals.append(exercise_total)
        net_calories.append(net)

    days.reverse()
    day_names = [day.strftime("%a") for day in days]
    food_totals.reverse()
    exercise_totals.reverse()
    net_calories.reverse()

    for meal in meal_types:
        table_data[meal].reverse()

    context = {
        "week_type": "Rolling Week",
        "days": day_names,
        "table_data": table_data,
        "food_totals": food_totals,
        "exercise_totals": exercise_totals,
        "net_calories": net_calories,
        "rolling_title": "Rolling Summary",
    }

    return render(request, "overview/rolling_week_summary.html", context)


def yearly_summary(request, year=None):
    user = request.user
    year = year or timezone.now().date().year
    year = int(year)

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
        net_total = net_calorie_month(user, year, month)

        food_monthly.append(food_total)
        cardio_monthly.append(cardio_total)
        net_monthly.append(net_total)

    food_year = FoodLog.total_food_year(user, year)
    cardio_year = CardioLog.total_burn_year(user, year)
    net_year = net_calorie_year(user, year)

    context = {
        "monthly_title": "Monthly Summary",
        'table_data': {
            'months': months,
            'food_monthly': food_monthly,
            'exercise_monthly': cardio_monthly,
            'net_monthly': net_monthly,
        },
        'summary_stats': {
            'food_year': food_year,
            'cardio_year': cardio_year,
            'net_year': net_year,
        }
    }

    return render(request, 'overview/yearly_summary.html', context)

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Log Meal"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Food Log added successfully!")
        return super().form_valid(form)


class FoodUpdateView(UpdateView):
    model = FoodLog
    form_class = FoodForm
    template_name = 'food/add_food.html'
    success_url = reverse_lazy('calorie_tracker:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Update Meal"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Food Log updated successfully!")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            pk=self.kwargs['pk'],
            user=self.request.user
        )


class FoodDeleteView(DeleteView):
    model = FoodLog
    template_name = 'food/delete_food.html'
    page_title = 'Delete Food'
    success_url = reverse_lazy('calorie_tracker:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Delete Food"
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Food log deleted successfully!")
        return super().delete(request, *args, **kwargs)


class CardioCreateView(CreateView):
    model = CardioLog
    form_class = CardioForm
    template_name = 'cardio/add_cardio.html'
    success_url = reverse_lazy('calorie_tracker:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Log Cardio"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Cardio Log added successfully!")
        return super().form_valid(form)


class CardioUpdateView(UpdateView):
    model = CardioLog
    form_class = CardioForm
    template_name = 'cardio/add_cardio.html'
    success_url = reverse_lazy('calorie_tracker:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Update Cardio"
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        messages.success(self.request, "Food Log updated successfully!")
        return super().form_valid(form)

    def get_object(self, queryset=None):
        return get_object_or_404(
            self.model,
            pk=self.kwargs['pk'],
            user=self.request.user
        )


class CardioDeleteView(DeleteView):
    model = CardioLog
    template_name = 'cardio/delete_cardio.html'
    success_url = reverse_lazy('calorie_tracker:home')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['page_title'] = "Delete Cardio"
        return context

    def delete(self, request, *args, **kwargs):
        messages.success(request, "Cardio log deleted successfully!")
        return super().delete(request, *args, **kwargs)
