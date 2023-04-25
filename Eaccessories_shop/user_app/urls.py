from django.urls import path
from . import views

urlpatterns = [
    path('contact/',views.Contact_Page, name='contact'),
    path('register/',views.HandleRegister, name='register'),
    path('login/',views.HandleLogin, name='login'),
    path('logout/',views.HandleLogout, name='logout'),
    path('account/',views.Account, name='account'),
    path('profile/',views.PROFILE, name='profile'),
    path('profile/update',views.PROFILE_UPDATE, name='profile_update'),
    
   # path('success/',views.success, name='success'),
    
]
