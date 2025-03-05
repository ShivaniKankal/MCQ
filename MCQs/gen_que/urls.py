from django.urls import path
from .views import start_test, submit_answer, get_results

urlpatterns = [
    path('start/', start_test, name='start_test'),
    path('submit/', submit_answer, name='submit_answer'),
    path('results/<str:session_id>/', get_results, name='get_results'),
]
