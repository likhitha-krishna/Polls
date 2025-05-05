from rest_framework import serializers
from .models import Question,Choice, Vote
from django.contrib.auth import get_user_model

User = get_user_model()

class ChoiceSerializer(serializers.ModelSerializer):
    voters = serializers.SerializerMethodField()


    class Meta:
        model = Choice
        fields = ["id","choice_text","votes", "voters"]

    def get_voters(self,obj):
        votes = Vote.objects.filter(choice=obj)
        return [vote.user.username for vote in votes]


class QuestionSerializer(serializers.ModelSerializer):
    choices = ChoiceSerializer(many=True, source ="choice_set")
    class Meta:
        model = Question
        #fields = "__all__"
        fields=["id","question_text","code","published_date","choices"]

    def create(self, validated_data):
        choices_data = validated_data.pop("choice_set")
        question = Question.objects.create(**validated_data)
        for choice in choices_data:
            Choice.objects.create(question=question,**choice)
        return question


class VoteSerializer(serializers.ModelSerializer):
    username = serializers.SerializerMethodField()
    total_votes_for_question = serializers.SerializerMethodField()
    question_text = serializers.CharField(source="choice.question.question_text")
    class Meta:
        model = Vote
        fields = ["id","question_text","username","total_votes_for_question"]

    def get_username(self,obj):
        if obj.user:
            return obj.user.username
        return None
        
    def get_total_votes_for_question(self,obj):
        question = obj.choice.question
        total_votes = Vote.objects.filter(choice__question=question).count()
        return total_votes

