from rest_framework.decorators import action
from rest_framework.views import APIView
from rest_framework import generics, viewsets
from .serializers import *
from .models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .permissions import IsStaffOrReadOnly
from rest_framework.exceptions import NotFound
# Create your views here.


class SignInView(APIView):
    def get(self, request):
        response = {
            'message': 'Enter username and password'
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SignInSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            response = {
                'message': 'Log in successfully',
                'user': user.username,
                'email': user.email
            }
            return Response(response, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SignUpView(APIView):

    def get(self, request):
        response = {
            'message': 'Enter username , password and email for registeration'
        }
        return Response(response, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = SignUpSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChangePasswordView(generics.UpdateAPIView):
    serializer_class = ChangePasswordSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self, queryset=None):
        obj = self.request.user
        return obj

    def update(self, request, *args, **kwargs):
        self.object = self.get_object()
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            if not self.object.check_password(serializer.data.get('old_password')):
                response = {
                    'error': 'old password is wrong'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                self.object.set_password(serializer.data.get('new_password'))
                self.object.save()
                response = {
                    'messages': 'Password Changed Successfully'
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)
        return Response(self.serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CategoryView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    authentication_classes = ()
    permission_classes = ()


class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = (IsStaffOrReadOnly,)

    def retrieve(self, request, *args, **kwargs):
        quiz = self.get_object()

        if not quiz.is_available():
            return Response(
                {
                    'error': 'this quiz is not started or finished'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not quiz.can_access(request.user):
            return Response(
                {
                    'error': 'You don not have any access for this quiz'
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = QuizDeatilSerializer(quiz)
        return Response(
            {
                'message': 'SUCCESS',
                'data': serializer.data
            },
            status=status.HTTP_200_OK,
        )

    @action(
        methods=['POST'],
        detail=True
    )
    def add_question(self, *args, **kwargs):
        quiz = self.get_object()
        serializer = QuestionSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['quiz'] = quiz
        serializer.save()
        return Response(
            {
                'message': 'SUCCESS'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        url_path=r'questions/(?P<question_pk>[^/.]+)/add-choice'
    )
    def add_choice(self, *args, **kwargs):
        question_pk = kwargs.get('question_pk')
        question = Question.objects.filter(pk=question_pk).first()
        if not question:
            return Response(
                {
                    'message': 'Not Found'
                },
                status=status.HTTP_404_NOT_FOUND
            )
        serializer = QuestionChoiceSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['question'] = question
        serializer.save()
        return Response(
            {
                'message': 'SUCCESS'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def quiz_attempt(self, *args, **kwargs):
        quiz = self.get_object()
        QuizAttempt.objects.create(
            user=self.request.user,
            quiz=quiz
        )
        privacy = Privacy.objects.filter(quiz=quiz).first()
        privacy.shared_with.add(self.request.user)
        privacy.save()
        return Response(
            {
                'message': 'SUCCESS'
            },
            status=status.HTTP_200_OK
        )

    @action(
        methods=['POST'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def finish(self, request, *args, **kwargs):
        quiz = self.get_object()
        answers = request.data.get('answers', [])
        answers_objs = []

        for answer in answers:
            question = Question.objects.filter(
                quiz=quiz, pk=answer['question']).first()
            self.check_obj(question)
            selected_choice = QuestionChoice.objects.filter(
                pk=answer['selected_choice'],
                question=question
            ).first()
            self.check_obj(selected_choice)

            answer = QuizResult(
                quiz=quiz,
                user=request.user,
                question=question,
                selected_choice=selected_choice
            )
            answers_objs.append(answer)

        if not answers_objs:
            return Response(
                {
                    'message': 'Empty answers'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        QuizResult.objects.bulk_create(answers_objs)
        return Response(
            {
                'message': 'SUCCESS'
            },
            status=status.HTTP_200_OK
        )

    def check_obj(self, obj):
        if not obj:
            raise NotFound(
                {
                    'error': 'Not Found'
                }
            )

    @action(
        methods=['GET'],
        detail=True,
        permission_classes=[IsAuthenticated]
    )
    def quiz_marks(self, request, *args, **kwargs):
        quiz = self.get_object()
        results = QuizResult.objects.select_related(
            'question'
        ).filter(user=request.user, quiz=quiz)
        total = 0
        for result in results:
            if result.is_correct:
                total += result.question.degree
            pass
        return Response(
            {
                'message': 'SUCCESS',
                'quiz': quiz.title,
                'total_marks': total
            },
            status=status.HTTP_200_OK
        )
