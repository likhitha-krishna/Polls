from django.http import HttpResponse
from rest_framework import status
from rest_framework.views import APIView
#from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Question,Choice
from .serializers import QuestionSerializer , ChoiceSerializer
from django.shortcuts import get_object_or_404

def welcome(request):
    response_data = """
    <h1> Welcome to my POLLS project</h1>
    <a href="/questions">Question</a>"""
    return HttpResponse(response_data)

class QuestionList(APIView):
    """
    List of all question
    """
    def get(self,request):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions,many=True)
        return Response(serializer.data)


class QuestionDetail(APIView):
    """
    Retrieve, update or delete a question by it's unique code along with choices.
    """

    def get(self,request,code):
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code")
            # NotFound(detail="No such question with provided code")

        choices = question.choice_set.all()

        question_data = {
            "question_text" : question.question_text,
            "published_date" : question.published_date,
            "choices" : ChoiceSerializer(choices,many=True).data    #.data gives you the final Python list of dictionaries
        }

        return Response(question_data)
    
    def patch(self,request,code):
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code")
        
        serializer = QuestionSerializer(question, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,code):
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code")
        
        question.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    
class QuestionCreate(APIView):
    """
    Create a new question with a unique code.
    """

    def post (self, request):
        serializer = QuestionSerializer(data=request.data) #request.data is user filled data

        if Question.objects.filter(question_text=request.data.get("question_text")).exists():
            return Response("This question already exists",status=status.HTTP_400_BAD_REQUEST)
        
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data,status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class VoteAPIView(APIView):
    """
    Allow users to vote for choice
    """

    def post(self,request):
        #choice_id = request.data.get("choice_id")
        choice_text = request.data.get("choice_text")
        #if not choice_id:
        if not choice_text:
            return Response({"error":"Invalid choice_text"}, status=status.HTTP_400_BAD_REQUEST)
        
        #case insensitive match
        choice = get_object_or_404(Choice,choice_text__iexact=choice_text)

        choice.votes += 1
        choice.save()

        question_text = choice.question.question_text
        return Response({
        
            "question_text": question_text,
            "choice_text" : choice_text,
            "message":"Vote successfull",
            "updated_votes" : choice.votes,      

        }, status=status.HTTP_200_OK)
    
class ResultsView(APIView):
    """
    Return a list of all choices sorted by vote count
    """
    # def get(self,request):
    #     choices=Choice.objects.all().order_by("votes")
    #     serializer = ChoiceSerializer(choices,many=True)
    #     return Response(serializer.data)

    """
    Retrieving result of  list of all choices sorted by vote count using unique code
    """

    def get(self,request,code):
        try:
            unique_code=Question.objects.get(code=code)
        except Question.DoesNotExist:
            return Response("No such question with provided code")
        choices=unique_code.choice_set.all().order_by("votes")
        serializer = ChoiceSerializer(choices,many=True)
        return Response(serializer.data)
