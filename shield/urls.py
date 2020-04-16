from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.auth import views
from django.urls import path
from rest_framework import routers

from links.views import (
    IndexView,
    LinkListView,
    FileListView,
    ReferenceListView,
    ReferenceCheckView,
)
from links.views import (
    FileViewSet,
    LinkViewSet,
    StatisticsViewSet,
)


router = routers.DefaultRouter()
router.register(r'files', FileViewSet)
router.register(r'links', LinkViewSet)
router.register(r'statistics', StatisticsViewSet)

urlresources = [
    url(
        r'^{}/list.html'.format(resource),
        view.as_view(),
        name='resources_{}_list'.format(resource)
    )
    for resource, view in dict(
        links=LinkListView,
        files=FileListView,
        references=ReferenceListView,
    ).items()
]

urlresources.append(
    url(
        r'^references/(?P<rid>[-\w]+)/',
        ReferenceCheckView.as_view(),
        name="resources_references_check"
    )
)

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    path(r'login/', views.LoginView.as_view(), name='login'),
    path(r'logout/', views.LogoutView.as_view(), name='logout'),
    path(r'admin/', admin.site.urls),
    url(r'^api/', include(router.urls)),
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),
] + urlresources \
    + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
