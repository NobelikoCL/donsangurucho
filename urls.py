<<<<<<< HEAD
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ventas.urls')),
]
=======
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('ventas.urls')),
]
>>>>>>> 94c198e9cc54935981968c971a6cbe5d4f0e02d5
