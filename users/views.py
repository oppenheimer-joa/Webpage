from django.shortcuts import render, redirect # p205

# add moduels - p208, p213, 227
from users.forms import LoginForm, SignupForm # p221
from django.contrib.auth import authenticate, login, logout # p215
from users.models import User

# create view - p197
def login_view(request):

    # add additional settings - p205
    # 추후 이 부분을 적절히 수정
    if request.user.is_authenticated:
        return redirect('/posts/feeds/')
    
    # add additional settings - p212
    if request.method == "POST":
        form = LoginForm(data=request.POST)
        request.session['login_session'] = form.login_session
        request.session.set_expiry(0) # 브라우저 닫을 시 세션 삭제
        print('login session :::::::: ', request.session['login_session'])
        print('form.is_valid():', form.is_valid())
        print('form.cleaned_data:', form.cleaned_data)

        # add additional settings - p213
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            

            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                print(request)
                return redirect('/posts/main')
            else:
                # add additional settings - p217
                form.add_error(None, "입력한 자격증명에 해당하는 사용자가 없습니다.")
                # removed - p217
                # print('로그인에 실패했습니다.')

        context = {'form' : form}
        return render(request, 'users/login.html', context)

    else:
        form = LoginForm()
        context = {'form' : form}
        return render(request, 'users/login.html', context)

    # removed - p212
    # add additional settings - p208
    # form = LoginForm()
    # context = {'form' : form,}
    # return render(request, 'users/login.html', context)
    
# add logout - p215
def logout_view(request):
    logout(request)
    return redirect('/users/login')

# add signup - p219
def signup(request):
    # add additional settings - p223
    if request.method == "POST":
        # removed - p230
        # print(request.POST)
        # print(request.FILES)

        # add additional settings - p225
        form = SignupForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/posts/feeds/')
        # removed - p232
        # else:
            # context = {'form':form}
            # return render(request, 'users/signup.html', context)

            # removed - p231
            # username = form.cleaned_data['username']
            # password1 = form.cleaned_data['password1']
            # password2 = form.cleaned_data['password2']
            # profile_image = form.cleaned_data['profile_image']
            # short_description = form.cleaned_data['short_description']

            # # add logins - p230
            # user = User.objects.create_user(
            #     username=username,
            #     password=password1,
            #     profile_image=profile_image,
            #     short_description=short_description,
            # )
            # login(request, user)
            # return redirect(request, 'users/signup.html', context)

            # removed - p230
            # print(username)
            # print(password1, password2)
            # print(profile_image)
            # print(short_description)

            # removed - p230
            # add additional settings - p227
            # if password1 != password2:
            #     form.add_error("password2", "비밀번호와 비밀번호 확인란의 값이 다릅니다")
            # if User.objects.filter(username=username).exists():
            #     form.add_error("username", "입력한 사용자명은 이미 사용중입니다.")
            # if form.errors:
            #     context = {'form' : form}
            #     return render(request, 'users/signup.html', context)                
            # else:
            #     user = User.objects.create_user(
            #         username=username,
            #         password=password1,
            #         profile_image=profile_image,
            #         short_description=short_description,
            #     )
            #     login(request, user)
            #     return redirect('/posts/feeds/')
    else:
        form = SignupForm()
    
    context = {'form' : form}
    return render(request, 'users/signup.html', context)

def index(request):
    # add settings - p206
    if request.user.is_authenticated:
        return redirect('/posts/main/')
    else:
        return redirect('/users/login/')