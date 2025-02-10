from django.shortcuts import render, redirect

from django.contrib.auth import authenticate, login, logout


def log_in(request):

    if request.method == 'POST':

        c = {}

        username = request.POST.get('u')
        password = request.POST.get('p')

        user = authenticate(username = username, password = password)

        if user:

            login(request, user)

            return redirect('/d4shb0ard')

        else: 

            c['e'] = True

            return render(request, 'login.html', c)
        
    else:
    
        return render(request, 'login.html')


def log_out(request):

    logout(request)

    return redirect('/4d-log1n')