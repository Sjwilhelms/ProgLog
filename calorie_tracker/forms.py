from .models import UserProfile, FoodLog, CardioLog
from django import forms


class ProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = [
            "height",
            "weight",
            "weight_goal",
            "cardio_goal",
        ]


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
