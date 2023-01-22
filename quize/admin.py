from django.contrib import admin
from .models import Category, Quiz, Question, QuestionChoice
# Register your models here.


class QuestionChoiceInlines(admin.TabularInline):
    model = QuestionChoice


class QuestionChoiceAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_correct']
    ordering = ['id']


class QuestionAdmin(admin.ModelAdmin):
    list_display = ['title', 'technique', 'level', 'degree', 'is_active']
    inlines = (QuestionChoiceInlines,)


admin.site.register(Category)
admin.site.register(Quiz)
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionChoice, QuestionChoiceAdmin)
