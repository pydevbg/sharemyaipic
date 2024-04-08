
from django.urls import path


from django.conf.urls.static import static

from sharemypic import settings
from sharemypic.accounts.views import LoginUserView, RegisterUserView, logout_user, ProfileDetailView, ProfileEditView, \
    ProfileDeleteView

urlpatterns = [
    path('login/',LoginUserView.as_view(),name='login'),
    path('register/',RegisterUserView.as_view(),name='register'),
    path('logout/' ,logout_user, name ='logout'),
    path("profile/<int:pk>/", ProfileDetailView.as_view(), name="details profile"),
    path('edit/<int:pk>/',ProfileEditView.as_view(), name="edit profile"),
    path('delete/<int:pk>/',ProfileDeleteView.as_view(), name="delete profile"),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
