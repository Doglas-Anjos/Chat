from django.contrib.auth import authenticate, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views import View


class LogarUsuario(View):
    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        usuario = authenticate(request, username=username, password=password)
        if usuario is None:
            form_login = AuthenticationForm()
            return render(request, 'login.html', {'form_login': form_login})
        else:
            login(request, usuario)
            return redirect('/chat/')

    def get(self, request):
        form_login = AuthenticationForm()
        return render(request, 'login.html', {'form_login': form_login})


@login_required(login_url='/')
def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            form_usuario.save()
            return redirect('logar_usuario')
    else:
        form_usuario = UserCreationForm()
    return render(request, 'cadastro.html', {'form_usuario': form_usuario})


@login_required(login_url='/')
def deslogar_usuario(request):
    logout(request)
    return redirect('logar_usuario')


@login_required(login_url='/')
def alterar_senha(request):
    if request.method == "POST":
        form_senha = PasswordChangeForm(request.user, request.POST)
        if form_senha.is_valid():
            user = form_senha.save()
            update_session_auth_hash(request, user)
            return redirect('logar_usuario')
    else:
        form_senha = PasswordChangeForm(request.user)
    return render(request, 'alterar_senha.html', {'form_senha': form_senha})

