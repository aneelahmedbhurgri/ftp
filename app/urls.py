from django.urls import path,include
from app import views

urlpatterns = [
    path('upload/',views.upload,name='upload'),
    path('permitupload/',views.permitUpload,name='permitupload'),
    path('authlogin/', views.authUser,name='authsection'),
    path('permitdownload/',views.permitDownload,name='permitdownload'),
    path('authlogout/',views.authlogout,name='logout'),
    path('authregister/',views.authregisteration,name='authreg'),
    path('authindex/',views.indexAuth),
]
