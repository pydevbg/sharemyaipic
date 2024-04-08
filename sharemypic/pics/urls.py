
from django.urls import path


from django.conf.urls.static import static

from sharemypic import settings
from sharemypic.pics.views import ImageCreateView, ImageDetailView, ImageEditView, ImageDeleteView, my_gallery

urlpatterns = [
                path('upload/', ImageCreateView.as_view(), name='upload pic'),
                path('details/<int:pk>/', ImageDetailView.as_view(), name='details pic'),
                path('details/edit/<int:pk>/', ImageEditView.as_view(), name='edit pic'),
                path('details/delete/<int:pk>/', ImageDeleteView.as_view(), name='delete pic'),
                path('my-gallery/', my_gallery, name='my-gallery')


]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
