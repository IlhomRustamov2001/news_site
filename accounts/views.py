from django.shortcuts import render, redirect
from .forms import *
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.views.generic import CreateView, View
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from .models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
def user_login(request):
    form=LoginForm(request.POST)
    if form.is_valid():
        data=form.cleaned_data#malumotni olayabdi toza qilib
        print(data)
        user=authenticate(request, username=data['username'],#bazadagi parol va usernamesi 
                          password=data['password'])#bilan solishtiradi
        print(user)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponse("Muvaffaqiyatli login amalga oshiriladi!")
            else:
                return HttpResponse("Sizning profilingiz faol holatda emas!")
        
        else:
            return HttpResponse("Login va Parolda xatolik bor!")
    else:
        form=LoginForm()
        context={
            'form':form
        }
    return render(request, 'account/login.html', context)

@login_required
def dashboard_view(request):
    user=request.user
    profil_info=Profile.objects.get(user=user)
    context={
        'user':user, 
        'profil':profil_info
    }
    return render(request, 'pages/user_profile.html', context)


def register(request):
    if request.method=='POST':
        user_form=UserRegistrationForm(request.POST) # forma to'ldiriladi
        if user_form.is_valid(): # forma tekshiriladi
            new_user=user_form.save(commit=False) # bazaga saqlanmasligi uchun shunday bo'ldi
            new_user.set_password(
                user_form.cleaned_data['password']
            ) #parol o'rnatildi
            new_user.save() # user saqlandi bazaga 
            Profile.objects.create(user=new_user)
            context={
                'new_user':new_user
            }
            return render(request, 'account/register_done.html', context)
    else:
        user_form=UserRegistrationForm()
        print(user_form)
        context={
            'user_form':user_form
        }
        return render(request, 'account/register.html', context)

class SignUp(CreateView):
    form_class=UserCreationForm
    success_url=reverse_lazy('login')
    template_name='account/register.html'

@login_required
def edit_user(request):
    if request.method=='POST':
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile, data=request.POST, 
                                     files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')
    else:
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
    return render(request, 'account/profile_edit.html', {"user_form":user_form, 'profile_form':profile_form})

class EditUserView(LoginRequiredMixin, View):

    def get(self, request):
        user_form=UserEditForm(instance=request.user)
        profile_form=ProfileEditForm(instance=request.user.profile)
        return render(request, 'account/profile_edit.html', {"user_form":user_form, 'profile_form':profile_form})
            
    def post(self, request):
        user_form=UserEditForm(instance=request.user, data=request.POST)
        profile_form=ProfileEditForm(instance=request.user.profile, data=request.POST, 
                                     files=request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('user_profile')

