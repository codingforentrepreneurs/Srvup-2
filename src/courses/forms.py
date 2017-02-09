from django import forms
from django.db.models import Q

from videos.models import Video
from .models import Course, Lecture


class LectureAdminForm(forms.ModelForm):
    class Meta:
        model = Lecture
        fields = [
            'order',
            'title',
            'free',
            'video',
            'description',
            'slug', 
        ]
    def __init__(self, *args, **kwargs):
        super(LectureAdminForm, self).__init__(*args, **kwargs)
        obj = kwargs.get("instance")
        qs = Video.objects.all().unused()
        if obj:
            if obj.video:
                this_ = Video.objects.filter(pk=obj.video.pk)
                qs = (qs | this_)
            self.fields['video'].queryset = qs
        else:
            self.fields['video'].queryset = qs



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