from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views

from sharemypic.common.models import ImageLike
from sharemypic.pics.models import Image, Tag
from django import forms
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image_file', 'title', 'generation_description', 'tagged_images']

class TagForm(forms.ModelForm):
    class Meta:
        model = Tag
        fields = ['name']


# Create your views here.
class ImageCreateView(views.CreateView):
    model = Image
    fields = ['image_file', 'title', 'generation_description']
    template_name = 'pics/create_pic.html'
    success_url = reverse_lazy('index')

    def form_valid(self, form):
        form.instance.user = self.request.user
        image = form.save()

        tag_form = TagForm(self.request.POST)
        if tag_form.is_valid():
            tag_names = tag_form.cleaned_data['name'].split(',')
            for tag_name in tag_names:
                tag_name = tag_name.strip()
                if tag_name:
                    tag, created = Tag.objects.get_or_create(name=tag_name)
                    image.tagged_images.add(tag)

        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag_form'] = TagForm()
        return context

        # Process tags
        # tags_input = form.cleaned_data.get('tags')
        # if tags_input:
        #     tags_list = [tag.strip() for tag in tags_input.split(',')]
        #     for tag_name in tags_list:
        #         tag, _ = Tags.objects.get_or_create(name=tag_name)
        #         image_instance.tags.add(tag)
        #
        # return redirect(self.success_url)





class ImageDetailView(LoginRequiredMixin, views.DetailView):
    model = Image
    template_name = 'pics/details_pic.html'
    context_object_name = 'image'

    def post(self, request, *args, **kwargs):
        image = self.get_object()
        user = request.user

        if 'like' in request.POST:
            # User clicked the like button
            like, created = ImageLike.objects.get_or_create(user=user, image=image)
            if not created:
                # If the like already exists, remove it (toggle functionality)
                like.delete()

        return redirect(reverse('details pic', kwargs={'pk': image.pk}))

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object()
        context['tagged_images'] = image.tagged_images.all()
        context['has_liked'] = ImageLike.objects.filter(user=self.request.user, image=image).exists()
        context['like_count'] = image.likes.count()
        return context




class ImageEditView(views.UpdateView):
    model = Image
    fields = ['title', 'image_file','generation_description']
    template_name = 'pics/edit_pic.html'

    def get_success_url(self):
        return reverse_lazy('details pic', kwargs={'pk': self.object.pk})

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        if not self.object.can_edit(request.user):
            return HttpResponseForbidden("You do not have permission to edit this image.")
        return super().dispatch(request, *args, **kwargs)



class ImageDeleteView(views.DeleteView):
    queryset = Image.objects.all()
    template_name = 'pics/delete.html'
    success_url = reverse_lazy('index')


def all_images(request):
    images = Image.objects.all()
    return render(request, 'index/index.html', {'images': images})


def my_gallery(request):
    # Filter images based on the currently logged-in user
    username = request.user.username
    images = Image.objects.filter(user=request.user)
    return render(request, 'pics/my_gallery.html', {'images': images, 'username': username})
