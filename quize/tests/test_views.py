from rest_framework.test import APITestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status

class TestView(APITestCase):

    def setUp(self):
        self.user=User.objects.create_user(username='test',password='test',email='test@gmail.com')
        # to login 
        self.client.force_login(self.user)
        data={
            "name":"test"
        }
        self.client.post(reverse('categories'), data, format='json')
    
    def test_signin_view(self):
        url=reverse('signin')
        data={
            "username":self.user.username,
            "password":"test"
        }
        response=self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_not_signup_view(self):
        url=reverse('signup')
        data={
            'username':'test',
            'password':'test',
            'email':'testt@gmail.com'
        }
        response=self.client.post(url, data, format='json')
        self.assertEquals(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_get_category_view(self):
        url=reverse('categories')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_post_categories_view(self): 
        data={
            "name":"test"
        }
        url=reverse('categories')
        response=self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], 'test')
    
    def test_put_category_view(self): 
        data={
            "name":"test"
        }
        url=reverse('category_detail', kwargs={'pk':1})
        response=self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'test')

    def test_delete_category_view(self):
        obj=reverse('category_detail', kwargs={'pk':1})
        response=self.client.delete(obj)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
    
    def test_quizes_view(self): 
        url=reverse('quizes')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)   

    def test_quiz_detail_view(self):
        url=reverse('quiz_detail',kwargs={'pk':1})
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_questions_view(self):
        url=reverse('questions')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_question_detail_view(self):
        url=reverse('question_detail',kwargs={'pk':1})
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_question_choices_view(self):
        url=reverse('questions_choices')
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_question_choice_detail_view(self):
        url=reverse('choice_detail',kwargs={'pk':1})
        response=self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)