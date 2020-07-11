from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from django.db.models import Q
from .models import Profile

def register(request):
    if request.method=='POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            user = User.objects.get(username=username)
            user_profile = Profile(user=user)
            user_profile.save()
            messages.success(request, f'Account created for {username}! You can now login.')
            return redirect('user-login')
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'title':'Register','form':form})

@login_required
def myProfile(request):
    if request.method=='POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, f'Your account has been updated!')
            return redirect('my-profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form':u_form,
        'p_form':p_form,
        'title':'Edit Profile'
    }
    
    return render(request, 'users/my-profile.html', context)

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/user_list.html'
    context_object_name = 'objects'

    def get_queryset(self):
        query = self.request.GET.get("q", None)
        if query is not None:
            return User.objects.filter(
                Q(username__icontains=query) | 
                Q(profile__full_name__icontains=query) | 
                Q(profile__profession__icontains=query) | 
                Q(profile__skill_1__icontains=query) |
                Q(profile__skill_2__icontains=query) |
                Q(profile__skill_3__icontains=query)
                )
        else:
            return User.objects.all()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = "All Users"
        return context
