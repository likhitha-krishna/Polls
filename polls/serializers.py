from rest_framework import serializers
from .models import Question,Choice

class ChoiceSerializer(serializers.ModelSerializer):
    question = serializers.CharField(source="question.question_text")
    class Meta:
        model = Choice
        fields = ["id","question","choice_text","votes"]

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True,read_only=True,source="choice_set")
    class Meta:
        model = Question
        #fields = "__all__"
        fields=["id","question_text","code","pub_date","choices"]
