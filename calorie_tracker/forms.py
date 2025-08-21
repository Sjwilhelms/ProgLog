from .models import FoodLog, CardioLog
from django import forms

# form for user submitted Meal/Snack


class FoodForm(forms.ModelForm):
    class Meta:
        model = FoodLog
        fields = [
            "meal_name",
            "meal_desc",
            "meal_type",
            "calories_in",
        ]

# form for user submitted exercise


class CardioForm(forms.ModelForm):
    class Meta:
        model = CardioLog
        fields = [
            "cardio_name",
            "cardio_desc",
            "duration",
            "calories_out",
        ]
