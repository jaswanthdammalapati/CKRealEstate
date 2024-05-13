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
                  path('property/<int:pk>/mark_featured/', views.mark_property_as_featured, name='mark_featured'),
 path('property/<int:pk>/change_status/', views.change_property_status, name='change_status'),
                  path('property/add/', views.add_property, name='add_property'),
path('property/<int:pk>/edit/', views.edit_property, name='edit_property'),
path('property/<int:pk>/delete/', views.delete_property, name='delete_property'),
path('event/<int:pk>/delete/', views.delete_event, name='delete_event'),
                  path('event/add/', views.add_event, name='add_event'),
                  path('generate-report/', views.generate_report, name='generate_report'),
path('property/<int:property_id>/', views.property_detail, name='property_detail'),
    path('property/<int:property_id>/contact/', views.contact_form_page, name='contact_form_page'),
    path('property/<int:property_id>/contact_agent/', views.contact_agent, name='contact_agent'),
                path('thank_you_page/', views.thank_you_page, name='thank_you_page'),
                  path('generate_excel_report/', views.generate_excel_report, name='generate_excel_report'),
path('contact/', views.contact_page, name='contact_page'),

              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
