from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path
from rest_framework.authtoken import views as token_views

from links.views import (
    IndexView,
    ReferenceListView,
    ReferenceCheckView,
    ReferencesView,
    ReferenceView,
    StatisticsView,
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    path(r'login/', views.LoginView.as_view(), name='login'),
    path(r'logout/', views.LogoutView.as_view(), name='logout'),
    path(r'admin/', admin.site.urls),
    url(
        r'^references/(?P<rid>[-\w]+)/',
        ReferenceCheckView.as_view(),
        name="references_check"
    ),
    url(
        r'^references/',
        ReferenceListView.as_view(),
        name='references_list'
    ),
    url(r'^api/tokens/', token_views.obtain_auth_token),
    url(r'^api/references/(?P<rid>[-\w]+)/', ReferenceView.as_view(),
        name='api_reference'),
    url(r'^api/references/', ReferencesView.as_view()),
    url(r'^api/statistics/', StatisticsView.as_view()),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
