from django.urls import path
from .views import (
    loginPage, 
    dashboard, 
    logoutUser, 
    addCandidate, 
    addCompany, 
    deleteUser, 
    getJobs,
)

urlpatterns = [
    path('', loginPage, name='admin-login'),
    path('dashboard/', dashboard, name='dashboard'),

    path('candidate/', addCandidate, name='candidate'),
    path('company/', addCompany, name='company'),

    path('delete-user/<str:pk>/', deleteUser, name='delete-user'),

    path('job/', getJobs, name='job'),

    path('logout/', logoutUser, name='logout'),

]
   

