

from django.contrib import admin
from django.urls import path
from myapp import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('test-logging/', views.test_logging, name='test_logging'),
    path('test-template-error/', views.test_template_error, name='test_template_error'),
    path('test-db-error/', views.test_db_error, name='test_db_error'),
]