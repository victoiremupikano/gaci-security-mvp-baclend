from django.urls import path
from . views import(
    CustomTokenVerifyView, 
    SendPasswordResetEmailView, 
    UserChangeStatusView,
    UserChangePasswordView, 
    UserLoginView, 
    UserLogoutView,
    UserRegistrationView, 
    UserPasswordResetView, 
    AgentDetailView,
    AgentListView,
    AgentListCreateView,
    AgentUpdateView,
    AgentDeleteView,
    AgentChangeStatusView,
    ProfileDetailView,
    ProfileListCreateView, 
    ProfileUpdateView, 
    ProfileDeleteView,  
    FunctionDetailView, 
    FunctionListView,
    FunctionListCreateView, 
    FunctionUpdateView, 
    FunctionDeleteView, 
    AssignmentListView,
    AssignmentDetailIdAgentView,
    AssignmentDeleteView, 
    AssignmentDetailView, 
    AssignmentListCreateView, 
    AssignmentUpdateView,
    UserDetailView,
    UserListView,
    RateDetailView,
    RateListView,
    RateListCreateView,
    RateUpdateView,
    RateDeleteView,
    StationDetailView,
    StationListView,
    StationListCreateView,
    StationUpdateView,
    StationDeleteView,
    UsageDetailView,
    UsageListView,
    UsageListCreateView,
    UsageUpdateView,
    UsageDeleteView,
    Buy_ModeDetailView,
    Buy_ModeListView,
    Buy_ModeListCreateView,
    Buy_ModeUpdateView,
    Buy_ModeDeleteView,

    # rps
    AgentListActifView,
    AgentListNoActifView,
    RateListView
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
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('logout/', UserLogoutView.as_view(), name='logout'),
    path('changepassword/', UserChangePasswordView.as_view(), name='changepassword'),
    path('changestatus/', UserChangeStatusView.as_view(), name='changestatus'),
    path('send-reset-password-email/', SendPasswordResetEmailView.as_view(), name='send-reset-password-email'),
    path('reset-password/<uid>/<token>/', UserPasswordResetView.as_view(), name='reset-password'),
    # user list only or all
    path('user-detail/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('user-list/', UserListView.as_view(), name='user-list'),
    # agent
    path('agent-detail/<int:pk>/', AgentDetailView.as_view(), name='agent-detail'),
    path('agent-list-all/', AgentListView.as_view(), name='agent-list-all'),
    path('agent-list-create/', AgentListCreateView.as_view(), name='agent-list-create'),
    path('agent-update/<int:pk>/', AgentUpdateView.as_view(), name='agent-update'),
    path('agent-delete/<int:pk>/', AgentDeleteView.as_view(), name='agent-delete'),
    path('agent-changestatus/', AgentChangeStatusView.as_view(), name='agent-changestatus'),
    # profile
    path('profile-detail/<int:pk>/', ProfileDetailView.as_view(), name='profile-detail'),
    path('profile-list-create/', ProfileListCreateView.as_view(), name='profile-list-create'),
    path('profile-update/<int:pk>/', ProfileUpdateView.as_view(), name='profile-update'),
    path('profile-delete/<int:pk>/', ProfileDeleteView.as_view(), name='profile-delete'),
    # function
    path('function-detail/<int:pk>/', FunctionDetailView.as_view(), name='function-detail'),
    path('function-list-all/', FunctionListView.as_view(), name='function-list-all'),
    path('function-list-create/', FunctionListCreateView.as_view(), name='function-list-create'),
    path('function-update/<int:pk>/', FunctionUpdateView.as_view(), name='function-update'),
    path('function-delete/<int:pk>/', FunctionDeleteView.as_view(), name='function-delete'),
    # assignment
    path('assignment-detail/<int:pk>/', AssignmentDetailView.as_view(), name='assignment-detail'),
    path('assignment-detail-id-agent/<int:agent_id>/', AssignmentDetailIdAgentView.as_view(), name='assignment-detail-id-agent'),
    path('assignment-list/', AssignmentListView.as_view(), name='assignment-list'),
    path('assignment-list-create/', AssignmentListCreateView.as_view(), name='assignment-list-create'),
    path('assignment-update/<int:pk>/', AssignmentUpdateView.as_view(), name='assignment-update'),
    path('assignment-delete/<int:pk>/', AssignmentDeleteView.as_view(), name='assignment-delete'),
    # rate
    path('rate-detail/<int:pk>/', RateDetailView.as_view(), name='rate-detail'),
    path('rate-list-all/', RateListView.as_view(), name='rate-list-all'),
    path('rate-list-create/', RateListCreateView.as_view(), name='rate-list-create'),
    path('rate-update/<int:pk>/', RateUpdateView.as_view(), name='rate-update'),
    path('rate-delete/<int:pk>/', RateDeleteView.as_view(), name='rate-delete'),
    # station
    path('station-detail/<int:pk>/', StationDetailView.as_view(), name='station-detail'),
    path('station-list-all/', StationListView.as_view(), name='station-list-all'),
    path('station-list-create/', StationListCreateView.as_view(), name='station-list-create'),
    path('station-update/<int:pk>/', StationUpdateView.as_view(), name='station-update'),
    path('station-delete/<int:pk>/', StationDeleteView.as_view(), name='station-delete'),
    # usage
    path('usage-detail/<int:pk>/', UsageDetailView.as_view(), name='usage-detail'),
    path('usage-list-all/', UsageListView.as_view(), name='usage-list-all'),
    path('usage-list-create/', UsageListCreateView.as_view(), name='usage-list-create'),
    path('usage-update/<int:pk>/', UsageUpdateView.as_view(), name='usage-update'),
    path('usage-delete/<int:pk>/', UsageDeleteView.as_view(), name='usage-delete'),
    # buy-mode
    path('buy-mode-detail/<int:pk>/', Buy_ModeDetailView.as_view(), name='buy-mode-detail'),
    path('buy-mode-list-all/', Buy_ModeListView.as_view(), name='buy-mode-list-all'),
    path('buy-mode-list-create/', Buy_ModeListCreateView.as_view(), name='buy-mode-list-create'),
    path('buy-mode-update/<int:pk>/', Buy_ModeUpdateView.as_view(), name='buy-mode-update'),
    path('buy-mode-delete/<int:pk>/', Buy_ModeDeleteView.as_view(), name='buy-mode-delete'),

    # les lien pour les donnes des rapport

    # 1.liste de tous les utilisateur --> auth line 70
    # 2.un seul utilisateur --> auth line 71
    # 3.liste de tous les agents reconnues actifs 
    path('agent-list-all-actif/', AgentListActifView.as_view(), name='agent-list-all-actif'),
    # 4.liste de tous les agents reconnues non actifs 
    path('agent-list-all-no-actif/', AgentListNoActifView.as_view(), name='agent-list-all-no-actif'),
    # 5.liste de tous les agents chacun avec son dossier complet (fucntion assigner) --> auth line 100
    # 6.un seul agent avec son dossier complet (fucntion assigner) --> auth line 99
    # 24.lister tous les taux lier au salaire d'un agent par rapport aux parcels lotis
    path('rate-by-agent-allot-list-all/<int:pk>/<int:station_id>/', RateListView.as_view(), name='rate-by-agent-allot-list-all'),
]