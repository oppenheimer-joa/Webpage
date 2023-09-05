from django import forms
from .models import UserInfo

class LoginForm(forms.Form) :
    user_id = forms.CharField (
        max_length = 100,
        label = '아이디',
        widget = forms.TextInput(
            attrs = {
                'class' : 'user_id',
                'placeholder' : '아이디'
            }
        ),
        error_messages={'required' : '아이디를 입력해주세요'}
    )
    user_pw = forms.CharField (
        max_length = 100,
        label = '비밀번호',
        widget = forms.PasswordInput(
            attrs = {
                'class' : 'user_pw',
                'placeholder' : '비밀번호'
            }
        ),
        error_messages={'required' : '비밀번호를 입력해주세요'}
    )

    field_order = [
        'user_id',
        'user_pw'
    ]

    def clean(self) :
        cleaned_data = super().clean() 

        user_id = cleaned_data.get('user_id', '')
        user_pw = cleaned_data.get('user_pw', '')

        try :
            user = UserInfo.objects.get(user_id=user_id)
        except :
            return self.add_error('user_id' , '다시 확인해주세요.')
        
        self.login_session = [user.user_id, user.user_pw]
        