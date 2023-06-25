from django.urls import path
from . views import (
    # Auth Token
    CustomTokenVerifyView, 
    # Auth User
    UserDetailView,
    UserListView,
    UserLogoutView,
    SendPasswordResetEmailView, 
    UserChangePasswordView, 
    UserChangeStatusView,
    UserLoginView, 
    UserNoStaffRegistrationViewMSCM, 
    UserStaffRegistrationViewMSCM, 
    UserPasswordResetView, 
    # Auth Profile
    ProfileDetailView,
    ProfileUserIdDetailView,
    ProfileUserLoggedListView, 
    ProfileListCreateView, 
    ProfileUpdateView, 
    ProfileDeleteView
)
# import du jwt pour la gestion de token
from rest_framework_simplejwt.views import (
    TokenRefreshView, # token de refreshissement
)

urlpatterns = [
    # access token and refresh token
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', CustomTokenVerifyView.as_view(), name='token_verify'),
    # accounts
    path('no-staff-register-mscm/', UserNoStaffRegistrationViewMSCM.as_view(), name='no-staff-register-mscm'),
    path('staff-register-mscm/', UserStaffRegistrationViewMSCM.as_view(), name='staff-register-mscm'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('changestatus/', UserChangeStatusView.as_view(), name='changestatus'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    # user list only or all
    path('user-detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user-list/', UserListView.as_view(), name='user-list'),
    # profile
    path('profile-detail/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile-user-id-detail/<int:user_id>/', ProfileUserIdDetailView.as_view(), name='profile-user-id-detail'),
    path('profile-user-logged/', ProfileUserLoggedListView.as_view(), name='profile-user-logged'),
    path('profile-list-create/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profile-update/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile-delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile-delete'),
]