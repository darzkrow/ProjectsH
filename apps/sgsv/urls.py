from django.urls import path
from . import views

urlpatterns = [
    path('events/', views.EvSeguridad, name='Eventos-SEG'),


    path('dashboard/', views.home, name='index'),
    ## URLS DE PERSON
    path('search/', views.SearchPerson, name='search'),
    path('person/list/',views.lperson,name='lperson'),
    path('person/create/', views.Cperson, name='cperson'),

    path('person/<str:dni>/view/', views.PersonDetail, name='PersonDetail'),
  
    path('person/<str:dni>/edit/', views.Eperson, name='eperson'),
    path('person/<str:pk>/del/', views.SoftdeletePerson, name='softdelele'),
    path('person/trash', views.Tperson, name='tperson'),



 ## URLS DE ACCESS
    path('access/person/list/', views.laccess, name='laccess'),
    path('daccess/<int:access_id>/', views.detailaccess, name='daccess'),    
    path('raccess/person/<str:dni>/', views.raccess, name='raccess'),
    path('report/access/list', views.reportexcel, name='reportexcel'),
    #path('eaccess/<int:dni>/edit/', views.Eaccess, name='eaccess'),

]