from django.http import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from sharemypic.pics.models import Image, Tag
from django import forms

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


class ImageDetailView(views.DetailView):
    model = Image
    template_name = 'pics/details_pic.html'  # Adjust template name as needed
    context_object_name = 'image'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        image = self.get_object()
        context['tagged_images'] = image.tagged_images.all()  # Assuming tags is a ManyToManyField in Image model
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
