from django.contrib import messages
from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, TemplateView
from django.urls import reverse_lazy
from django.utils import timezone
from .models import FoodLog, CardioLog
from .forms import FoodForm, CardioForm

# dashboard view


def dashboard_view(request):
    user = request.user
    today = timezone.now().date()

    # day totals
    total_food_day = FoodLog.total_food_day(user, today)
    total_burn_day = CardioLog.total_burn_day(user, today)
    net_day = total_food_day - total_burn_day

    # rolling week totals
    total_food_rolling_week = FoodLog.total_food_rolling_week(user)
    total_burn_rolling_week = CardioLog.total_burn_rolling_week(user)
    net_rolling_week = total_food_rolling_week - total_burn_rolling_week

    # calendar week totals
    total_food_calendar_week = FoodLog.total_food_calendar_week(user)
    total_burn_calendar_week = CardioLog.total_burn_calendar_week(user)
    net_calendar_week = total_food_calendar_week - total_burn_calendar_week

    food_logs = FoodLog.logs_for_day(user, today)
    cardio_logs = CardioLog.logs_for_day(user, today)

    context = {
        # day context
        "total_food_day": total_food_day,
        "total_burn_day": total_burn_day,
        "net_day": net_day,

        "total_food_rolling_week": total_food_rolling_week,
        "total_burn_rolling_week": total_burn_rolling_week,
        "net_rolling_week": net_rolling_week,

        "total_food_calendar_week": total_food_calendar_week,
        "total_burn_calendar_week": total_burn_calendar_week,
        "net_calendar_week": net_calendar_week,

        "food_logs": food_logs,
        "cardio_logs": cardio_logs,
    }

    return render(request, "overview/dashboard.html", context)


# List Views for viewing overview logs


class OverviewDayView(TemplateView):
    template_name = 'overview/overview_day.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['food_logs'] = FoodLog.logs_for_day(self.request.user)
        context['cardio_logs'] = CardioLog.logs_for_day(self.request.user)
        return context

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
