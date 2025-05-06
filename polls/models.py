from django.db import models
import datetime
from django.utils import timezone
from django.contrib import admin 
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError
from django.contrib.auth import get_user_model

class Question(models.Model):
    question_text = models.CharField(max_length=200)
    published_date = models.DateTimeField(default=timezone.now) 
    code = models.CharField(
        max_length=8,
        unique=True,
        blank=True,
        null=True,
        validators=[
            RegexValidator(
                regex="^[a-zA-Z]+$",
                message="Code must only contain letters (no numbers, symbols, or spaces).",
            )
        ],
        help_text="Enter a unique 8 Character code",
    )

    def __str__(self):
        return self.question_text
    
    @admin.display(
            boolean = True,     # Show a ✅ or ❌ in admin (instead of True/False)
            ordering = "published_date",      # Allows sorting the column using published_date
            description = "Published recently?",    # Custom column title
    )
    
    def was_published_recently(self):
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= self.published_date <= now
    
class Choice(models.Model):
    question=models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes=models.IntegerField(default=0)

    def __str__(self):
        return self.choice_text
    
User = get_user_model()    #to get current user model, helps in custom model
class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    choice = models.ForeignKey(Choice,on_delete=models.CASCADE)
    voted_at = models.DateTimeField(auto_now_add=True)  #current time

class Meta:
    unique_together = ("user","question")        
