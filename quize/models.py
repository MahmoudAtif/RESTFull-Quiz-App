from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
# Create your models here.


class AbstractModel(models.Model):
    created_at = models.DateTimeField(_("Created At"), auto_now_add=True)
    updated_at = models.DateTimeField(_("Updated At"), auto_now=True)

    class Meta:
        abstract = True


class Category(AbstractModel):
    name = models.CharField(verbose_name=_('Category Name'), max_length=50)

    def __str__(self):
        return self.name


class Quiz(AbstractModel):
    title = models.CharField(
        verbose_name=_('Quize Title'),
        max_length=200,
        default='New Quize'
    )
    category = models.ForeignKey(
        Category,
        verbose_name=_("Category Name"),
        on_delete=models.DO_NOTHING
    )
    started_at = models.DateTimeField(_("Started At"))
    ends_on = models.DateTimeField(_("Ends On"))
    is_available = models.BooleanField(default=True)

    @property
    def get_question_number(self):
        total = self.quize_questions.all().count()
        return total

    def can_access(self, user):
        if self.privacy.is_public():
            return True
        else:
            return user in self.privacy.shared_with.all()

    def is_available(self):
        time_now = timezone.now()
        if not self.is_available:
            return False
        if not time_now >= self.started_at and time_now < self.ends_on:
            return False
        return True

    def __str__(self):
        return self.title


class Question(AbstractModel):

    class TypesEnum(models.IntegerChoices):
        MULTIPLECHOICES = 1, 'MultipleChoices'
        COMPLETE = 2, 'Complete'
        ESSAY = 3, 'Essay'

    class LevelsEnum(models.IntegerChoices):
        BEGINNER = 1, 'Beginner'
        INTERMEDIATE = 2, 'Intermediate'
        ADVANCED = 3, 'Advanced'

    quiz = models.ForeignKey(
        Quiz,
        verbose_name=_("Quize Title"),
        on_delete=models.CASCADE,
        related_name='questions'
    )
    title = models.CharField(_('Question Title'), max_length=200)
    degree = models.DecimalField(max_digits=5, decimal_places=2)
    technique = models.IntegerField(
        verbose_name=_('Question Type'),
        choices=TypesEnum.choices,
    )
    level = models.IntegerField(
        verbose_name=_('Question Dificulty'),
        choices=LevelsEnum.choices,
    )
    is_active = models.BooleanField(verbose_name=_("Active"), default=False)

    def __str__(self):
        return self.title


class QuestionChoice(AbstractModel):
    question = models.ForeignKey(
        Question,
        verbose_name=_("Question Name"),
        on_delete=models.CASCADE,
        related_name='choices'
    )
    title = models.CharField(_('Answer'), max_length=200)
    is_correct = models.BooleanField(verbose_name=_('Correct'), default=False)

    def __str__(self):
        return self.title


class QuizAttempt(AbstractModel):
    user = models.ForeignKey(
        User,
        verbose_name=_("User"),
        related_name='attempts',
        on_delete=models.CASCADE
    )
    quiz = models.ForeignKey(
        Quiz,
        verbose_name=_("Quiz"),
        related_name='attempts',
        on_delete=models.CASCADE
    )

    class Meta:
        unique_together = ['user', 'quiz']

    def __str__(self):
        return f'{self.user} - {self.quiz}'


class QuizResult(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="quiz_result"
    )
    quiz = models.ForeignKey(
        Quiz,
        on_delete=models.CASCADE,
        related_name="result"
    )
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    selected_choice = models.ForeignKey(
        QuestionChoice,
        on_delete=models.CASCADE
    )
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.user} - {self.quiz}'

    def save(self, *args, **kwargs):
        if self.selected_choice.is_correct:
            self.is_correct = True
        else:
            self.is_correct = False
        super(QuizResult, self).save(*args, **kwargs)


class Privacy(models.Model):

    class OptionsEnum(models.IntegerChoices):
        PUBLIC = 1, 'Public',
        PRIVATE = 2, 'Private',
        CUSTOM = 3, 'Custom'

    quiz = models.OneToOneField(
        Quiz,
        verbose_name=_("Quiz"),
        related_name='privacy',
        on_delete=models.CASCADE
    )
    option = models.IntegerField(
        choices=OptionsEnum.choices,
        default=OptionsEnum.PRIVATE
    )
    shared_with = models.ManyToManyField(User, blank=True)

    def is_public(self):
        return self.option == self.OptionsEnum.PUBLIC

    def is_private(self):
        return self.option == self.OptionsEnum.PRIVATE

    def is_custom(self):
        return self.option == self.OptionsEnum.CUSTOM

    def __str__(self):
        return f'{self.quiz} - {self.OptionsEnum(self.option).label}'
