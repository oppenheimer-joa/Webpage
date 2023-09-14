from django import forms
from django.conf import settings

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class RatingForm(forms.ModelForm):
    class Meta:
        model = Rating
        fields = ['stars']

    def __init__(self, *args, **kwargs):
        super(RatingForm, self).__init__(*args, **kwargs)
        # user 필드를 사용자 정의 사용자 모델로 설정합니다.
        self.fields['user'].queryset = settings.AUTH_USER_MODEL.objects.all()