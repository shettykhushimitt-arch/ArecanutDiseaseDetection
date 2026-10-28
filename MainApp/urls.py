from django.urls import path
from . import views

urlpatterns = [

    path('', views.index, name="index"),

    path('register/', views.register, name="register"),

    path('login/', views.login, name="login"),

    path('logout/', views.logout, name="logout"),

    path('dashboard/', views.dashboard, name="dashboard"),
    path('upload/', views.upload_image, name="upload"),
    path('live-scan/', views.live_scan, name="live_scan"),
    path('live-predict/', views.live_predict, name="live_predict"),

path('history/', views.history, name="history"),
path('predict/<int:id>/',
     views.predict,
     name="predict"),
path(
    'result/<int:id>/',
    views.result,
    name='result'
),
    path(
        'result/<int:id>/symptoms/',
        views.result_symptoms,
        name='result_symptoms'
    ),
    path(
        'result/<int:id>/cause/',
        views.result_cause,
        name='result_cause'
    ),
    path(
        'result/<int:id>/prevention/',
        views.result_prevention,
        name='result_prevention'
    ),
    path(
        'result/<int:id>/treatment/',
        views.result_treatment,
        name='result_treatment'
    ),

]
