from django.conf.urls import url
from . import views
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    url('^$', views.safaricom, name='safaricom'),
    url(r'^create_payment/', views.create_payment, name='create_payment'),
    url(r'^verify_payment/$', views.verify_payment, name='verify_payment'),

]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)