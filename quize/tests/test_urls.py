from rest_framework.test import APITestCase
from quize.views import *
from django.urls import resolve, reverse

class TestUrl(APITestCase):

    def test_signin_url(self):
        url=reverse('signin')
        self.assertEqual(resolve(url).func.view_class, SignInView)

    def test_signup_url(self):
        url=reverse('signup')
        self.assertEqual(resolve(url).func.view_class, SignUpView)

    def test_change_password_url(self):
        url=reverse('change_password')
        self.assertEqual(resolve(url).func.view_class, ChangePasswordView)

    def test_categories_url(self):
        url=reverse('categories')
        self.assertEqual(resolve(url).func.view_class, CategoryView)

    def test_category_detail_url(self):
        url=reverse('category_detail',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class, CategoryDetailView)

    def test_quizes_url(self):
        url=reverse('quizes')
        self.assertEqual(resolve(url).func.view_class, QuizView)
    
    def test_quiz_detail_url(self):
        url=reverse('quiz_detail',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class, QuizDetailView)
    
    def test_questions_url(self):
        url=reverse('questions')
        self.assertEqual(resolve(url).func.view_class, QuestionView)

    
    def test_question_detail_url(self):
        url=reverse('question_detail',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class, QuestionDetailView)

    def test_question_choices_url(self):
        url=reverse('questions_choices')
        self.assertEqual(resolve(url).func.view_class, QuestionChoiceView)

    def test_question_choice_detail_url(self):
        url=reverse('choice_detail',kwargs={'pk':1})
        self.assertEqual(resolve(url).func.view_class, QuestionChoiceDetailView)