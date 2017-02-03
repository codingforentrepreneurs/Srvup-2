from django import forms

from .models import Course


class CourseForm(forms.ModelForm):
    # number = forms.IntegerField()
    class Meta:
        model = Course
        fields = [
            'title',
            'description',
            'slug',
            'price',

        ]