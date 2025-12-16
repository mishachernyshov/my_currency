from django.urls import include, path


app_name = 'core'
urlpatterns = [
    path('api/', include(('core.api.urls', 'core')), name='api'),
]
