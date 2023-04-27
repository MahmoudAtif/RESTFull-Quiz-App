from django.test import TestCase
from quize.models import *

class TestModel(TestCase):
    
    def setUp(self):
        self.category=Category.objects.create(name='test')
        self.quiz=Quiz.objects.create(title='Test Quiz', category=self.category,started_at="2023-01-08T10:00:00+02:00",ends_on="2023-01-08T11:00:00+02:00")
        self.question=Question.objects.create(quiz=self.quiz, title='Test Quetion', degree=1, technique='MultipleChoices',level='Beginner',is_active=True)
        self.question_choice=QuestionChoice.objects.create(question=self.question, title='Test Choice', is_correct=True)

    def test_category_model(self):
        self.assertEqual(self.category.name, 'test')
    
    def test_quiz_model(self):
        self.assertEqual(self.quiz.title, 'Test Quiz')
        self.assertEqual(self.quiz.category, self.category)
        self.assertEqual(self.quiz.started_at, "2023-01-08T10:00:00+02:00")
        self.assertEqual(self.quiz.ends_on, "2023-01-08T11:00:00+02:00")
        

    def test_quetion_model(self):
        self.assertEqual(self.question.quiz, self.quiz)
        self.assertEqual(self.question.title, 'Test Quetion')
        self.assertEqual(self.question.degree, 1)
        self.assertEqual(self.question.technique, 'MultipleChoices')
        self.assertEqual(self.question.level, 'Beginner')
        self.assertEqual(self.question.is_active, True)

    def test_question_choice_model(self):
        self.assertEqual(self.question_choice.question, self.question)
        self.assertEqual(self.question_choice.title, 'Test Choice')
        self.assertEqual(self.question_choice.is_correct, True)


    