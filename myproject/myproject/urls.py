from django.contrib import admin
from django.urls import path, include
from myapp.views import upload_file, process_file
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('upload_file/', upload_file, name='upload_file'),
    path('process_file/', process_file, name='process_file'),
    path('', upload_file, name='home'),  # Root URL pointing to the upload view
    path('', include('myapp.urls'))
]   


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
