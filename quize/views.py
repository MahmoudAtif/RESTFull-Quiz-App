from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, UpdateAPIView
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
# Create your views here.


class SignInView(APIView):
    def get(self, request):
        response={
            'message':'Enter username and password'
        }
        return Response(response,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=SignInSerializer(data=request.data)
        if serializer.is_valid():
            user=serializer.validated_data['user']
            response={
                'message':'Log in successfully',
                'user':user.username,
                'email':user.email
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class SignUpView(APIView):
   
    def get(self, request):
        response={
            'message':'Enter username , password and email for registeration'
        }
        return Response(response,status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ChangePasswordView(UpdateAPIView):
    serializer_class=ChangePasswordSerializer
    permission_classes=(IsAuthenticated,)

    def get_object(self,queryset=None):
        obj=self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object=self.get_object()
        serializer=self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                response={
                    'error':'old password is wrong'
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
            else:
                self.object.set_password(serializer.data.get('new_password'))
                self.object.save()
                response={
                    'messages':'Password Changed Successfully'
                }
                return Response(response,status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer.errors,status=status.HTTP_400_BAD_REQUEST)



class CategoryView(APIView):
    def get(self, request):
        queryset=Category.objects.all()
        serializer=CategorySerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CategoryDetailView(APIView):
    def get_object(self,pk):
        try:
            category=Category.objects.get(pk=pk)
            return category
        
        except Category.DoesNotExist:
            return None
    
    def get(self, request, pk):
        category=self.get_object(pk)
        serializer=CategorySerializer(category)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer=CategorySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        category=self.get_object(pk)
        category.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class MyPaginationClass(PageNumberPagination):
    page_size = 1
    page_size_query_param = 'page_size'
    max_page_size = 1

class QuizView(APIView):  
    permission_classes=(IsAuthenticated,)
    pagination_class = MyPaginationClass
    
    def get(self, request):
        queryset=Quiz.objects.all()
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer=QuizSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)
    
    def get(self, request):
        queryset=Quiz.objects.all()
        paginator = self.pagination_class()
        results = paginator.paginate_queryset(queryset, request)
        serializer=QuizSerializer(results, many=True)
        # return Response(serializer.data, status=status.HTTP_200_OK)
        return paginator.get_paginated_response(serializer.data)
    

    def post(self, request):
        serializer=QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuizDetailView(APIView):
    def get_object(self,pk):
        try:
            quiz=Quiz.objects.get(pk=pk)
            return quiz
        
        except Quiz.DoesNotExist:
            return None
    
    def get(self, request, pk):
        quiz=self.get_object(pk)
        serializer=QuizSerializer(quiz)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer=QuizSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        quiz=self.get_object(pk)
        quiz.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



class QuestionView(APIView): 
    permission_classes=(IsAuthenticated,)

    def get(self, request, format=None):
        queryset=Question.objects.all()
        serializer=QuestionSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class QuestionDetailView(APIView):
    
    def get_object(self,pk):
        try:
            question=Question.objects.get(pk=pk)
            return question
        except Question.DoesNotExist:
            return None
            
    def get(self, request, pk):
        question=self.get_object(pk)
        serializer=QuestionSerializer(question)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer=QuestionSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        question=self.get_object(pk)
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)    


class QuestionChoiceView(APIView):  
    permission_classes=(IsAuthenticated,)

    def get(self, request):
        queryset=QuestionChoice.objects.all()
        serializer=QuestionChoiceSerializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self, request):
        serializer=QuestionChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class QuestionChoiceDetailView(APIView):
    
    def get_object(self,pk):
        try:
            choice=QuestionChoice.objects.get(pk=pk)
            return choice
        except QuestionChoice.DoesNotExist:
            return None
            
    def get(self, request, pk):
        choice=self.get_object(pk)
        serializer=QuestionChoiceSerializer(choice)
        return Response(serializer.data,status=status.HTTP_200_OK)
    
    def put(self, request, pk):
        serializer=QuestionChoiceSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        choice=self.get_object(pk)
        choice.delete()
        return Response(status=status.HTTP_204_NO_CONTENT) 