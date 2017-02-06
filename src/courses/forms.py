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

    def clean_slug(self):
        slug = self.cleaned_data.get("slug")
        qs = Course.objects.filter(slug=slug)
        if qs.count() > 1:
            raise forms.ValidationError("Slug must be unique")
        return slug