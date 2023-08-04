from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import include, path

from blog import views

urlpatterns = [
    path("", include("blog.urls")),
    path('admin/', admin.site.urls),
]

urlpatterns += [
    path('accounts/', include('django.contrib.auth.urls')),
    path("accounts/profile/", views.UserProfile.as_view(), name="profile"),
    path("accounts/update_profile/", views.UpdateProfileView.as_view(), name="update_profile"),
]

if settings.DEBUG:
    # import debug_toolbar
    urlpatterns += [
        # path("__debug__/", include(debug_toolbar.urls)),
        # path("silk/", include("silk.urls", namespace="silk")),
        ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) + static(settings.MEDIA_URL,
                                                                                     document_root=settings.MEDIA_ROOT)
