from django.urls import path
from .views import(
    # Want_To_Research
    Want_To_ResearchDetailView,
    Want_To_ResearchIsFinishListView,
    Want_To_ResearchIsCancelListView,
    Want_To_ResearchInProgressListView, 
    Want_To_ResearchListCreateView, 
    Want_To_ResearchUpdateView,
    Want_To_ResearchDeleteView, 
    # Curfew_And_Instability
    Curfew_And_InstabilityDetailView,
    Curfew_And_InstabilityIsFinishListView,
    Curfew_And_InstabilityIsCancelListView,
    Curfew_And_InstabilityInProgressListView, 
    Curfew_And_InstabilityListCreateView, 
    Curfew_And_InstabilityUpdateView,
    Curfew_And_InstabilityDeleteView, 
    # Population_Alert
    Population_AlertDetailView,
    Population_AlertIsFinishListView,
    Population_AlertIsCancelListView,
    Population_AlertInProgressListView, 
    Population_AlertListCreateView, 
    Population_AlertUpdateView,
    Population_AlertDeleteView,
    # Try_RecognitionRunACheckView
    Try_RecognitionRunACheckListCreateView, 
    RecognizedDetailView,
    RecognizedListView
)

urlpatterns = [
    # wtr
    path('wtr-detail/<int:pk>/', Want_To_ResearchDetailView.as_view(), name='wtr-detail'),
    path('wtr-is-finish-list-all/', Want_To_ResearchIsFinishListView.as_view(), name='wtr-is-finish-list-all'),
    path('wtr-is-cancel-list-all/', Want_To_ResearchIsCancelListView.as_view(), name='wtr-is-cancel-list-all'),
    path('wtr-in-progress-list-all/', Want_To_ResearchInProgressListView.as_view(), name='wtr-in-progress-list-all'),
    path('wtr-list-create/', Want_To_ResearchListCreateView.as_view(), name='wtr-list-create'),
    path('wtr-update/<int:pk>/', Want_To_ResearchUpdateView.as_view(), name='wtr-update'),
    path('wtr-delete/<int:pk>/', Want_To_ResearchDeleteView.as_view(), name='wtr-delete'),
    # cai
    path('cai-detail/<int:pk>/', Curfew_And_InstabilityDetailView.as_view(), name='cai-detail'),
    path('cai-is-finish-list-all/', Curfew_And_InstabilityIsFinishListView.as_view(), name='cai-is-finish-list-all'),
    path('cai-is-cancel-list-all/', Curfew_And_InstabilityIsCancelListView.as_view(), name='cai-is-cancel-list-all'),
    path('cai-in-progress-list-all/', Curfew_And_InstabilityInProgressListView.as_view(), name='cai-in-progress-list-all'),
    path('cai-list-create/', Curfew_And_InstabilityListCreateView.as_view(), name='cai-list-create'),
    path('cai-update/<int:pk>/', Curfew_And_InstabilityUpdateView.as_view(), name='cai-update'),
    path('cai-delete/<int:pk>/', Curfew_And_InstabilityDeleteView.as_view(), name='cai-delete'),
    # cai
    path('pa-detail/<int:pk>/', Population_AlertDetailView.as_view(), name='pa-detail'),
    path('pa-is-finish-list-all/', Population_AlertIsFinishListView.as_view(), name='pa-is-finish-list-all'),
    path('pa-is-cancel-list-all/', Population_AlertIsCancelListView.as_view(), name='pa-is-cancel-list-all'),
    path('pa-in-progress-list-all/', Population_AlertInProgressListView.as_view(), name='pa-in-progress-list-all'),
    path('pa-list-create/', Population_AlertListCreateView.as_view(), name='pa-list-create'),
    path('pa-update/<int:pk>/', Population_AlertUpdateView.as_view(), name='pa-update'),
    path('pa-delete/<int:pk>/', Population_AlertDeleteView.as_view(), name='pa-delete'),
    # try-recognition-run-a-check 
    path('try-recognition-run-a-check/', Try_RecognitionRunACheckListCreateView.as_view(), name='try-recognition-run-a-check'),
    # recognized
    path('recognized-detail/<int:pk>/', RecognizedDetailView.as_view(), name='recognized-detail'),
    path('recognized-list-all/', RecognizedListView.as_view(), name='recognized-list-all'),

]