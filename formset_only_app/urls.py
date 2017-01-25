from django.conf.urls import url
from .views import ItemCreateNGView, ItemCreateOKView

urlpatterns = [
    url(r'ng$', ItemCreateNGView.as_view(), name='ng'),
    url(r'ok$', ItemCreateOKView.as_view(), name='ok'),
]