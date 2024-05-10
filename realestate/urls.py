from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
                  path('', views.index, name='home'),
                  path('login/', views.user_login, name='login'),
                  path('logout/', views.user_logout, name='logout'),
                  path('about/', views.about, name='about'),
                  path('omaha_events/', views.omaha_events, name='events'),
                  path('properties/', views.property_listings, name='property_listings'),
                  path('property/<int:pk>/', views.property_detail, name='property_detail'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
