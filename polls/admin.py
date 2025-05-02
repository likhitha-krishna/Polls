from django.contrib import admin
from .models import Choice , Question, Vote

class ChoiceInline (admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin (admin.ModelAdmin):
    #fields = ["question_text","published_date"]
    fieldsets = [
        (None,{"fields":["question_text","code"]}),
        ("Date Information", {"fields":["published_date"], "classes":["collapse"],}),
    ]
    list_per_page = 5 # Set the number of questions per page in the admin
    list_display = ["question_text","published_date","was_published_recently","code"]
    list_filter = ["published_date"]
    search_fields = ["question_text"]
    inlines = [ChoiceInline]
admin.site.register(Question, QuestionAdmin)

class VoteAdmin (admin.ModelAdmin):
    list_display = ["get_username","get_question","choice"]
    list_per_page = 10
    def get_username(self,obj):
        return obj.user.username
    get_username.short_description = "Username"
    def get_question(self,obj):
        return obj.choice.question.question_text
    get_question.short_description = "Question"
    
admin.site.register(Vote,VoteAdmin)
