from django.shortcuts import render

from sharemypic.pics.models import Image


# Create your views here.
def index(request):
    images = Image.objects.all()
    context = {'images': images}
    return render(request, 'index/index.html', context)