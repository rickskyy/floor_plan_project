from django.conf import settings
from django.conf.urls import url
from django.urls import include, path, re_path
from django.conf.urls.static import static
from django.contrib import admin
from django.views.generic import TemplateView
from django.views import defaults as default_views
from django.views.static import serve

urlpatterns = [
    re_path(r'^$', TemplateView.as_view(template_name='index.html'), name='index'),
    # Django Admin, use {% url 'admin:index' %}
    path(settings.ADMIN_URL, admin.site.urls),
    path(
        "floor_plans/api/",
        include("floor_plan_project.floor_plans.urls", namespace='floor_plans')
    ),

    # re_path(r'^(?:.*)/?$', TemplateView.as_view(template_name='index.html'), name='catchall'),
] + static(
    settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
)

if settings.DEBUG:
    # This allows the error pages to be debugged during development, just visit
    # these url in browser to see how these error pages look like.
    urlpatterns += [
        path(
            "400/",
            default_views.bad_request,
            kwargs={"exception": Exception("Bad Request!")},
        ),
        path(
            "404/",
            default_views.page_not_found,
            kwargs={"exception": Exception("Page not Found")},
        ),
        path("500/", default_views.server_error),
        re_path(r'^media/(?P<path>.*)$', serve, {
            'document_root': settings.MEDIA_ROOT,
        }), # for serving urls in dev version but still not working
    ]
    # if "debug_toolbar" in settings.INSTALLED_APPS:
    #     import debug_toolbar
    #
    #     urlpatterns = [path("__debug__/", include(debug_toolbar.urls))] + urlpatterns
