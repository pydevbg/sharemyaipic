from django.http import HttpResponseForbidden
from django.shortcuts import render
from django.urls import reverse_lazy, reverse
from django.views import generic as views
from sharemypic.pics.models import Image


# Create your views here.
class ImageCreateView(views.CreateView):
    model = Image
    fields = ['image_file', 'title', 'generation_description']
    template_name = 'pics/create_pic.html'
    success_url = reverse_lazy('index')


    # Associate Image with User
    def form_valid(self, form):

        form.instance.user = self.request.user  # Associate image with current user
        if 'image' in self.request.FILES:
            form.instance.image = self.request.FILES['image']
        return super().form_valid(form)

class ImageDetailView(views.DetailView):
    model = Image
    template_name = 'pics/details_pic.html'  # Adjust template name as needed
    context_object_name = 'image'


class ImageEditView(views.UpdateView):
    model = Image
    fields = ['image_file', 'title', 'generation_description']
    template_name = 'pics/edit_pic.html'
    def get_success_url(self):
        return reverse_lazy('details pic', kwargs={'pk': self.object.pk})

    # limit permission to edit
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