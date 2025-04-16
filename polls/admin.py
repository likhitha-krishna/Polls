from django.contrib import admin
from .models import Choice , Question

class ChoiceInline (admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin (admin.ModelAdmin):
    #fields = ["question_text","pub_date"]
    fieldsets = [
        (None,{"fields":["question_text","code"]}),
        ("Date Information", {"fields":["pub_date"], "classes":["collapse"],}),
    ]
    list_display = ["question_text","pub_date","was_published_recently","code"]
    list_filter = ["pub_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]
admin.site.register(Question, QuestionAdmin)

