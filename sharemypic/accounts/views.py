from django.shortcuts import render, redirect
from django.contrib.auth import views as auth_views, login, logout
from django.urls import reverse_lazy, reverse
from django.views import generic as views


from sharemypic.accounts.forms import SMPUserRegistrationForm
from sharemypic.accounts.models import Profile
from sharemypic.pics.models import Image


# Create your views here.




class LoginUserView(auth_views.LoginView):
    template_name = 'accounts/login.html'
    redirect_authenticated_user = True


class RegisterUserView(views.CreateView):
    template_name = 'accounts/register.html'
    form_class = SMPUserRegistrationForm
    success_url = reverse_lazy('index')

    # custom behaviour register -> auto login !!!
    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, form.instance)
        return result


def logout_user(request):
    logout(request)
    return redirect('index')


class ProfileDetailView(views.DetailView):
    queryset = Profile.objects.all().prefetch_related('user').all()
    template_name = 'accounts/details.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Get the user profile object
        profile = context['object']
        # Get the count of images associated with the user
        image_count = Image.objects.filter(user=profile.user).count()
        # Add the image count to the context
        context['image_count'] = image_count
        return context


class ProfileEditView(views.UpdateView):
    queryset = Profile.objects.all()
    template_name = 'accounts/edit.html'
    fields = ('first_name', 'last_name','email', 'date_of_birth', 'profile_pic')

    def get_form(self, form_class=None):
        form = super().get_form(form_class=form_class)
        form.fields['date_of_birth'].widget.attrs['type'] = 'date'
        form.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        form.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        form.fields['email'].widget.attrs['placeholder'] = 'Email'
        form.fields['date_of_birth'].widget.attrs['placeholder'] = 'Birth Date'
        form.fields['profile_pic'].widget.attrs['placeholder'] = 'Choose your profile picture'
        return form

    def form_valid(self, form):
        instance = form.save(commit=False)
        if 'image' in self.request.FILES:
            instance.image = self.request.FILES['image']
        instance.save()
        return super().form_valid(form)

    def get_success_url(self):
        return reverse('details profile',kwargs={'pk':self.object.pk})

class ProfileDeleteView(views.DeleteView):
    queryset = Profile.objects.all()
    template_name = 'accounts/delete.html'
    success_url = reverse_lazy('index')