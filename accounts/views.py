from django.contrib.auth import login
from django.contrib import messages
from django.shortcuts import redirect, render
from django.contrib.auth.models import Group

from accounts.forms import UserRegistrationForm


def signup(request):
    if request.method == 'POST':

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            #messages.success(request, '')
            user_group = Group.objects.get(name="Estudantes")
            user.groups.add(user_group)
            login(request, user)
            return redirect('home', messages.success(request, 'Perfil criado com sucesso!'))
        else:
            messages.error(request, 'Credências não autentitadas')

    else:
        form = UserRegistrationForm()

    contexto = {
        'form': form
    }
    return render(request, 'signup.html', contexto)
