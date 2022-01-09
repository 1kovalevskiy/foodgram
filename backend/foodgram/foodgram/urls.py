from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('api/admin/', admin.site.urls),
    path('api/', include('users.urls', namespace='authentication')),
    path('api/', include('tags.urls', namespace='tags')),
    path('api/', include('ingredients.urls', namespace='ingredients')),
    path('api/', include('recipes.urls', namespace='recipes')),
]
