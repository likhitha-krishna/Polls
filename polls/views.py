from rest_framework import status
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from rest_framework.response import Response
from .models import Question,Choice
from .serializers import QuestionSerializer , ChoiceSerializer

class QuestionList(APIView):
    """
    List of all question
    """
    def get(self,request,format=None):
        questions = Question.objects.all()
        serializer = QuestionSerializer(questions,many=True)
        return Response(serializer.data)


class QuestionDetail(APIView):
    """
    Retrieve a question by it's unique code along with choices.
    """

    def get(self,request,code,format=None):
        try:
            question = Question.objects.get(code=code)
        except Question.DoesNotExist:
            #return Response("No such question with provided code")
            raise NotFound(detail="No such question with provided code")

        choices = question.choice_set.all()

        question_data = {
            "question_text" : question.question_text,
            "pub_date" : question.pub_date,
            "choices" : ChoiceSerializer(choices,many=True).data    #.data gives you the final Python list of dictionaries
        }

        return Response(question_data)
    
class QuestionCreate(APIView):
    """
    Create a new question with a unique code.
    """

    def post (self, request, format=None):
        serializer = QuestionSerializer(data=request.data) #request.data is user filled data
        if serializer.is_valid():
            serializer.save()
            return Response (serializer.data,status=status.HTTP_201_CREATED)
        return Response (serializer.errors, status=status.HTTP_400_BAD_REQUEST)

