from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import generic as views

from sharemypic.common.models import ImageComment
from sharemypic.pics.models import Image


# Create your views here.
class CreateImageComment(LoginRequiredMixin, views.CreateView):
    model = ImageComment
    template_name = 'common/create_comment.html'
    fields = ['text']
    success_url = reverse_lazy('index')

    def dispatch(self, request, *args, **kwargs):
        self.image = get_object_or_404(Image, pk=self.kwargs['pk'])
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['image'] = self.image
        return context

    def form_valid(self, form):
        form.instance.user = self.request.user
        form.instance.image = self.image
        return super().form_valid(form)



class UpdateImageComment(LoginRequiredMixin, UserPassesTestMixin, views.UpdateView):
   pass

class DeleteImageComment(LoginRequiredMixin, UserPassesTestMixin, views.DeleteView):
   pass