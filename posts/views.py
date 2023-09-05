from django.shortcuts import render, redirect # p205

# add feeds - p201
def main(request):

    # add users and settings - p203
    user = request.user
    is_authenticated = user.is_authenticated
    print('user:', user)
    print('is_authenticated:', is_authenticated)

    # add aditional settings - p205
    # 추후 이 부분을 수정
    if not is_authenticated:
        return redirect('/users/login')

    return render(request, 'posts/main.html')

