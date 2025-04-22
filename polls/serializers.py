from rest_framework import serializers
from .models import Question,Choice

class ChoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Choice
        fields = ["id","choice_text","votes"]

class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source ="choice_set")
    class Meta:
        model = Question
        #fields = "__all__"
        fields=["id","question_text","code","pub_date","choices"]

    def create(self, validated_data):
        choices_data = validated_data.pop("choice_set")
        question = Question.objects.create(**validated_data)
        for choice in choices_data:
            Choice.objects.create(question=question,**choice)
        return question