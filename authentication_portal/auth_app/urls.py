from django.urls import path

from .views import SignupView, LoginView, DashboardView, logout_view

urlpatterns = [
    path('signup/', SignupView.as_view()),
    path('login/', LoginView.as_view()),
    path('dashboard/', DashboardView.as_view()),
    path('logout/', logout_view)
]
