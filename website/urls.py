from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    # path('', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('record/<int:pk>', views.customer_record, name='record'),
    path('delete_record/<int:pk>', views.delete_record, name='delete_record'),
    path('add_record/', views.add_record, name='add_record'),
    path('update_record/<int:pk>', views.update_record, name='update_record'),
    path('photos/', views.photo_list, name='photo_list'),
    path('photos/<int:pk>/view/', views.photo_view, name='photo_view'),
    path('photos/<int:pk>/', views.photo_detail, name='photo_detail'),
    path('photos/new/', views.photo_create, name='photo_create'),
    path('photos/<int:pk>/edit/', views.photo_update, name='photo_update'),
    path('photos/<int:pk>/delete/', views.photo_delete, name='photo_delete'),
    path('send-all-emails/', send_all_emails, name='send_all_emails'),


]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)