from django.contrib import admin
from django.urls import path, include
from .views import (
    UserRegistration, 
    UserLogin, 
    GetCompany, 
    UpdateDetails, 
    GetCandidate, 
    UserActivation, 
    Activation, 
    EducationView, 
    SubEducation, 
    ExperienceView, 
    SubExperience, 
    Notification,
    ChangePw,
    ResetPassword
)

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    # path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # path('activate_account/', UserActivation.as_view(), name='activate_account'),
    # path('activate/<uidb64>/<token>', Activation.as_view(), name='activate'),

    path('register/', UserRegistration.as_view(), name='register'),
    path('login/', UserLogin.as_view(), name='login'),
    path('change-password/', ChangePw.as_view(), name='change-password'),
    path('reset-password/', ResetPassword.as_view(), name='reset-password'),

    path('company/', GetCompany.as_view(), name='company'),
    path('candidate/', GetCandidate.as_view(), name='candidate'),
    path('edit-user/', UpdateDetails.as_view(), name='edit-user'),

    path('education/', EducationView.as_view(), name='education'),
    path('education-update/', SubEducation.as_view(), name='education'),
    path('experience/', ExperienceView.as_view(), name='education'),
    path('exp-update/', SubExperience.as_view(), name='education'),

    path('notification/', Notification.as_view(), name='token'),
]