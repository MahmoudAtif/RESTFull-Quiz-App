from django.db import models
from django.utils.translation import gettext_lazy as _
# Create your models here.


class Category(models.Model):
    name = models.CharField(verbose_name=_('Category Name'), max_length=50)

    def __str__(self):
        return self.name


class Quiz(models.Model):
    title = models.CharField(verbose_name=_(
        'Quize Title'), max_length=200, default='New Quize')
    category = models.ForeignKey(Category, verbose_name=_(
        "Category Name"), on_delete=models.DO_NOTHING)
    started_at = models.DateTimeField(_("Started At"))
    ends_on = models.DateTimeField(_("Ends On"))
    date_created = models.DateTimeField(auto_now_add=True)

    @property
    def get_question_number(self):
        total = self.quize_questions.all().count()
        return total

    def __str__(self):
        return self.title


class Question(models.Model):
    TYPES = (
        ('MultipleChoices', 'MultipleChoices'),
        ('Complete', 'Complete'),
        ('Essay', 'Essay'),
    )
    LEVELS = (
        ('Beginner', 'Beginner'),
        ('Intermediate', 'Intermediate'),
        ('Advanced', 'Advanced'),
    )
    quiz = models.ForeignKey(Quiz, verbose_name=_(
        "Quize Title"), on_delete=models.CASCADE, related_name='quiz_questions')
    title = models.CharField(_('Question Title'), max_length=200)
    degree = models.DecimalField(max_digits=5, decimal_places=2)
    technique = models.CharField(verbose_name=_(
        'Question Type'), choices=TYPES, max_length=50)
    level = models.CharField(verbose_name=_(
        'Question Dificulty'), choices=LEVELS, max_length=50)
    is_active = models.BooleanField(verbose_name=_("Active"), default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class QuestionChoice(models.Model):
    question = models.ForeignKey(Question, verbose_name=_(
        "Question Name"), on_delete=models.CASCADE, related_name='question_choices')
    title = models.CharField(_('Answer'), max_length=200)
    is_correct = models.BooleanField(verbose_name=_('Correct'), default=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
