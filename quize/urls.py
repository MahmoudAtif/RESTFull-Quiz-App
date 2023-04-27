from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register('quizes', views.QuizViewSet, basename='quiz')

urlpatterns = [
    path('auth-api', include('rest_framework.urls')),
    path('signin/', views.SignInView.as_view(), name='signin'),
    path('signup/', views.SignUpView.as_view(), name='signup'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change_password'),
    path('reset-password/', include('django_rest_passwordreset.urls')),
    
    path('categories/', views.CategoryView.as_view(), name='categories'),
    path('', include(router.urls))
    # path('quizes/', views.QuizView.as_view(), name='quizes'),
    # path('quizes/<int:pk>/', views.QuizDetailView.as_view(), name='quiz_detail'),
    # path('questions/', views.QuestionView.as_view(), name='questions'),
    # path('questions/<int:pk>/', views.QuestionDetailView.as_view(), name='question_detail'),
    # path('question-choices/', views.QuestionChoiceView.as_view(), name='questions_choices'),
    # path('question-choices/<int:pk>/', views.QuestionChoiceDetailView.as_view(), name='choice_detail')
]
