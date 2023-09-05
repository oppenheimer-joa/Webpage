from django.shortcuts import render, redirect
from .forms import LoginForm

# Create your views here.
def login(request) :
    loginform = LoginForm()
    context = {'forms' : loginform}

    if request.method == "GET" :
        return render(request, 'account/login.html', context)
    elif request.method == "POST" : 
        loginform = LoginForm(request.POST)

        if loginform.is_valid() :
            request.session['login_session'] = loginform.login_session
            request.session.set_expiry(0) # 브라우저 닫을 시 세션 삭제
            return redirect("/userinfo")
        else :
            context['forms'] = loginform
            if loginform.errors :
                for value in loginform.errors.values() :
                    context['error'] = value
    return render(request, 'account/login.html', context)
