from django.db import transaction
from rest_framework import serializers
from .models import *
from django.db.models import Sum
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from rest_framework.validators import ValidationError


class SignInSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def validate(self, attrs):
        username = attrs['username']
        password = attrs['password']
        if username and password:
            user = authenticate(username=username, password=password)
            if user is not None:
                if not user.is_active:
                    raise serializers.ValidationError({
                        'status': 'error',
                        'msg': 'Your account is disabled'
                    })
            else:
                raise serializers.ValidationError({
                    'status': 'error',
                    'msg': 'unable to log in with provided crediential'
                })
        else:
            raise serializers.ValidationError({
                'status': 'error',
                'msg': 'username and password must be not empty'
            })
        attrs['user'] = user
        return attrs


class SignUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name',
                  'last_name', 'password', 'email']

    def create(self, validated_data):

        user = self.Meta.model(**validated_data)
        password = validated_data.pop('password', None)

        if password is not None:
            user.set_password(password)
            user.save()
            return user

    def validate(self, attrs):

        email_exists = User.objects.filter(email=attrs['email']).exists()
        if email_exists:
            raise ValidationError('email already exist')
        return super().validate(attrs)


class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class QuestionChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuestionChoice
        fields = ['id', 'title', 'is_correct']
        extra_kwargs = {
            'question': {
                'required': False
            }
        }


class QuestionSerializer(serializers.ModelSerializer):
    choices = QuestionChoiceSerializer(many=True, required=False)

    class Meta:
        model = Question
        fields = '__all__'
        extra_kwargs = {
            'quiz': {
                'required': False
            }
        }

    @transaction.atomic
    def create(self, validated_data):
        choices = validated_data.pop('question_choices', None)
        question = super().create(validated_data)
        if choices:
            for choice in choices:
                QuestionChoice.objects.create(
                    question=question,
                    **choice
                )
        return question


class QuizSerializer(serializers.ModelSerializer):
    category = serializers.StringRelatedField()

    class Meta:
        model = Quiz
        fields = '__all__'


class QuizDeatilSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    number_of_questions = serializers.SerializerMethodField(
        'get_question_number'
    )
    duration = serializers.SerializerMethodField('get_quize_duration')
    quiz_marks = serializers.SerializerMethodField('get_quiz_marks')

    class Meta:
        model = Quiz
        # fields=['title','number_of_questions','quiz_marks','duration','quiz_questions']
        fields = '__all__'

    def get_question_number(self, quiz):
        total = quiz.questions.all().count()
        return total

    def get_quize_duration(self, quiz):
        duration = (quiz.ends_on - quiz.started_at)/60
        return duration

    def get_quiz_marks(self, quiz):
        total = quiz.questions.all().aggregate(sum=Sum('degree'))['sum']
        return total


class QuizResultSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizResult
        fields = '__all__'
        

